import requests
import json
import urllib.parse
import os
from git import Repo, RemoteProgress
from git.exc import InvalidGitRepositoryError
from git import GitCommandError

class MyProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

def download_group_repos(api_url, group, token):
    group_info = {}
    page = 1

    while True:
        response = requests.get(f"{api_url}/groups/{urllib.parse.quote_plus(group)}/projects", headers={"Private-Token": token}, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Failed to get projects for group {group}. Response: {response.text}")
            return group_info

        projects = json.loads(response.text)
        if not projects:
            break

        for project in projects:
            repo_url = project['http_url_to_repo']
            repo_name = project['name']

            repo_url_parts = list(urllib.parse.urlsplit(repo_url))
            repo_url_parts[1] = f"oauth2:{token}@{urllib.parse.urlsplit(repo_url).netloc}"
            repo_url_with_token = urllib.parse.urlunsplit(repo_url_parts)

            try:
                print(f"Cloning all branches of {repo_name}...")
                repo = Repo.clone_from(repo_url_with_token, f"{group}/{repo_name}", multi_options=['--mirror'], no_single_branch=True)
                group_info[repo_name] = {"url": repo_url, "path": f"{group}/{repo_name}"}
            except GitCommandError as e:
                print(f"Failed to clone {repo_name}: {e}")

        page += 1
    download_subgroups(api_url, group, token, group_info)
    return group_info

def download_subgroups(api_url, parent_group, token, group_info):
    page = 1
    while True:
        response = requests.get(f"{api_url}/groups/{urllib.parse.quote_plus(parent_group)}/subgroups", headers={"Private-Token": token}, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Failed to get subgroups for group {parent_group}. Response: {response.text}")
            return

        subgroups = json.loads(response.text)
        if not subgroups:
            break

        for subgroup in subgroups:
            subgroup_name = subgroup['name']
            subgroup_path = subgroup['full_path']
            print(f"Downloading subgroup {subgroup_name}")

            os.makedirs(subgroup_path, exist_ok=True)
            subgroup_info = download_group_repos(api_url, subgroup_path, token)
            
            group_info.update(subgroup_info)

        page += 1

def create_or_get_group(api_url, token, group_name, parent_id=None):
    params = {}
    if parent_id:
        params['parent_id'] = parent_id
    response = requests.get(f"{api_url}/groups", headers={"Private-Token": token}, params=params)
    if response.status_code == 200:
        groups = json.loads(response.text)
        for group in groups:
            if group['name'] == group_name:
                return group['id']
    
    # Check for existence under the parent group, if parent_id is given
    if parent_id:
        response = requests.get(f"{api_url}/groups/{parent_id}/subgroups", headers={"Private-Token": token})
        if response.status_code == 200:
            subgroups = json.loads(response.text)
            for subgroup in subgroups:
                if subgroup['name'] == group_name:
                    return subgroup['id']

    sanitized_group_name = group_name.replace(" ", "_").replace("-", "_").lower()
    payload = {"name": group_name, "path": sanitized_group_name}
    if parent_id:
        payload['parent_id'] = parent_id

    response = requests.post(f"{api_url}/groups", headers={"Private-Token": token}, json=payload)
    if response.status_code == 201:
        return json.loads(response.text)['id']
    else:
        print(f"Failed to create group {group_name}. Response: {response.text}")
        return None

def create_and_upload_to_new_instance(api_url, token, repo_info, group=None):
    for repo_name, repo_data in repo_info['group_info'].items():
        repo_path_parts = repo_data['path'].split("/")
        print(f"Processing {repo_name} with path parts: {repo_path_parts}")

        if group:
            group_parts = group.split("/")
            if all(x not in repo_path_parts for x in group_parts):
                repo_path_parts = group_parts + repo_path_parts
            print(f"Group specified. Updated path parts: {repo_path_parts}")

        parent_id = None
        for part in repo_path_parts[:-1]:
            print(f"Creating or getting group: {part}")
            parent_id = create_or_get_group(api_url, token, part, parent_id)
            if parent_id is None:
                return
            print(f"Group {part} created or fetched with ID: {parent_id}")

        sanitized_repo_name = repo_name.replace(" ", "_").replace("-", "_").lower()
        payload = {"name": repo_name, "path": sanitized_repo_name}
        
        if parent_id:
            payload['namespace_id'] = parent_id

        print(f"Creating new project: {repo_name} under parent ID: {parent_id}")

        response = requests.post(f"{api_url}/projects", headers={"Private-Token": token}, json=payload)
        if response.status_code == 201:
            new_repo_url = json.loads(response.text)['http_url_to_repo']
        else:
            print(f"Failed to create project {repo_name}. Trying to fetch existing one. Response: {response.text}")
            # Fetch the existing project URL
            existing_project_response = requests.get(f"{api_url}/projects/{urllib.parse.quote_plus(repo_name)}", headers={"Private-Token": token})
            if existing_project_response.status_code != 200:
                print(f"Failed to get existing project {repo_name}. Response: {existing_project_response.text}")
                continue
            new_repo_url = json.loads(existing_project_response.text)['http_url_to_repo']
        
        repo_path = repo_data['path']
        repo = Repo(repo_path)


        # Construct new remote URL with the token
        new_repo_url_parts = list(urllib.parse.urlsplit(new_repo_url))
        new_repo_url_parts[1] = f"oauth2:{token}@{urllib.parse.urlsplit(new_repo_url).netloc}"
        new_repo_url_with_token = urllib.parse.urlunsplit(new_repo_url_parts)

        # Add new remote
        new_remote_name = "new-origin"
        repo.create_remote(new_remote_name, url=new_repo_url_with_token)

        # Configurer le suivi des branches pour le nouveau remote
        for branch in repo.branches:
            # Configurer chaque branche locale pour suivre la même branche sur le nouveau remote
            branch_name = branch.name
            try:
                branch.set_tracking_branch(repo.remotes[new_remote_name].refs[branch_name])
                print(f"Branch {branch_name} set to track {new_remote_name}/{branch_name}")
            except IndexError:
                print(f"Remote branch {new_remote_name}/{branch_name} does not exist. Skipping.")

        # Pousser toutes les branches et tags au nouveau remote
        try:
            print(f"Pushing all branches and tags of {repo_name} to {new_repo_url_with_token}")
            repo.git.push(new_remote_name, '--all')
            repo.git.push(new_remote_name, '--tags')
            print(f"Successfully pushed all branches and tags of {repo_name}")
        except GitCommandError as e:
            print(f"Failed to push repository {repo_name}: {e}")





def find_git_repos(path, repo_info):
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            try:
                repo = Repo(folder_path)
                if repo.git_dir:
                    branches = [branch.name for branch in repo.branches]
                    repo_info[folder] = {
                        "path": folder_path,
                        "branches": branches
                    }
            except InvalidGitRepositoryError:
                find_git_repos(folder_path, repo_info)
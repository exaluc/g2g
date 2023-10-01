import click
import os
import json
from datetime import datetime
import shutil
from g2g.gitlab_utils import download_group_repos, create_and_upload_to_new_instance, find_git_repos

@click.group()
def cli():
    pass

@cli.command()
@click.option('--api-url', help='The original GitLab API URL', required=True)
@click.option('--token', help='The GitLab Private Token', required=False)
@click.option('--group', help='The GitLab group to download', required=True)
@click.option('--output-file', default='repo_info.json', help='Output JSON file for repo information')
@click.option('--clean-all', is_flag=True, help='Remove all existing repos before download')
def download(api_url, token, group, output_file, clean_all):
    if not token:
        token = click.prompt('Please enter your GitLab Private Token', hide_input=True)

    if clean_all and os.path.exists(group):
        print(f"Removing existing group directory: {group}")
        shutil.rmtree(group)

    if not os.path.exists(group):
        os.makedirs(group)

    group_info = download_group_repos(api_url, group, token)
    timestamp = datetime.now().strftime('%Y%m%d')
    group_for_filename = group.replace("/", "_")
    backup_file_name = f"migration_{group_for_filename}_{timestamp}.json"

    with open(backup_file_name, 'w') as f:
        json.dump({"group_info": group_info}, f)

@cli.command()
@click.option('--api-url', help='The new GitLab API URL', required=True)
@click.option('--token', help='The GitLab Private Token for the new instance', required=False)
@click.option('--group', help='The GitLab group to upload to', required=False)
@click.option('--input-file', default='repo_info.json', help='Input JSON file for repo information', required=False)
def upload(api_url, token, group, input_file):
    if not token:
        token = click.prompt('Please enter your GitLab Private Token for the new instance', hide_input=True)

    if input_file and os.path.exists(input_file):
        with open(input_file, 'r') as f:
            repo_info = json.load(f)
        create_and_upload_to_new_instance(api_url, token, repo_info, group)
    else:
        if group and os.path.exists(group):
            repo_info = {}
            find_git_repos(group, repo_info)
            if repo_info:
                print(json.dumps(repo_info, indent=4))
                create_and_upload_to_new_instance(api_url, token, {"group_info": repo_info}, group)
            else:
                print(f"No git repositories found in folder {group}.")
        else:
            print(f"Either specify an input JSON file or ensure the specified group folder {group} exists.")


if __name__ == '__main__':
    cli()

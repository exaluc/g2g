# g2g: GitLab to GitLab Group Migrator

`g2g` is a Python CLI utility designed to streamline the process of migrating groups, and subgroups from one GitLab instance to another.

## Features

- Migrate entire group with his nested subgroups/repositories.
- Works with private and public repositories.
- Handles existing groups and repositories elegantly.
- Generate a JSON backup of Group metadata.
- Token-based authentication for security.

## Installation

You can install the package from PyPI:

```bash
pip install g2g
```

## Usage

### Basic usage:

The primary commands for `g2g` are `download` and `upload`.

```bash
g2g download --api-url "https://gitlab.com/api/v4" --group "mloops" --clean-all
Please enter your GitLab Private Token: 
Removing existing group directory: mloops
Cloning devops-within...
Cloning devops-brother...
Downloading subgroup devops-card
Cloning devops-Mr...
Downloading subgroup devops-animal
Cloning devops-life...
Downloading subgroup devops-home
Cloning devops-free...
Downloading subgroup devops-recently
Cloning devops-leave...
Cloning devops-trouble...
Downloading subgroup devops-time
Cloning devops-while...
Downloading subgroup devops-girl
Cloning devops-hotel...
```

```bash
g2g upload --api-url https://new.instance.localhost/api/v4 --group mloops
Please enter your GitLab Private Token for the new instance: 
{
    "devops-brother": {
        "path": "mloops/devops-brother"
    },
    "devops-trouble": {
        "path": "mloops/devops-home/devops-recently/devops-trouble"
    },
    "devops-leave": {
        "path": "mloops/devops-home/devops-recently/devops-leave"
    },
    "devops-free": {
        "path": "mloops/devops-home/devops-free"
    },
    "devops-while": {
        "path": "mloops/devops-time/devops-while"
    },
    "devops-hotel": {
        "path": "mloops/devops-time/devops-girl/devops-hotel"
    },
    "devops-within": {
        "path": "mloops/devops-within"
    },
    "devops-life": {
        "path": "mloops/devops-card/devops-animal/devops-life"
    },
    "devops-Mr": {
        "path": "mloops/devops-card/devops-Mr"
    }
}
Processing devops-brother with path parts: ['mloops', 'devops-brother']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-brother']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating new project: devops-brother under parent ID: 3228
Successfully created and pushed to https://new.instance.localhost/mloops/devops-brother.git
Processing devops-trouble with path parts: ['mloops', 'devops-home', 'devops-recently', 'devops-trouble']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-home', 'devops-recently', 'devops-trouble']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-home
Group devops-home created or fetched with ID: 3230
Creating or getting group: devops-recently
Group devops-recently created or fetched with ID: 3231
Creating new project: devops-trouble under parent ID: 3231
Successfully created and pushed to https://new.instance.localhost/mloops/devops-home/devops-recently/devops-trouble.git
Processing devops-leave with path parts: ['mloops', 'devops-home', 'devops-recently', 'devops-leave']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-home', 'devops-recently', 'devops-leave']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-home
Group devops-home created or fetched with ID: 3230
Creating or getting group: devops-recently
Group devops-recently created or fetched with ID: 3231
Creating new project: devops-leave under parent ID: 3231
Successfully created and pushed to https://new.instance.localhost/mloops/devops-home/devops-recently/devops-leave.git
Processing devops-free with path parts: ['mloops', 'devops-home', 'devops-free']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-home', 'devops-free']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-home
Group devops-home created or fetched with ID: 3230
Creating new project: devops-free under parent ID: 3230
Successfully created and pushed to https://new.instance.localhost/mloops/devops-home/devops-free.git
Processing devops-while with path parts: ['mloops', 'devops-time', 'devops-while']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-time', 'devops-while']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-time
Group devops-time created or fetched with ID: 3235
Creating new project: devops-while under parent ID: 3235
Successfully created and pushed to https://new.instance.localhost/mloops/devops-time/devops-while.git
Processing devops-hotel with path parts: ['mloops', 'devops-time', 'devops-girl', 'devops-hotel']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-time', 'devops-girl', 'devops-hotel']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-time
Group devops-time created or fetched with ID: 3235
Creating or getting group: devops-girl
Group devops-girl created or fetched with ID: 3237
Creating new project: devops-hotel under parent ID: 3237
Successfully created and pushed to https://new.instance.localhost/mloops/devops-time/devops-girl/devops-hotel.git
Processing devops-within with path parts: ['mloops', 'devops-within']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-within']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating new project: devops-within under parent ID: 3228
Successfully created and pushed to https://new.instance.localhost/mloops/devops-within.git
Processing devops-life with path parts: ['mloops', 'devops-card', 'devops-animal', 'devops-life']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-card', 'devops-animal', 'devops-life']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-card
Group devops-card created or fetched with ID: 3240
Creating or getting group: devops-animal
Group devops-animal created or fetched with ID: 3241
Creating new project: devops-life under parent ID: 3241
Successfully created and pushed to https://new.instance.localhost/mloops/devops-card/devops-animal/devops-life.git
Processing devops-Mr with path parts: ['mloops', 'devops-card', 'devops-Mr']
Group specified. Updated path parts: ['mloops', 'mloops', 'devops-card', 'devops-Mr']
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: mloops
Group mloops created or fetched with ID: 3228
Creating or getting group: devops-card
Group devops-card created or fetched with ID: 3240
Creating new project: devops-Mr under parent ID: 3240
Successfully created and pushed to https://new.instance.localhost/mloops/devops-card/devops-Mr.git
```

### Additional Options:

- `--token TEXT` The GitLab Private Token for CI/CD
- `--output-file` to specify the JSON file for saving repo information.
- `--input-file` to specify the JSON file for reading repo information.
- `--clean-all` to remove all existing repos before download.

## Contributing

All contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT Licensed. See [LICENSE](LICENSE) for full details.

## Author

- [Lucian BLETAN](https://github.com/exaluc)
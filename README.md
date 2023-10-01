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
g2g download --api-url https://gitlab.com/api/v4 --token <GitLab_Private_Token> --group <GitLab_Group>
```

```bash
g2g upload --api-url https://new.instance.localhost/api/v4 --token <New_GitLab_Private_Token> [--group <New_GitLab_Group>]
```

### Additional Options:

- `--output-file` to specify the JSON file for saving repo information.
- `--input-file` to specify the JSON file for reading repo information.
- `--clean-all` to remove all existing repos before download.

## Contributing

All contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT Licensed. See [LICENSE](LICENSE) for full details.

## Author

- [Lucian BLETAN](https://github.com/exaluc)
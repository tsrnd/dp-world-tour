# Demo Project - World Tour

[![Build Status](https://travis-ci.com/tsrnd/dp-world-tour.svg?branch=master)](https://travis-ci.com/tsrnd/dp-world-tour)

## Development

### Setup

- Install `pyenv` for Python version management
- Install `pipenv` for project dependencies management

Please follow [this guide](https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c) for installation instruction.

- Install [Visual Code]() Editor
- Update your bash profile

```bash
# ~/.bashrc, ~/.bash_profile, ~/.zshrc
export PIPENV_VENV_IN_PROJECT=1
export PYTHONDONTWRITEBYTECODE=1
```

- Install project dependencies (includes dev)

```bash
$ make install
```

### Make Commands

| Command | Description |
|:-|:-|
| `make build` | Build app image |
| `make up` | Up all service in detach mode |
| `make stop` | Stop all services |
| `make test` | Test app |
| `make migrations` | Creating new migrations based on the changes you have made to your models |
| `make up-data` | Up data services |
| `make logs-myapp` | Logs myapp container |
| `make up-client` | Up clientside and show logs (open new terminal) |
| `make up-mailhost` | Up smtp mail host for development (open new terminal) |
| `make clean` | Remove exited containers, dangling images, Python cache |
| `make clean-data` | Remove existed data of data services |

### Seed commands
| Command | Description |
|:-|:-|
| `python3 manage.py seed --settings=myproject.settings_myapp` | Seed all tables |

### Docker Commands

| Command | Description |
|:-|:-|
| `docker-compose run app <cmd>` | Run command `<cmd>` in app service |
| `docker-compose logs -f <service>` | View & follow `<service>` logs |

### Debugging

- Start PostgreSQL database service with Docker

```
$ make up-data
```

- Start debugging from Visual Code menu

### Remote Debugging

> WIP

## Deployment

> WIP

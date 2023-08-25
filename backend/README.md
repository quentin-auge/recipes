# Recipes backend

![Python version](https://img.shields.io/badge/python-3.10+-blue.svg)
[![Backend CI status](https://github.com/quentin-auge/recipes/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/quentin-auge/recipes/actions/workflows/backend-ci.yml)

A backend fetching and serving recipes

## Install

### Optional: install Task

- Homebrew: `brew install go-task`
- Other package managers: https://taskfile.dev/installation/

List all tasks: `task -l`

### Install

```bash
task install
# or
pip install .
```

#### Dev install
```bash
task install-dev
# or
pip install -e '.[test]'
```

#### Run tests

```bash
task test
# or
pytest -vv
```
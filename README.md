# task-tracker-widget
A hacky widget that displays in-progress tasks from a central source of truth ticketing system (e.g. Azure DevOps work items)

## Purpose

I have ADHD, and I pretty often forget which task I'm working on when I context switch. My current project uses Azure DevOps as a ticketing system, and it's UX isn't convenient enough for me to open a browser tab every time - (a) I'd rather something faster and (b) opening a browser tab opens opportunities for distraction, which is the enemy when trying to be productive on a task.

## Getting started

**Install**

```bash
# TODO: pip install 'some-package-name'
```

**Configuration**

1. Create your own `.env` file (you can use [`.env.example`](./.env.example) for reference)

<!-- TODO: write up steps for ADO work items to get Personal Access Token, along with screenshots showing where to go in the ADO web UI -->
**TODO**

**[anything else important]**

<!-- TODO: write anything else important for getting started -->
**TODO**

## Development

### Installation

```bash
git clone <repository_url>
cd <root_dir_of_local_repository>
poetry install  # installs dependencies in their own venv
poetry run pre-commit install  # installs pre-commit hooks
```

### Usage

```bash
poetry run python -m tasktrackerdesktopwidget
```

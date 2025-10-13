"""Main entry point for the ToDo List application.

This file initializes all the necessary components (repository, service, CLI) and starts
the application's CLI. It is the root of the application.
"""

import os

from dotenv import load_dotenv

from todolist.cli import Cli
from todolist.repository import InMemoryProjectRepository
from todolist.service import ProjectService

def main() -> None:
    """Run the application."""
    load_dotenv()

    max_projects = int(os.environ.get("MAX_NUMBER_OF_PROJECT"))
    max_tasks = int(os.environ.get("MAX_NUMBER_OF_TASK"))

    repository = InMemoryProjectRepository()
    service = ProjectService(repository, max_projects, max_tasks)
    cli = Cli(service)

    cli.run()


if __name__ == '__main__':
    main()

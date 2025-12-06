"""Main entry point for the ToDo List application.

This file initializes all the necessary components (repository, service, CLI) and starts
the application's CLI. It is the root of the application.
"""

import os

from dotenv import load_dotenv

from src.app.cli.console import Cli
from src.app.db.session import SessionLocal
from src.app.core.config import get_settings
from src.app.repositories.sqlalchemy_project_repository import \
    SqlAlchemyProjectRepository
from src.app.repositories.sqlalchemy_task_repository import \
    SqlAlchemyTaskRepository
from src.app.services.project_service import ProjectService
from src.app.services.task_service import TaskService


def main() -> None:
    """Run the application."""
    load_dotenv()

    settings = get_settings()
    max_projects = settings.MAX_NUMBER_OF_PROJECT
    max_tasks = settings.MAX_NUMBER_OF_TASK

    # Create a new database session
    db_session = SessionLocal()

    try:
        project_repo = SqlAlchemyProjectRepository(session=db_session)
        task_repo = SqlAlchemyTaskRepository(session=db_session)

        project_service = ProjectService(project_repo, max_projects)
        task_service = TaskService(task_repo, project_repo, max_tasks)

        cli = Cli(project_service, task_service)

        cli.run()
    finally:
        db_session.close()


if __name__ == '__main__':
    main()
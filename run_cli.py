"""Main entry point for the ToDo List application.

This file initializes all the necessary components (repository, service, CLI) and starts
the application's CLI. It is the root of the application.
"""

import os

from dotenv import load_dotenv

from src.app.cli.console import Cli
from src.app.db.session import SessionLocal
from src.app.repositories.sqlalchemy_repository import SqlAlchemyProjectRepository
from src.app.services.project_service import ProjectService


def main() -> None:
    """Run the application."""
    load_dotenv()

    max_projects = int(os.environ.get("MAX_NUMBER_OF_PROJECT"))
    max_tasks = int(os.environ.get("MAX_NUMBER_OF_TASK"))

    # Create a new database session
    db_session = SessionLocal()

    try:
        # Initialize the SQLAlchemy repository with the session
        repository = SqlAlchemyProjectRepository(session=db_session)
        service = ProjectService(repository, max_projects, max_tasks)
        cli = Cli(service)

        cli.run()
    finally:
        db_session.close()


if __name__ == '__main__':
    main()
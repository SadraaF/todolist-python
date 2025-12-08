"""(DEPRECATED) Main entry point for the ToDo List CLI.

This file initializes all the necessary components (repository, service, CLI)
and starts the application's command-line interface. It is the root of the
deprecated application.
"""

import asyncio
import sys

from dotenv import load_dotenv

from src.app.cli.console import Cli
from src.app.core.config import get_settings
from src.app.db.session import AsyncSessionLocal
from src.app.repositories.sqlalchemy_project_repository import \
    SqlAlchemyProjectRepository
from src.app.repositories.sqlalchemy_task_repository import \
    SqlAlchemyTaskRepository
from src.app.services.project_service import ProjectService
from src.app.services.task_service import TaskService


async def main_async() -> None:
    """Sets up asynchronous dependencies and runs the CLI's main loop."""
    load_dotenv()

    settings = get_settings()
    max_projects = settings.MAX_NUMBER_OF_PROJECT
    max_tasks = settings.MAX_NUMBER_OF_TASK

    # Asynchronously create a new database session
    async with AsyncSessionLocal() as db_session:
        project_repo = SqlAlchemyProjectRepository(session=db_session)
        task_repo = SqlAlchemyTaskRepository(session=db_session)

        project_service = ProjectService(project_repo, max_projects)
        task_service = TaskService(task_repo, project_repo, max_tasks)

        cli = Cli(project_service, task_service)

        await cli.run()


def main() -> None:
    """Synchronous entry point that runs the async main function.

    Handles setting the correct asyncio event loop policy for Windows.
    """
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main_async())


if __name__ == '__main__':
    main()
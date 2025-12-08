"""A command-line script to automatically close overdue tasks."""
import asyncio
import sys
from src.app.core.config import get_settings
from src.app.db.session import AsyncSessionLocal
from src.app.repositories.sqlalchemy_project_repository import \
    SqlAlchemyProjectRepository
from src.app.repositories.sqlalchemy_task_repository import \
    SqlAlchemyTaskRepository
from src.app.services.task_service import TaskService


async def autoclose_logic():
    """The core async logic for the auto-close job."""
    print("Running async job: Auto-closing overdue tasks...")
    settings = get_settings()

    async with AsyncSessionLocal() as db_session:
        try:
            # Instantiate repositories with the async session
            project_repo = SqlAlchemyProjectRepository(session=db_session)
            task_repo = SqlAlchemyTaskRepository(session=db_session)

            # Initialize the service with its dependencies
            service = TaskService(
                task_repo=task_repo,
                project_repo=project_repo,
                max_tasks=settings.MAX_NUMBER_OF_TASK
            )

            # Await the service call
            closed_count = await service.autoclose_overdue_tasks()
            print(f"Successfully closed {closed_count} overdue tasks.")
        except Exception as e:
            print(f"An error occurred during the autoclose job: {e}")


def run_autoclose():
    """Initializes dependencies and runs the auto-closing service logic."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(autoclose_logic())


if __name__ == "__main__":
    run_autoclose()
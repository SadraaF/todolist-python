"""A command-line script to automatically close overdue tasks."""
from src.app.core.config import get_settings
from src.app.db.session import SessionLocal
from src.app.repositories.sqlalchemy_project_repository import \
    SqlAlchemyProjectRepository
from src.app.repositories.sqlalchemy_task_repository import \
    SqlAlchemyTaskRepository
from src.app.services.task_service import TaskService


def run_autoclose():
    """Initializes dependencies and runs the auto-closing service logic."""
    print("Running job: Auto-closing overdue tasks...")
    settings = get_settings()

    db_session = SessionLocal()
    try:
        project_repo = SqlAlchemyProjectRepository(session=db_session)
        task_repo = SqlAlchemyTaskRepository(session=db_session)

        # Initialize the service with its dependencies
        service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks=settings.MAX_NUMBER_OF_TASK  
        )
        closed_count = service.autoclose_overdue_tasks()
        print(f"Successfully closed {closed_count} overdue tasks.")
    finally:
        db_session.close()


if __name__ == "__main__":
    run_autoclose()
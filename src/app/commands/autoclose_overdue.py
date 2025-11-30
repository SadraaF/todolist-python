"""A command-line script to automatically close overdue tasks."""
from src.app.core.config import get_settings
from src.app.db.session import SessionLocal
from src.app.repositories.sqlalchemy_repository import SqlAlchemyProjectRepository
from src.app.services.project_service import ProjectService


def run_autoclose():
    """Initializes dependencies and runs the auto-closing service logic."""
    print("Running job: Auto-closing overdue tasks...")
    settings = get_settings()

    db_session = SessionLocal()
    try:
        repo = SqlAlchemyProjectRepository(session=db_session)
        service = ProjectService(
            repo,
            max_projects=settings.MAX_NUMBER_OF_PROJECT,
            max_tasks=settings.MAX_NUMBER_OF_TASK
        )
        closed_count = service.autoclose_overdue_tasks()
        print(f"Successfully closed {closed_count} overdue tasks.")
    finally:
        db_session.close()


if __name__ == "__main__":
    run_autoclose()
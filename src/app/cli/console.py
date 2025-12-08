"""(DEPRECATED) Command-Line Interface for the Todo List application.

This module provides the user-facing interface for interacting with the application
from the command line. It handles command parsing, calls the appropriate service
methods, and displays the results or errors to the user.
"""

import shlex
from datetime import datetime, date

from src.app.exceptions.base import TodolistError, ValidationError
from src.app.services.project_service import ProjectService
from src.app.services.task_service import TaskService


class Cli:
    """The command-line interface for the application."""

    def __init__(self, project_service: ProjectService, task_service: TaskService):
        """Initialize the CLI with service dependencies.

        :param project_service: The service for project-related business logic.
        :param task_service: The service for task-related business logic.
        """
        self._project_service = project_service
        self._task_service = task_service
        self._commands = {
            # Project Commands
            "create_project": self._create_project,
            "list_projects": self._list_projects,
            "edit_project": self._edit_project,
            "delete_project": self._delete_project,
            # Task Commands
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "edit_task": self._edit_task,
            "delete_task": self._delete_task,
            "set_task_status": self._set_task_status,
            # System Commands
            "help": self._display_help,
            "exit": self._exit,
        }

    @staticmethod
    def _parse_id(self, id_str: str, entity_name: str) -> int | None:
        """Parse an ID string to an integer, handling potential errors.

        :param id_str: The string representation of the ID.
        :param entity_name: The name of the entity (e.g., 'Project', 'Task').
        :return: The integer ID, or None if parsing fails.
        """
        try:
            return int(id_str)
        except ValueError:
            print(f"Invalid {entity_name} ID. ID must be an integer.")
            return None

    @staticmethod
    def _parse_deadline(deadline_str: str | None) -> date | None:
        """Parse a deadline string from 'YYYY-MM-DD' format to a date object.

        :param deadline_str: The string containing the deadline.
        :raises ValidationError: If the date format is invalid.
        :return: A date object, or None if the input is None.
        """
        if deadline_str is None:
            return None
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Invalid deadline format. Use YYYY-MM-DD")

    async def _display_help(self, args: list[str]) -> None:
        """Display the list of available commands.

        :param args: Command arguments (not used).
        """
        print("Available commands:")
        print("  create_project <name> <description>")
        print("  add_task <project_id> <title> <description> [deadline:YYYY-MM-DD]")
        print("  edit_task <project_id> <task_id> <title> <description> "
              "<status> [deadline:YYYY-MM-DD]")
        print("  delete_task <project_id> <task_id>")
        print("  set_task_status <project_id> <task_id> <todo|doing|done>")
        print("  list_tasks <project_id>")
        print("  edit_project <project_id> <new_name> <new_description>")
        print("  delete_project <project_id>")
        print("  list_projects")
        print("  help")
        print("  exit")

    async def _exit(self, args: list[str]) -> None:
        """Exit the application.

        :param args: Command arguments (not used).
        :raises SystemExit: To terminate the application loop.
        """
        raise SystemExit()

    async def _create_project(self, args: list[str]) -> None:
        """Handle the 'create_project' command.

        :param args: A list containing the project name and description.
        """
        if len(args) != 2:
            print("Invalid number of arguments.")
            return

        name, description = args
        project = await self._project_service.create_project(name, description)
        print(f"Created project '{project.name}' with ID {project.id}.")

    async def _list_projects(self, args: list[str]) -> None:
        """Handle the 'list_projects' command.

        :param args: Command arguments (not used).
        """
        projects = await self._project_service.get_all_projects()
        if not projects:
            print("No projects found.")
            return

        print("Projects:")
        for project in projects:
            created_date = project.created_at.strftime("%Y-%m-%d")
            print(f"  - ID: {project.id}, Name: '{project.name}', "
                  f"Description: '{project.description}', "
                  f"Created: {created_date}")

    async def _add_task(self, args: list[str]) -> None:
        """Handle the 'add_task' command.

        :param args: A list containing project ID, title, description, and optional deadline.
        """
        if not (3 <= len(args) <= 4):
            print("Invalid number of arguments.")
            return

        project_id_str, title, description = args[:3]
        deadline_str = args[3] if len(args) == 4 else None

        project_id = self._parse_id(project_id_str, "Project")
        if project_id is None:
            return

        deadline = self._parse_deadline(deadline_str)

        task = await self._task_service.add_task_to_project(project_id, title,
                                                            description, deadline)

        print(f"Added task '{task.title}' with ID {task.id}.")

    async def _edit_project(self, args: list[str]) -> None:
        """Handle the 'edit_project' command.

        :param args: A list containing project ID, new name, and new description.
        """
        if len(args) != 3:
            print("Invalid number of arguments.")
            return

        project_id_str, new_name, new_description = args
        project_id = self._parse_id(project_id_str, "Project")
        if project_id is None:
            return

        project = await self._project_service.edit_project(project_id, new_name, new_description)
        print(f"Edited project '{project.name}' with ID {project.id}.")

    async def _delete_project(self, args: list[str]) -> None:
        """Handle the 'delete_project' command.

        :param args: A list containing the project ID to delete.
        """
        if len(args) != 1:
            print("Invalid number of arguments.")
            return

        project_id_str = args[0]
        project_id = self._parse_id(project_id_str, "Project")
        if project_id is None:
            return

        await self._project_service.delete_project(project_id)
        print(f"Deleted project ID {project_id} and all of its tasks.")

    async def _set_task_status(self, args: list[str]) -> None:
        """Handle the 'set_task_status' command.

        :param args: A list containing project ID, task ID, and new status.
        """
        if len(args) != 3:
            print("Invalid number of arguments.")
            return

        project_id_str, task_id_str, new_status = args
        project_id = self._parse_id(project_id_str, "Project")
        task_id = self._parse_id(task_id_str, "Task")

        if task_id is None or project_id is None:
            return

        task = await self._task_service.change_task_status(project_id, task_id, new_status)
        print(f"Changed status of task '{task.title}' with "
              f"ID {task.id} to '{new_status}'.")

    async def _list_tasks(self, args: list[str]) -> None:
        """Handle the 'list_tasks' command for a specific project.

        :param args: A list containing the project ID.
        """
        if len(args) != 1:
            print("Invalid number of arguments.")
            return

        project_id_str = args[0]
        project_id = self._parse_id(project_id_str, "Project")
        if project_id is None:
            return

        project = await self._project_service.find_project_by_id(project_id)
        print(f"Tasks of project '{project.name}' with ID {project.id}:")
        if not project.tasks:
            print("  No tasks found.")
            return

        for task in project.tasks:
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else \
                "No deadline assigned"
            print(f"  - Task ID: {task.id}, Status: {task.status}")
            print(f"  - Title: {task.title}, Description: {task.description}")
            print(f"  - Deadline: {deadline_str}")

    async def _edit_task(self, args: list[str]) -> None:
        """Handle the 'edit_task' command.

        :param args: A list with project ID, task ID, new title, new description, new status, and optional new deadline.
        """
        if not 5 <= len(args) <= 6:
            print("Invalid number of arguments.")
            return

        project_id_str, task_id_str, new_title, new_description, new_status = args[:5]
        new_deadline_str = args[5] if len(args) == 6 else None

        project_id = self._parse_id(project_id_str, "Project")
        task_id = self._parse_id(task_id_str, "Task")

        if task_id is None or project_id is None:
            return

        new_deadline = self._parse_deadline(new_deadline_str)

        task = await self._task_service.edit_task(project_id, task_id, new_title, new_description,
                                                  new_status, new_deadline)

        print(f"Edited task '{task.title}' with ID {task.id} in "
              f"project ID {project_id}.")

    async def _delete_task(self, args: list[str]) -> None:
        """Handle the 'delete_task' command.

        :param args: A list containing the project ID and task ID.
        """
        if len(args) != 2:
            print("Invalid number of arguments.")
            return

        project_id_str, task_id_str = args
        project_id = self._parse_id(project_id_str, "Project")
        task_id = self._parse_id(task_id_str, "Task")

        if task_id is None or project_id is None:
            return

        await self._task_service.delete_task(project_id, task_id)
        print(f"Deleted task with ID {task_id} in project ID {project_id}.")

    async def run(self) -> None:
        """Main loop for the CLI"""

        print("\n" + "="*60)
        print("WARNING: The CLI is deprecated and will be removed in a future version.")
        print("Please use the new Web API for all operations.")
        print("="*60 + "\n")

        await self._display_help([])
        while True:
            try:
                raw_input = input("> ")
                if not raw_input:
                    continue

                parts = shlex.split(raw_input)
                command_str = parts[0]
                args = parts[1:]

                command = self._commands.get(command_str)
                if command is None:
                    print("Invalid command. Type 'help' for a list of commands.")
                    continue

                await command(args)

            except TodolistError as e:
                print(f"Error: {e}")
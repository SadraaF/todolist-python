"""Command-Line Interface (CLI) for the Todo List application

This module provides the user-facing interface for interacting with the application.
It handles command parsing, calls the appropriate service methods, and displays
the results or errors to the user.
"""

import shlex

from todolist.exceptions import TodolistError
from todolist.service import ProjectService

class Cli:
    """The command-line interface for the application."""

    def __init__(self, service: ProjectService):
        self._service = service
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

    def _parse_id(self, id_str: str, entity_name: str) -> int | None:
        """Helper function to parse an ID string to an int and handle errors."""
        try:
            return int(id_str)
        except ValueError:
            print(f"Invalid {entity_name} ID. ID must be an integer.")
            return None

    def _display_help(self, args: list[str]) -> None:
        """Displays the available commands."""
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

    def _exit(self, args: list[str]) -> None:
        """Exits the application."""
        raise SystemExit()

    def _create_project(self, args: list[str]) -> None:
        """Handles the create_project command."""
        if len(args) != 2:
            print("Invalid number of arguments.")
            return

        title, description = args
        project = self._service.create_project(title, description)
        print(f"Created project '{project.name}' with ID {project.id}.")

    def _list_projects(self, args: list[str]) -> None:
        """Handles the list_projects command."""
        projects = self._service.get_all_projects()
        if not projects:
            print("No projects found.")
            return

        print("Projects:")
        for project in projects:
            created_date = project.creation_date.strftime("%Y-%m-%d")
            print(f"  - ID: {project.id}, Name: '{project.name}', "
                  f"Description: '{project.description}', "
                  f"Created: {created_date}")

    def _add_task(self, args: list[str]) -> None:
        """Handles the add_task command."""
        if not (3 <= len(args) <= 4):
            print("Invalid number of arguments.")
            return

        project_id_str, title, description = args[:3]
        deadline = args[3] if len(args) == 4 else None

        project_id = self._parse_id(project_id_str, "Project")
        task = self._service.add_task_to_project(project_id, title,
                                                 description, deadline)

        print(f"Added task '{task.title}' with ID {task.id}.")

    def _edit_project(self, args: list[str]) -> None:
        """Handles the edit_project command."""
        if len(args) != 3:
            print("Invalid number of arguments.")
            return

        project_id_str, new_name, new_description = args
        project_id = self._parse_id(project_id_str, "Project")

        project = self._service.edit_project(project_id, new_name, new_description)
        print(f"Edited project '{project.name}' with ID {project.id}.")

    def _delete_project(self, args: list[str]) -> None:
        """Handles the delete_project command."""
        if len(args) != 1:
            print("Invalid number of arguments.")
            return

        project_id_str = args[0]
        project_id = self._parse_id(project_id_str, "Project")

        self._service.delete_project(project_id)
        print(f"Deleted project ID {project_id} and all of its tasks.")

    def _set_task_status(self, args: list[str]) -> None:
        """Handles the set_task_status command."""
        if len(args) != 3:
            print("Invalid number of arguments.")
            return

        project_id_str, task_id_str, new_status = args
        project_id = self._parse_id(project_id_str, "Project")
        task_id = self._parse_id(task_id_str, "Task")

        task = self._service.change_task_status(project_id, task_id, new_status)
        print(f"Changed status of task '{task.title}' with "
              f"ID {task.id} to '{new_status}'.")

    def _list_tasks(self, args: list[str]) -> None:
        """Handles the list_tasks command."""
        if len(args) != 1:
            print("Invalid number of arguments.")
            return

        project_id_str = args[0]
        project_id = self._parse_id(project_id_str, "Project")

        project = self._service.find_project_by_id(project_id)
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

    def _edit_task(self, args: list[str]) -> None:
        """Handles the edit_task command."""
        if not 5 <= len(args) <= 6:
            print("Invalid number of arguments.")
            return

        project_id_str, task_id_str, new_title, new_description, new_status = args[:5]
        new_deadline = args[5] if len(args) == 6 else None

        project_id = self._parse_id(project_id_str, "Project")
        task_id = self._parse_id(task_id_str, "Task")

        task = self._service.edit_task(project_id, task_id, new_title, new_description,
                                       new_status, new_deadline)

        print(f"Edited task '{task.title}' with ID {task.id} in "
              f"project ID {project_id}.")

    def _delete_task(self, args: list[str]) -> None:
        """Handles the delete_task command."""
        if len(args) != 2:
            print("Invalid number of arguments.")
            return

        project_id_str, task_id_str = args
        project_id = self._parse_id(project_id_str, "Project")
        task_id = self._parse_id(task_id_str, "Task")

        self._service.delete_task(project_id, task_id)
        print(f"Deleted task with ID {task_id} in project ID {project_id}.")

    def run(self) -> None:
        """Main loop for the CLI"""
        self._display_help([])
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

                command(args)

            except TodolistError as e:
                print(f"Error: {e}")
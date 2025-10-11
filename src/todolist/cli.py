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
            "create_project": self._create_project,
            "add_task": self._add_task,
            "edit_project": self._edit_project,
            "list_projects": self._list_projects,
            "help": self._display_help,
            "exit": self._exit
        }

    def _display_help(self, args: list[str]) -> None:
        """Displays the available commands."""
        print("Available commands:")
        print("  create_project <name> <description>")
        print("  add_task <project_id> <title> <description> [deadline:YYYY-MM-DD]")
        print("  edit_project <project_id> <new_title> <new_description>")
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

        try:
            project_id = int(project_id_str)
        except ValueError:
            print("Invalid project ID. Project ID must be an integer.")
            return

        task = self._service.add_task_to_project(project_id, title,
                                                 description, deadline)

        print(f"Added task '{task.title}' with ID {task.id}.")

    def _edit_project(self, args: list[str]) -> None:
        """Handles the edit_project command."""
        if len(args) != 3:
            print("Invalid number of arguments.")
            return

        project_id_str, new_name, new_description = args
        try:
            project_id = int(project_id_str)
        except ValueError:
            print("Invalid project ID. Project ID must be an integer.")
            return

        project = self._service.edit_project(project_id, new_name, new_description)
        print(f"Edited project '{project.name}' with ID {project.id}.")

    def run(self) -> None:
        """Main loop for the CLI"""
        self._display_help([])
        while True:
            try:
                raw_input = input("> ")
                if not raw_input:
                    continue

                parts = shlex.split(raw_input)
                command = parts[0]
                args = parts[1:]

                command = self._commands.get(command)
                if command is None:
                    print("Invalid command. Type 'help' for a list of commands.")
                    continue

                command(args)

            except TodolistError as e:
                print(f"Error: {e}")
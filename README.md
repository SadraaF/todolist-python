
# ToDo List - Python (Phase 1 - In-Memory)

This project is a command-line ToDo list application built in Python. It was developed as part of a software engineering course to demonstrate core Object-Oriented Programming (OOP) principles, clean architecture, and modern Python development practices.

In this first phase, the application uses in-memory storage, meaning all data is cleared when the program exits. The architecture is designed to be extensible, allowing for persistent storage (e.g., a database) to be added in future phases without altering the core business logic.

## Architectural Analysis

The application is divided into three distinct layers:

-   **Presentation Layer (`cli.py`):** Handles user input and output.
-   **Business Logic Layer (`service.py`):** Enforces application rules and constraints.
-   **Data Access Layer (`repository.py`):** Manages data storage and retrieval.

## Technologies Used

-   **Language:** Python 3.12+
-   **Dependency Management:** Poetry
-   **Core Libraries:** `python-dotenv` for managing environment configurations.

## How to Run

1.  **Prerequisites:**
    Ensure you have [Poetry](https://python-poetry.org/) installed on your system.

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/SadraaF/todolist-python.git
    cd todolist-python
    ```

3.  **Install dependencies:**
    Poetry will create a virtual environment and install the required packages from `pyproject.toml`.
    ```bash
    poetry install
    ```

4.  **Run the application:**
    Use Poetry to run the main script from within the project's virtual environment.
    ```bash
    poetry run python main.py
    ```

## Project Architecture

The codebase is organized into a modular, layered structure to ensure a clean separation of concerns:

-   `main.py`: The application's entry point. It initializes all components and wires them together using dependency injection.
-   `cli.py`: Implements the Command-Line Interface. It is responsible for parsing user commands and displaying output, but contains no business logic.
-   `service.py`: Contains the core business logic. It validates data, enforces rules (like project limits), and orchestrates calls to the repository.
-   `repository.py`: Manages data persistence. It defines an interface (`IProjectRepository`) and provides an `InMemoryProjectRepository` implementation.
-   `models.py`: Defines the primary data structures (`Project`, `Task`) using Python's `dataclasses`.
-   `exceptions.py`: Contains custom exception classes for handling application-specific errors cleanly.
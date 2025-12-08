"""Scheduler to run periodic background jobs for the application.

This script uses the 'schedule' library to run tasks at defined intervals.
It is designed to be run as a long-running process.
"""

import time
import schedule

from src.app.commands.autoclose_overdue import run_autoclose

def main() -> None:
    """Set up and run the scheduled jobs.

    This function configures the schedule for all periodic tasks and enters
    an infinite loop to execute them as they become due.
    """
    print("Starting scheduler...")

    schedule.every(15).minutes.do(run_autoclose)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
"""Scheduler to run periodic jobs."""

import time
import schedule

from src.app.commands.autoclose_overdue import run_autoclose

def main():
    """Sets up and runs the scheduled jobs."""
    print("Starting scheduler...")

    schedule.every(15).minutes.do(run_autoclose)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
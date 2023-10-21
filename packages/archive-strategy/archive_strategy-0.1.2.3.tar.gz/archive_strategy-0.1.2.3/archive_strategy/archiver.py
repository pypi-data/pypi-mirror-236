"""
@name: archive_backups.py
@description: This script will archive the backups according to the pre-defined
              retention policy.
@author: Pieter Paulussen
"""

import shutil
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from rich.console import Console

Console = Console()


class Archiver:
    def __init__(self, base_dir, archive_dir, archive_user, archive_group=None, test_mode=False, delete=False):
        self.base_dir = base_dir
        self.archive_dir = archive_dir
        self.archive_user = archive_user
        self.test_mode = test_mode
        self.delete = delete
        self.backups = []

        if archive_group is None:
            self.archive_group = archive_user
        else:
            self.archive_group = archive_group

    def show_info(self):
        Console.log(f"Config: Archive directory: {self.archive_dir}")
        Console.log(f"Config: Archive user: {self.archive_user}")
        Console.log(f"Config: Archive group: {self.archive_group}")
        Console.log(f"Config: Test mode: {self.test_mode}")
        Console.log(f"Config: Delete backups: {self.delete}")

    def own(self, path):
        if not self.test_mode:
            shutil.chown(path, user=self.archive_user, group=self.archive_group)
        Console.log(
            f"Backup {path} is now owned by {self.archive_user}:{self.archive_group}"
        )

    def move(self, path, target):
        if not self.test_mode:
            # Check if the file is accessed by another process
            try:
                path.rename(path)
                path.replace(target)
            except PermissionError:
                Console.log(
                    f"Could not move {path}. It is being accessed by another "
                    f"process.", style="bold red"
                )

        Console.log(f"Moved {path.name} to {target}")
        return target

    def remove_backup(self, path):
        if not self.test_mode and self.delete:
            path.unlink()
        Console.log(f"Deleting {path}")

    def archive(self):
        Console.log("Starting Archiver", style="bold green")

        # Move all files in the customer directory to the archive directory
        for customer_dir in Path(self.base_dir).iterdir():
            self.backups = []
            if not customer_dir.is_dir():
                Console.log(f"Ignoring {customer_dir}")
                continue

            # Ensure an archive directory exists for the customer
            archive_dir = Path(self.archive_dir, customer_dir.name)
            if not archive_dir.exists():
                archive_dir.mkdir()

            # Move all *.gz files in the customer directory to the archive directory
            for backup_elem in customer_dir.glob("*.gz"):
                target_location = Path(archive_dir, backup_elem.name)
                self.own(backup_elem)
                self.move(backup_elem, target_location)

    def prepare_archive_folders(self, customer_dir):
        # Create the daily, weekly and monthly directories if they don't exist
        daily_dir = Path(customer_dir, "daily")
        if not daily_dir.exists():
            Console.log(f"Created {customer_dir} daily folder", style="white")
            daily_dir.mkdir()

        weekly_dir = Path(customer_dir, "weekly")
        if not weekly_dir.exists():
            Console.log(f"Created {customer_dir} weekly folder", style="white")
            weekly_dir.mkdir()

        monthly_dir = Path(customer_dir, "monthly")
        if not monthly_dir.exists():
            Console.log(f"Created {customer_dir} monthly folder", style="white")
            monthly_dir.mkdir()

        return daily_dir, weekly_dir, monthly_dir

    def organise(self):
        # Part 2: Organize the archive folder according to the retention policy
        # Iterate over all customer directories in the archive directory
        for customer_dir in Path(self.archive_dir).iterdir():
            self.backups = []
            if not customer_dir.is_dir():
                Console.log(f"Ignoring {customer_dir}")
                continue

            Console.log(f"Re-organizing folder for {customer_dir.name}", style="bold green")
            daily, weekly, monthly = self.prepare_archive_folders(customer_dir)

            # Iterate over all backup files in the customer directory (including those
            # in the daily, weekly and monthly directories) and organize them in a list
            for backup_elem in customer_dir.rglob("*.gz"):
                # The first part of the filename is the epoch timestamp
                backup_dt = datetime.fromtimestamp(int(backup_elem.name.split("_")[0]))
                age = datetime.now() - backup_dt
                self.backups.append(
                    {
                        "path": backup_elem,
                        "timestamp": backup_dt,
                        "age": age,
                        "week": backup_dt.isocalendar()[1],
                        "month": backup_dt.month,
                    }
                )

            self.cleanup(customer_dir, daily, weekly, monthly)

    def cleanup(self, customer_dir, daily, weekly, monthly):
        self.backups.sort(key=lambda x: x["timestamp"])

        # Iterate over the backups and move them to the correct directory
        weeks = defaultdict(list)
        months = defaultdict(list)
        for backup in self.backups:
            Console.log(f"{customer_dir.name}: Processing {backup['path'].name}. Age: {backup['age']}")

            # If the backup is less than 3 days old, move it to the daily directory
            if backup["age"] < timedelta(days=3):
                backup['path'] = self.move(backup['path'], Path(daily, backup['path'].name))

            # If the backup is less than 4 weeks old, move it to the weekly directory
            elif backup["age"] < timedelta(weeks=4):
                backup['path'] = self.move(backup['path'], Path(weekly, backup['path'].name))
                weeks[backup["week"]].append(backup)

            # If the backup is less than 12 months old, move it to the monthly directory
            elif backup["age"] < timedelta(days=365):
                backup['path'] = self.move(backup['path'], Path(monthly, backup['path'].name))
                months[backup["month"]].append(backup)

        for week, backups in weeks.items():
            if len(backups) > 1:
                # Sort youngest to oldest
                backups.sort(key=lambda backup: backup["age"])
                to_delete = backups[1:]
                # Remove oldest backup from the list
                for backup in to_delete:
                    Console.log(f"{customer_dir.name}: Backup {backup['path'].name} is no longer the most recent backup for week {week}. Deleting it.")
                    self.remove_backup(backup['path'])

        for month, backups in months.items():
            if len(backups) > 1:
                # Sort youngest to oldest
                backups.sort(key=lambda backup: backup["age"])
                # Remove oldest backup from the list
                to_delete = backups[1:]
                for backup in to_delete:
                    Console.log(f"{customer_dir.name}: Backup {backup['path'].name} is no longer the most recent backup for month {month}. Deleting it.")
                    self.remove_backup(backup['path'])

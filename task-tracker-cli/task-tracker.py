#!/usr/bin/env python3

from datetime import datetime
from dataclasses import dataclass, asdict
import sys
import uuid
from pathlib import Path
import json
import argparse

from typing import Any, List

# --- Aesthetics Configuration ---

@dataclass(frozen=True)
class Colors:
    """Catppuccin Mocha Palette (TrueColor)"""
    RESET: str = "\033[0m"
    BOLD: str = "\033[1m"
    DIM: str = "\033[2m"
    
    # Core Colors
    ROSEWATER: str = "\033[38;2;245;224;220m"
    FLAMINGO: str = "\033[38;2;242;205;205m"
    PINK: str = "\033[38;2;245;194;231m"
    MAUVE: str = "\033[38;2;203;166;247m"
    RED: str = "\033[38;2;237;135;150m"
    MAROON: str = "\033[38;2;238;153;160m"
    PEACH: str = "\033[38;2;245;169;127m"
    YELLOW: str = "\033[38;2;238;212;159m"
    GREEN: str = "\033[38;2;166;227;161m"
    TEAL: str = "\033[38;2;148;226;213m"
    SKY: str = "\033[38;2;137;220;235m"
    SAPPHIRE: str = "\033[38;2;122;162;247m"
    BLUE: str = "\033[38;2;137;180;250m"
    LAVENDER: str = "\033[38;2;180;190;254m"
    TEXT: str = "\033[38;2;205;214;244m"
    SUBTEXT1: str = "\033[38;2;186;194;222m"
    OVERLAY0: str = "\033[38;2;108;112;134m"

@dataclass(frozen=True)
class Icons:
    """Nerd Font Glyphs"""
    CHECK: str = ""
    ERROR: str = ""
    WARN: str = ""
    INFO: str = ""
    TASK: str = ""
    CALENDAR: str = ""
    CLOCK: str = ""
    EDIT: str = ""
    TRASH: str = ""
    TODO: str = ""
    PROGRESS: str = ""
    DONE: str = ""
    ARROW: str = ""

C = Colors()
I = Icons()

# --- Application Logic ---

@dataclass
class Task:
    description: str
    id: int = str(uuid.uuid4())
    status: str = "todo"
    createdAt: str = (datetime.now()).strftime("%Y/%m/%d %H:%M:%S")
    updatedAt: str = ""

    @staticmethod
    def _check_description(description: str) -> str:
        """Validate the value and type of the description"""
        if description.isspace():
            raise ValueError(
                f"{C.RED}{I.ERROR} Invalid Input!{C.RESET} The description cannot ONLY contain whitespaces!"
            )

        description_length = len(description)
        if description_length > 100:
            raise ValueError(
                f"{C.RED}{I.ERROR} Length Error:{C.RESET} The description length ({description_length}) CANNOT be GREATER THAN 100 CHARACTERS."
            )

        return description

    @staticmethod
    def _check_status(status) -> str:
        """Validate the value and type of the status"""
        if status not in ["todo", "in-progress", "done"]:
            raise ValueError(
                f"{C.RED}{I.ERROR} Invalid Status!{C.RESET} Allowed values: {C.YELLOW}'todo', 'in-progress', 'done'{C.RESET}"
            )

        return status

    def __post_init__(self) -> None:
        """Check the input values of the isinstance in the initiation."""
        self.description = self._check_description(self.description)
        self.status = self._check_status(self.status)

    def _update_date_time(self) -> None:
        self.updatedAt = (datetime.now()).strftime("%Y/%m/%d %H:%M:%S")

    def print_description(self) -> None:
        # Determine icon color based on status
        status_color = C.TEXT
        status_icon = I.TODO
        if self.status == "in-progress":
            status_color = C.YELLOW
            status_icon = I.PROGRESS
        elif self.status == "done":
            status_color = C.GREEN
            status_icon = I.DONE

        print(f"{C.MAUVE}╭──────────────────────────────────────────────────────────────╮{C.RESET}")
        print(f"{C.MAUVE}│{C.RESET} {C.BOLD}{C.LAVENDER}{I.TASK} Task ID:{C.RESET} {self.id}")
        print(f"{C.MAUVE}│{C.RESET} {C.BOLD}Description:{C.RESET} {self.description}")
        print(f"{C.MAUVE}│{C.RESET} {C.BOLD}Status:{C.RESET}      {status_color}{status_icon} {self.status.upper()}{C.RESET}")
        print(f"{C.MAUVE}│{C.RESET} {C.DIM}{I.CALENDAR} Created:  {self.createdAt}{C.RESET}")
        if self.updatedAt:
            print(f"{C.MAUVE}│{C.RESET} {C.DIM}{I.CLOCK} Updated:  {self.updatedAt}{C.RESET}")
        print(f"{C.MAUVE}╰──────────────────────────────────────────────────────────────╯{C.RESET}\n")

    def set_description(self, new_description) -> None:
        old_description = self.description
        old_updated_date_time = self.updatedAt

        try:
            self.description = self._check_description(new_description[0])
            print(f"{C.BLUE}{I.EDIT} Update Successful:{C.RESET}")
            print(f"  {C.OVERLAY0}ID:{C.RESET} {self.id}")
            print(f"  {C.RED}-{C.RESET} {old_description}")
            print(f"  {C.GREEN}+{C.RESET} {self.description}")
            self._update_date_time()
        except Exception as e:
            print(f"{C.RED}{I.ERROR} Update Failed!{C.RESET}\n{C.DIM}{e}{C.RESET}")
            self.description = old_description
            self.updatedAt = old_updated_date_time

    def set_status(self, input_status: str) -> None:
        old_status = self.status
        old_updated_date_time = self.updatedAt

        try:
            self.status = self._check_status(input_status)
            print(f"{C.TEAL}{I.CHECK} Status Updated:{C.RESET}")
            print(f"  {C.OVERLAY0}ID:{C.RESET} {self.id}")
            print(f"  {C.RED}-{C.RESET} {old_status}")
            print(f"  {C.GREEN}+{C.RESET} {self.status}")
            self._update_date_time()
        except Exception as e:
            print(f"{C.RED}{I.ERROR} Status Update Failed!{C.RESET}\n{C.DIM}{e}{C.RESET}")
            self.status = old_status
            self.updatedAt = old_updated_date_time


@dataclass
class TaskList:
    list = []

    @staticmethod
    def load_json_file() -> List[dict[str | Any]]:
        """Load the data from the json file"""
        file_path = "taskDB.json"
        path = Path(file_path)
        try:
            if not path.exists():
                with open(file_path, "w") as f:
                    f.write("")
                return []
            else:
                with open(file_path, "r") as f:
                    content = f.read()
                    if not content.strip():  # Check for empty file
                        return []
                    f.seek(0)
                    json_data = json.load(f)

                return [Task(**item) for item in json_data]

        except FileNotFoundError as e:
            print(f"{C.RED}{I.ERROR} File Not Found:{C.RESET} {file_path}\n{C.DIM}{e}{C.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{C.RED}{I.ERROR} Unexpected Error:{C.RESET}\n{C.DIM}{e}{C.RESET}")
            sys.exit(1)

    def write_json_file(self) -> None:
        """Write into json file"""
        file_path = "taskDB.json"

        json_data = [asdict(obj) for obj in self.list]
        try:
            with open(file_path, "w") as f:
                json.dump(json_data, f, indent=4)
        except FileNotFoundError as e:
            print(f"{C.RED}{I.ERROR} Database Missing:{C.RESET} {file_path}\n{C.DIM}{e}{C.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{C.RED}{I.ERROR} Write Error:{C.RESET}\n{C.DIM}{e}{C.RESET}")
            sys.exit(1)

    def __post_init__(self) -> None:
        self.list = self.load_json_file()

    def create_task(self, description: str) -> None:
        new_task = Task(description)
        self.list.append(new_task)
        self.write_json_file()
        print(f"{C.GREEN}{I.CHECK} Task Created Successfully!{C.RESET}")
        print(f"  {C.BOLD}ID:{C.RESET} {new_task.id}")
        print(f"  {C.BOLD}Desc:{C.RESET} {description}")

    def return_specific_task(self, id: str) -> Task:
        for task in self.list:
            if task.id == id[0]:
                return task

        print(f"{C.RED}{I.ERROR} Task Not Found:{C.RESET} ID {C.YELLOW}{id[0]}{C.RESET} does not exist.")
        sys.exit(1)

    def remove_specific_task(self, id: str) -> None:
        try:
            list_cp = self.list[:]
            found = False
            for task_index, task in enumerate(list_cp):
                if list_cp[task_index].id in id:
                    self.list.remove(task)
                    print(f"{C.RED}{I.TRASH} Deleted Task:{C.RESET} {C.DIM}{task.id}{C.RESET}")
                    found = True
            
            if not found:
                 print(f"{C.YELLOW}{I.WARN} No task found with ID:{C.RESET} {id}")
                 
        except IndexError as e:
            print(f"{C.RED}{I.ERROR} Index Error:{C.RESET}\n{C.DIM}{e}{C.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{C.RED}{I.ERROR} Error Removing Task:{C.RESET}\n{C.DIM}{e}{C.RESET}")
            sys.exit(1)


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"{C.MAUVE}{I.TASK} Task-CLI Tracker{C.RESET} - Manage your tasks efficiently."
    )

    subparsers = parser.add_subparsers(dest="command", help="The available commands")

    add_parser = subparsers.add_parser("add", help="Add task.")
    add_parser.add_argument("description", type=str, help="Task description", nargs=1)

    list_parser = subparsers.add_parser("list", help="List the tasks by status or all.")
    list_parser.add_argument(
        "list",
        help="[type]",
        default="all",
        nargs="?",
        choices=["all", "in-progress", "todo", "done"],
    )

    update_parser = subparsers.add_parser("update", help="Update description")
    update_parser.add_argument("id", type=str, help="ID of the task", nargs=1)
    update_parser.add_argument("description", type=str, help="New description", nargs=1)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=str, help="ID of the task", nargs="+")

    mark_progress_parser = subparsers.add_parser(
        "mark-in-progress", help="Mark a task as 'in-progress'"
    )
    mark_progress_parser.add_argument("id", type=str, help="ID of the task", nargs=1)

    mark_done_parser = subparsers.add_parser("mark-done", help="Mark a task as 'done'")
    mark_done_parser.add_argument("id", type=str, help="ID of the task", nargs=1)

    mark_todo_parser = subparsers.add_parser("mark-todo", help="Mark a task as 'todo'")
    mark_todo_parser.add_argument("id", help="ID of the task", nargs=1)

    args = parser.parse_args()

    return args


def main():
    args = arguments()
    task_list = TaskList()

    if args.command == "add":
        task_list.create_task(args.description[0])

    if args.command == "mark-todo":
        task = task_list.return_specific_task(args.id)
        task.set_status("todo")
        task_list.write_json_file()

    if args.command == "mark-in-progress":
        task = task_list.return_specific_task(args.id)
        task.set_status("in-progress")
        task_list.write_json_file()

    if args.command == "mark-done":
        task = task_list.return_specific_task(args.id)
        task.set_status("done")
        task_list.write_json_file()

    if args.command == "delete":
        task_list.remove_specific_task(args.id)
        task_list.write_json_file()

    if args.command == "update":
        task = task_list.return_specific_task(args.id)
        task.set_description(args.description)
        task_list.write_json_file()

    if args.command == "list":
        count = 0
        if args.list == "all":
            for task in task_list.list:
                task.print_description()
                count += 1
        elif args.list in ["done", "in-progress", "todo"]:
            for task in task_list.list:
                if task.status == args.list:
                    task.print_description()
                    count += 1
        
        if count == 0:
            print(f"{C.OVERLAY0}{I.INFO} No tasks found for category: {args.list}{C.RESET}")


if __name__ == "__main__":
    main()

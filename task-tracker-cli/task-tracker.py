#!/usr/bin/env python3

from datetime import datetime
from dataclasses import dataclass, asdict
import sys
import uuid
from pathlib import Path
import json
import argparse

from typing import Any, List


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
                "Invalid Input! The description cannot ONLY contain whitespaces!"
            )

        description_length = len(description)
        if description_length > 100:
            raise ValueError(
                f"The length of the description: {description_length}\n The length of the description CANNOT be GREATER THAN 100 CHARACTERS."
            )

        return description

    @staticmethod
    def _check_status(status) -> str:
        """Validate the value and type of the status"""
        if status not in ["todo", "in-progress", "done"]:
            raise ValueError(
                "The input value of the status is Invalid! There are already three status: 'todo', 'in-progress', 'done'"
            )

        return status

    def __post_init__(self) -> None:
        """Check the input values of the isinstance in the initiation."""
        self.description = self._check_description(self.description)
        self.status = self._check_status(self.status)

    def _update_date_time(self) -> None:
        self.updatedAt = (datetime.now()).strftime("%Y/%m/%d %H:%M:%S")

    def print_description(self) -> None:
        print(
            f"Task:\n\tID: {self.id}\n\tDescription: {self.description}\n\tStatus: {self.status}\n\tCreated At: {self.createdAt}\n\tUpdated At: {self.updatedAt}\n"
        )
        print("-------------------------------------------------------------\n")

    def set_description(self, new_description) -> None:
        old_description = self.description
        old_updated_date_time = self.updatedAt

        try:
            self.description = self._check_description(new_description[0])
            print(
                f"Task: {self.id}\nOld Description: {old_description}\nNew Description: {self.description}"
            )
            self._update_date_time()
        except Exception as e:
            print(f"Something went wrong!\n\nMore detail: {e}")
            self.description = old_description
            self.updatedAt = old_updated_date_time

    def set_status(self, input_status: str) -> None:
        old_status = self.status
        old_updated_date_time = self.updatedAt

        try:
            self.status = self._check_status(input_status)
            print(
                f"Task: {self.id}\nDescription: {self.description}\nOld Status: {old_status}\nNew Status: {self.status}"
            )
            self._update_date_time()
        except Exception as e:
            print(f"Something went wrong!\n\nMore detail: {e}")
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
                    json_data = json.load(f)

                return [Task(**item) for item in json_data]

        except FileNotFoundError as e:
            print(f"Could not found the {file_path}.\nMore detail: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An Exception ocurred.\nMore detail: {e}")
            sys.exit(1)

    def write_json_file(self) -> None:
        """Write into json file"""
        file_path = "taskDB.json"

        json_data = [asdict(obj) for obj in self.list]
        try:
            with open(file_path, "w") as f:
                json.dump(json_data, f, indent=4)
        except FileNotFoundError as e:
            print(f"Could Not find the {file_path} 'taskDB.json'\nMore detail: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An Exception ocurred: {e}")
            sys.exit(1)

    def __post_init__(self) -> None:
        self.list = self.load_json_file()

    def create_task(self, description: str) -> None:
        self.list.append(Task(description))
        self.write_json_file()

    def return_specific_task(self, id: str) -> Task:
        for task in self.list:
            if task.id == id[0]:
                return task

        raise ValueError("The ID could not found.\n")

    def remove_specific_task(self, id: str) -> None:
        for task_number in range(len(self.list)):
            if self.list[task_number].id == id[0]:
                del self.list[task_number]
                self.write_json_file()
                print(f"The {id} sucessfully deleted!")
                return None

        raise ValueError("The ID could not found.\n")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manage your tasks in terminal environment with Task-CLI"
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
    delete_parser.add_argument("id", type=str, help="ID of the task", nargs=1)

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
        if args.list == "all":
            for task in task_list.list:
                task.print_description()
        elif args.list in ["done", "in-progress", "todo"]:
            for task in task_list.list:
                if task.status == args.list:
                    task.print_description()


if __name__ == "__main__":
    main()

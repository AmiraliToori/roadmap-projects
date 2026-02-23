#!/usr/bin/env python3

import json
import sys
import argparse
import os

from datetime import datetime
from pathlib import Path
from typing import Any


# ─────────────────────────────────────────────────────────────────────────────
#  Catppuccin Mocha · ANSI TrueColor palette
# ─────────────────────────────────────────────────────────────────────────────
_MAUVE   = "\033[38;2;203;166;247m"   # accent / headers
_TEXT    = "\033[38;2;205;214;244m"   # primary text
_GREEN   = "\033[38;2;166;227;161m"   # success / done
_RED     = "\033[38;2;243;139;168m"   # error
_YELLOW  = "\033[38;2;249;226;175m"   # in-progress / warning
_BLUE    = "\033[38;2;137;180;250m"   # IDs / numeric accents
_PEACH   = "\033[38;2;250;179;135m"   # delete / destructive
_SUBTEXT = "\033[38;2;166;173;200m"   # dates / secondary info
_BOLD    = "\033[1m"
_DIM     = "\033[2m"
_RESET   = "\033[0m"

# Nerd Font glyphs
_ICON_ADD      = "\uf067"   # 
_ICON_DELETE   = "\uf1f8"   # 
_ICON_EDIT     = "\uf044"   # 
_ICON_BOLT     = "\uf0e7"   # 
_ICON_DONE     = "\uf00c"   # 
_ICON_PROGRESS = "\uf110"   # 
_ICON_TODO     = "\uf10c"   # 
_ICON_DB       = "\uf1c0"   # 
_ICON_WARN     = "\uf071"   # 
_ICON_BAN      = "\uf05e"   # 
_ICON_ARROW    = "\uf061"   # 


def _fmt_error_db(msg: str, detail: Any) -> str:
    """Format a database-level error (JSON decode / schema)."""
    return (
        f"\n  {_RED}{_BOLD}{_ICON_DB}  Database Error{_RESET}\n"
        f"  {_RED}{msg}{_RESET}\n"
        f"  {_DIM}{_SUBTEXT}Detail › {detail}{_RESET}\n"
    )


def _fmt_error_notfound(item_id: Any, detail: Any) -> str:
    """Format a not-found error."""
    return (
        f"\n  {_RED}{_BOLD}{_ICON_WARN}  Not Found{_RESET}\n"
        f"  {_RED}Could not find task {_BOLD}#{item_id}{_RESET}{_RED} in the database.{_RESET}\n"
        f"  {_DIM}{_SUBTEXT}Detail › {detail}{_RESET}\n"
    )


def _fmt_error_io(detail: Any) -> str:
    """Format an I/O write error."""
    return (
        f"\n  {_RED}{_BOLD}{_ICON_BAN}  I/O Error{_RESET}\n"
        f"  {_RED}Something went wrong while writing to the database.{_RESET}\n"
        f"  {_DIM}{_SUBTEXT}Detail › {detail}{_RESET}\n"
    )


def _color_status(status_str: str) -> str:
    """Return a colored, icon-prefixed status token for any status string variant."""
    s = status_str
    if s in ("done", "[x]"):
        return f"{_GREEN}{_BOLD}{_ICON_DONE}  [x]{_RESET}"
    elif s in ("in-progress", "[-]"):
        return f"{_YELLOW}{_BOLD}{_ICON_PROGRESS}  [-]{_RESET}"
    elif s in ("todo", "[ ]"):
        return f"{_MAUVE}{_BOLD}{_ICON_TODO}  [ ]{_RESET}"
    else:
        return f"{_SUBTEXT}{s}{_RESET}"


# ─────────────────────────────────────────────────────────────────────────────


def handle_path() -> Path:
    """Handle path and directory of configs"""
    file_name = "taskDB.json"
    directory = ".config/task-tracker/"
    home_path = os.getenv("HOME")

    config_directory = os.path.join(home_path, directory)

    if not os.path.exists(config_directory):
        os.mkdir(config_directory)

    full_path = os.path.join(config_directory, file_name)

    return Path(full_path)


class TaskList:
    def _read_json() -> Any:
        """Read and return the json file"""

        def validate_database_dict(python_obj: Any) -> Any:
            """Validate the schema and data in the python object"""
            if not python_obj.get("id_counter"):
                python_obj.update({"id_counter": {"counter": 1, "available_ids": []}})

            if not python_obj.get("items"):
                python_obj.update({"items": {}})

            return python_obj

        def update_counter(python_obj: Any) -> Any:
            """Update the counter and fetch the maximum counter"""
            task_items = python_obj.get("items")
            max_number = 0
            for id, item in task_items.items():
                item_id = int(id)

                max_number = max(item_id, max_number)

            python_obj["id_counter"].update({"counter": max_number})

            return python_obj

        path = handle_path()

        try:
            with open(path, "r", encoding="utf-8") as f:
                python_obj = json.load(f)

            python_obj = validate_database_dict(python_obj)
            python_obj = update_counter(python_obj)

            return python_obj

        except json.JSONDecodeError as e:
            print(_fmt_error_db("Failed to decode the database JSON file.", e))
            sys.exit(1)

        except FileNotFoundError as e:
            print(_fmt_error_db("Database file could not be found.", e))
            sys.exit(1)

    _id_counter = 0
    _available_ids = []
    _database_dict = _read_json()

    @classmethod
    def _load_counter(cls) -> None:
        """Load the current ID counter"""
        cls._id_counter = cls._database_dict.get("id_counter").get("counter", 1)
        cls._available_ids = cls._database_dict.get("id_counter").get(
            "available_ids", []
        )

    @classmethod
    def _write(cls) -> None:
        """Write the python dictionary object to json"""
        path = handle_path()

        with open(path, "w", encoding="utf-8") as f:
            json.dump(cls._database_dict, f, indent=4)

    @classmethod
    def _save_id(cls) -> int:
        """Save the ID"""
        cls._load_counter()

        if not cls._available_ids:
            cls._id_counter = cls._id_counter + 1
            cls._database_dict["id_counter"].update({"counter": cls._id_counter})

            return cls._id_counter
        else:
            popped_id = cls._available_ids.pop(0)
            cls._database_dict["id_counter"].update(
                {"available_ids": cls._available_ids}
            )

            return popped_id

    def __init__(self) -> None:
        self._load_counter()
        self._write()

    @classmethod
    def add_task(cls, description: str) -> None:
        """Add a task"""
        try:
            id = cls._save_id()
            input_description = description
            created_date = (datetime.now()).strftime("%Y/%m/%d %H:%M:%S")
            status = "todo"

            cls._database_dict["items"].update(
                {
                    str(id): {
                        "description": input_description,
                        "status": status,
                        "createdAt": created_date,
                        "updatedAt": "N/A",
                    }
                }
            )

            cls._write()

            print(
                f"\n  {_GREEN}{_BOLD}{_ICON_ADD}  Task Added{_RESET}\n"
                f"  {_SUBTEXT}ID          {_RESET}{_BLUE}{_BOLD}#{id}{_RESET}\n"
                f"  {_SUBTEXT}Description {_RESET}{_TEXT}{description}{_RESET}\n"
            )

        except IndexError as e:
            print(_fmt_error_notfound(id, e))
            sys.exit(1)

        except IOError as e:
            print(_fmt_error_io(e))
            sys.exit(1)

    @classmethod
    def delete_task(cls, id: str) -> None:
        """Delete a task"""
        try:
            deleted_id = id
            del cls._database_dict["items"][deleted_id]
            cls._available_ids.append(deleted_id)

            cls._write()

            print(
                f"\n  {_PEACH}{_BOLD}{_ICON_DELETE}  Task Deleted{_RESET}\n"
                f"  {_SUBTEXT}ID {_RESET}{_BLUE}{_BOLD}#{id}{_RESET}{_PEACH} has been removed from the database.{_RESET}\n"
            )

        except IndexError as e:
            print(_fmt_error_notfound(id, e))
            sys.exit(1)

        except IOError as e:
            print(_fmt_error_io(e))
            sys.exit(1)

    @staticmethod
    def _get_current_datetime() -> str:
        return (datetime.now()).strftime("%Y/%m/%d %H:%M:%S")

    @classmethod
    def update_status(cls, id: str, status: str) -> None:
        """Update the status of a task"""
        try:
            cls._database_dict["items"][id].update(
                {"status": status, "updatedAt": cls._get_current_datetime()}
            )

            cls._write()

            print(
                f"\n  {_MAUVE}{_BOLD}{_ICON_BOLT}  Status Updated{_RESET}\n"
                f"  {_SUBTEXT}ID         {_RESET}{_BLUE}{_BOLD}#{id}{_RESET}\n"
                f"  {_SUBTEXT}New Status {_RESET}{_color_status(status)}\n"
            )

        except IndexError as e:
            print(_fmt_error_notfound(id, e))
            sys.exit(1)

        except IOError as e:
            print(_fmt_error_io(e))
            sys.exit(1)

    @classmethod
    def update_description(cls, id: str, description: str) -> None:
        """update the description of a task"""
        try:
            cls._database_dict["items"][id].update(
                {"description": description, "updatedAt": cls._get_current_datetime()}
            )

            cls._write()

            print(
                f"\n  {_MAUVE}{_BOLD}{_ICON_EDIT}  Description Updated{_RESET}\n"
                f"  {_SUBTEXT}ID          {_RESET}{_BLUE}{_BOLD}#{id}{_RESET}\n"
                f"  {_SUBTEXT}Description {_RESET}{_TEXT}{description}{_RESET}\n"
            )

        except IndexError as e:
            print(_fmt_error_notfound(id, e))
            sys.exit(1)

        except IOError as e:
            print(_fmt_error_io(e))
            sys.exit(1)

    @classmethod
    def display_tasks(cls) -> None:
        """Print all the tasks"""
        dict_items = cls._database_dict.get("items")

        for id, item in dict_items.items():
            item_id = id
            description = item.get("description", "N/A")
            status = item.get("status", "N/A")
            created_date = item.get("createdAt", "N/A")
            update_date = item.get("updatedAt", "N/A")

            if status == "done":
                status = "[x]"
            elif status == "in-progress":
                status = "[-]"
            elif status == "todo":
                status = "[ ]"

            print(
                f"  {_color_status(status)}  "
                f"{_BLUE}{_BOLD}#{item_id:<4}{_RESET}  "
                f"{_SUBTEXT}{created_date}{_RESET}  "
                f"{_DIM}{_SUBTEXT}(U: {update_date}){_RESET}  "
                f"{_MAUVE}{_ICON_ARROW}{_RESET}  "
                f"{_TEXT}{description}{_RESET}"
            )

    @classmethod
    def filter_display_tasks(cls, status: str) -> None:
        """Print specific tasks with requested status"""
        dict_items = cls._database_dict["items"]

        for id, item in dict_items.items():
            item_id = id
            description = item.get("description", "N/A")
            item_status = item.get("status", "N/A")
            created_date = item.get("createdAt", "N/A")
            update_date = item.get("updatedAt", "N/A")

            if status == item_status:
                if status == "done":
                    status = "[x]"
                elif status == "in-progress":
                    status = "[-]"
                elif status == "todo":
                    status = "[ ]"

            print(
                f"  {_color_status(status)}  "
                f"{_BLUE}{_BOLD}#{item_id:<4}{_RESET}  "
                f"{_SUBTEXT}{created_date}{_RESET}  "
                f"{_DIM}{_SUBTEXT}(U: {update_date}){_RESET}  "
                f"{_MAUVE}{_ICON_ARROW}{_RESET}  "
                f"{_TEXT}{description}{_RESET}"
            )


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Task-CLI Tracker - Manage your tasks efficiently."
    )

    subparsers = parser.add_subparsers(dest="command", help="The available commands")

    add_parser = subparsers.add_parser("add", help="Add task.")
    add_parser.add_argument(
        "--description", required=True, type=str, help="Task description", nargs=1
    )

    list_parser = subparsers.add_parser("list", help="List the tasks by status or all.")
    list_parser.add_argument(
        "--status",
        help="Display a specific tasks with desired status",
        required=False,
        nargs=1,
        choices=["in-progress", "todo", "done"],
    )

    update_parser = subparsers.add_parser("update", help="Update description")
    update_parser.add_argument(
        "--id", type=str, required=True, help="ID of the task", nargs=1
    )
    update_parser.add_argument(
        "--description", type=str, required=True, help="New description", nargs=1
    )

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument(
        "--id", type=str, required=True, help="ID of the task", nargs=1
    )

    mark_progress_parser = subparsers.add_parser(
        "mark-in-progress", help="Mark a task as 'in-progress'"
    )
    mark_progress_parser.add_argument(
        "--id", type=str, required=True, help="ID of the task", nargs=1
    )

    mark_done_parser = subparsers.add_parser("mark-done", help="Mark a task as 'done'")
    mark_done_parser.add_argument(
        "--id", type=str, required=True, help="ID of the task", nargs=1
    )

    mark_todo_parser = subparsers.add_parser("mark-todo", help="Mark a task as 'todo'")
    mark_todo_parser.add_argument(
        "--id", type=str, required=True, help="ID of the task", nargs=1
    )

    args = parser.parse_args()

    return args


def main() -> None:
    args = arguments()

    task_list = TaskList()

    if args.command == "add":
        task_list.add_task(args.description[0])

    if args.command == "mark-todo":
        task_list.update_status(args.id[0], "todo")

    if args.command == "mark-in-progress":
        task_list.update_status(args.id[0], "in-progress")

    if args.command == "mark-done":
        task_list.update_status(args.id[0], "done")

    if args.command == "delete":
        task_list.delete_task(args.id[0])
    if args.command == "update":
        task_list.update_description(args.id[0], args.description[0])

    if args.command == "list":
        if args.status:
            task_list.filter_display_tasks(args.status[0])
        else:
            task_list.display_tasks()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import sys
import re
import os

from datetime import datetime


############## Expense Class #################


class Expense:
    @staticmethod
    def _handle_path() -> Path:
        file_name = "expenseDB.json"
        home_path = os.getenv("HOME")
        config_path = ".config/expense-tracker/"

        config_directory = os.path.join(home_path, config_path)
        full_path = os.path.join(home_path, config_path, file_name)

        if not os.path.exists(config_directory):
            os.mkdir(config_directory)
            print(f"Making the config directory at {config_directory}...")

        return full_path

    file_path = Path(_handle_path())

    @staticmethod
    def _load_python_object(file_path: Path):
        """Load json file and return a Python object"""
        try:
            if file_path.exists():
                with open(file_path, "r") as f:
                    dict_object = json.load(f)
                    return dict_object
            else:
                id_counter_obj = {
                    "id_counter": {"counter": 1, "available_ids": []},
                    "items": {},
                }

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(id_counter_obj, f, indent=4)

                with open(file_path, "r") as f:
                    dict_object = json.load(f)
                    return dict_object

        except IOError as e:
            print(f"Something went wrong when writing and loading!\nMore detail: {e}")
            sys.exit(1)

        except json.JSONDecodeError as e:
            print(f"The json file is not valid for reading!\nMore detail: {e}")
            sys.exit(1)

        except Exception as e:
            print(f"A rare exception ocurred!\nMore detail: {e}")
            sys.exit(1)

    python_json_object = _load_python_object(file_path)
    id_counter = 1
    available_ids = []

    @classmethod
    def _load_counter(cls) -> None:
        """Load ID counter"""
        try:
            cls.id_counter = cls.python_json_object.get("id_counter").get("counter")
            cls.available_ids = cls.python_json_object.get("id_counter").get(
                "available_ids"
            )
        except Exception as e:
            print(f"A rare exception ocurred!\nMore detail: {e}")
            sys.exit(1)

    @classmethod
    def _write_counter(cls) -> None:
        """Write new counter"""
        try:
            with open(cls.file_path, "w", encoding="utf-8") as f:
                cls.python_json_object["id_counter"]["counter"] = cls.id_counter
                cls.python_json_object["id_counter"]["available_ids"] = (
                    cls.available_ids
                )
                json.dump(cls.python_json_object, f, indent=4)

        except IOError as e:
            print(f"Something went wrong when writing and loading\nMore detail: {e}")
            sys.exit(1)

        except Exception as e:
            print(f"A rare exception ocurred!\nMore detail: {e}")
            sys.exit(1)

    @classmethod
    def _final_writing(cls) -> None:
        """Write the Python object into a JSON file"""
        try:
            with open(cls.file_path, "w", encoding="utf-8") as f:
                json.dump(cls.python_json_object, f, indent=4)

        except IOError as e:
            print(f"Something went wrong when writing and loading\nMore detail: {e}")
            sys.exit(1)

        except Exception as e:
            print(f"A rare exception ocurred!\nMore detail: {e}")
            sys.exit(1)

    def __init__(self) -> None:
        Expense._load_counter()

    @classmethod
    def add_expense_record(cls, description: str, amount: float) -> None:
        """Add new item expense record"""
        if cls.available_ids:
            input_id = cls.available_ids.pop(0)
        else:
            input_id = cls.id_counter
            cls.id_counter = cls.id_counter + 1

        input_description = description
        input_amount = amount
        date = datetime.now().strftime("%Y-%m-%d")

        cls.python_json_object["items"].update(
            {
                str(input_id): {
                    "description": input_description,
                    "amount": input_amount,
                    "date": date,
                }
            }
        )

        cls._final_writing()
        cls._write_counter()

        print(
            f"The {input_description} with {input_id} ID with amount of {input_amount} on {date} ADDED!"
        )

    @classmethod
    def delete_item(cls, id: int) -> None:
        """Delete a ID."""
        try:
            expense_item = cls.python_json_object["items"][id]
            del cls.python_json_object["items"][id]
        except IndexError as e:
            print(f"Incorrect ID!\nMore detail: {e}")
            sys.exit(1)

        cls.available_ids.append(id)
        cls.available_ids.sort()

        cls._final_writing()

        item_description = expense_item.get("description")
        item_amount = expense_item.get("amount")
        item_date = expense_item.get("date")

        print(
            f"The item {id} deleted.\nDescription: {item_description}\nAmount: {item_amount}\nDate: {item_date}"
        )

    @classmethod
    def list_items(cls) -> None:
        """List all the items"""
        expense_items = cls.python_json_object.get("items")
        for key, item in expense_items.items():
            description = item.get("description")
            amount = item.get("amount")
            date = item.get("date")

            print("ID:", key)
            print(description)
            print(amount)
            print(date, "\n")
            print("-------------------------------------")

    @classmethod
    def summary_items(cls, month=0) -> None:
        """Summary of the total expenses"""
        expense_items = cls.python_json_object.get("items")

        if month == 0:
            summary = 0
            for key, item in expense_items.items():
                summary = summary + item["amount"]
        else:
            summary = 0
            for key, item in expense_items.items():
                date = item["date"]
                extracted_month = re.findall(r"^\d+\-(\d+)\-\d+", date)[0]
                if int(extracted_month) == int(month):
                    summary = summary + item["amount"]

        print(f"{summary}t")

    @staticmethod
    def _update_date() -> str:
        """Update date"""
        return datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def update_description(cls, id, new_description) -> None:
        """Update the description of an item"""
        try:
            new_date = cls._update_date()

            cls.python_json_object["items"][id]["description"] = new_description
            cls.python_json_object["items"][id]["date"] = new_date

            cls._final_writing()

            print(f"The {id} ID updated to {new_description}.\nDate: {new_date}")

        except IndexError as e:
            print(f"Incorrect ID!\nMore details: {e}")
            sys.exit(1)

    @classmethod
    def update_amount(cls, id, new_amount) -> None:
        """Update the amount of an item"""
        try:
            new_date = cls._update_date()

            cls.python_json_object["items"][id]["amount"] = new_amount
            cls.python_json_object["items"][id]["date"] = new_date

            cls._final_writing()

            print(f"The {id} ID updated to {new_amount}.\nDate: {new_date}")

        except IndexError as e:
            print(f"Incorrect ID!\nMore details: {e}")
            sys.exit(1)


################## Helper methods ######################


def validate_amount(input_amount: str) -> int:
    """Validate the input amount"""
    try:
        input_amount = float(input_amount)
        if input_amount <= 0:
            raise ValueError("The input amount cannot be ZERO or NEGATIVE!")
        else:
            return input_amount
    except Exception as e:
        print(f"An error ocurred!\nMore detail: {e}")
        sys.exit(1)


def validate_string(input_string: str) -> str:
    """Validate input description"""
    try:
        if input_string.isspace():
            raise ValueError("The description cannot be empty space characters.")
        elif input_string == "":
            raise ValueError("The description cannot be empty.")
        else:
            return input_string
    except Exception as e:
        print(f"An error ocurred!\nMore detail: {e}")
        sys.exit(1)


def validate_month_input(input_month: str) -> int:
    """Validate the enterd input for the month. (Type and Value)"""
    try:
        input_month = int(input_month)
        if input_month <= 12 and input_month >= 1:
            return input_month
        else:
            raise ValueError("The input must be in the range between 1 and 12.")
    except Exception as e:
        print(f"An error ocurred!\nMore detail: {e}")
        sys.exit(1)


def arguments() -> argparse.Namespace:
    """Argparse arguments"""
    parser = argparse.ArgumentParser(
        description="Manage the expenses via the Expense Tracker"
    )
    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add", help="Add Expense")
    add_parser.add_argument(
        "--description",
        required=True,
        help="The description of the item.",
        metavar="<DESCRIPTION>",
        type=validate_string,
        nargs=1,
    )
    add_parser.add_argument(
        "--amount",
        required=True,
        help="Specify the amount of the expense",
        metavar="<AMOUNT>",
        type=validate_amount,
        nargs=1,
    )

    list_parser = subparser.add_parser("list", help="List all the expenses.")

    summary_parser = subparser.add_parser(
        "summary", help="Get a summary of all expenses or a specific date."
    )
    summary_parser.add_argument(
        "--month",
        required=False,
        help="Specify the number of the month.",
        metavar="<MONTH NUMBER>",
        type=validate_month_input,
        nargs=1,
    )

    delete_parser = subparser.add_parser("delete", help="Delete a specific item.")
    delete_parser.add_argument(
        "--id",
        required=True,
        help="Specifiy the item id that you want to get deleted.",
        metavar="<ID>",
        nargs=1,
    )

    update_parser = subparser.add_parser("update", help="Update a specific item.")
    update_parser.add_argument(
        "--id",
        required=True,
        help="Specify the item id that you want to get updated.",
        metavar="<ID>",
        nargs=1,
    )
    update_parser.add_argument(
        "--description",
        help="The new description for the item.",
        metavar="<DESCRIPTION>",
        nargs=1,
    )
    update_parser.add_argument(
        "--amount", help="The new amount for the item.", metavar="<AMOUNT>", nargs=1
    )

    return parser.parse_args()


############### Main Program #################


def main() -> None:
    args = arguments()
    expense_record = Expense()

    if args.command == "add":
        expense_record.add_expense_record(args.description[0], args.amount[0])
    elif args.command == "delete":
        expense_record.delete_item(args.id[0])
    elif args.command == "list":
        expense_record.list_items()
    elif args.command == "summary":
        if args.month:
            expense_record.summary_items(args.month[0])
        else:
            expense_record.summary_items()
    elif args.command == "update":
        if args.description and args.amount:
            expense_record.update_description(args.id[0], args.description[0])
            expense_record.update_amount(args.id[0], args.amount[0])
        elif args.amount:
            expense_record.update_amount(args.id[0], args.amount[0])
        elif args.description:
            expense_record.update_description(args.id[0], args.description[0])


if __name__ == "__main__":
    main()

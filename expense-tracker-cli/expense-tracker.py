#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import sys

from datetime import datetime


############## Expense Class #################


class Expense:
    file_path = Path("expenseDB.json")

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
        if Expense.available_ids:
            input_id = Expense.available_ids.pop(0)
        else:
            input_id = Expense.id_counter
            Expense.id_counter = Expense.id_counter + 1

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

        Expense._final_writing()
        Expense._write_counter()

    def delete(self, id: int) -> None:
        """Delete a ID."""
        Expense.available_ids.append(id)
        Expense.available_ids.sort()

    def update_date(self) -> None:
        """Update date"""
        self.date = datetime.now().strftime("%Y-%m-%d")


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
        print(expense_record)


if __name__ == "__main__":
    main()

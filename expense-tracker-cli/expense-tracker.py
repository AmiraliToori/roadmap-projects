#!/usr/bin/env python3

import argparse
import sys

from datetime import datetime


class Expense:
    __id_counter = 0
    _available_ids = []

    def __init__(self, description: str, amount: float) -> None:
        if Expense._available_ids:
            self.__id = Expense._available_ids.pop(0)
        else:
            self.__id = +Expense.__id_counter

        self._description = description
        self._amount = amount
        self._date = datetime.now().strftime("%Y-%m-%d")

    def return_specification_dict(self) -> dict:
        return {
            self.id: {
                "description": self.description,
                "amount": self.amount,
                "date": self.date,
            }
        }

    def delete(self, id: int) -> None:
        """Delete a ID."""
        Expense._available_ids.append(id)
        Expense._available_ids.sort()

    @property
    def id(self) -> int:
        """Getter: ID"""
        return self.__id

    @property
    def description(self) -> str:
        """Getter: description"""
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        """Setter: description"""
        self.description = new_description

    @property
    def amount(self) -> float:
        """Getter: amount"""
        return self._amount

    @amount.setter
    def amount(self, new_amount: float) -> None:
        """Setter: amount"""
        self.amount = new_amount

    @property
    def date(self) -> str:
        """Getter: date"""
        return self._date

    @date.setter
    def date(self) -> None:
        """Setter: update date"""
        self.date = datetime.now().strftime("%Y-%m-%d")


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
    subparser = parser.add_subparsers(title="command")

    add_parser = subparser.add_parser("add", help="Add Expense")
    add_parser.add_argument(
        "--description",
        help="The description of the item.",
        metavar="<DESCRIPTION>",
        type=validate_string,
        nargs=1,
    )
    add_parser.add_argument(
        "--amount",
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
        help="Specify the number of the month.",
        metavar="<MONTH NUMBER>",
        type=validate_month_input,
        nargs=1,
    )

    delete_parser = subparser.add_parser("delete", help="Delete a specific item.")
    delete_parser.add_argument(
        "--id",
        help="Specifiy the item id that you want to get deleted.",
        metavar="<ID>",
        nargs=1,
    )

    update_parser = subparser.add_parser("update", help="Update a specific item.")
    update_parser.add_argument(
        "--id",
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


def main() -> None:
    args = arguments()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import sys


def validate_amount(input_amount: str) -> int:
    """Validate the input amount"""
    try:
        input_amount = int(input_amount)
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

    return parser.parse_args()


def main() -> None:
    args = arguments()


if __name__ == "__main__":
    main()

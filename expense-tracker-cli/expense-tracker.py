#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import sys
import re
import os
import csv
from datetime import datetime

# ==============================================================================
#  THEME ENGINE (Catppuccin Mocha) & UTILS
# ==============================================================================


class Theme:
    """ANSI Escape Codes for Catppuccin Mocha Palette"""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    TEXT = "\033[38;2;205;214;244m"
    SUBTEXT = "\033[38;2;166;173;200m"
    OVERLAY = "\033[38;2;108;112;134m"
    MAUVE = "\033[38;2;203;166;247m"  # Accent
    BLUE = "\033[38;2;137;180;250m"  # Info
    GREEN = "\033[38;2;166;227;161m"  # Success
    RED = "\033[38;2;243;139;168m"  # Error
    YELLOW = "\033[38;2;249;226;175m"  # Warning
    PEACH = "\033[38;2;250;179;135m"

    # Glyphs (Nerd Font)
    ICON_SUCCESS = ""
    ICON_ERROR = ""
    ICON_WARN = ""
    ICON_INFO = ""
    ICON_MONEY = ""
    ICON_DATE = ""
    ICON_ID = ""
    ICON_EDIT = ""
    ICON_TRASH = ""
    ICON_LIST = ""


class UI:
    @staticmethod
    def print_success(msg: str):
        print(
            f"\n {Theme.GREEN}{Theme.ICON_SUCCESS}  SUCCESS:{Theme.TEXT} {msg}{Theme.RESET}"
        )

    @staticmethod
    def print_error(msg: str):
        print(
            f"\n {Theme.RED}{Theme.ICON_ERROR}  ERROR:{Theme.TEXT} {msg}{Theme.RESET}"
        )

    @staticmethod
    def print_info(msg: str):
        print(f"\n {Theme.BLUE}{Theme.ICON_INFO}  INFO:{Theme.TEXT} {msg}{Theme.RESET}")

    @staticmethod
    def header(title: str):
        print(f"\n {Theme.MAUVE}{Theme.BOLD}{title.upper()}{Theme.RESET}")
        print(f" {Theme.OVERLAY}{'─' * 40}{Theme.RESET}")

    @staticmethod
    def table_row(col1, col2, col3, col4, col5, header=False):
        """Formats a strict columnar table row"""
        c1_w, c2_w, c3_w, c4_w, c5_w = 6, 14, 30, 30, 12

        # Truncate description if too long
        if len(str(col3)) > c3_w - 2:
            col3 = str(col3)[: c3_w - 3] + "…"

        if header:
            color = Theme.MAUVE + Theme.BOLD
            reset = Theme.RESET
            sep = f"{Theme.OVERLAY}│{Theme.RESET}"
        else:
            color = Theme.TEXT
            reset = Theme.RESET
            sep = f"{Theme.OVERLAY}│{Theme.RESET}"

        # F-string padding
        print(
            f" {color}{str(col1):<{c1_w}}{reset} {sep} "
            f"{Theme.BLUE if not header else color}{str(col2):<{c2_w}}{reset} {sep} "
            f"{color}{str(col3):<{c3_w}}{reset} {sep} "
            f"{color}{str(col4):<{c4_w}}{reset} {sep} "
            f"{Theme.GREEN if not header else color}{str(col5):>{c5_w}}{reset}"
        )

    @staticmethod
    def format_currency(amount):
        return f"${float(amount):,.2f}"


############## Expense Class #################


class Expense:
    @staticmethod
    def _handle_path() -> Path:
        """Create and store the JSON in a specific path"""
        file_name = "expenseDB.json"
        home_path = os.getenv("HOME")
        config_path = ".config/expense-tracker/"

        config_directory = os.path.join(home_path, config_path)
        full_path = os.path.join(home_path, config_path, file_name)

        if not os.path.exists(config_directory):
            try:
                os.mkdir(config_directory)
            except OSError:
                pass  # Handle quietly or use print_error if strictly needed

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
            UI.print_error(f"IO Error during load: {e}")
            sys.exit(1)

        except json.JSONDecodeError as e:
            UI.print_error(f"Corrupt JSON file: {e}")
            sys.exit(1)

        except Exception as e:
            UI.print_error(f"Unexpected error: {e}")
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
            UI.print_error(f"Error loading counter: {e}")
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
            UI.print_error(f"Write error: {e}")
            sys.exit(1)

        except Exception as e:
            UI.print_error(f"Unexpected error: {e}")
            sys.exit(1)

    @classmethod
    def _final_writing(cls) -> None:
        """Write the Python object into a JSON file"""
        try:
            with open(cls.file_path, "w", encoding="utf-8") as f:
                json.dump(cls.python_json_object, f, indent=4)

        except IOError as e:
            UI.print_error(f"Write error: {e}")
            sys.exit(1)

        except Exception as e:
            UI.print_error(f"Unexpected error: {e}")
            sys.exit(1)

    def __init__(self) -> None:
        Expense._load_counter()

    @classmethod
    def add_expense_record(cls, description: str, amount: float, category: str) -> None:
        """Add new item expense record"""
        if cls.available_ids:
            input_id = cls.available_ids.pop(0)
        else:
            input_id = cls.id_counter
            cls.id_counter = cls.id_counter + 1

        input_description = description
        input_amount = amount
        date = datetime.now().strftime("%Y-%m-%d")
        input_category = category

        cls.python_json_object["items"].update(
            {
                str(input_id): {
                    "description": input_description,
                    "amount": input_amount,
                    "date": date,
                    "category": input_category,
                }
            }
        )

        cls._final_writing()
        cls._write_counter()

        UI.print_success(
            f"Expense added: {Theme.BOLD}{input_description}{Theme.RESET} "
            f"({Theme.GREEN}${input_amount}{Theme.RESET}) in {Theme.YELLOW}{input_category}{Theme.RESET} category."
        )

    @classmethod
    def delete_item(cls, id: int) -> None:
        """Delete a ID."""
        try:
            expense_item = cls.python_json_object["items"][id]
            del cls.python_json_object["items"][id]
        except (IndexError, KeyError):
            UI.print_error(f"ID {id} not found.")
            sys.exit(1)

        cls.available_ids.append(int(id))
        cls.available_ids.sort()

        cls._final_writing()
        cls._write_counter()  # Ensure counter/available_ids are saved too

        item_description = expense_item.get("description")

        UI.print_success(
            f"Deleted item {Theme.BOLD}#{id}{Theme.RESET} ({item_description})"
        )

    @classmethod
    def list_items(cls, specific_category: str = "all") -> None:
        """List all or a specific category of the item expenses."""
        expense_items = cls.python_json_object.get("items")

        if not expense_items:
            UI.print_info("No expenses found.")
            return

        print("")
        UI.table_row("ID", "DATE", "DESCRIPTION", "CATEGORY", "AMOUNT", header=True)
        print(
            f" {Theme.OVERLAY}────── ┼ ────────────── ┼ ────────────────────────────── ┼ ────────────────────────────── ┼ ────────────{Theme.RESET}"
        )

        # Sort by ID for cleaner look
        sorted_items = dict(
            sorted(expense_items.items(), key=lambda item: int(item[0]))
        )

        for key, item in sorted_items.items():
            description = item.get("description")
            amount = item.get("amount")
            date = item.get("date")
            category = item.get("category", "General")

            if category != specific_category and specific_category != "all":
                continue

            UI.table_row(
                f"#{key}", date, description, category, UI.format_currency(amount)
            )
        print("")

    @classmethod
    def summary_of_all_items(cls) -> None:
        """Get the summary of all items"""
        expense_items = cls.python_json_object.get("items")
        summary = 0

        for key, item in expense_items.items():
            summary = summary + item["amount"]
        UI.header("Total Expenses")

        print(
            f" {Theme.TEXT}Total:{Theme.RESET} {Theme.GREEN}{Theme.BOLD}{UI.format_currency(summary)}{Theme.RESET}\n"
        )

    @classmethod
    def summary_items_by_month(cls, month: int) -> None:
        """Summary of items by month"""
        expense_items = cls.python_json_object.get("items")
        summary = 0

        for key, item in expense_items.items():
            date = item["date"]
            extracted_month = re.findall(r"^\d+\-(\d+)\-\d+", date)[0]
            if int(extracted_month) == int(month):
                summary = summary + item["amount"]

            month_name = datetime(2000, int(month), 1).strftime("%B")
        UI.header(f"Expenses for {month_name}")

        print(
            f" {Theme.TEXT}Total:{Theme.RESET} {Theme.GREEN}{Theme.BOLD}{UI.format_currency(summary)}{Theme.RESET}\n"
        )

    @classmethod
    def summary_items_by_category(cls, input_category: str) -> None:
        """Summary of items by category"""
        expense_items = cls.python_json_object.get("items")
        summary = 0

        for key, item in expense_items.items():
            item_category = item.get("category", "General")
            if input_category == item_category:
                summary = summary + item["amount"]

        UI.header(f"Expenses for {input_category}")

        print(
            f" {Theme.TEXT}Total:{Theme.RESET} {Theme.GREEN}{Theme.BOLD}{UI.format_currency(summary)}{Theme.RESET}\n"
        )

    @staticmethod
    def _update_date() -> str:
        """Update date"""
        return datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def update_description(cls, id, new_description) -> None:
        """Update the description of an item"""
        try:
            if id not in cls.python_json_object["items"]:
                raise IndexError("ID not found")

            new_date = cls._update_date()

            cls.python_json_object["items"][id]["description"] = new_description
            cls.python_json_object["items"][id]["date"] = new_date

            cls._final_writing()

            UI.print_success(f"Item {Theme.BOLD}#{id}{Theme.RESET} updated.")
            print(f"   {Theme.OVERLAY}New Desc:{Theme.RESET} {new_description}")

        except IndexError:
            UI.print_error(f"ID {id} does not exist.")
            sys.exit(1)

    @classmethod
    def update_amount(cls, id, new_amount) -> None:
        """Update the amount of an item"""
        try:
            if id not in cls.python_json_object["items"]:
                raise IndexError("ID not found")

            new_date = cls._update_date()

            cls.python_json_object["items"][id]["amount"] = float(new_amount)
            cls.python_json_object["items"][id]["date"] = new_date

            cls._final_writing()

            UI.print_success(f"Item {Theme.BOLD}#{id}{Theme.RESET} updated.")
            print(
                f"   {Theme.OVERLAY}New Amount:{Theme.RESET} {Theme.GREEN}{UI.format_currency(new_amount)}{Theme.RESET}"
            )

        except IndexError:
            UI.print_error(f"ID {id} does not exist.")
            sys.exit(1)
        except ValueError:
            UI.print_error("Amount must be a number.")
            sys.exit(1)

    @classmethod
    def update_category(cls, id, new_category: str) -> None:
        """Update the category of an item"""
        try:
            if id not in cls.python_json_object["items"]:
                raise IndexError("ID not found")

            new_date = cls._update_date()

            cls.python_json_object["items"][id]["category"] = new_category
            cls.python_json_object["items"][id]["date"] = new_date

            cls._final_writing()

            UI.print_success(f"Item {Theme.BOLD}#{id}{Theme.RESET} updated.")
            print(
                f"   {Theme.OVERLAY}New Category:{Theme.RESET} {Theme.GREEN}{new_category}{Theme.RESET}"
            )

        except IndexError:
            UI.print_error(f"ID {id} does not exist.")
            sys.exit(1)
        except ValueError:
            UI.print_error("Category must be a valid string.")
            sys.exit(1)

    @classmethod
    def export_csv(cls) -> None:
        expense_items = cls.python_json_object.get("items")

        fieldnames = ["id", "description", "amount", "date", "category"]

        file_name = "expense_items.csv"

        try:
            with open(file_name, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()

                for user_id, info in expense_items.items():
                    row = {"id": user_id}
                    row.update(info)

                    writer.writerow(row)

            UI.print_success(f"Exported to {Theme.BOLD}{file_name}{Theme.RESET}")

        except IOError as e:
            UI.print_error(f"Could not write CSV: {e}")


################## Helper methods ######################


def validate_amount(input_amount: str) -> float:
    """Validate the input amount"""
    try:
        input_amount = float(input_amount)
        if input_amount <= 0:
            raise ValueError("The input amount cannot be ZERO or NEGATIVE!")
        else:
            return input_amount
    except ValueError:
        UI.print_error("Amount must be a positive number.")
        sys.exit(1)
    except Exception as e:
        UI.print_error(f"An error occurred: {e}")
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
        UI.print_error(f"Validation Error: {e}")
        sys.exit(1)


def validate_month_input(input_month: str) -> int:
    """Validate the entered input for the month. (Type and Value)"""
    try:
        input_month = int(input_month)
        if input_month <= 12 and input_month >= 1:
            return input_month
        else:
            raise ValueError("The input must be in the range between 1 and 12.")
    except Exception:
        UI.print_error("Month must be an integer between 1 and 12.")
        sys.exit(1)


def display_categories() -> None:
    """Display a list of categories"""
    list_of_categories = [
        "General",
        "Food",
        "Daily",
        "Cafe and Restaurant",
        "Beauty & Health",
        "Bills & Charging",
        "Clothes",
        "Travel & Transportation",
        "House",
        "Entertainment",
        "Savings",
        "Sports",
        "Gifting",
        "Other",
        "Money Transfer",
        "Loan Installments",
        "Culture & Art",
    ]

    print("List of the available category options:")
    for category in list_of_categories:
        print(f"\t{category}")


def arguments() -> argparse.Namespace:
    """Argparse arguments"""
    # Custom help formatter could be added here, but staying within constraints
    parser = argparse.ArgumentParser(description="Manage your expenses.")
    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add", help="Add Expense")
    add_parser.add_argument(
        "--description",
        required=True,
        help="The description of the item.",
        metavar="DESC",
        type=validate_string,
        nargs=1,
    )
    add_parser.add_argument(
        "--amount",
        required=True,
        help="Specify the amount of the expense",
        metavar="AMT",
        type=validate_amount,
        nargs=1,
    )
    add_parser.add_argument(
        "--category",
        required=False,
        help="Specify the category of the items.",
        metavar="CAT",
        choices=[
            "General",
            "Food",
            "Daily",
            "Cafe and Restaurant",
            "Beauty & Health",
            "Bills & Charging",
            "Clothes",
            "Travel & Transportation",
            "House",
            "Entertainment",
            "Savings",
            "Sports",
            "Gifting",
            "Other",
            "Money Transfer",
            "Loan Installments",
            "Culture & Art",
        ],
        nargs=1,
        default=["General"],
    )

    list_parser = subparser.add_parser("list", help="List all the expenses.")
    list_parser.add_argument(
        "--list-categories",
        help="List of the categories that are available.",
        action="store_true",
        required=False,
    )
    list_parser.add_argument(
        "--category",
        help="Filter the expenses by specific type of category.",
        nargs=1,
        required=False,
        metavar="CAT",
    )

    summary_parser = subparser.add_parser(
        "summary", help="Get a summary of all expenses or a specific date."
    )
    summary_parser.add_mutually_exclusive_group(required=False)
    summary_parser.add_argument(
        "--month",
        required=False,
        help="Specify the number of the month.",
        metavar="NUM",
        type=validate_month_input,
        nargs=1,
    )
    summary_parser.add_argument(
        "--category",
        required=False,
        help="Specify the category of item.",
        metavar="CAT",
        choices=[
            "General",
            "Food",
            "Daily",
            "Cafe and Restaurant",
            "Beauty & Health",
            "Bills & Charging",
            "Clothes",
            "Travel & Transportation",
            "House",
            "Entertainment",
            "Savings",
            "Sports",
            "Gifting",
            "Other",
            "Money Transfer",
            "Loan Installments",
            "Culture & Art",
        ],
        nargs=1,
    )

    delete_parser = subparser.add_parser("delete", help="Delete a specific item.")
    delete_parser.add_argument(
        "--id",
        required=True,
        help="Specify the item id that you want to get deleted.",
        metavar="ID",
        nargs=1,
    )

    update_parser = subparser.add_parser("update", help="Update a specific item.")
    update_parser.add_argument(
        "--id",
        required=True,
        help="Specify the item id that you want to get updated.",
        metavar="ID",
        nargs=1,
    )
    update_parser.add_argument(
        "--description",
        help="The new description for the item.",
        metavar="DESC",
        nargs=1,
    )
    update_parser.add_argument(
        "--amount", help="The new amount for the item.", metavar="AMT", nargs=1
    )
    update_parser.add_argument(
        "--category",
        required=False,
        help="Specify the category of the items.",
        metavar="CAT",
        choices=[
            "General",
            "Food",
            "Daily",
            "Cafe and Restaurant",
            "Beauty & Health",
            "Bills & Charging",
            "Clothes",
            "Travel & Transportation",
            "House",
            "Entertainment",
            "Savings",
            "Sports",
            "Gifting",
            "Other",
            "Money Transfer",
            "Loan Installments",
            "Culture & Art",
        ],
        nargs=1,
    )

    export_parser = subparser.add_parser(
        "export", help="Export the expenses as a CSV file."
    )

    return parser.parse_args()


############### Main Program #################


def main() -> None:
    try:
        args = arguments()

        # If no arguments provided, show help
        if not args.command:
            print(f"\n {Theme.MAUVE}{Theme.BOLD}EXPENSE TRACKER CLI{Theme.RESET}")
            print(
                f" {Theme.OVERLAY}Use 'python3 expense-tracker.py --help' for usage.{Theme.RESET}\n"
            )
            sys.exit(0)

        expense_record = Expense()

        if args.command == "add":
            expense_record.add_expense_record(
                args.description[0], args.amount[0], args.category[0]
            )

        elif args.command == "delete":
            expense_record.delete_item(args.id[0])

        elif args.command == "list":
            if args.list_categories:
                display_categories()
            else:
                if args.category:
                    expense_record.list_items(args.category[0])
                else:
                    expense_record.list_items()

        elif args.command == "summary":
            if args.month:
                expense_record.summary_items_by_month(args.month[0])
            elif args.category:
                expense_record.summary_items_by_category(args.category[0])
            else:
                expense_record.summary_of_all_items()

        elif args.command == "update":
            if args.description and args.amount and args.category:
                expense_record.update_description(args.id[0], args.description[0])
                expense_record.update_amount(args.id[0], args.amount[0])
                expense_record.update_category(args.id[0], args.category[0])

            elif args.description and args.amount:
                expense_record.update_description(args.id[0], args.description[0])
                expense_record.update_amount(args.id[0], args.amount[0])

            elif args.amount:
                expense_record.update_amount(args.id[0], args.amount[0])

            elif args.description:
                expense_record.update_description(args.id[0], args.description[0])

            elif args.category:
                expense_record.update_category(args.id[0], args.category[0])

        elif args.command == "export":
            expense_record.export_csv()

    except KeyboardInterrupt:
        print(f"\n{Theme.RED}Operation cancelled.{Theme.RESET}")
        sys.exit(0)
    except Exception as e:
        UI.print_error(f"Critical failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

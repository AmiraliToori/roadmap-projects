#!/usr/bin/env python3

import argparse
import sys
import os
from time import sleep


def clear_terminal() -> None:
    """Helper method to clear the terminal environment"""
    os.system("cls" if os.name == "nt" else "clear")


class Timer:
    @staticmethod
    def rest(rest_time: int) -> None:
        """Rest between the sets."""
        clear_terminal()
        print("Resting...")
        sleep(rest_time)
        clear_terminal()

    def count_the_timer(
        self, time: int, rep: int = 1, rest_time: int | None = None
    ) -> None:
        """Count and start the timer."""
        self.time = time
        self.rep = rep
        self.rest_time = rest_time

        print("Starting the timer...")
        sleep(1)

        clear_terminal()

        for rep_count in range(1, self.rep + 1):
            for count in range(1, self.time + 1):
                print(rep_count, count)
                sleep(1)
                clear_terminal()

            if rep_count != self.rep and isinstance(self.rest_time, int):
                self.rest(self.rest_time)

        print("Timer Ended.")
        sleep(1)

        clear_terminal()

        sys.exit(0)


def validate_time_input(input_number: str) -> int:
    """Validate the input value of the --rep and --time argument"""
    try:
        number = int(input_number)
        if number <= 0:
            raise ValueError("The input value cannot be 0 or NEGATIVE!")
        else:
            return number
    except TypeError:
        raise TypeError("The input value must be a integer number!")
    except Exception:
        raise Exception("A rare exception occurred.")


def arguments() -> argparse.Namespace:
    """Arguments function for the argparse module."""
    parser = argparse.ArgumentParser(description="A simple and plain Python CLI Timer.")

    subparser = parser.add_subparsers(dest="command", help="Available commands")

    count_parser = subparser.add_parser(
        "count", help="Count a specific amount of time."
    )

    count_parser.add_argument(
        "--time",
        help="The amount of seconds that you want to count.",
        type=validate_time_input,
        metavar="<TIME>",
        required=True,
        nargs=1,
    )

    count_parser.add_argument(
        "--rep",
        help="The number of sets you want to do it.",
        type=validate_time_input,
        metavar="<REP>",
        required=False,
        nargs=1,
    )

    count_parser.add_argument(
        "--rest",
        help="Rest time between each set.",
        type=validate_time_input,
        metavar="<REST>",
        required=False,
        nargs=1,
    )

    return parser.parse_args()


def main() -> None:
    args = arguments()

    timer = Timer()

    try:
        if args.command == "count":
            if args.time and args.rep and args.rest:
                timer.count_the_timer(args.time[0], args.rep[0], args.rest[0])
            elif args.time and args.rep:
                timer.count_the_timer(args.time[0], args.rep[0])
            else:
                timer.count_the_timer(args.time[0])
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import sys
import os
from time import sleep


def clear_terminal() -> None:
    """Helper method to clear the terminal environment"""
    os.system("cls" if os.name == "nt" else "clear")


class Timer:
    def __init__(
        self,
        second: int = 0,
        minute: int = 0,
        hour: int = 0,
        rep: int = 1,
        rest_time: int | None = None,
    ) -> None:
        self.second = second
        self.minute = minute
        self.hour = hour
        self.rep = rep
        self.rest_time = rest_time

    @staticmethod
    def stopwatch() -> None:
        """Stopwatch mode"""
        second = 0
        minute = 0

        while True:
            print(minute, second)

            sleep(1)

            second = second + 1
            if second == 60:
                minute = minute + 1
                second = 0

            clear_terminal()

    @staticmethod
    def _rest(rest_time: int) -> None:
        """Rest between the sets."""
        clear_terminal()
        print("Resting...")
        sleep(rest_time)
        clear_terminal()

    def countdown(self) -> None:
        """Count and start the timer."""
        second = self.second
        minute = self.minute
        hour = self.hour
        rep = self.rep
        rest_time = self.rest_time

        print("Starting the timer...")
        sleep(1)

        clear_terminal()

        for rep_count in range(1, rep + 1):
            while (hour > 0) or (minute > 0) or (second > 0):
                print(f"Set: {rep_count}", hour, minute, second)

                sleep(1)

                if second >= 1:
                    second = second - 1
                elif second == 0 and minute >= 1:
                    minute = minute - 1
                    second = 59
                elif (second == 0 and minute == 0) and hour >= 1:
                    hour = hour - 1
                    minute = 59
                    second = 59
                clear_terminal()

            second = self.second
            minute = self.minute
            hour = self.hour

            if rep_count != rep and isinstance(rest_time, int):
                self._rest(rest_time)

        print("Timer Ended.")
        sleep(1)

        clear_terminal()

        sys.exit(0)


def validate_second_input(input_number: str) -> int:
    """Validate the input value of seconds"""
    try:
        number = int(input_number)
        if number < 0 or number > 60:
            raise ValueError("The seconds input must be between 0 and 60")
        else:
            return number
    except TypeError:
        raise TypeError("The input value must be a integer number!")
    except Exception:
        raise Exception("A rare exception occurred.")


def validate_minute_input(input_number: str) -> int:
    """Validate the input value of minutes"""
    try:
        number = int(input_number)
        if number < 0 or number > 60:
            raise ValueError("The minutes input must be between 0 and 60")
        else:
            return number
    except TypeError:
        raise TypeError("The input value must be a integer number!")
    except Exception:
        raise Exception("A rare exception occurred.")


def validate_hour_input(input_number: str) -> int:
    """Validate the input value of hours"""
    try:
        number = int(input_number)
        if number < 0 or number >= 24:
            raise ValueError("The hour input must be between 0 and 24")
        else:
            return number
    except TypeError:
        raise TypeError("The input value must be a integer number!")
    except Exception:
        raise Exception("A rare exception occurred.")


def validate_rep_input(input_number: str) -> int:
    """Validate the input value of reps"""
    try:
        number = int(input_number)
        if number <= 0:
            raise ValueError("The set value cannot be between 0 or NEGATIVE!")
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

    countdown_parser = subparser.add_parser("countdown", help="Countdown Mode")

    countdown_parser.add_argument(
        "--second",
        help="The amount of seconds that you want to count.",
        type=validate_second_input,
        metavar="<SEC>",
        nargs=1,
        default=[0],
    )

    countdown_parser.add_argument(
        "--minute",
        help="The amount of minutes that you want to count.",
        type=validate_minute_input,
        metavar="<MIN>",
        nargs=1,
        default=[0],
    )

    countdown_parser.add_argument(
        "--hour",
        help="The amount of hours that you want to count.",
        type=validate_hour_input,
        metavar="<HR>",
        nargs=1,
        default=[0],
    )

    countdown_parser.add_argument(
        "--rep",
        help="The number of sets you want to do it.",
        type=validate_rep_input,
        metavar="<REP>",
        required=False,
        nargs=1,
        default=[1],
    )

    countdown_parser.add_argument(
        "--rest",
        help="Rest time between each set.",
        type=validate_second_input,
        metavar="<REST>",
        required=False,
        nargs=1,
        default=[0],
    )

    stopwatch_parser = subparser.add_parser("stopwatch", description="Stopwatch Mode")

    return parser.parse_args()


def main() -> None:
    args = arguments()

    timer = Timer()

    try:
        if args.command == "countdown":
            timer = Timer(
                args.second[0], args.minute[0], args.hour[0], args.rep[0], args.rest[0]
            )
            if args.second or args.minute or args.second:
                timer.countdown()
        elif args.command == "stopwatch":
            timer.stopwatch()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


if __name__ == "__main__":
    main()

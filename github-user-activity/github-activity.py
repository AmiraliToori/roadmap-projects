#!/usr/bin/env python3

import requests
import sys
import re


class COLOR:
    """
    ANSI TrueColor helper for Catppuccin Mocha theme.
    Format: \033[38;2;R;G;Bm for Foreground
    Format: \033[48;2;R;G;Bm for Background
    """

    # --- Styles ---
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    STRIKETHROUGH = "\033[9m"

    ROSEWATER = "\033[38;2;245;224;220m"  # #f5e0dc
    FLAMINGO = "\033[38;2;242;205;205m"  # #f2cdcd
    PINK = "\033[38;2;245;194;231m"  # #f5c2e7
    MAUVE = "\033[38;2;203;166;247m"  # #cba6f7
    RED = "\033[38;2;237;135;150m"  # #f38ba8
    MAROON = "\033[38;2;238;153;160m"  # #eba0ac
    PEACH = "\033[38;2;245;169;127m"  # #fab387
    YELLOW = "\033[38;2;238;212;159m"  # #f9e2af
    GREEN = "\033[38;2;166;227;161m"  # #a6e3a1
    TEAL = "\033[38;2;148;226;213m"  # #94e2d5
    SKY = "\033[38;2;137;220;235m"  # #89dceb
    SAPPHIRE = "\033[38;2;122;162;247m"  # #74c7ec
    BLUE = "\033[38;2;137;180;250m"  # #89b4fa
    LAVENDER = "\033[38;2;180;190;254m"  # #b4befe
    TEXT = "\033[38;2;205;214;244m"  # #cdd6f4
    SUBTEXT1 = "\033[38;2;186;194;222m"  # #bac2de
    SUBTEXT0 = "\033[38;2;166;173;200m"  # #a6adc8

    # --- Backgrounds ---
    BG_SURFACE0 = "\033[48;2;49;50;68m"  # #313244
    BG_BASE = "\033[48;2;30;30;46m"  # #1e1e2e
    BG_MANTLE = "\033[48;2;24;24;37m"  # #181825


def validate_user_name() -> str:
    if len(sys.argv) > 2 or len(sys.argv) == 0:
        print(f"Usage {sys.argv[0]} <username>")
        sys.exit(1)

    user_name = str(sys.argv[1])

    if re.search(
        r" |!|\"|#|\$|%|&|\'|\(|\)|\*|\+|,|\.|/|:|;|<|=|>|\?|@|\[|\]|\^|_|`|\{|\||\}|~|[A-Z]",
        user_name,
    ):
        print("The username can only contain 'lowerspace','0-9','-' characters.")
        sys.exit(1)
    elif len(user_name) == 0:
        print("Minimum characters for user is 1. You entered empty.")
        sys.exit(1)
    elif len(user_name) >= 40:
        print(
            "Maximum characters of a username GitHub account is 39. You entered more than that!"
        )
        sys.exit(1)
    else:
        return user_name


def verify_user_name(user_name: str):
    try:
        response = requests.get(f"https://api.github.com/users/{user_name}")
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            print("404: User Not found")
            sys.exit(1)
        elif response.status_code == 403:
            print("403: Forbidden")
            sys.exit(1)
        elif response.status_code == 304:
            print("304: Not Modified")
            sys.exit(1)
        elif response.status_code == 503:
            print("503: Service Not Available")
            sys.exit(1)

    except requests.exceptions.Timeout as e:
        print(
            f"Connection Timeout. There is some problem in conncetion.\n\nMore detail:\n{e}"
        )
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occured.\n\nMore detail:\n{e}")
        sys.exit(1)
    except requests.exceptions.InvalidURL as e:
        print(f"URL is invalid!\n\nMore detail:\n{e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"There is a rare exception occured.\n\nMore detail:\n{e}")
        sys.exit(1)


def reformat_date(date_time: str) -> str:
    date_time_list = re.findall(r"(\d+-0*\d+-0*\d+)T(0*\d+:0*\d+:0*\d+)Z", date_time)

    for date_format, time_format in date_time_list:
        return date_format + " " + time_format


def handling_json(events) -> None:
    print(f"{COLOR.BOLD}{COLOR.MAUVE}Output:{COLOR.RESET}")
    for event in events:
        repository = event["repo"]["name"]
        created_at = reformat_date(event["created_at"])

        # print(json.dumps(event, indent=4))
        if event["type"] == "PushEvent":
            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {COLOR.BOLD}{COLOR.GREEN}Pushed{COLOR.RESET} into {COLOR.BOLD}{COLOR.PEACH}{repository}{COLOR.RESET} on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )

        elif event["type"] == "WatchEvent":
            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {COLOR.BOLD}{COLOR.YELLOW}Starred{COLOR.RESET} the {COLOR.BOLD}{COLOR.PEACH}{repository}{COLOR.RESET} on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )

        elif event["type"] == "DeleteEvent":
            item = event["payload"]["ref"]
            item_type = event["payload"]["ref_type"]

            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {COLOR.BOLD}{COLOR.RED}Deleted{COLOR.RESET} the {COLOR.UNDERLINE}{COLOR.MAROON}{item} {item_type}{COLOR.RESET} from {COLOR.BOLD}{COLOR.PEACH}{repository}{COLOR.RESET} on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )

        elif event["type"] == "PullRequestEvent":
            action = event["payload"]["action"]
            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {COLOR.BOLD}{COLOR.GREEN}{action.capitalize()}{COLOR.RESET} the {COLOR.BOLD}{COLOR.TEAL}pull request{COLOR.RESET} for {COLOR.BOLD}{COLOR.PEACH}{repository}{COLOR.RESET} on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )
        elif event["type"] == "CreateEvent":
            item = event["payload"]["ref"]
            item_type = event["payload"]["ref_type"]

            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {COLOR.BOLD}{COLOR.GREEN}Created{COLOR.RESET} {COLOR.UNDERLINE}{COLOR.MAROON}{item} {item_type}{COLOR.RESET}  on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )
        elif event["type"] == "IssueCommentEvent":
            action = event["payload"]["action"]
            issue_title = event["payload"]["issue"]["title"]

            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {action.capitalize()} comment in {COLOR.UNDERLINE}{COLOR.PINK}{issue_title}{COLOR.RESET} at {COLOR.BOLD}{COLOR.PEACH}{repository}{COLOR.RESET} on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )
        elif event["type"] == "IssuesEvent":
            action = event["payload"]["action"]
            issue_title = event["payload"]["issue"]["title"]

            print(
                f"{COLOR.BOLD}{COLOR.RED}-{COLOR.RESET} {action.capitalize()} {COLOR.BOLD}{COLOR.RED}issue{COLOR.RESET} {issue_title} at {COLOR.BOLD}{COLOR.PEACH}{repository}{COLOR.RESET} on {COLOR.BOLD}{COLOR.BLUE}{created_at}{COLOR.RESET}."
            )


def get_events_url(events_url: str) -> None:
    params = {"per_page": 10, "page": 1, "sort": "updated"}

    try:
        response = requests.get(events_url, params=params)
        if response.status_code == 200 and response.json():
            events = response.json()
            handling_json(events)
    except requests.exceptions.Timeout as e:
        print(
            f"Connection Timeout. There is some problem in conncetion.\n\nMore detail:\n{e}"
        )
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occured.\n\nMore detail:\n{e}")
        sys.exit(1)
    except requests.exceptions.InvalidURL as e:
        print(f"URL is invalid!\n\nMore detail:\n{e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"There is a rare exception occured.\n\nMore detail:\n{e}")
        sys.exit(1)


def get_profile_url(profile_url: str):
    profile = requests.get(profile_url)
    profile_json = profile.json()

    user_name = profile_json["login"]
    name = profile_json["name"]
    location = profile_json["location"]

    print(f"\n{COLOR.BOLD}{COLOR.MAUVE} USER NAME: {user_name}{COLOR.RESET}")
    print(f"{COLOR.BOLD}{COLOR.MAUVE} Name: {name}{COLOR.RESET}")
    print(f"{COLOR.BOLD}{COLOR.MAUVE} Location: {location}{COLOR.RESET}\n")


def main() -> None:
    user_name = validate_user_name()
    verify_user_name(user_name)
    events_url = f"https://api.github.com/users/{user_name}/events"
    profile_url = f"https://api.github.com/users/{user_name}"
    get_profile_url(profile_url)

    get_events_url(events_url)


if __name__ == "__main__":
    main()

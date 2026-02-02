#!/usr/bin/env python3

import requests
import sys
import re

# --- Aesthetics Configuration ---


class Colors:
    """Catppuccin Mocha Palette (TrueColor)"""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Core Palette
    ROSEWATER = "\033[38;2;245;224;220m"
    FLAMINGO = "\033[38;2;242;205;205m"
    PINK = "\033[38;2;245;194;231m"
    MAUVE = "\033[38;2;203;166;247m"
    RED = "\033[38;2;237;135;150m"
    MAROON = "\033[38;2;238;153;160m"
    PEACH = "\033[38;2;245;169;127m"
    YELLOW = "\033[38;2;238;212;159m"
    GREEN = "\033[38;2;166;227;161m"
    TEAL = "\033[38;2;148;226;213m"
    SKY = "\033[38;2;137;220;235m"
    SAPPHIRE = "\033[38;2;122;162;247m"
    BLUE = "\033[38;2;137;180;250m"
    LAVENDER = "\033[38;2;180;190;254m"
    TEXT = "\033[38;2;205;214;244m"
    SUBTEXT1 = "\033[38;2;186;194;222m"
    OVERLAY0 = "\033[38;2;108;112;134m"

    # Backgrounds
    BG_SURFACE0 = "\033[48;2;49;50;68m"


class Icons:
    """Nerd Font Glyphs"""

    GITHUB = ""
    USER = ""
    LOCATION = ""
    ERROR = ""
    WARN = ""
    INFO = ""

    # Events
    PUSH = ""
    STAR = ""
    TRASH = ""
    PR = ""
    CREATE = ""
    COMMENT = ""
    ISSUE = ""
    CLOCK = ""
    REPO = ""
    TAG = ""


C = Colors
I = Icons


def validate_user_name() -> str:
    if len(sys.argv) > 2 or len(sys.argv) == 0:
        print(f"{C.RED}{I.ERROR} Usage:{C.RESET} {sys.argv[0]} <username>")
        sys.exit(1)

    user_name = str(sys.argv[1])

    if re.search(
        r" |!|\"|#|\$|%|&|\'|\(|\)|\*|\+|,|\.|/|:|;|<|=|>|\?|@|\[|\]|\^|_|`|\{|\||\}|~|[A-Z]",
        user_name,
    ):
        print(
            f"{C.RED}{I.ERROR} Invalid Input:{C.RESET} The username can only contain 'lowerspace','0-9','-' characters."
        )
        sys.exit(1)
    elif len(user_name) == 0:
        print(
            f"{C.RED}{I.ERROR} Input Error:{C.RESET} Minimum characters for user is 1. You entered empty."
        )
        sys.exit(1)
    elif len(user_name) >= 40:
        print(
            f"{C.RED}{I.ERROR} Input Error:{C.RESET} Maximum characters of a username GitHub account is 39. You entered more than that!"
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
            print(f"{C.RED}{I.ERROR} 404:{C.RESET} User Not found")
            sys.exit(1)
        elif response.status_code == 403:
            print(f"{C.YELLOW}{I.WARN} 403:{C.RESET} Forbidden")
            sys.exit(1)
        elif response.status_code == 304:
            print(f"{C.BLUE}{I.INFO} 304:{C.RESET} Not Modified")
            sys.exit(1)
        elif response.status_code == 503:
            print(f"{C.RED}{I.ERROR} 503:{C.RESET} Service Not Available")
            sys.exit(1)

    except requests.exceptions.Timeout as e:
        print(
            f"{C.RED}{I.ERROR} Connection Timeout:{C.RESET} There is some problem in connection.\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(
            f"{C.RED}{I.ERROR} HTTP Error:{C.RESET} An HTTP error occurred.\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)
    except requests.exceptions.InvalidURL as e:
        print(
            f"{C.RED}{I.ERROR} Invalid URL:{C.RESET} URL is invalid!\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(
            f"{C.RED}{I.ERROR} Exception:{C.RESET} A rare exception occurred.\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)


def reformat_date(date_time: str) -> str:
    date_time_list = re.findall(r"(\d+-0*\d+-0*\d+)T(0*\d+:0*\d+:0*\d+)Z", date_time)

    for date_format, time_format in date_time_list:
        return date_format + " " + time_format


def handling_json(events) -> None:
    print(f"\n{C.BOLD}{C.MAUVE}{I.GITHUB}  Recent Activity Log:{C.RESET}")
    print(f"{C.DIM}──────────────────────────────────────────────────{C.RESET}")

    for event in events:
        repository = event["repo"]["name"]
        created_at = reformat_date(event["created_at"])

        # Base format for time
        time_str = f"{C.DIM}{I.CLOCK} {created_at}{C.RESET}"
        repo_str = f"{C.BOLD}{C.BLUE}{repository}{C.RESET}"

        if event["type"] == "PushEvent":
            print(
                f" {C.GREEN}{I.PUSH}  Pushed{C.RESET} commits to {repo_str}   {time_str}"
            )

        elif event["type"] == "WatchEvent":
            print(
                f" {C.YELLOW}{I.STAR}  Starred{C.RESET} the repo {repo_str}   {time_str}"
            )

        elif event["type"] == "DeleteEvent":
            item = event["payload"]["ref"]
            item_type = event["payload"]["ref_type"]
            print(
                f" {C.RED}{I.TRASH}  Deleted{C.RESET} {item_type} {C.MAROON}{C.UNDERLINE}{item}{C.RESET} from {repo_str}   {time_str}"
            )

        elif event["type"] == "PullRequestEvent":
            action = event["payload"]["action"]
            print(
                f" {C.TEAL}{I.PR}  {action.capitalize()}{C.RESET} pull request in {repo_str}   {time_str}"
            )

        elif event["type"] == "CreateEvent":
            item = event["payload"]["ref"]
            item_type = event["payload"]["ref_type"]
            # If item is None (repository creation), handle gracefully
            ref_display = (
                f"{C.MAROON}{C.UNDERLINE}{item}{C.RESET}" if item else "repository"
            )

            print(
                f" {C.GREEN}{I.CREATE}  Created{C.RESET} {item_type} {ref_display}   {time_str}"
            )

        elif event["type"] == "IssueCommentEvent":
            action = event["payload"]["action"]
            issue_title = event["payload"]["issue"]["title"]
            print(
                f" {C.PINK}{I.COMMENT}  {action.capitalize()}{C.RESET} comment on {C.ITALIC}'{issue_title}'{C.RESET} in {repo_str}   {time_str}"
            )

        elif event["type"] == "IssuesEvent":
            action = event["payload"]["action"]
            issue_title = event["payload"]["issue"]["title"]
            print(
                f" {C.PEACH}{I.ISSUE}  {action.capitalize()}{C.RESET} issue {C.ITALIC}'{issue_title}'{C.RESET} in {repo_str}   {time_str}"
            )

    print(f"{C.DIM}──────────────────────────────────────────────────{C.RESET}\n")


def get_events_url(events_url: str) -> None:
    params = {"per_page": 10, "page": 1, "sort": "updated"}

    try:
        response = requests.get(events_url, params=params)
        if response.status_code == 200 and response.json():
            events = response.json()
            handling_json(events)
    except requests.exceptions.Timeout as e:
        print(
            f"{C.RED}{I.ERROR} Connection Timeout:{C.RESET} There is some problem in connection.\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(
            f"{C.RED}{I.ERROR} HTTP Error:{C.RESET} An HTTP error occurred.\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)
    except requests.exceptions.InvalidURL as e:
        print(
            f"{C.RED}{I.ERROR} Invalid URL:{C.RESET} URL is invalid!\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(
            f"{C.RED}{I.ERROR} Exception:{C.RESET} A rare exception occurred.\n\n{C.DIM}More detail:\n{e}{C.RESET}"
        )
        sys.exit(1)


def get_profile_url(profile_url: str):
    try:
        profile = requests.get(profile_url)
        profile.raise_for_status()
        profile_json = profile.json()

        # Safely get values, handling None/Null from API
        user_name = str(profile_json.get("login", "N/A"))
        name = str(profile_json.get("name") or "N/A")  # 'or' handles None
        location = str(profile_json.get("location") or "N/A")

        print(f"{C.BOLD}{C.MAUVE}{I.GITHUB}  User Profile {C.RESET}")

        print(I.USER, "Username", user_name)
        print("", "Name", name)
        print(I.LOCATION, "Location", location)
    except Exception:
        print(f"{C.RED}{I.ERROR} Could not fetch profile data.{C.RESET}")


def main() -> None:
    user_name = validate_user_name()
    verify_user_name(user_name)
    events_url = f"https://api.github.com/users/{user_name}/events"
    profile_url = f"https://api.github.com/users/{user_name}"
    get_profile_url(profile_url)

    get_events_url(events_url)


if __name__ == "__main__":
    main()

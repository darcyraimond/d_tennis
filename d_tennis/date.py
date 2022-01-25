# Functionality for player static information to be stored and retrieved
# (this is information about a player at the time of the match)


# Import any required packages
from termcolor import colored
from datetime import datetime


# ==================================================
# Content below this point
# ==================================================


def str_to_date(dt):

    if type(dt) is not str:
        print(colored("Fatal Error:", "red"),
                f"value {dt} of type {type(dt)} couldn't be converted to date")
        exit(1)

    if dt == "":
        return None

    if dt[0] == "t":
        return None

    if len(dt) == 6:
        dt += "15"

    if len(dt) == 8:
        # Pre-process for missing parts of dates
        if dt[4:8] == "0000":
            dt = dt[0:4] + "0701"
        elif dt[6:8] == "00":
            dt = dt[0:6] + "15"
        return datetime.strptime(dt, "%Y%m%d").date()


    print(colored("Fatal Error:", "red"),
            f"string \"{dt}\" couldn't be converted to date")
    exit(1)
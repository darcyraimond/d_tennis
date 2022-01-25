# Functionality for player static information to be stored and retrieved
# (this is information about a player at the time of the match)


# Import any required packages
from termcolor import colored


# ==================================================
# Content below this point
# ==================================================

def _assign_seed(seed):
    if seed.isnumeric():
        return int(seed)
    elif seed == "":
        return None
    else:
        print(colored("Fatal Error:", "red"),
                f"can't convert seed {seed} of type {type(seed)}")
        exit(1)


def _assign_entry(entry):
    match entry:
        case "WC": return "Wild card"
        case "Q": return "Qualifier"
        case "LL": return "Lucky loser"
        case "PR": return "Protected ranking"
        case "ITF": return "ITF entry"
        case "S": return "Special exempt"
        case "SE": return "Special exempt"
        case "ALT": return "Alternative"
        case "Alt": return None
        case "": return None
        case _:
            print(colored("Fatal Error:", "red"),
                f"can't convert entry {entry} of type {type(entry)}")
            exit(1)


def _assign_rank(rank):
    if rank.isnumeric():
        return int(rank)
    elif rank == "":
        return None
    else:
        print(colored("Fatal Error:", "red"),
                f"can't convert rank {rank} of type {type(rank)}")
        exit(1)


def _assign_rank_points(rank_points):
    if rank_points.isnumeric():
        return int(rank_points)
    elif rank_points == "":
        return None
    else:
        print(colored("Fatal Error:", "red"),
                f"can't convert points {rank_points} of type {type(rank_points)}")
        exit(1)


class PlayerStatic:

    def __init__(self, d, winner):
        """
        PlayerStatic:
            - winner_seed, loser_seed
            - winner_entry, loser_entry
            - winner_rank, loser_rank
            - winner_rank_points, loser_rank_points
        """
        if winner:
            self.seed = _assign_seed(d["winner_seed"])
            self.entry = _assign_entry(d["winner_entry"])
            self.rank = _assign_rank(d["winner_rank"])
            self.rank_points = _assign_rank_points(d["winner_rank_points"])
        else:
            self.seed = _assign_seed(d["loser_seed"])
            self.entry = _assign_entry(d["loser_entry"])
            self.rank = _assign_rank(d["loser_rank"])
            self.rank_points = _assign_rank_points(d["loser_rank_points"])

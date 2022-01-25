# Functionality for loading data from a file path

# Import any required packages
import os
from termcolor import colored

from .csv_utils import csv_to_dicts
from .player import Player, player_array
from .match import Match, MatchArray, match_array
from .tournament import TournamentArray, tournament_array


# ==================================================
# Content below this point
# ==================================================


def load(path, silent=False):

    global match_array, player_array

    if not silent:
        print(colored("Loading from specified path.", "blue"), 
                colored("This may take several seconds.", "blue"))

    # Read files in folder and extract relevant titles to array
    files = os.listdir(path)
    contains_players = False
    match_files = []
    for file in files:
        if len(file) == 20 and file[:11] == "atp_matches":
            match_files.append(file)
        elif file == "atp_players.csv":
            contains_players = True

    # Error checking
    if not contains_players:
        print(colored("Fatal error:", "red"),
                f'path {path} does not contain file "atp_players.csv"' )
        exit(1)
    if len(match_files) == 0:
        print(colored("Fatal error:", "red"),
                f'path {path} does not contain any "atp_players.csv" files')
        exit(1)

    if not silent:
        print(colored("Loading players...", "blue"), end = "\r")

    # Add players
    ds = csv_to_dicts(f"{path}/atp_players.csv")
    for d in ds:
        new_player = Player(d)
        player_array.append(new_player)
    if not silent:
        print(colored("Loaded players successfully.", "blue"))

    # Make changes to players
    for player in player_array:
        player.matches = MatchArray()
        player.tournaments = TournamentArray()

    # Add matches
    for file in sorted(match_files):
        if not silent:
            print(colored(f"Loading matches from {file[12:16]}...",
                    "blue"), end = "\r")
        ds = csv_to_dicts(f"{path}/{file}")
        for d in ds:
            new_match = Match(d, player_array, tournament_array)
            match_array.append(new_match)
    if not silent:
        print(colored("Loaded matches successfully.      ", "blue"))
    
    if not silent:
        print(colored("Applying post-processing...", "blue"), end = "\r")

    tournament_array.post_process()
    match_array.post_process()
    player_array.post_process()
    if not silent:
        print(colored("Post-processing complete.  ", "blue"))

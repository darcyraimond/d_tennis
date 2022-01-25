# Functionality for round to be stored and retrieved


# Import any required packages
from termcolor import colored
from .player import Player, PlayerArray
from .match import Match, MatchArray


# ==================================================
# Content below this point
# ==================================================


def _assign_round(rd):
    if rd == "R128": return "Round of 128"
    if rd == "R64": return "Round of 64"
    if rd == "R32": return "Round of 32"
    if rd == "R16": return "Round of 16"
    if rd == "QF": return "Quarter Finals"
    if rd == "SF": return "Semi Finals"
    if rd == "F": return "Final"
    if rd == "RR": return "Round Robin"
    if rd == "BR": return "Bronze Medal Match"
    if rd == "ER": return "Elimination Round"

    print(colored("Fatal error:", "red"), f'"{rd}" is not a valid round')
    exit(1)


def _round_enum(rd):
    if rd == "R128": return 1/128
    if rd == "R64": return 1/64
    if rd == "R32": return 1/32
    if rd == "R16": return 1/16
    if rd == "QF": return 1/8
    if rd == "SF": return 1/4
    if rd == "F": return 1/2
    if rd == "RR": return -1
    if rd == "BR": return 1/3
    if rd == "ER": return 0

    print(colored("Fatal error:", "red"), f'"{rd}" is not a valid round')
    exit(1)


class Round:

    def __init__(self, d):
        self.abbr = d["round"]
        self.name = _assign_round(self.abbr)

        self.players = PlayerArray()
        self.matches = MatchArray()

        self.tournament = None

        self.is_processed = False

    def __lt__(self, oth):
        self_val = _round_enum(self.abbr)
        oth_val = _round_enum(oth.abbr)
        return self_val < oth_val

    def show(self, summary=False):
        if summary:
            print(f"{self.name} ({self.abbr}): {len(self.players)} players, {len(self.matches)} matches")
        else:
            print("ROUND INFORMATION")
            print(f"Tournament: ", end = "")
            self.tournament.show(summary = True)
            print(f"Name: {self.name} ({self.abbr})")
            """print("Players:")
            for player in self.players:
                print("  - ", end = "")
                player.show(summary = True)"""
            print("Matches:")
            for match in self.matches:
                print("  - ", end = "")
                match.show(summary = True)
            print("")

    def append(self, obj):
        if type(obj) == Match:
            self.matches.append(obj, safe = True)
        elif type(obj) == Player:
            self.players.append(obj, safe = True)

    def post_process(self):
        if self.is_processed: return
        self.matches.post_process()
        #self.players.sort()
        self.is_processed = True


class RoundArray:

    def __init__(self):

        self.rounds = []
        self.has_index = False

    def append(self, round):
        self.rounds.append(round)
        self.has_index = False

    def index(self):
        self.abbr_index = {}
        for i, rd in enumerate(self.rounds):
            self.abbr_index[rd.abbr] = i

    def __contains__(self, abbr):
        if not self.has_index:
            self.index()
        return abbr in self.abbr_index

    def __getitem__(self, key):
        if type(key) is str:
            if not self.has_index:
                self.index()
            k = self.abbr_index[key]
            return self.rounds[k]
        elif type(key) is int:
            return self.rounds[key]
        else:
            print(colored("Fatal Error:", "red"),
                    f"{type(key)} is not supported as a key in RoundArray")
            exit(1)

    def assign(self, d):
        if d["round"] in self:
            return self[d["round"]]
        else:
            new_round = Round(d)
            self.append(new_round)
            return new_round
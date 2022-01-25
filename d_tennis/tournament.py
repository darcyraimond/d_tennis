# Functionality for tournament information to be stored and retrieved


# Import any required packages
from termcolor import colored

from .date import str_to_date
from .player import PlayerArray
from .round import RoundArray


# ==================================================
# Content below this point
# ==================================================


class Tournament:

    def __init__(self, d):

        """
        Tournament:
            - tourney_id
            - tourney_name
            - surface
            - draw_size
            - tourney_level
            - tourney_date
            - best_of
        """

        # Data filled here
        self.id = d["tourney_id"]
        self.name = d["tourney_name"]
        self.surface = d["surface"]
        self.draw_size = int(d["draw_size"])
        self.level = d["tourney_level"]
        self.date = str_to_date(d["tourney_date"])
        
        # Arrays for later filling
        self.rounds = RoundArray()
        self.players = PlayerArray()

        self.is_processed = False

    def __lt__(self, oth):
        if self.date != oth.date:
            return self.date < oth.date
        elif self.name != oth.name:
            return self.name < oth.name

        print(colored("Fatal error", "red"), "could not separate tournaments")
        self.show()
        oth.show()
        exit(1)

    def add_player(self, player):
        if not player in self.players:
            self.players.append(player)

    def show(self, summary=False):

        if summary:
            print(f"{self.name} ({self.date.strftime('%A %d %B %Y')}, {self.surface})")
        else:
            print("TOURNAMENT INFORMATION")
            print(f"Name: {self.name}")
            print(f"Start date: {self.date.strftime('%A %d %B %Y')}")
            print(f"Surface: {self.surface}")
            print(f"Level: {self.level}")
            print(f"Draw size: {self.draw_size} (official), {len(self.players)} (actual)")
            for r in self.rounds:
                r.show(summary = True)
            print("")

    def post_process(self):
        if self.is_processed: return
        self.rounds.rounds.sort()
        for r in self.rounds.rounds:
            r.tournament = self
            r.post_process()
        self.is_processed = True


class TournamentArray:

    def __init__(self):
        self.tournaments = []
        self.has_index = False

    def __len__(self):
        return len(self.tournaments)

    def append(self, tournament, safe = False):
        if safe:
            if not tournament in self:
                if not self.has_index:
                    self.index()
                self.id_index[tournament.id] = len(self)
                self.tournaments.append(tournament)
        else:
            if not self.has_index:
                self.index()
            self.id_index[tournament.id] = len(self)
            self.tournaments.append(tournament)

    def index(self):
        self.id_index = {}
        for i, tournament in enumerate(self.tournaments):
            self.id_index[tournament.id] = i
        self.has_index = True

    def __contains__(self, obj):
        return obj in self.tournaments

    def __getitem__(self, key):

        if type(key) is int:
            return self.tournaments[key]
        elif type(key) is str:
            if not self.has_index:
                self.index()
            return self.tournaments[self.id_index[key]]

    def assign(self, d, verify=True):
        if not self.has_index:
            self.index()
        if d["tourney_id"] in self.id_index:
            t = self.tournaments[self.id_index[d["tourney_id"]]]

            if verify:
                try:
                    assert t.name == d["tourney_name"]
                    assert t.surface == d["surface"]
                    assert t.draw_size == int(d["draw_size"])
                    assert t.level == d["tourney_level"]
                    assert t.date == str_to_date(d["tourney_date"])
                except AssertionError:
                    fixed = False
                    # Put any final checks here

                    if not fixed:
                        print(colored("Fatal Error:", "red"),
                                "mismatch between assigned tournament and match data")
                        print("ASSIGNED TOURNAMENT DETAILS")
                        print(f"    Name: {t.name}")
                        print(f"    Surface: {t.surface}")
                        print(f"    Draw size: {t.draw_size}")
                        print(f"    Level: {t.level}")
                        print(f"    Date: {t.date}")
                        print("MATCH DATA")
                        print(f"    Name: {d['tourney_name']}")
                        print(f"    Surface: {d['surface']}")
                        print(f"    Draw size: {int(d['draw_size'])}")
                        print(f"    Level: {d['tourney_level']}")
                        print(f"    Date: {str_to_date(d['tourney_date'])}")
                        exit(1)

            return t

        else:
            new_tournament = Tournament(d)
            self.append(new_tournament)
            return new_tournament

    def post_process(self):
        self.tournaments.sort()
        for t in self.tournaments:
            t.post_process()


tournament_array = TournamentArray()


def get_tournament_array():

    if tournament_array is None:
        print(colored("Fatal Error:", "red"),
                "cannot load tournament_array without loaded data.",
                "Call load(path) first.")
        exit(1)
    else:
        return tournament_array
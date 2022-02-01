# Functionality for player information to be stored and retrieved


# Import any required packages
from termcolor import colored
from .date import str_to_date


# ==================================================
# Content below this point
# ==================================================

# Checks for valid id and returns it
def _assign_id(id):
    if type(id) is not str:
        print(colored("Fatal error:", "red"), f"id of {id} is not a string")
        exit(1)
    elif not id.isnumeric():
        print(colored("Fatal error:", "red"), f"id of {id} is not numeric")
        exit(1)
    else:
        return int(id)


# Cheks for valid hand and returns it
def _assign_hand(hand):
    if hand == "L":
        return "Left"
    elif hand == "R":
        return "Right"
    elif hand == "A":
        return "Ambidextrous"
    elif hand == "U" or hand == "":
        return "Unknown"
    else:
        print(colored("Fatal error:", "red"), f'"{hand}" is not a valid hand')
        exit(1)


# Checks whether a string can be cast as a number
def _is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        print("not number")
        return False


# Checks for valid height and returns it
def _assign_height(height):
    if height == "" or height == "0":
        return None
    elif _is_number(height):
        height = float(height)
        if height > 130 and height < 230:
            return int(round(height))
        elif height > 1.3 and height < 2.3:
            return int(round(height * 100))
        else:
            print(colored("Fixable error:", "yellow"),
                    f"Height of {height} is currently invalid")
            exit(1)
        
    else:
        print(colored("Fatal error:", "red"),
                f"{height} is not a valid height")
        exit(1)


class Player:

    def __init__(self, d):

        self.id = _assign_id(d["player_id"])
        self.first_name = d["name_first"]
        self.last_name = d["name_last"]
        self.hand = _assign_hand(d["hand"])
        self.dob = str_to_date(d["dob"])
        self.country = d["ioc"]
        self.height = _assign_height(d["height"])
        self.full_name = self.first_name + " " + self.last_name
        self.array_id = None

        # For later use
        self.matches = None
        self.tournaments = None

    def show(self, summary=False, show_matches=False):
        
        if summary:
            print(f"{self.first_name} {self.last_name}",
                    f"({self.country})")
        else:
            print("PLAYER INFORMATION")
            print(f"Name: {self.first_name} {self.last_name}")
            if self.dob is None:
                print("DOB: Unknown")
            else:
                print(f"DOB: {self.dob.strftime('%A %d %B %Y')}")
            print(f"Hand: {self.hand}")
            print(f"Country code: {self.country}")
            if self.height is None:
                print("Height: unknown")
            else:
                print(f"Height: {self.height}cm")
            if show_matches:
                print("Matches played:")
                for tournament in self.tournaments:
                    print(" > ", end = "")
                    tournament.show(summary = True)
                    for match in self.matches:
                        if match.tournament == tournament:
                            print("    - ", end = "")
                            match.show(summary = True)
            print("")

    def add_match(self, match):
        # Must always be safe
        if match in self.matches and self.full_name != "U Unknown":
            print(colored("Fatal Error:", "red"), 
                    "Unable to add Match to Player.matches due to duplicate.",
                    "Matches follow:")
            for m in self.matches:
                m.show(summary = True)
            print("Attempted to add: ", end = "")
            match.show(summary = True)
            exit(1)
        else:
            self.matches.append(match)

    def add_tournament(self, tournament):
        if not tournament in self.tournaments:
            self.tournaments.append(tournament)

    def post_process(self):
        self.matches.post_process()
        self.tournaments.post_process()


class PlayerArray:

    def __init__(self):

        self.players = []
        self.has_index = False

    def __len__(self):
        return len(self.players)

    def __contains__(self, player):
        return player in self.players

    def append(self, player, safe=False):
        if safe:
            if player not in self.players:
                self.players.append(player)
        else:  
            self.players.append(player)            
        self.has_index = False

    def assign_player_ids(self):
        for i, player in enumerate(self.players):
            player.array_id = i

    def index(self):
        self.id_index = {}
        for i, player in enumerate(self.players):
            self.id_index[player.id] = i
        self.has_index = True

    def __getitem__(self, key):
        if type(key) is tuple:
            if key[1] == "player_id":
                if not self.has_index:
                    self.index()
                return self.players[self.id_index[key[0]]]
            else:
                print(colored("Fatal Error:", "red"),
                    f"{key[1]} is not a valid index type")
                exit(1)
            
        elif type(key) is int:
            return self.players[key]
        elif type(key) is str:
            key = key.lower()
            out = PlayerArray()
            for player in self.players:
                if key in (player.first_name + " " + player.last_name).lower():
                    out.append(player)
            if len(out) == 0:
                return None
            elif len(out) == 1:
                return out[0]
            else:
                return out
        else:
            print(colored("Fatal Error:", "red"),
                    f"{type(key)} is not supported as a key")
            exit(1)

    def show(self, summary=False):
        if summary:
            print(f"PlayerArray of length {len(self.players)}.")
        else:
            print("PLAYER ARRAY INFORMATION")
            print(f"{len(self.players)} players:")
            for player in self.players:
                player.show(summary = True)
            print("")

    def assign(self, d, winner, verify=True):

        if winner:
            assigned_player = self[int(d["winner_id"]), "player_id"]
            full_name = d["winner_name"]
            hand = _assign_hand(d["winner_hand"])
            height = _assign_height(d["winner_ht"])
            country = d["winner_ioc"]
        else:
            assigned_player = self[int(d["loser_id"]), "player_id"]
            full_name = d["loser_name"]
            hand = _assign_hand(d["loser_hand"])
            height = _assign_height(d["loser_ht"])
            country = d["loser_ioc"]

        if verify:
            try:
                assert full_name == assigned_player.full_name
                assert hand == assigned_player.hand or hand == "Unknown"
                assert height == assigned_player.height or height is None
                assert country == assigned_player.country
            except AssertionError:
                fixed = False

                # If hands mismatch, update player to have unknown hand
                if (assigned_player.hand == "Left" and hand == "Right") \
                        or (assigned_player.hand == "Right" and hand == "Left") \
                        or assigned_player.hand == "Unknown":
                    assigned_player.hand = "Unknown"
                    fixed = True
                
                # No fixes available
                if not fixed:
                    print(colored("Fatal Error:", "red"),
                            "mismatch between assigned player and match data")
                    print("ASSIGNED PLAYER DETAILS")
                    print(f"    Name: {assigned_player.full_name}")
                    print(f"    Hand: {assigned_player.hand}")
                    print(f"    Height: {assigned_player.height}")
                    print(f"    Country: {assigned_player.country}")
                    print("MATCH DATA")
                    print(f"    Name: {full_name}")
                    print(f"    Hand: {hand}")
                    print(f"    Height: {height}")
                    print(f"    Country: {country}")
                    exit(1)

        return assigned_player

    def post_process(self):
        for player in self.players:
            player.post_process()


player_array = PlayerArray()


def get_player_array():

    if player_array is None:
        print(colored("Fatal Error:", "red"),
                "cannot load player_array without loaded data.",
                "Call load(path) first.")
        exit(1)
    else:
        player_array.assign_player_ids()
        return player_array
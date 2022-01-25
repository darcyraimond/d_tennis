# Functionality for match information to be stored and retrieved


# Import any required packages
from termcolor import colored
from .player_static import PlayerStatic
from .score import Score


# ==================================================
# Content below this point
# ==================================================


class Match:

    def __init__(self, d, m_arr, t_arr):

        """
        Tournament:
            - tourney_id
            - tourney_name
            - surface
            - draw_size
            - tourney_level
            - tourney_date
            - best_of

        Round:
            - round
            - Add this to tournament and tournament to this etc
        
        PlayerStatic:
            - winner_seed, loser_seed
            - winner_entry, loser_entry
            - winner_rank, loser_rank
            - winner_rank_points, loser_rank_points

        Player: 
            - winner_name, loser_name
            - winner_hand, loser_hand
            - winner_ht, loser_ht
            - winner_ioc, loser_ioc

        Score: TODO
            - score
            - minutes
            - w_ace, l_ace
            - w_df, l_df
            - w_svpt, l_svpt
            - w_1stin, l_1stin
            - w_1stWon, l_1stWon
            - w_2ndWon, l_2ndWon
            - w_SvGms, l_SvGms
            - w_bpSaved, w_bpFaced

        Other:
            - winner_id, loser_id: can set this up to search
        """
        self.tournament = t_arr.assign(d)
        self.round = self.tournament.rounds.assign(d)

        self.winner = m_arr.assign(d, winner = True)
        self.loser = m_arr.assign(d, winner = False)
        self.winner_static = PlayerStatic(d, winner = True)
        self.loser_static = PlayerStatic(d, winner = False)

        self.score = Score(d)
        self.match_num = int(d["match_num"])
        self.best_of = int(d["best_of"])

        # Edit other stuff e.g. TournamentArray, RoundArray etc
        self.tournament.add_player(self.winner)
        self.tournament.add_player(self.loser)
        self.round.append(self.winner)
        self.round.append(self.loser)
        self.round.append(self)
        self.winner.add_match(self)
        self.winner.add_tournament(self.tournament)
        self.loser.add_match(self)
        self.loser.add_tournament(self.tournament)

    def show(self, summary=False):
        if summary:
            print(f"{self.winner.full_name} def. {self.loser.full_name}",
                    f"({self.round.name})")
        else:
            print("MATCH INFORMATION")
            print("Tournament: ", end = "")
            self.tournament.show(summary = True)
            print(f"Round: {self.round.name} ({self.round.abbr})")
            print("Winner: ", end = "")
            self.winner.show(summary = True)
            print("Loser: ", end = "")
            self.loser.show(summary = True)
            print(f"Best of: {self.best_of}")
            print(f"Match number: {self.match_num}")
            print("")

    def __lt__(self, oth):

        # Check date
        if self.tournament.date < oth.tournament.date:
            return True
        if self.tournament.date > oth.tournament.date:
            return False
        
        # Check round
        if self.round < oth.round:
            return True
        if self.round > oth.round:
            return False
        
        # Check names
        if self.winner.last_name < self.loser.last_name:
            return True
        if self.winner.last_name > self.loser.last_name:
            return False
        if self.winner.first_name < self.loser.first_name:
            return True
        if self.winner.first_name > self.loser.first_name:
            return False

        if self.winner.full_name == "U Unknown":
            return False

        self.show()
        oth.show()

        print(colored("Fatal Error:", "red"), "can't find a way to sort matches")
        exit(1)


class MatchArray:

    def __init__(self):

        self.matches = []

        self.is_processed = False

    def __len__(self):
        return len(self.matches)

    def __contains__(self, match):
        return match in self.matches

    def append(self, match, safe=False):
        if safe:
            if match not in self.matches:
                self.matches.append(match)
            else:
                print(colored("Fatal Error:", "red"),
                        "could not append Match to MatchArray")
        else:  
            self.matches.append(match)

    def __getitem__(self, key):
        if type(key) is int:
            return self.matches[key]
        else:
            print(colored("Fatal Error:", "red"),
                    f"{type(key)} is not supported as a key")


    def post_process(self):
        if self.is_processed: return
        self.matches.sort()
        self.is_processed = True


match_array = MatchArray()


def get_match_array():

    if match_array is None:
        print(colored("Fatal Error:", "red"),
                "cannot load match_array without loaded data.",
                "Call load(path) first.")
        exit(1)
    else:
        return match_array
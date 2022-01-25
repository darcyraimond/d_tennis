# Functionality for tournament information to be stored and retrieved


# Import any required packages
from termcolor import colored


# ==================================================
# Content below this point
# ==================================================

dct = None

def _anum(val):
    if val.isnumeric():
        return int(val)
    elif val == "":
        return None
    elif val[0] == "-" and val[1:].isnumeric():
        return 0
    else:
        print(colored("Fatal Error:", "red"),
                f"can't assign value {val} of type {type(val)}")
        exit(1)


class Set:

    def __init__(self, score, tiebreak, outcome, is_complete):
        self.score = score
        self.tiebreak = tiebreak
        self.outcome = outcome
        self.is_complete = is_complete


def _get_sets(sets):
    out = []
    split_sets = sets.strip().split(" ")

    # Go through sets
    for i, s in enumerate(split_sets):

        # Handle special cases first:
        if s == "W/O" or s == "NA" or s == "DEF" or s == "Walkover":
            out.append(Set(None, None, "Walkover", False))
        elif s ==  "UNK" or s == "?-?":
            out.append(Set(None, None, "Unknown", False))
        elif s == "RET" or s == "ABD":
            out.append(Set(None, None, "Retired", False))
        elif s == "Default" or s == "Def.":
            out.append(Set(None, None, "Default", False))
        elif s == "Unfinished":
            out.append(Set(None, None, "Incomplete", False))
        elif s == "Played":
            assert split_sets[i+1] == "and"
            assert split_sets[i+2] == "unfinished" or split_sets[i+2] == "abandoned"
            assert len(split_sets) == i + 3
            out.append(Set(None, None, "Incomplete", False))
            break
        elif s == "In":
            assert split_sets[i+1] == "Progress" and len(split_sets) == i + 2
            out.append(Set(None, None, "In Progress", False))
            break
            
        # Cases where a score has eroneously turned into a date
        elif s == "Apr-00":
                out.append(Set((4,0), None, "Incomplete", False))

        # Handle general case
        elif len(s) == 3:
            if s[1] == "-":
                out.append(Set((int(s[0]), int(s[2])), None, "Complete", True))
            else:
                print(colored("Fatal Error", "red"),
                        f"No case in _get_sets matches {s}")
                print(dct)
                exit(1)

        elif len(s) == 4:
            if s[2] == "-":
                out.append(Set((10*int(s[0]) + int(s[1]), int(s[3])), None, "Complete", True))
            elif [s[1], s[3]] == ["-", "?"]:
                out.append(Set((int(s[0]), int(s[2])), None, "Incomplete", False))
            elif s[1] == "-":
                out.append(Set((int(s[0]), 10*int(s[2]) + int(s[3])), None, "Complete", True))
            else:
                print(colored("Fatal Error", "red"),
                        f"No case in _get_sets matches {s}")
                print(dct)
                exit(1)

        elif len(s) == 5:
            if [s[0], s[2], s[4]] == ["[", "-", "]"]:
                out.append(Set(None, (int(s[1]), int(s[3])), "Tiebreak", True))
            elif s[2] == "-":
                out.append(Set((10*int(s[0]) + int(s[1]), 10*int(s[3]) + int(s[4])), None, "Complete", True))
            else:
                print(colored("Fatal Error", "red"),
                        f"No case in _get_sets matches {s}")
                print(dct)
                exit(1)

        elif len(s) == 6:
            if [s[1], s[3], s[5]] == ["-", "(", ")"]:
                out.append(Set((int(s[0]), int(s[2])), int(s[4]), "Complete", True))
            elif [s[0], s[3], s[5]] == ["[", "-", "]"]:
                out.append(Set(None, (10*int(s[1]) + int(s[2]), int(s[4])), "Tiebreak", True))
            elif [s[0], s[2], s[5]] == ["[", "-", "]"]:
                out.append(Set(None, (10*int(s[1]) + int(s[3]), int(s[4])), "Tiebreak", True))
            else:
                print(colored("Fatal Error", "red"),
                        f"No case in _get_sets matches {s}")
                print(dct)
                exit(1)
        
        elif len(s) == 7:
            if [s[0], s[3], s[6]] == ["[", "-", "]"]:
                out.append(Set(None, (10*int(s[1]) + int(s[2]), 10*int(s[4]) + int(s[5])), "Tiebreak", True))
            elif [s[1], s[3], s[6]] == ["-", "(", ")"]:
                out.append(Set((int(s[0]), int(s[2])), 10*int(s[4]) + int(s[5]), "Tiebreak", True))
            else:
                print(colored("Fatal Error", "red"),
                        f"No case in _get_sets matches {s}")
                print(dct)
                exit(1)

        else:
            print(colored("Fatal Error", "red"),
                    f"No case in _get_sets matches {s}")
            print(dct)
            exit(1)
                

    # Do some post-processing
    for i, s in enumerate(out):
        if type(s.score) is tuple:
            assert len(s.score) == 2
            assert type(s.score[0]) is int
            assert type(s.score[1]) is int
            if type(s.tiebreak) is tuple:
                assert len(s.tiebreak) == 2
                assert type(s.tiebreak[0]) is int
                assert type(s.tiebreak[1]) is int
            elif type(s.tiebreak) is int:
                if s.score[0] > s.score[1]:
                    s.tiebreak = (max(7, s.tiebreak + 2), s.tiebreak)
                elif s.score[0] < s.score[1]:
                    s.tiebreak = (s.tiebreak, max(7, s.tiebreak + 2))
                elif s.score[0] == 6 and s.score[1] == 6:
                    s.tiebreak = None
                else:
                    print(colored("Fatal Error:", "red"),
                            "need to add more cases")
                    exit(1)
            elif s.tiebreak is None:
                pass
            else:
                print(colored("Fatal Error:", "red"), "need to add more cases")
                exit(1)
        elif s.score is None:
            if s.tiebreak is None:
                if s.outcome == "Unknown" or s.outcome == "Retired" \
                        or s.outcome == "Walkover" or s.outcome == "Incomplete" \
                        or s.outcome == "Default" or s.outcome == "In Progress":
                    if i != 0:
                        out[i-1].outcome = s.outcome
                    else:
                        assert i == len(out) - 1
                else:
                    print(colored("Fatal Error:", "red"),
                            "need to add more cases")
                    exit(1)
            elif type(s.tiebreak) is tuple:
                assert len(s.tiebreak) == 2
                assert type(s.tiebreak[0]) is int
                assert type(s.tiebreak[1]) is int
            else:
                print(colored("Fatal Error:", "red"), "need to add more cases")
                exit(1)
        else:
            print(colored("Fatal Error:", "red"), "need to add more cases")
            exit(1)

    # Look at final set to determine outcome/complete
    if (out[-1].outcome == "Complete" or out[-1].outcome == "Tiebreak") \
            and out[-1].is_complete:
        outcome = "Complete"
        is_complete = True
    elif (out[-1].outcome == "Unknown" or out[-1].outcome == "Retired" or out[-1].outcome == "Walkover" or out[-1].outcome == "Incomplete" or out[-1].outcome == "Default" or out[-1].outcome == "In Progress") and not out[-1].is_complete:
        outcome = out[-1].outcome
        is_complete = False
    else:
        print(colored("Fatal Error:", "red"), "need to add more cases")
        exit(1)


    return out, outcome, is_complete



class Score:

    def __init__(self, d):
        """
        Score:
            - score
            - minutes
            - w_ace, l_ace
            - w_df, l_df
            - w_svpt, l_svpt
            - w_1stin, l_1stIn
            - w_1stWon, l_1stWon
            - w_2ndWon, l_2ndWon
            - w_SvGms, l_SvGms
            - w_bpSaved, w_bpFaced
        """
        global dct
        dct = d

        # Match data
        self.minutes = _anum(d["minutes"])
        self.score_string = d["score"]
        self.sets, self.outcome, self.complete = _get_sets(d["score"])

        # Winner data
        self.winner_aces = _anum(d["w_ace"])
        self.winner_double_faults = _anum(d["w_ace"])
        self.winner_service_points = _anum(d["w_svpt"])
        self.winner_first_in = _anum(d["w_1stIn"])
        self.winner_first_won = _anum(d["w_1stWon"])
        self.winner_second_won = _anum(d["w_2ndWon"])
        self.winner_service_games = _anum(d["w_SvGms"])
        self.winner_break_points_saved = _anum(d["w_bpSaved"])
        self.winner_break_points_faced = _anum(d["w_bpFaced"])

        # Loser data
        self.loser_aces = _anum(d["l_ace"])
        self.loser_double_faults = _anum(d["l_ace"])
        self.loser_service_points = _anum(d["l_svpt"])
        self.loser_first_in = _anum(d["l_1stIn"])
        self.loser_first_won = _anum(d["l_1stWon"])
        self.loser_second_won = _anum(d["l_2ndWon"])
        self.loser_service_games = _anum(d["l_SvGms"])
        self.loser_break_points_saved = _anum(d["l_bpSaved"])
        self.loser_break_points_faced = _anum(d["l_bpFaced"])






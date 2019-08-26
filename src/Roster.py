from constants import FLEX_POSITIONS, TEAM_NAMES
import random
from itertools import combinations

class Roster():

    def __init__(self, team_number, team_name, player_names):
        self.team_number = team_number
        self.team_name = team_name
        self.player_names = player_names
        self.team_players = []
        self.starters = []
        self.starter_total = None

    def update_team_players(self, all_players):
        for n in self.player_names:
            for p in all_players:
                if n == p.name:
                    self.team_players.append(p)

    def get_starters(self, positions, lineup_slots, nf=True):
        team_players = self.team_players
        slots_dict = lineup_slots

        if len(self.starters) > 1:
            self.starters = []

        for p in positions:
            if p == 'FLEX':
                pos_starters = [tp for tp in team_players if tp.position in FLEX_POSITIONS]
                pos_starters = [tp for tp in pos_starters if tp not in self.starters]
            else:
                pos_starters = [tp for tp in team_players if tp.position == p]
            if nf:
                pos_starters.sort(key=lambda x: x.nf_projection, reverse=True)
            else:
                pos_starters.sort(key=lambda x: x.yh_projection, reverse=True)
            n_pos = slots_dict[p]
            pos_starters = pos_starters[0: n_pos]
            self.starters.extend(pos_starters)

    def compute_starter_total(self):
        self.starter_total = sum([p.nf_projection for p in self.starters])

    def get_random_player(self, min_to_get = 1, max_toget = 3):
        n_toget = random.randint(min_to_get, max_toget)
        index_toget = random.sample(range(0, len(self.starters)), n_toget)
        p_list = [self.starters[i] for i in index_toget]
        return p_list

    def get_players(self, toget):
        players = [p for p in self.team_players if p.name in toget]
        return players

    def update_roster(self, team_players):
        self.team_players = team_players

    def get_combos(self, min, max, blacklist = []):
        combos = []
        for n in range(min, max + 1):
            players = [p for p in self.team_players if p.name not in blacklist]
            combos.extend(combinations(players, n))
        return combos

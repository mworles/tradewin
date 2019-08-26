import random
from copy import copy
from constants import MY_TEAM, POSITIONS, LINEUP_SLOTS

class Trade:

    def __init__(self, my_roster, other_roster):
        self.my_team = my_roster
        self.other_team = other_roster
        self.my_nf_pre = sum([p.nf_projection for p in self.my_team.starters])
        self.my_yh_pre = sum([p.yh_projection for p in self.my_team.starters])
        self.other_yh_pre = sum([p.yh_projection for p in self.other_team.starters])
        self.players_to_give = None
        self.players_to_get = None
        self.my_team_new = copy(self.my_team)
        self.other_team_new = copy(self.other_team)
        self.my_nf_post = None
        self.my_yh_post = None
        self.other_yh_post = None
        self.my_nf_gain = None
        self.my_yh_gain = None
        self.other_yh_gain = None

    def get_random_players(self, other_min = 1, other_max = 2):
        to_get = self.other_team.get_random_player(other_min, other_max)
        min_to_give = len(to_get)
        max_to_give = min_to_give + 1
        to_give = self.my_team.get_random_player(min_to_give, max_to_give)
        self.players_to_give = to_give
        self.players_to_get = to_get

    def get_random_my_players(self, to_get_names):
        self.players_to_get = self.other_team.get_players(to_get_names)
        min_to_give = len(self.players_to_get)
        max_to_give = min_to_give + 1
        to_give = self.my_team.get_random_player(min_to_give, max_to_give)
        self.players_to_give = to_give

    def get_set_players(self, to_give_names, to_get_names, free_agents):
        self.players_to_give = self.my_team.get_players(to_give_names)
        self.players_to_get = self.other_team.get_players(to_get_names)

        if set(p.name for p in self.players_to_get) == set(to_get_names):
            pass
        else:
            to_get_more_names =  list(set(to_get_names) - set(p.name for p in self.players_to_get))
            for n in to_get_more_names:
                fa = [p for p in free_agents if p.name == n][0]
                self.players_to_get.append(fa)

        if set(p.name for p in self.players_to_give) == set(to_give_names):
            pass
        else:
            to_give_more_names =  list(set(to_give_names) - set(p.name for p in self.players_to_give))
            for n in to_give_more_names:
                fa = [p for p in free_agents if p.name == n][0]
                self.players_to_give.append(fa)

    def trade_result(self):
        my_new = [p for p in self.my_team.team_players if p not in self.players_to_give]
        other_new = [p for p in self.other_team.team_players if p not in self.players_to_get]
        my_new.extend(self.players_to_get)
        other_new.extend(self.players_to_give)
        self.my_team_new.update_roster(my_new)
        self.other_team_new.update_roster(other_new)
        self.my_team_new.get_starters(POSITIONS, LINEUP_SLOTS)
        self.other_team_new.get_starters(POSITIONS, LINEUP_SLOTS, nf=False)
        self.my_team_new.compute_starter_total()
        self.other_yh_post = sum([p.yh_projection for p in self.other_team_new.starters])
        self.my_yh_post = sum([p.yh_projection for p in self.my_team_new.starters])
        self.my_nf_gain = self.my_team_new.starter_total - self.my_nf_pre
        self.my_yh_gain = self.my_yh_post - self.my_yh_pre
        self.other_yh_gain = self.other_yh_post - self.other_yh_pre
        self.my_nf_other_yh = self.my_nf_gain * self.other_yh_gain

    def print_trade(self):
        print self.other_team.team_name
        print 'my points gained'
        print self.my_nf_gain
        print 'my yahoo gained'
        print self.my_yh_gain
        print 'players received'
        print [p.name for p in self.players_to_get]
        print 'players given'
        print [p.name for p in self.players_to_give]
        print 'other points gained'
        print self.other_yh_gain
        print ''

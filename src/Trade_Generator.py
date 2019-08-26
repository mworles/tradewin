import numpy as np
import random
from copy import copy
from constants import MY_TEAM, POSITIONS, POSITIONS_NOFLEX, LINEUP_SLOTS, TEAM_NAMES
from Trade import Trade
from itertools import combinations, product
#from pathos.multiprocessing import ProcessingPool as Pool

teams = TEAM_NAMES.keys()

def run_trade(x, my_team, other_team, trades, free_agents):

    togive = x[0]
    toget = x[1]

    my_positions_new = [p.position for p in my_team.team_players if p not in togive]
    my_positions_new.extend([p.position for p in toget])
    my_positions_missing = [p for p in POSITIONS_NOFLEX if p not in my_positions_new]

    if len(my_positions_missing) != 0:
        for pos in my_positions_missing:
            pool = [p for p in free_agents if p.position == pos]
            pool.sort(key=lambda x: x.nf_projection, reverse=True)
            toget_list = list(toget)
            toget_list.append(pool[0])
            toget = tuple(toget_list)

    other_positions_new = [p.position for p in other_team.team_players if p not in toget]
    other_positions_new.extend([p.position for p in togive])
    other_positions_missing = [p for p in POSITIONS_NOFLEX if p not in other_positions_new]

    if len(other_positions_missing) != 0:
        for pos in other_positions_missing:
            pool = [p for p in free_agents if p.position == pos]
            pool.sort(key=lambda x: x.nf_projection, reverse=True)
            togive_list = list(togive)
            togive_list.append(pool[0])
            togive = tuple(togive_list)

    try:
        to_get_names = [p.name for p in toget]
    except:
        to_get_names = [toget.name]

    try:
        to_give_names = [p.name for p in togive]
    except:
        to_give_names = [togive.name]

    trade = Trade(my_team, other_team)

    trade.get_set_players(to_give_names, to_get_names, free_agents)

    trade.trade_result()

    #if trade.my_nf_gain > 0 and trade.other_yh_gain > 0.0:
    trades.append(trade)
    #else:
        #pass

class TradeGenerator:

    def __init__(self, rosters, free_agents):
        self.rosters = rosters
        self.free_agents = free_agents
        self.my_team = next((r for r in self.rosters if r.team_number == MY_TEAM), None)
        self.roster_numbers = [r.team_number for r in self.rosters]
        self.other_rosters = [r for r in self.rosters if r != self.my_team]
        self.other_team = None

    def update_trades(self):

        if trade.my_nf_gain > 0 and trade.other_yh_gain > 0:
            self.trades.append(trade)
        else:
            pass

    def get_random_team(self):
        other_rosters = [r for r in self.rosters if r != self.my_team]
        other_team = random.choice(other_rosters)
        return other_team

    def get_team(self, team_number = 1):
        other_team = next((r for r in self.rosters if r.team_number == team_number), None)
        return other_team

    def get_trades(self, teams = None, my_max=2, other_max=2,
                   to_give=[], to_get=[], my_bl=[], other_bl=[]):

        def add_combo(x, player_count, player_set):
            x_names = [p.name for p in x]
            uc = [set(c) for c in list(combinations(x_names, player_count))]
            if player_set in uc:
                return x

        if teams is None:
            teams = [t.team_number for t in self.rosters if t.team_number !=4]

        trades = []

        free_agents = copy(self.free_agents)
        my_team = copy(self.my_team)
        my_combos = self.my_team.get_combos(1, my_max, my_bl)

        if len(to_give) != 0:
            player_count = len(to_give)
            player_set = set(to_give)
            my_combos_select = map(lambda x: add_combo(x, player_count, player_set), my_combos)
            my_combos_select = [x for x in my_combos_select if x is not None]
        else:
            my_combos_select = my_combos

        for t in teams:

            other_team = copy(self.get_team(team_number = t))
            print other_team.team_name
            combos = other_team.get_combos(1, other_max, other_bl)
            '''
            combos_select = []

            if len(to_get) != 0:
                ntg = len(to_get)
                stg = set(to_get)
                for c in combos:
                    c_names = [p.name for p in c]
                    uc = [set(x) for x in list(combinations(c_names, ntg))]
                    if stg in uc:
                        combos_select.append(c)
            else:
                combos_select = combos

            '''
            if len(to_get) != 0:
                player_count = len(to_get)
                player_set = set(to_get)
                combos_select = map(lambda x: add_combo(x, player_count, player_set), combos)
                combos_select = [x for x in combos_select if x is not None]
            else:
                combos_select = combos

            all_trades = np.asarray(list(product(my_combos_select, combos_select)))

            print len(all_trades)

            map(lambda x: run_trade(x, my_team, other_team, trades, free_agents), all_trades)

        return trades

    def test_trade(self, to_give_names, to_get_names):

        trades = []

        my_team = copy(self.my_team)

        other_team = None

        while not other_team:
            for r in self.rosters:
                ot_players = [p.name for p in r.team_players]
                for p in to_get_names:
                    if p in ot_players:
                        other_team = copy(r)

        trade = Trade(my_team, other_team)
        trade.get_set_players(to_give_names, to_get_names)
        trade.trade_result()
        trades.append(trade)
        return trades

import pickle
import os

def get_names(trade, how):
    if how=='give':
        names = [x.name for x in trade.players_to_give]
    if how=='get':
        names = [x.name for x in trade.players_to_get]
    return names

def no_exclusions(names, exclusions):
    if (any(x in names for x in exclusions)):
        return False
    else:
        return True
        
def has_players(names, inclusions):
    if set(inclusions).issubset(names):
        return True
    else:
        return False
        
def filter_trade(trade, my_min=0, other_min=0, ex_teams=None,
                 ex_give=None, ex_get=None, give=None, get=None):
    crit = True
    if my_min is not None:
        if trade.my_nf_gain <= my_min:
            crit = False
            return crit
    if other_min is not None:
        if trade.other_yh_gain <= other_min:
            crit = False
            return crit
    if ex_teams is not None:
        if trade.other_team.team_number in ex_teams:
            crit = False
            return crit
    if give is not None:
        if not has_players(get_names(trade, 'give'), give):
            crit = False
            return crit
    if get is not None:        
        if not has_players(get_names(trade, 'get'), get):
            crit = False
            return crit
    if ex_give is not None:
        if not no_exclusions(get_names(trade, 'give'), ex_give):
            crit = False
            return crit
    if ex_get is not None:
        if not no_exclusions(get_names(trade, 'get'), ex_get):
            crit = False
            return crit
    return crit
                    
def filter_trades(trades, my_min=0, other_min=0, ex_teams=None, ex_give=None,
                  ex_get=None, give=None, get=None):
    ft = [t for t in trades if filter_trade(t, my_min=my_min,
                                            other_min=other_min,
                                            ex_teams=ex_teams,
                                            ex_give=ex_give,
                                            ex_get=ex_get,
                                            give=give,
                                            get=get)]
    return ft

at = os.listdir("../trades/")

pik_now = "../trades/trade_run.dat"
infile = open(pik_now,'rb')
trades = pickle.load(infile)
infile.close()

my_min = 15
other_min = 10
rt = [t.other_team.team_number for t in trades]

ex_teams = None #[6] # rt
ex_get = ['A.J. Green', 'Aaron Jones', 'Jameis Winston']
ex_give = []
get =  []
give =  []

trades = filter_trades(trades, my_min=my_min, other_min=other_min,
                       ex_teams=ex_teams, get=get, give=give,
                       ex_get=ex_get,
                       ex_give=ex_give)
sortfunc = lambda x: x.my_nf_gain
trades.sort(key=sortfunc)

for t in trades[-50:]:
    t.print_trade()

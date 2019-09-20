from collectors import update_rosters, update_free_agents
from constants import POSITIONS, LINEUP_SLOTS, MY_TEAM
from Trade_Generator import TradeGenerator
import pickle
import datetime
import shutil

def get_dt():
    now = datetime.datetime.now()
    date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
    time = str(now.hour) + '_' + str(now.minute)
    dt = date + time
    return dt

NF_CSV = '../data/nf_projections.csv'
ROSTER_CSV = '../data/rosters.csv'
YAHOO_CSV = '../data/yahoo_projections.csv'

rosters = update_rosters(NF_CSV, YAHOO_CSV, ROSTER_CSV)
free_agents = update_free_agents(NF_CSV, YAHOO_CSV, ROSTER_CSV)
tg = TradeGenerator(rosters, free_agents)
tgt_teams = [9] #[t.team_number for t in rosters]
#tgt_teams.remove(3)
my_max = 3
other_max = 2
to_get = ['Mike Evans', 'Lamar Jackson']

trades = tg.get_trades(teams = tgt_teams,
                       my_max = my_max,
                       other_max = other_max)

trades = [t for t in trades if t.my_nf_gain > 5 and t.other_yh_gain > 5]
sortfunc = lambda x: x.my_nf_gain #lambda x: x.my_nf_gain + x.other_yh_gain
trades.sort(key=sortfunc) #, reverse=True)

for t in trades[-50:]:
    t.print_trade()

pik = "../trades/trade_run_" + get_dt() +  ".dat"
pik_now = "../trades/trade_run.dat"

with open(pik, "wb") as f:
    pickle.dump(trades, f)

shutil.copy(pik, pik_now)

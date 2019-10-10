from collectors import update_rosters, update_free_agents
from constants import POSITIONS, LINEUP_SLOTS
from Trade_Generator import TradeGenerator
import pickle
import datetime
import shutil
from League import LEAGUE as LEAGUE

def get_dt():
    now = datetime.datetime.now()
    date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
    time = str(now.hour) + '_' + str(now.minute)
    dt = date + time
    return dt

lid=1
TEAM_NAMES = LEAGUE[lid]['TEAM_NAMES']
MY_TEAM = LEAGUE[lid]['MY_TEAM']

lgdir = 'league_' + str(lid)
NF_CSV = '../data/nf_projections.csv'
ROSTER_CSV = "".join(['../data/', lgdir, '/rosters.csv'])
YAHOO_CSV = "".join(['../data/', lgdir, '/yahoo_projections.csv'])

rosters = update_rosters(NF_CSV, YAHOO_CSV, ROSTER_CSV, lid)


free_agents = update_free_agents(NF_CSV, YAHOO_CSV, ROSTER_CSV, lid)
tg = TradeGenerator(rosters, free_agents, lid)
tgt_teams = [t.team_number for t in rosters if t.team_number != MY_TEAM]
my_max = 3
other_max = 2
to_get = ['Kenny Golladay', '']
to_give = ['Todd Gurley',] 
my_bl = [] 
other_bl = []

trades = tg.get_trades(teams = tgt_teams,
                       my_max = my_max,
                       other_max = other_max,
                       to_get = to_get,
                       to_give = to_give,
                       my_bl = my_bl, 
                       other_bl = other_bl)

pik = "../trades/trade_run_" + get_dt() +  ".dat"
pik_now = "../trades/trade_run.dat"

with open(pik, "wb") as f:
    pickle.dump(trades, f)

shutil.copy(pik, pik_now)

mt = [t for t in rosters if t.team_number == MY_TEAM][0]
for p in mt.team_players:
    print p.name
    print p.nf_projection

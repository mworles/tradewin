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

op = []

for r in rosters:
    for p in r.team_players:
        op.append(p)

sortfunc = lambda x: x.nf_yh
op.sort(key=sortfunc)

for p in op[-20:]:
    print p.name, p.nf_yh


mt = [t for t in rosters if t.team_number == MY_TEAM][0]
for p in mt.team_players:
    print p.name
    print p.nf_yh

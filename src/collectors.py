import pandas as pd
import numpy as np
import csv
from NFL_Player import NFLPlayer
from Roster import Roster
from constants import (score_dict, TEAM_MATCHER, POSITIONS, LINEUP_SLOTS)
import itertools
from League import LEAGUE as LEAGUE

def get_all_players(file_path):
    file_path = file_path
    players = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                float(row[-1])
                name_split = row[0].split(' ')
                if len(name_split) > 2:
                    nm = ' '.join(name_split[0:2])
                else:
                    nm = row[0]
                #players.append(NFLPlayer(nm, row[1], row[2], float(row[-1])))
                players.append(NFLPlayer(nm, row[2], row[1], float(row[-1])))
            except:
                pass
    return players

def get_rosters(file_path, lid):
    TEAM_NUMS = {y:x for x,y in LEAGUE[lid]['TEAM_NAMES'].iteritems()}
    file_path = file_path
    rosters = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tname = row[0]
            tnum = TEAM_NUMS[tname]
            tp = row[1:]
            names = []
            for p in tp:
                p_split = p.split(' ')
                if len(p_split) > 2:
                    names.append(' '.join(p_split[0:2]))
                else:
                    names.append(p)
            rosters.append(Roster(tnum, tname, names))
    return rosters

def score_nf(file_path, lid):
    score_dict = LEAGUE[lid]['SETTINGS']
    file_path = file_path
    data = pd.read_csv(file_path)
    cmpatt = data['cmp/att'].apply(lambda x: x.split('/'))
    data['pss_cmp'] = cmpatt.apply(lambda x: float(x[0]))
    data['pss_inc'] = cmpatt.apply(lambda x: float(x[1])) - data['pss_cmp']
    data['proj'] = data.apply(lambda x: sum([x[s] * score_dict[s] for s in score_dict]), axis=1)
    data.to_csv(file_path, index=False)

def get_yahoo_projections(file_path):
    file_path = file_path
    yahoo = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            name_split = row[0].split(' ')
            fi = name_split[0].replace('.', '')[0]
            last = name_split[1]
            if row[1].upper() in TEAM_MATCHER:
                tm = TEAM_MATCHER[row[1].upper()]
            else:
                tm = row[1].upper()
            yahoo.append([fi, last, tm, row[2], float(row[-1])])
    return yahoo

def update_rosters(NF_CSV, YAHOO_CSV, ROSTER_CSV, lid):
    MY_TEAM = MY_TEAM = LEAGUE[lid]['MY_TEAM']
    #score_nf(NF_CSV, lid)
    all_players = get_all_players(NF_CSV)
    yahoo = get_yahoo_projections(YAHOO_CSV)
    [x.update_yh_projection(yahoo) for x in all_players]
    [x.update_nf_yh() for x in all_players]

    rosters = get_rosters(ROSTER_CSV, lid)

    for r in rosters:
        r.update_team_players(all_players)
        if r.team_number == MY_TEAM:
            r.get_starters(POSITIONS, LINEUP_SLOTS)
        else:
            r.get_starters(POSITIONS, LINEUP_SLOTS, nf=False)
        r.compute_starter_total()
    return rosters

def update_free_agents(NF_CSV, YAHOO_CSV, ROSTER_CSV, lid):
    #score_nf(NF_CSV, lid)
    all_players = get_all_players(NF_CSV)
    yahoo = get_yahoo_projections(YAHOO_CSV)
    [x.update_yh_projection(yahoo) for x in all_players]
    [x.update_nf_yh() for x in all_players]

    rosters = get_rosters(ROSTER_CSV, lid)
    taken = []

    for r in rosters:
        r.update_team_players(all_players)
        taken.extend(p for p in r.team_players)

    fa = [p for p in all_players if p not in taken]
    return fa

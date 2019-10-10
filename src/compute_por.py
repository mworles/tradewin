import pandas as pd
import numpy as np
import sys
sys.path.append("..")
from constants import N_TEAMS, ROSTER, rep_start, rep_bench

def rep_level(data, rank_column, rep_dict):
    '''Function to obtain the replacement-level point projection for each position.
    Requires three inputs:
    A dataframe with players, position, projections, and position rank.
    Name of position rank column.
    A dict with the replacement index'''
    df = data
    rep_pt = {}

    for p in rep_dict:
        rep_dict[p] = rep_dict[p]
        dfs = df[df['pos'] == p]
        rep = float(dfs[dfs[rank_column] == rep_dict[p]]['fpts'])
        rep_pt[p] = float(rep)
    return rep_pt

def get_porp(row, rep_dict):
    '''Function to obtain points over replacement level for each position.
    Requires two inputs:
    A dataframe with players, position, and projections.
    A dict with the projected points of replacement level for each position'''
    pos = row['pos']
    porp = round(row['fpts'] - rep_dict[pos], 2)
    #if row['rank_pos'] < 5:
    if porp < 0:
        return 0
    else:
        return porp

# set base data directory
data_in = "../data/"

# import projections data
df = pd.read_csv(data_in + '/league_1/projections_scored.csv')

# create position rank
df = df.sort_values(['pos', 'fpts'], ascending=False)
df['rank_pos'] = df.groupby('pos').cumcount() + 1

print "calculating points over replacement, starters"
rep_start_points = rep_level(df, 'rank_pos', rep_start)
df['por_start'] = df.apply(lambda x: get_porp(x, rep_start_points), axis=1)

# compute points over replacement for bench
print "calculating points over replacement, bench"
rep_bench_points = rep_level(df, 'rank_pos', rep_bench)
df['por_bench'] = df.apply(lambda x: get_porp(x, rep_bench_points), axis=1)

# compute vor per game
df['porpg_start'] = df['por_start'] / 16
df['porpg_bench'] = df['por_bench'] / 16

def is_starter(row):
    start_index = rep_start[row['pos']]
    if row['rank_pos'] <= start_index:
        return 1
    else:
        return 0

def is_owned(row):
    if row['por_bench'] > 0:
        return 1
    else:
        return 0

df['starter'] = df.apply(is_starter, axis=1)
df['owned'] = df.apply(is_owned, axis=1)

df = df.sort_values(['por_start', 'por_bench'], ascending=False)

# save file
file_name = data_in + '/league_1/por.csv'
print "writing %s" % (file_name)
df.to_csv(file_name, index=False)

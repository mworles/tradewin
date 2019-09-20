import sys
sys.path.append("..")
import math
import pandas as pd
import numpy as np
from constants import N_TEAMS, ROSTER, ROSTER_SIZE, ROSTER_START, BUDGET, N_START
from constants import rep_start, rep_bench, PCT_START

# import por file
data_in = "../data/"
df = pd.read_csv(data_in + 'por.csv')

# budget per team for skill positions
budget_skill = BUDGET - 2
# non K and DST slots to draft
slots = ROSTER_SIZE - 2

# compute budgets
budget_team = (N_TEAMS * BUDGET) - (N_TEAMS * 2)
budget_bench = round(budget_team * (1 - PCT_START))
budget_start = round(budget_team * PCT_START)
n_starters = sum(ROSTER_START.values()) * N_TEAMS
n_bench = (sum(ROSTER.values()) - sum(ROSTER_START.values())) * N_TEAMS

# indicators for starters and bench players
is_starter = df['starter'] == 1
is_bench = (df['starter'] == 0) & (df['owned'] == 1)
is_owned = df['owned'] == 1

func_round1 = lambda x: round(x, 1)

# set initial value of owned players to 1
df['val'] = np.where(df['owned'] == 1, 1, 0)

# compute total por for starters
sum_por_strt = float(df.loc[is_starter, 'por_start'].sum())
# compute multiplier for starters points over bench
mp_start = budget_start / sum_por_strt
# compute value over replacement bench for starters 
df['vor_start'] = (df['por_start'] * mp_start).apply(func_round1)

# compute total points over available for all players
sum_por_bench = float(df.loc[is_owned, 'por_bench'].sum())
# remove the baseline value of 1 from the bench budget
budget_ob = budget_team
# compute multiplier for bench points over available
mp_all = budget_ob / sum_por_bench
# use multiplier to compute value over available
df['vor_bench'] = (df['por_bench'] * mp_all).apply(func_round1)

# compute total points over available for all players
sum_por_bench = float(df.loc[is_owned, 'por_bench'].sum())
# remove the baseline value of 1 from the bench budget
budget_ob = budget_team
# compute multiplier for bench points over available
mp_all = budget_ob / sum_por_bench
# use multiplier to compute value over available
df['vor_bench'] = (df['por_bench'] * mp_all).apply(func_round1)

# dict to hold vor_bench value for each position bench replacement level
pos_rep_val = {}
# unique position types to loop over
pos_list = set(list(df.pos))

# add to dict the bench replacement value of vor_bench for each position
for pos in pos_list:
    pos_i = rep_start[pos]
    rep_player = (df['pos'] == pos) & (df['rank_pos'] == pos_i)
    pos_rep_val[pos] = round(df[rep_player]['por_bench'])

def set_base(row):
    """Returns position bench replacement value for each row if starter.
    If not starter, returns row bench replacement value"""
    pos = row['pos']
    if row['starter'] == 1:
        return pos_rep_val[pos]
    else:
        return row['por_bench']

df['por_start_bl'] = df.apply(set_base, axis=1)



# allocate bench budget across all players
sum_por_bl = df.loc[is_owned, 'por_start_bl'].sum()
# compute multiplier for bench points over available
mp_bl = (budget_bench + n_starters) / sum_por_bl
# use multiplier to compute value over available
df['vor_bl'] = df['por_start_bl'] * mp_bl

# compute total por for starters
sum_por_strt = float(df.loc[is_starter, 'por_start'].sum())
# compute baseline starter total to remove from vor budget
bl_remove = df.loc[is_starter, 'vor_bl'].sum()
# compute multiplier for starters points over bench
mp_start = (budget_start - bl_remove) / sum_por_strt
# compute value over replacement bench for starters 
df['vor_start'] = (df['por_start'] * mp_start).apply(func_round1)

# add vor starter value to starter baseline
df['vor'] = df['vor_start'] + df['vor_bl']
df['vor'] = df['vor'].apply(lambda x: round(x,0))

# set all backup te and qb to 1
for pos in ['qb', 'te']:
    mod_i = range(rep_start[pos], int(rep_bench[pos]))
    mod_f = (df['pos'] == pos) & (df['rank_pos'].isin(mod_i))
    df['vor'] = np.where(mod_f, 1, df['vor'])

# set last n_teams rb and wr to 1
for pos in ['rb', 'wr']:
    mod_i = range(int(rep_bench[pos] - N_TEAMS), int(rep_bench[pos]))
    mod_f = (df['pos'] == pos) & (df['rank_pos'].isin(mod_i))
    df['vor'] = np.where(mod_f, 1, df['vor'])


# assign remaining budget to projected starters
# compute multiplier
remain = budget_team - df['vor'].sum()
mp_remain = mp_bl = remain / sum_por_strt
df['vor_remain'] = (df['por_start'] * mp_remain).apply(func_round1)

df['vor_f'] = (df['vor'] + df['vor_remain']).apply(lambda x: round(x, 0))

# assign value of 1 to projected non-owned players
df['vor_f'] = np.where(df['vor_f'] == 0, 1, df['vor_f'])

# clean file before save
keep_cols = ['name', 'team', 'pos', 'vor_f', 'fpts', 'rank_pos', 'por_start',
             'por_bench', 'owned']
df = df[keep_cols]
df = df.rename(columns={'vor_f': 'vor'})
df['vor'] = df['vor'].astype(int)

# sort by vor, then projected points
df = df.sort_values(['vor', 'por_bench', 'fpts'], ascending=False)

# save file
file_name = data_in + 'vor.csv'
print "writing %s" % (file_name)
df.to_csv(file_name, index=False)

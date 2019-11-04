import pandas as pd
import numpy as np
import sys
from League import LEAGUE

def score_row(row, cols, lid=1):
    score_dict = LEAGUE[lid]['SETTINGS']
    pts = 0
    for c in cols:
        try:
            pts_col = row[c] * score_dict[c]
            pts += pts_col
        except:
            pass
    pts = round(pts, 1)
    return pts

def score_projections(lid=1):
    
    score_dict = LEAGUE[lid]['SETTINGS']
    
    # set base data directory
    data_in = "../data/"
    
    # import clean projections data
    df = pd.read_csv(data_in + 'nf_projections.csv')

    df['pss_cmp'] = df['cmp/att'].apply(lambda x: float(x.split('/')[0]))
    df['pss_att'] = df['cmp/att'].apply(lambda x: float(x.split('/')[1]))
    df['pss_inc'] = df['pss_att'] - df['pss_cmp'] 

    keep_cols = ['name', 'pos', 'team']
    stat_cols = score_dict.keys()
    stat_cols = [x for x in score_dict.keys() if x in df.columns]
    keep_cols.extend(stat_cols)

    cols = list(df.columns)

    print "scoring projections"
    df['fpts'] = df.apply(lambda x: score_row(x, cols), axis=1)
    keep = ['name', 'team', 'pos', 'fpts']
    df = df[keep]

    df = df.sort_values('fpts', ascending=False)

    lg_sub = 'league_' + str(lid) + '/'
    
    file_name = data_in + lg_sub + 'projections_scored.csv'
    print "writing %s" % (file_name)
    df.to_csv(file_name, index=False)

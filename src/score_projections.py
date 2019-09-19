import pandas as pd
import numpy as np
import sys
from constants import SETTINGS as score_dict

def score_row(row, cols, score_dict):
    pts = 0
    for c in cols:
        try:
            pts_col = row[c] * score_dict[c]
            pts += pts_col
        except:
            pass
    pts = round(pts, 1)
    return pts

# set base data directory
data_in = "../data/"

# import clean projections data
df = pd.read_csv(data_in + 'nf_projections.csv')
print df.head()
print df.columns
"""
cols = list(df.columns)

print "scoring projections"
df['fpts'] = df.apply(lambda x: score_row(x, cols, score_dict), axis=1)
keep = ['name', 'team', 'pos', 'fpts']
df = df[keep]

file_name = data_in + 'projections_scored.csv'
print "writing %s" % (file_name)
df.to_csv(file_name, index=False)
"""

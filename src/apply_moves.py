#cd "c:/users/mworley/tradewin/src"
import pandas as pd
import sys
import csv

df = pd.read_csv("../data/draft_results.csv", header=None)
mv = pd.read_csv("../data/moves.csv", header=None)


df = df.set_index(0)

team_dict = {}

for n in range(0, df.shape[0]):
    team = df.iloc[n].name
    team_dict[team] = df.iloc[n].values.tolist()

for row in mv.values:
    team = row[0]
    name = row[1]
    action = row[2]
    if action == 'Added Player':
        team_dict[team].append(name)
    elif action == 'Dropped Player':
        team_dict[team] = [x for x in team_dict[team] if x != name]
    else:
        sys.exit('not add or drop, exiting script')

f = '../data/rosters.csv'

with open(f, 'wb') as file:
    writer = csv.writer(file, delimiter=',')
    print 'writing %s' % (f)
    for key in team_dict:
        team_row = [key]
        team_row.extend(team_dict[key])
        writer.writerow(team_row)

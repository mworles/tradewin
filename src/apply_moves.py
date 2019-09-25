#cd "c:/users/mworley/tradewin/src"
import pandas as pd
import sys
import csv


def apply_moves(lid=1):
    file_loc = "".join(["../data/", "league_", str(lid), "/"])
    df = pd.read_csv(file_loc + "draft_results.csv", header=None)
    mv = pd.read_csv(file_loc + "moves.csv", header=None)
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
        elif action == 'Traded to':
            for t, p in team_dict.items():
                if name in p:
                    from_team = t
            team_dict[from_team] = [x for x in team_dict[from_team] if x != name]
            print 'from team'
            print team_dict[from_team]
            team_dict[team].append(name)
            print 'to team'
            print team_dict[team]

        else:
            sys.exit('not add or drop, exiting script')

    outfile = file_loc + 'rosters.csv'

    with open(outfile, 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        print 'writing %s' % (outfile)
        for key in team_dict:
            team_row = [key]
            team_row.extend(team_dict[key])
            writer.writerow(team_row)

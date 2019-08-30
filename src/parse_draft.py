#cd "c:/users/mworley/tradewin/src"
import urllib
import csv
from bs4 import BeautifulSoup as bsoup

import sys
sys.path.append("..")

# %%
def parse_row(row):
    player = row.find('a', {'class': 'name'}).get_text()
    team = row.find('td', {'class': 'last Px-sm'}).get('title')
    team = team.encode('ascii', 'ignore')
    return [player, team]

def parse_table(table):
    table_picks = []
    rows = table.find_all('tr')[1:]
    table_picks.extend(map(lambda x: parse_row(x), rows))
    return table_picks

def assign_picks(picks):
    team_dict = {}
    for row in picks:
        if row[1] not in team_dict.keys():
            team_dict[row[1]] = []
        else:
            pass
        team_dict[row[1]].append(row[0])
    return team_dict

# %%
picks = []
soup = bsoup(urllib.urlopen("../data/draft.html").read(), features="lxml")
dt = soup.find('div', {'id': 'drafttables'})
tables = dt.find_all('table')

for table in tables:
    table_picks = parse_table(table)
    picks.extend(table_picks)

team_dict = assign_picks(picks)

f = '../data/draft_results.csv'

with open(f, 'wb') as file:
    writer = csv.writer(file, delimiter=',')
    print 'writing %s' % (f)
    for key in team_dict:
        team_row = [key]
        team_row.extend(team_dict[key])
        writer.writerow(team_row)

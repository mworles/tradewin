#cd "c:/users/mworley/tradewin/src"
import urllib
import csv
from bs4 import BeautifulSoup as bsoup
import os
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

def parse_file(file):
    file_name = "".join(["../data/", file])
    print 'parsing %s' % (file_name)
    soup = bsoup(urllib.urlopen(file_name).read(), features="lxml")
    div = soup.find('div', {'id': 'fantasy'})
    rows = div.find_all('tr')

    file_moves = []
    # each move
    for row in rows:
        tds = row.find_all('td')
        actions = tds[0].find_all('span')
        names = tds[1].find_all('a', {'target': 'sports'})
        team = tds[2].find('a', {'class': "Tst-team-name"}).get_text()

        n_moves = len(actions)
        
        row_moves = []

        for n in range(0, n_moves):
            action = actions[n].get('title')
            name = names[n].get_text()
            moves = [team, name, action]
            moves = map(lambda x: x.encode('ascii', 'ignore'), moves)
            row_moves.append(moves)
        
        file_moves.extend(row_moves)
    
    return file_moves
    
# %%
files = os.listdir("../data/")
files = [f for f in files if 'moves' in f]
files = [f for f in files if '.csv' not in f]
data = map(parse_file, files)

data = [item for sublist in data for item in sublist]

data.reverse()

f = '../data/moves.csv'

with open(f, 'wb') as file:
    writer = csv.writer(file, delimiter=',')
    print 'writing %s' % (f)
    for r in data:
        writer.writerow(r)

import urllib
import csv
from bs4 import BeautifulSoup as bsoup

#import sys
#sys.path.append("..")

# %%
def parse_row(row, team):
    try:
        player = row.find('a', {'class': 'name'}).get_text()
        #team = row.find('td', {'class': 'last Px-sm'}).get('title')
        return [player, team]
    except:
        return 'NA'

def parse_table(table):
    table_picks = []
    rows = table.tbody.find_all('tr')
    team = table.thead.find('th').get_text()
    team = team.encode('ascii', 'ignore')
    table_picks.extend(map(lambda x: parse_row(x, team), rows))
    table_picks = [t for t in table_picks if t != 'NA']
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
def parse_draft(lid=1):
    picks = []
    file_loc = "".join(["../data/", 'league_', str(lid), '/'])
    file = file_loc + 'draft.html'
    soup = bsoup(urllib.urlopen(file).read(), features="lxml")
    dt = soup.find('div', {'id': 'drafttables'})
    tables = dt.find_all('table')

    for table in tables:
        table_picks = parse_table(table)
        picks.extend(table_picks)
        print table_picks

    team_dict = assign_picks(picks)

    outfile = file_loc + 'draft_results.csv'

    with open(outfile, 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        print 'writing %s' % (outfile)
        for key in team_dict:
            team_row = [key]
            team_row.extend(team_dict[key])
            writer.writerow(team_row)

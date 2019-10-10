import pandas as pd
import urllib
import csv
from bs4 import BeautifulSoup as bsoup
import datetime
import shutil
import sys
import os
sys.path.append("..")

# %%
def parse_row(row):
    td = row.find_all('td')[1]
    div = td.find('div', {'class': 'ysf-player-name Nowrap Grid-u Relative Lh-xs Ta-start'})
    name = div.find('a').get_text()
    tm_pos = div.find('span').get_text()
    tm_pos = tm_pos.split('-')
    tm = tm_pos[0].replace(' ', '')
    pos = tm_pos[1].replace(' ', '')
    srs = row.find_all('span', {'class': "Fw-b"})
    if len(srs) > 1:
        proj = srs[-1].get_text()
    else:
        proj = srs[0].get_text()
    return [name, tm, pos, proj]

def parse_file(file):
    print 'parsing %s' % (file)
    soup = bsoup(urllib.urlopen(file).read(), features="lxml")
    divp = soup.find('div', {'class': 'players'})
    rows = divp.find('table').tbody.find_all('tr')[0:]
    file_data = map(parse_row, rows)
    return file_data

def parse_yahoo_proj(lid=1):
    file_loc = "".join(["../data/", "league_", str(lid), "/"])
    files = os.listdir(file_loc)
    files = [f for f in files if 'yahoo_proj_' in f]
    files = [file_loc + f for f in files]

    data = map(parse_file, files)
    data = [item for sublist in data for item in sublist]

    now = datetime.datetime.now()
    date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
    time = str(now.hour) + '_' + str(now.minute)
    date_time = date + time

    outfile = file_loc + 'yahoo_projections_' + date_time + '.csv'
    f_current = file_loc + 'yahoo_projections.csv'

    with open(outfile, 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        print 'writing %s' % (outfile)
        for r in data:
            try:
                float(r[-1])
            except:
                print r[0]
                print 'invalid projection'
                print r

            writer.writerow(r)

    shutil.copy(outfile, f_current)

    df = pd.read_csv(f_current)
    df = df.drop_duplicates()
    df.to_csv(f_current, index=False)

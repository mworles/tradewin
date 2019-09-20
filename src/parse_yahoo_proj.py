#cd "c:/users/mworley/tradewin/src"
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
    proj = row.find('span', {'class': "Fw-b"}).get_text()
    return [name, tm, pos, proj]

def parse_file(file):
    file_name = "".join(["../data/", file])
    print 'parsing %s' % (file_name)
    soup = bsoup(urllib.urlopen(file_name).read(), features="lxml")
    divp = soup.find('div', {'class': 'players'})
    rows = divp.find('table').tbody.find_all('tr')[0:]
    file_data = map(parse_row, rows)
    return file_data

# %%
files = os.listdir("../data/")
files = [f for f in files if 'yahoo_proj_' in f]

data = map(parse_file, files)
data = [item for sublist in data for item in sublist]

now = datetime.datetime.now()
date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
time = str(now.hour) + '_' + str(now.minute)
date_time = date + time

f = '../data/yahoo_projections_' + date_time + '.csv'
f_current = '../data/yahoo_projections.csv'

with open(f, 'wb') as file:
    writer = csv.writer(file, delimiter=',')
    print 'writing %s' % (f)
    for r in data:
        try:
            float(r[-1])
        except:
            print r[0]
            print 'invalid projection'

        writer.writerow(r)

shutil.copy(f, f_current)

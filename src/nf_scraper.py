import pandas as pd
import numpy as np
from urllib import urlopen
from bs4 import BeautifulSoup
import re
import csv
import datetime
import shutil

url = 'https://www.numberfire.com/nfl/fantasy/remaining-projections'

data_files = []

def scrape(url):
    html = urlopen(url)
    print 'scraping ' + url
    soup = BeautifulSoup(html.read(), "lxml")
    tables = soup.find_all('table')
    rows = tables[0].tbody.find_all('tr')

    rows_data = []

    for r in rows:
        name = r.find("span", {"class": "full"}).get_text()
        td = r.find('td').get_text()
        pos = re.search(r"(\()([\w ]*)(,)", td).group(2)
        team = re.search(r"(\w*)(\))", td).group(1)
        row_data = [name, pos, team]
        rows_data.append(row_data)

        rows = tables[1].tbody.find_all('tr')

        pdata = [[td.get_text().strip().lower() for td in row.find_all('td')] for row in rows]

        all = [['name', 'pos', 'team', 'fp', 'ci', 'rnk_ovr', 'rnk_pos',
                'cmp/att', 'pss_yds', 'pss_td', 'pss_int', 'rsh_att', 'rsh_yds',
                'rsh_td', 'rec_rec', 'rec_yds', 'rec_td']]

    for r, p in zip(rows_data, pdata):
        row = r
        row.extend(p)
        all.append(row)

    now = datetime.datetime.now()
    date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
    time = str(now.hour) + '_' + str(now.minute)
    date_time = date + time

    f = 'data/nf_projections_' + date_time + '.csv'
    f_current = 'data/nf_projections.csv'

    with open(f, 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        print 'writing %s' % (f)
        for r in all:
            writer.writerow(r)

    shutil.copy(f, f_current)

scrape(url)

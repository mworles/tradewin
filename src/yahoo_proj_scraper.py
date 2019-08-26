import pandas as pd
import numpy as np
from urllib import urlopen
from bs4 import BeautifulSoup as bsoup
import re
import csv
import datetime
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome('C:/Users/mworley/chromedriver.exe')
browser.get("https://football.fantasysports.yahoo.com/")

login = browser.find_element_by_link_text('Sign in')
login.click()

login_user = browser.find_element_by_id('login-username')
login_user.send_keys('phi_phi_411@yahoo.com')
submit = browser.find_element_by_name('signin')
submit.click()

time.sleep(5)

login_pwd = browser.find_element_by_id('login-passwd')
login_pwd.send_keys('kentucky2@')
submit = browser.find_element_by_id('login-signin')
submit.click()


url = 'https://football.fantasysports.yahoo.com/f1/624679/players?&sort=AR&sdir=1&status=ALL&pos=O&stat1=S_PSR_2018&jsenabled=1'
browser.get(url)

sortby = browser.find_element_by_link_text('Fan Pts')
sortby.click()
time.sleep(3)

data = []
print 'scraping %s' % (url)
n = 0
while n < 15:
    print 'scraping player page %s' % (n)
    try:
        soup = bsoup(browser.page_source, 'html.parser')
        tab = soup.find('div', {'class': 'players'})
        rows = tab.tbody.find_all('tr')
        for r in rows:
            name = r.find('a', {'class': 'Nowrap'}).get_text()
            tm_pos = r.find('span', {'class': 'Fz-xxs'}).get_text()
            tm_pos = tm_pos.split('-')
            tm = tm_pos[0].replace(' ', '')
            pos = tm_pos[1].replace(' ', '')
            #if n < 2:
                #proj = r.find_all('td')[6].get_text()
            #else:
            proj = r.find_all('td')[7].get_text()
            data.append([name, tm, pos, proj])

        next = browser.find_element_by_link_text('Next 25')
        n += 1
        next.click()
        time.sleep(3)
    except:
        break

browser.quit()

now = datetime.datetime.now()
date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
time = str(now.hour) + '_' + str(now.minute)
date_time = date + time

f = 'data/yahoo_projections_' + date_time + '.csv'
f_current = 'data/yahoo_projections.csv'

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

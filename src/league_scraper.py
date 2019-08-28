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
from League import LEAGUE as league

def scrape_league(league):
    
    global time
    
    #lg = league[2]
    id = league['LOGIN']
    key = league['KEY']
    league_id = league['LEAGUE_ID']

    n_teams = len(league['TEAM_NAMES'].values())

    browser = webdriver.Chrome('driver/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    browser.get("https://football.fantasysports.yahoo.com/")

    login = browser.find_element_by_link_text('Sign in')
    login.click()

    time.sleep(2)

    login_user = browser.find_element_by_id('login-username')
    login_user.send_keys(id)
    
    time.sleep(2)
    
    submit = browser.find_element_by_id('login-signin')
    submit.click()

    time.sleep(2)

    login_pwd = browser.find_element_by_id('login-passwd')
    login_pwd.send_keys(key)
    submit = browser.find_element_by_id('login-signin')
    submit.click()

    teams = []

    n_teams = range(1, n_teams + 1)

    url_base = "https://football.fantasysports.yahoo.com/f1/"
    url_league = "".join([url_base, str(league_id), '/'])

    for n in n_teams:
        url_team = url_league + str(n)
        browser.get(url_team)
        print 'scraping roster team %r' % (n)
        team = [n]
        soup = bsoup(browser.page_source, 'html.parser')
        a_names = soup.find_all('a', {'class': 'Nowrap name F-link'})
        names = [a.get_text() for a in a_names]
        team.extend(names)
        teams.append(team)

    browser.quit()

    now = datetime.datetime.now()
    date = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_'
    time = str(now.hour) + '_' + str(now.minute)
    date_time = date + time

    f = 'data/rosters_' + date_time + '.csv'
    f_current = 'data/rosters.csv'

    with open(f, 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        print 'writing %s' % (f)
        for r in teams:
            writer.writerow(r)

    shutil.copy(f, f_current)

my_league = league[2]
scrape_league(my_league)

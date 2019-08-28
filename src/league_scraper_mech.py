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

import mechanize
import cookielib
import html2text

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open("https://football.fantasysports.yahoo.com/")

sign_in = br.find_link(text="Sign in")
br.follow_link(sign_in)

# View available forms

br.select_form(nr=0)
br.form['username'] = 'mworles40'
br.form['passwd'] = 'kentucky2@'
br.submit(id='login-signin')

#url_base = "https://football.fantasysports.yahoo.com/f1/"
#url_team= "".join([url_base, str(league[2]['LEAGUE_ID']), '/', str(1)])

url = "https://football.fantasysports.yahoo.com/f1/1009392"
br.open(url_team)

for link in br.links():
    print link.text

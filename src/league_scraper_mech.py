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

import sys, logging
logger = logging.getLogger("mechanize.cookies")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

def print_link_text(links):
    for link in links:
        print link.text


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
#for f in br.forms():
    #print f
br.select_form(nr=0)

br.form['username'] = 'mworles40'
#br.click(name='signin')
br.form['passwd'] = 'kentucky2@'
br.set_simple_cookie('AO', 'u=1', '.yahoo.com', path='/')
br.set_simple_cookie('B',
                          '23mqeupemg7ej&b=4&d=eOkh961pYEJITp9VsPWCfZTpLTkzRjTm1GwaDg--&s=q2&i=IQaBIZc6MWVhDMLrsBz.',
                          '.yahoo.com', path='/')
br.set_simple_cookie('F',
                          'd=0U_gff89vJx2ETiwBsqG5J6jBiHzMbCAmABBmoQ-',
                          '.yahoo.com', path='/')
br.set_simple_cookie('GUC', 'AQEAAQJdaW1eNEIgTQTN&s=AQAAAPt3gggq&g=XWgd8w',
                          '.yahoo.com', path='/')
br.set_simple_cookie('GUCS', 'ARASEppE', '.yahoo.com', path='/')
br.set_simple_cookie('PH', 'fn=E0PIEOCed89JkOVJ.0TJcg--&l=en-US&i=us', '.yahoo.com', path='/')
br.set_simple_cookie('T', 'z=p3BadBpLpedB6f6zLKknHKGNDU0MQY1MzczNzVPNjc2&a=QAE&sk=DAArDLCXtDyzlu&ks=EAA9tevPxpsUQajZyo.NMl2Pw--~G&kt=EAAtwBx8ExCNgQWheBrUp8Ifw--~I&ku=FAAjGqWGll.0eYRqBZA7KCM6RalnmfMvUcZYtb4mJbGnO3PLpzgJxRze9QAfONk8xpVIcZh9Y0XC2GbmxocvTBAtY6IV79fc0OfJovYSZrI6WLKA.WNtiO07v1peoUjF83Vy3z5RTB.SZ1HMbvsKiy5X4EZZbJqS1uMCxf6AsV3TKk-~A&d=bnMBeWFob28BZwFWVldXTU4zWE81SUQ1RU1XVkNDQVhGQVA1UQFzbAFNekl6TmdFeU5EQTBNREk0TVRBeAFhAVFBRQFhYwFBRW83QURkbAFsYXQBcDNCYWRCAWNzAQFzYwFkZXNrdG9wX3dlYgFmcwFfcVRPbE5sZGFCM3ABenoBcDNCYWRCQTdF&af=JnRzPTE1NjcxMDQ0ODkmcHM9WE96Uk1zTmo5angzQWZKdUpsZTd0US0t', '.yahoo.com', path='/')
br.set_simple_cookie('Y', 'v=1&n=713qmr9teevs4&l=cmehb4iuq/o&p=m2j0iln00000000&r=f7&intl=us', '.yahoo.com', path='/')


#br.set_cookie("t=1567099041&j=0; expires=Friday, 20-Aug-20 23:12:40 GMT")
#for control in br.form.controls:
    #print control
    #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
response = br.submit()
print response.read()
"""
#click_response = br.click(name='signin')
#response = mechanize.urlopen(click_response)
#print(response.read())

#br.submit(name='signin')
#br.submit(id='login-signin')
#url_base = "https://football.fantasysports.yahoo.com/f1/"
#url_team= "".join([url_base, str(league[2]['LEAGUE_ID']), '/', str(1)])

url = "https://football.fantasysports.yahoo.com/f1/1009392"
br.open(url_team)
"""

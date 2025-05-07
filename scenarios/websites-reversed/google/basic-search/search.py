#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random


options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)


try:
    firefox.get("https://www.google.com")
except:
    pass

firefox.implicitly_wait(1)
time.sleep(5)


Search_Term="This is some text"


""" 
Top (and interesting) google searches Dec 2023
    - Chat GPT (cant)
    - Youtube (done)
    - Amazon (done)
    - Facebook (cant)
    - Weather
    - Google (done)
    - Gmail (done)
    - Wordle
    - Google translate (done)
    - ESPN
    - Target
    - Google maps
    - Netflix (cant)
    - Zillow
    - Craigslist
    - Twitch (done)
    - Discord (done)
"""


# Get the login fields
search_bar = firefox.find_element(By.CSS_SELECTOR, '[aria-label="Search"]')
search_bar.click()


# Type in the search phrase
for c in Search_Term:
    time.sleep(abs(random.gauss(0.05, 0.1)))
    webdriver.ActionChains(firefox)\
            .send_keys(c)\
            .perform()


webdriver.ActionChains(firefox)\
        .send_keys(u'\ue007')\
        .perform()


# Busy wait for the email
while True:
    continue


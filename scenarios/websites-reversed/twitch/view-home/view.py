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
    firefox.get("https://www.twitch.tv")
except:
    pass

firefox.implicitly_wait(1)



# Busy wait for the email
while True:
    continue


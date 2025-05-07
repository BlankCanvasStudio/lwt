#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random

# This simply watches the first streamer on the home page

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

tiles = firefox.find_element(By.XPATH, "//a/div/div/img")
tiles.click()

# Busy wait for the email
while True:
    continue


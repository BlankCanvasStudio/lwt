#!/bin/python3

from selenium import webdriver
import time, os

options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)

adbp_xpi = os.path.expanduser('~/ublock.xpi') # Downloaded in install step
firefox.install_addon(adbp_xpi)


time.sleep(3) # Let the adblocker install

try:
    firefox.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
except:
    pass


firefox.implicitly_wait(20)

# Check if there is an ad playing
webdriver.ActionChains(firefox)\
        .send_keys(" ")\
        .perform()


while True:
    continue

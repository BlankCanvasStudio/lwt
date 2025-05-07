#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)


try:
    firefox.get("https://zoom.us/signin#/login")
except:
    pass


zoom_email = "lwtchatone@gmail.com"
zoom_paswd = "1Nsecure!"


# Get user input info
email_input = firefox.find_element(By.ID, "email")
paswd_input = firefox.find_element(By.ID, "password")
login_buttn =  firefox.find_element(By.ID, "js_btn_login")


# This seems to remove banner ad for some reason
num_presses = 4
for _ in range(0, num_presses):
    email_input.click()
    webdriver.ActionChains(firefox)\
            .send_keys('w')\
            .perform()
    firefox.implicitly_wait(0.1)
    time.sleep(0.1)
# Now delete the text
email_input.click()
for _ in range(0, num_presses * 2):
    webdriver.ActionChains(firefox)\
            .send_keys('\ue003')\
            .perform()
    firefox.implicitly_wait(0.05)
    time.sleep(0.05)


# Enter email
"""
for c in zoom_email:
    email_input.click()
    webdriver.ActionChains(firefox)\
            .send_keys(c)\
            .perform()
    firefox.implicitly_wait(0.1)
    time.sleep(0.1)
firefox.implicitly_wait(2000)
time.sleep(2)
"""
webdriver.ActionChains(firefox)\
        .send_keys(zoom_email)\
        .perform()
firefox.implicitly_wait(2000)
time.sleep(2)


firefox.implicitly_wait(2000)
# Enter password
# paswd_input.click()
webdriver.ActionChains(firefox)\
        .send_keys(u'\ue004')\
        .perform()
firefox.implicitly_wait(2000)
webdriver.ActionChains(firefox)\
        .send_keys(zoom_paswd)\
        .perform()
firefox.implicitly_wait(2000)
# Actually login
login_buttn.click()
firefox.implicitly_wait(2000)


while True:
    continue

# Stop watching the video
firefox.quit()


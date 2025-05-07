#!/bin/python3

# Chat 2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time, random, string


# time.sleep(90) # Waiting for the email to send

options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)


try:
    firefox.get("https://www.gmail.com")
except:
    pass

firefox.implicitly_wait(1)

# Get the login fields
email_input = firefox.find_element(By.ID, "identifierId")

# Login settings
email = "lwtchattwo@gmail.com"
password = "1nsecure!"


# Input the email
email_input.click()
webdriver.ActionChains(firefox)\
        .send_keys(email)\
        .perform()
webdriver.ActionChains(firefox)\
        .send_keys(u'\ue007')\
        .perform()
firefox.implicitly_wait(10)
# Input the password
time.sleep(5)
wait(firefox, 150).until(EC.presence_of_element_located((By.NAME, "Passwd")))
passw_input = firefox.find_element(By.NAME, "Passwd")
passw_input.click()
webdriver.ActionChains(firefox)\
        .send_keys(password)\
        .perform()
webdriver.ActionChains(firefox)\
        .send_keys(u'\ue007')\
        .perform()
firefox.implicitly_wait(10)

# Busy wait for the email
while True:
    continue


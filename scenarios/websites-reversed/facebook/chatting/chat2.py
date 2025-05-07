#!/bin/python3

# Chat 2

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.FirefoxOptions()
# options.add_argument("-headless")

firefox = webdriver.Firefox(options=options)

try:
    firefox.get("https://www.facebook.com/login")
except:
    pass

firefox.implicitly_wait(1)

# Get the login fields
email_input = firefox.find_element(By.ID, "email")
passw_input = firefox.find_element(By.ID, "pass")
login_btton = firefox.find_element(By.ID, "loginbutton")


# Login settings
email = "testing@testing.com"
password = "1nsecure!"
# Input the email
email_input.click()
webdriver.ActionChains(firefox)\
        .send_keys(email)\
        .perform()
firefox.implicitly_wait(10)
# Input the password
passw_input.click()
webdriver.ActionChains(firefox)\
        .send_keys(password)\
        .perform()
firefox.implicitly_wait(10)
# Click the login button
login_btton.click()



while True:
    continue




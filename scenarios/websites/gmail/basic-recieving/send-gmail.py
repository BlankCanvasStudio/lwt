#!/bin/python3

# Chat 2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time, random, string

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
email = "lwtchatone@gmail.com"
password = "1nsecure!"
# Recipient settings
recp_email = "lwtchattwo@gmail.com"
email_subj = "A nice testing email"
email_character_length = 5000


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


firefox.implicitly_wait(10)
time.sleep(3)

# Start a new email
new_email = firefox.find_element(By.XPATH, '//div[text()="Compose"]')
new_email.click()
firefox.implicitly_wait(10)


# Enter sender
webdriver.ActionChains(firefox)\
        .send_keys(recp_email)\
        .perform()
webdriver.ActionChains(firefox)\
        .send_keys(u'\ue007')\
        .perform()
webdriver.ActionChains(firefox)\
        .send_keys(u'\ue004')\
        .perform()
# Enter subject
webdriver.ActionChains(firefox)\
        .send_keys(email_subj)\
        .perform()
webdriver.ActionChains(firefox)\
        .send_keys(u'\ue004')\
        .perform()
# Enter body
body = ''.join(random.choices(string.ascii_letters + string.digits, k=email_character_length))
webdriver.ActionChains(firefox)\
        .send_keys(body)\
        .perform()

firefox.implicitly_wait(10)
time.sleep(3)

# Send the email
send_email = firefox.find_element(By.XPATH, '//div[text()="Send"]')
send_email.click()
time.sleep(3)


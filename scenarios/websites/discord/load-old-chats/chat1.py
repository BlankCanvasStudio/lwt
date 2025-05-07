#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, string

email = "lwtchatone@gmail.com"
password = "1Nsecure!"
msg_length = 80
sec_between_chat = 8

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def write_text(text, time_mod=0.3):
    for c in text:
        sec = random.gauss(time_mod, time_mod / 2)
        webdriver.ActionChains(firefox)\
                .send_keys(c)\
                .perform()
        time.sleep(abs(sec))


options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)


try:
    firefox.get("https://www.discord.com/login")
except:
    pass

firefox.implicitly_wait(1)
time.sleep(5)


# Login to discord
# Click on email field
email_el = firefox.find_element(By.NAME, "email")
email_el.click()
firefox.implicitly_wait(4)
# Enter email
webdriver.ActionChains(firefox)\
        .send_keys(email)\
        .perform()
# Tab
webdriver.ActionChains(firefox)\
        .send_keys('\ue004')\
        .perform()
# Enter password
webdriver.ActionChains(firefox)\
        .send_keys(password)\
        .perform()
        .perform()
# Enter
webdriver.ActionChains(firefox)\
        .send_keys('\ue007')\
        .perform()

firefox.implicitly_wait(4)
time.sleep(5)
# Click on the dm
dm = firefox.find_element(By.CSS_SELECTOR, '[aria-label="lwtchattwo (direct message)"]')
dm.click()


msg_box = firefox.find_element(By.CSS_SELECTOR, '[aria-label="Message @lwtchattwo"')
msg_box.click()


while True:
    continue


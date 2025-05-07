#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, string

email = "lwtchatone@gmail.com"
password = "1Nsecure!"
msg_length = 80
sec_between_chat = 11

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def write_text(text, time_mod=0.15):
    for c in text:
        sec = random.gauss(time_mod, time_mod / 2)
        webdriver.ActionChains(firefox)\
                .send_keys(c)\
                .perform()
        time.sleep(abs(sec))



options = webdriver.FirefoxOptions()
# options.add_argument("-headless")

firefox = webdriver.Firefox(options=options)

try:
    firefox.get("https://chat.openai.com/auth/login")
except:
    pass

firefox.implicitly_wait(1)
time.sleep(5)

login_btn = firefox.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
login_btn.click()

firefox.implicitly_wait(4)
#/ time.sleep(6)
cloud_flare = firefox.find_element(By.XPATH, "//*[contains(type, 'checkbox')]")
cloud_flare.click()

while True:
    continue

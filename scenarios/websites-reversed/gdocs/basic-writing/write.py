#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time, random, string, math

# Login settings
email = "lwtchattwo@gmail.com"
password = "1nsecure!"
# Text settings
random_characters=True
text_length=1000
fixed_text=""


options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)


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



try:
    firefox.get("https://docs.google.com")
except:
    pass


firefox.implicitly_wait(1)

# Get the login fields
email_input = firefox.find_element(By.ID, "identifierId")

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

time.sleep(5)

# Skip "Not Now section"
try:
    not_now_btn = firefox.find_element(By.XPATH, "//*[ text() = ‘Get started free’ ]")
    not_now_btn.click()
    firefox.implicitly_wait(5)
except:
    pass


firefox.implicitly_wait(10)
img = firefox.find_element(By.CSS_SELECTOR, '[src="https://ssl.gstatic.com/docs/templates/thumbnails/docs-blank-googlecolors.png"]')
img.click()

time.sleep(5)

to_write = fixed_text
if random_characters:
    to_write = generate_random_string(text_length)

write_text(to_write)


while True:
    continue


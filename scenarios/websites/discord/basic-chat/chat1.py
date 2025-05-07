#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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

def rand_wait(time_mod=0.15):
    sec = random.gauss(time_mod, time_mod / 2)
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





email_el = firefox.find_element(By.NAME, "email")
email_el.click()
firefox.implicitly_wait(4)
# Enter email
write_text(email)
# Tab
webdriver.ActionChains(firefox)\
        .send_keys('\ue004')\
        .perform()
# Enter password
write_text(password)
# Tab
# webdriver.ActionChains(firefox)\
#         .send_keys('\ue004')\
#         .perform()
# Enter
webdriver.ActionChains(firefox)\
        .send_keys('\ue007')\
        .perform()

firefox.implicitly_wait(4)
time.sleep(5)


# Beat the capcha
action =  ActionChains(firefox);
mouse_x=832
mouse_y=562
current_x_index = 0
current_y_index = 0
while current_x_index < mouse_x and current_y_index < mouse_y:
    y_rand = random.randint(50, 100)
    x_rand = random.randint(50, 100)

    current_x_index += x_rand
    current_y_index += y_rand
    if current_x_index > mouse_x: x_rand = mouse_x - (current_x_index - x_rand)
    if current_y_index > mouse_y: y_rand = mouse_y - (current_y_index - y_rand)
    action.move_by_offset(x_rand,y_rand);
    action.perform();
    print(current_x_index, current_y_index)# Click on email field
    time.sleep(0.00005)

action.double_click().perform()
firefox.implicitly_wait(4)
time.sleep(2)


# Click on the dm
try:
    dm = firefox.find_element(By.CSS_SELECTOR, '[aria-label="lwtchattwo (direct message)"]')
except:
    dm = firefox.find_element(By.CSS_SELECTOR, '[aria-label="unread, lwtchattwo (direct message)"]')

dm.click()


msg_box = firefox.find_element(By.CSS_SELECTOR, '[aria-label="Message @lwtchattwo"')
msg_box.click()




# Busy wait for the email
while True:
    to_write = generate_random_string(msg_length)
    write_text(to_write)
    # Enter
    webdriver.ActionChains(firefox)\
        .send_keys('\ue007')\
        .perform()
    time.sleep(sec_between_chat)


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
    firefox.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
except:
    pass


firefox.implicitly_wait(20)

# Check if there is an ad playing
ad_frame = firefox.find_element(By.CLASS_NAME, "video-ads")

# Deal with ads
if ad_frame.is_displayed():
    firefox.implicitly_wait(1)
    webdriver.ActionChains(firefox)\
            .send_keys(" ")\
            .perform()
    firefox.implicitly_wait(10)
    try:
        skip_button = firefox.find_element(By.CLASS_NAME, "ytp-ad-skip-button-modern")
        while not skip_button.is_displayed():
            time.sleep(0.1)
        webdriver.ActionChains(firefox)\
                .click(skip_button)\
                .perform()
    except:
        pass



wait_time = 20
# This means ad is unskipable
if ad_frame.is_displayed(): wait_time += 15  


# Get the video player
player = firefox.find_element(By.ID, "movie_player")
# Check if the video is playing
if "paused-mode" in player.get_attribute("class").split(" "):
    # If not, play it
    firefox.implicitly_wait(1)
    webdriver.ActionChains(firefox)\
            .send_keys(" ")\
            .perform()


while true:
    continue


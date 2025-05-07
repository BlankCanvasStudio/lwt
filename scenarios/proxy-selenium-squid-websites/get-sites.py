#!/bin/python3

from selenium import webdriver
import time

PROXY = "10.0.5.2:3128"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome(options=chrome_options)

try:
    chrome.get("https://www.google.com")
except:
    pass


time.sleep(2)


try:
    chrome.get("https://www.wikipedia.com")
except:
    pass


time.sleep(4)


try:
    chrome.get("https://www.reddit.com")
except:
    pass


time.sleep(6)


chrome.quit()


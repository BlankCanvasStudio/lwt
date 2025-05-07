#!/bin/python3

# Chat 1

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.FirefoxOptions()
options.add_argument("-headless")

firefox = webdriver.Firefox(options=options)

try:
    firefox.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
except:
    pass


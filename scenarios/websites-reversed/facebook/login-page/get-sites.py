#!/bin/python3

from selenium import webdriver

options = webdriver.ChromeOptions() 
options.add_argument("--headless")

chrome = webdriver.Chrome(options=options)

chrome.get("https://www.facebook.com/login")

chrome.quit()


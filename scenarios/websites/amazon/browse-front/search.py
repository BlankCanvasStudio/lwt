#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, random, math


options = webdriver.FirefoxOptions()
options.add_argument("-headless")
options.add_argument("window-size=1400,600")

firefox = webdriver.Firefox(options=options)

firefox.set_window_size(1920, 1080)


try:
    firefox.get("https://www.amazon.com")
except:
    pass

firefox.implicitly_wait(1)
time.sleep(5)

email = "lwtchatone@gmail.com"
password = "1Nsecure!"


Search_Term="This is some text"


def wait_gaus(wait_param = 0.3):
    wait_time = abs(random.gauss(wait_param, wait_param / 2))
    time.sleep(wait_time)

def scroll_to_bottom(scroll_times = 10, wait_param = 0.3):
    for x in range(0, scroll_times):
        wait_time = abs(random.gauss(wait_param, wait_param / 2))
        time.sleep(wait_time)
        frm = str(x / scroll_times) + " * document.body.scrollHeight"
        to = str((x + 1) /scroll_times)  + " * document.body.scrollHeight"
        firefox.execute_script("window.scrollTo(" + frm + ", " + to + ");")

def scroll_mostly_bottom(scroll_times = 10, wait_param = 0.3, scroll_fraction=0.7):
    for x in range(0, scroll_times):
        wait_time = abs(random.gauss(wait_param, wait_param / 2))
        time.sleep(wait_time)
        frm = str((scroll_fraction) * (x / scroll_times)) + " * document.body.scrollHeight"
        to = str((scroll_fraction) * ((x + 1) /scroll_times))  + " * document.body.scrollHeight"
        firefox.execute_script("window.scrollTo(" + frm + ", " + to + ");")


def add_to_cart():
    # Check for sizing
    scroll_mostly_bottom(scroll_fraction=0.4)
    firefox.implicitly_wait(1)
    try:
        size = firefox.find_element(By.CSS_SELECTOR, '[aria-labelledby="size_name_0-announce"]')
        size.click()
        size.click() # This double click gets rid of edge case of not in that color
    except:
        try:
            size_fold = firefox.find_element(By.ID, 'dropdown_selected_size_name')
            size_fold.click()
            firefox.implicitly_wait(5)
            # size = firefox.find_element(By.ID, 'native_dropdown_selected_size_name_0')
            # size.click()
            webdriver.ActionChains(firefox)\
                    .send_keys(u'\ue007')\
                    .perform()
            firefox.implicitly_wait(5)
            webdriver.ActionChains(firefox)\
                    .send_keys(u'\ue015')\
                    .perform()

        except:
            try:
                size_nuclear = firefox.find_element(By.XPATH, "//li/span/span/span/input")
                size_nuclear.click()
            except Exception as e:
                pass


def search_pages(search_base, num_pages):
    for i in range(0, num_pages):
        scroll_to_bottom(wait_param = 0.9)
        try:
            see_all_button = firefox.find_element(By.ID, 'apb-desktop-browse-search-see-all')
            see_all_button.click()
        except:
            try:
                label = "Go to next page, page " + str(search_base)
                next_btn = firefox.find_element(By.CSS_SELECTOR, '[aria-label="' + label + '"]')
                next_btn.click()
                search_base += 1
            except:
                pass
    return search_base




interesting_field = firefox.find_element(By.ID, 'desktop-grid-2')
interesting_field.click()

search_base = 2

num_items_to_check = abs(math.ceil(random.gauss(2, 3)))

for _ in range(0, num_items_to_check):
    # See how many pages you need ot look through
    pages_to_search = math.ceil(random.uniform(1, 3))
    search_base = search_pages(search_base, pages_to_search)

    # Pick an item to look at
    item_to_check = math.ceil(random.gauss(10, 5))

    # Find all the items we can look at
    items = firefox.find_elements(By.XPATH, '//a/div/img')

    # Prevent indexing errors
    if item_to_check >= len(items): 
        item_to_check = len(items) - 1

    # Give a nice pause to decide on what to choose
    wait_gaus(4)

    items[item_to_check].click()

    # Visit the site fr a bit
    wait_gaus(5)
    amount_to_scroll = abs(random.gauss(0.7, 0.7))
    scroll_mostly_bottom(15, 1, amount_to_scroll)

    # Didn't like the item
    firefox.execute_script("window.history.go(-1)")

    # Do it again


print("Done")
# Busy wait for tester to kill machine
while True:
    continue


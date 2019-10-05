#! /usr/bin/python3

# Craigslist Bot  
#    1st Iteration - Selling My Brother's Car 

# do not use python-craigslist for selling; only for buying and scraping posts
# may need requests and beautifulsoup4
# import requests, bs4

import selenium_functions as sele
import mech_functions as mech
import sys


def selenium_browser(URL):
    browser = sele.sele_open_browser(URL)
    try:
        sele.sele_create_post(browser)
    except Exception as err:
        print("An exception occurred: " + str(err))
    return browser

def mechanical_browser(URL):
    browser = mech.open(URL)
    try:
        mech.create_post(browser)
    except Exception as err:
        print("An exception occurred: " + str(err))
    return browser


def main():
    URL = 'https://batonrouge.craigslist.org/'
    ans = input("Hello, I'm the Craigslist Bot!\nWould you like to make a post? ")
    affirmative = ('yes','yep', 'ye', 'y', '', 'mhmm', 'oui', 'si')
    if ans in affirmative:
        _type = input("What type of program: [mech]anicalsoup or [sele]nium? ")
        if _type != 'sele':
            # open browser with mechanical soup
            # currently mechanical is the only way that fully works
            browser = mechanical_browser(URL)
        else:
            browser = selenium_browser(URL)
    else:
        print("I'm sorry, I can only make posts for now. Goodbye!")
        sys.exit()
    sys.exit()

if __name__ == '__main__':
    main()   

#! /usr/bin/python3

# Craigslist Bot  
#    1st Iteration - Selling My Brother's Car 

# do not use python-craigslist for selling; only for buying and scraping posts
# may need requests and beautifulsoup4
# import requests, bs4

import clbot_functions as CLF
import clbot_mech_functions as mech
import sys


def selenium_browser(URL):
    browser = CLF.sele_open_browser(URL)
    try:
        CLF.sele_create_post(browser)
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
            browser = mechanical_browser(URL)
        else:
            browser = selenium_browser(URL)
    else:
        print("I'm sorry, I can only make posts for now. Goodbye!")
        exit()

    
    # currently, the program stops at Step 3.
    # quitting out of the program when at the end.
    sys.exit()

if __name__ == '__main__':
    main()   

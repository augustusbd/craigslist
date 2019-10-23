#! /usr/bin/python3

# Craigslist Bot  
#    1st Iteration - 'Create A Post' 

# do not use python-craigslist for selling; only for buying and scraping posts
# may need requests and beautifulsoup4
# import requests, bs4
import sys

import selenium_functions as sele
import general_functions as gen
import mech_class as mech


def selenium_browser_create_post(URL):
    """
    Selenium WebDriver Implementation of 'Create A Post'
    """
    browser = sele.sele_open_browser(URL)
    try:
        sele.sele_create_post(browser)

    except Exception as err:
        print(f"An exception occurred: {str(error)}")

    return browser


def mechanical_browser_create_post():
    """
    Mechanical Soup Implementation of 'Create A Post'
    """
    post = mech.CreatePost()
    try:
        post.begin_process()

    except Exception as error:
        print(f"An exception occurred: {str(error)}")

    return post


URL = 'https://batonrouge.craigslist.org/'

def main():
    print("Hello, I'm the Craigslist Bot!")
    confirmed = gen.ask_for_confirmation("Would you like to make a post? ")

    if confirmed:
        _input = input("What type of program: [mech]anicalsoup or [sele]nium? ")
        if _input != 'sele':
            # open browser with mechanical soup
            # currently mechanical is the only way that fully works
            post = mechanical_browser_create_post()

        else:
            browser = selenium_browser_create_post(URL)

    else:
        print("I'm sorry, I can only make posts for now. Goodbye!")

    sys.exit()


if __name__ == '__main__':
    main()   

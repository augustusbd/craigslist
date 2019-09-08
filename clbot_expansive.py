#! /usr/bin/python3

# Craigslist Bot - Selling Kenneth's Car 

# do not use python-craigslist for selling; buying and scraping posts is focus

from selenium import webdriver
# may need requests and beautifulsoup4
# import requests, bs4


def open_browser(URL):
    ''' 
    URL =     'https://batonrouge.craigslist.org/'
    '''
    browser = webdriver.Firefox()                   # WebDriver
    browser.get(URL)
    # type(browser) = <class 'selenium.webdriver.firefox.webdriver.WebDriver'>
    return browser



def create_post(browser):
    ''' 
    Creates A Post -- Starting The Process
    browser is the controlling WebDriver
    '''
    elem = browser.find_element_by_id('post')       # WebElement
    # type(elem) = <class 'selenium.webdriver.firefox.webelement.FirefoxWebElement'>
    if elem.text == 'create a posting':
        elem.click()
        navigate_options(browser)                                



def navigate_options(browser):
    ''' 
    Goes Through The Process Of Creating A Post
    '''     
    # 1st Step - 'what type of posting is this:'
    try:
        select_1st_option(browser)
    except Exception as err:
        print('Selection of first option went awry. Exception happened: ' + str(err))
    
    if (is_option_selected(browser, value='fso') == True):
        next_step = browser.find_element_by_name('go')
        next_step.click()
    else:
        # retry 1st Step
        
    
    
def select_1st_option(browser):
    options_1 = browser.find_elements_by_name('id') # finds all WebElements with name='id'
                                    # these elements are the options available to choose
    for option in options_1:
        if option.get_attribute('value') == 'fso':  # fso == for sale by owner
            try:
                option.click()                      # site may continue to next page
            except Exception as err:
                print('Went to another page and an exception happened: ' + str(err))
                break
        else:
            continue



def is_option_selected(browser, value):
    options = browser.find_elements_by_name('id')
    for option in options:
        if (option.is_selected() == True) and (option.get_attribute('value') == value):
            return True
        else:
            continue
    return False       
        
        
        
        

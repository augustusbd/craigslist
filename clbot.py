#! /usr/bin/python3

# Craigslist Bot - Selling Kenneth's Car 

# do not use python-craigslist for selling; buying and scraping posts is focus

from selenium import webdriver
# may need requests and beautifulsoup4
# import requests, bs4


def open_browser(URL):
    ''' 
    URL = 'https://batonrouge.craigslist.org/'
    '''
    browser = webdriver.Firefox()                   # type WebDriver
    browser.get(URL)
    
    return browser



def create_post(browser):
    ''' 
    Creates A Post -- Starting The Process
    browser is the controlling WebDriver
    '''
    elem = browser.find_element_by_id('post')       # type WebElement
    if elem.text == 'create a posting':
        elem.click()
        navigate_options(browser)                                



def navigate_options(browser):
    ''' 
    Goes Through The Process Of Creating A Post
    '''     
    # using requests and bs4 can allow the program to know exactly where to go and look
    
    # 1st Step - 'what type of posting is this:'
    select_1st_option(browser)          # browser = select_1st_option(browser)
    
    # 2nd Step - 'please choose a category:'
    select_2nd_option(browser)          # browser = select_2nd_option(browser)
        
    # 3rd Step - fill in details of posting
    fill_out_form(browser)
    
    
    
    
def select_1st_option(browser):
    '''
    1st Step of Create A Post - Choose Type
    '''
    options = browser.find_elements_by_name('id') # finds all WebElements with name='id'
                                    # these elements are the options available to choose
    for option in options:
        if option.get_attribute('value') == 'fso':  # fso == for sale by owner
            try:
                option.click()                      # site may continue to next page
                break
            except Exception as err:
                print('Went to another page and an exception happened: ' + str(err))
                break
        else:
            continue
    #return browser
    
    
     
def select_2nd_option(browser):
    '''
    2nd Step of Create A Post - Choose Category
    '''
    options = browser.find_elements_by_class_name('option-label')
    for option in options:
        if (option.text == 'cars & trucks - by owner'):
            try:
                option.click()
                break
            except Exception as err:
                print('Went to another page and an exception happened: ' + str(err))
                break
    #return browser 

    

def fill_out_form(browser):
    '''
    3rd Step of Create A Post - Create Posting
    '''
    json_inputs = browser.find_elements_by_class_name('json-form-input')
    for info in json_inputs:
        try:
            input_text = input('This input is for ' + info.get_attribute('name') + ': ')
            info.clear()
            info.send_keys(input_text)
        except KeyboardInterrupt:
            raise
        except Exception as err:
            print('An exception occured: ' + str(err))
            break
    

def main():
    URL = 'https://batonrouge.craigslist.org/'
    browser = open_browser(URL)
    
    create_post(browser)
        
    

if __name__ == '__main__':
    main()   
    
    
    
    
    
    
    
    
            
        
        
        

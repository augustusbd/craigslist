#! /usr/bin/python3

# Craigslist Bot  
#    1st Iteration - Selling My Brother's Car 

# do not use python-craigslist for selling; only for buying and scraping posts
# may need requests and beautifulsoup4
# import requests, bs4

import clbot_functions as CLF

    

def main():
    URL = 'https://batonrouge.craigslist.org/'
    
    ans = input("Hello, I'm the Craigslist Bot!\nWould you like to make a post? ")
    affirmative = ('yes','yep', 'ye', 'y', '', 'mhmm', 'oui', 'si')
    if ans in affirmative:
        browser = CLF.open_browser(URL)
        
    else:
        print("I'm sorry, I can only make posts for now. Goodbye!")
        exit()
    
    CLF.create_post(browser)    
        
    # currently, the program stops at Step 3.
    # quitting out of the program when at the end.
    browser.quit()

if __name__ == '__main__':
    main()   
    
    
    
    
    
    
    
    
            
        
        
        

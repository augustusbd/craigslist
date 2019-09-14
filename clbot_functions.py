#! /usr/bin/python3

# Craigslist Bot Functions
from selenium import webdriver


# want create_post to be hub for creating a post
#   which means telling the user which step they are on
#       giving the options available in that step
#           except for the 3rd step - filling in the details
#       choosing the option given by user
#   repeat


def open_browser(URL):
    ''' 
    URL = 'https://batonrouge.craigslist.org/'
            'https://craigslist.org/'
    '''
    browser = webdriver.Firefox()                   # type = WebDriver
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
    
    else:
        print("The 'create a posting' link is not on this page.")
        return None
    
    try:    
        step1(browser)                              # 1st Step - 'what type of posting is this:'
        step2(browser)                              # 2nd Step - 'please choose a category:' 
        step3(browser)                              # 3rd Step - fill in details of posting
    except Exception as err:
        print("An exception occurred: " + str(err))
    
    #try:
        #   navigate_options(browser)  
        #except Exception as err:
        #    print("Went to another page and an exception happened: " + str(err))
    return None



def step1(browser):
    '''
    1st Step of Create A Post - Choose Type
        prints the options for posting types and their values
        then the User inputs a value for posting type desired
        then that option, the user selected value, is selected (clicked on)
    '''
    # Gets the page's form title (with selenium, not bs4)
    form_title = get_title(browser)
    
    # Gets the radio buttons for the options available
    #   with bs4, I can find the input with type="radio"
    options_select = browser.find_elements_by_name('id')
    
    # Gets the text (next to the radio buttons) for the options available. 
    options_text = browser.find_elements_by_class_name('right-side')    # right side of radio button
    
    # Gets the value of the posting type
    posting_type = give_options(browser, 1, form_title, options_select, options_text)
    
    # Selects the chosen option
    select(browser, options_select, posting_type)    # select option associated with value
    return None



def step2(browser):
    '''
    2nd Step of Create A Post - Choose Category
        print the options for category types with their values
        then the User inputs a value for category type desired
        then that option, the user selected value, is selected (clicked on)
    '''
    # this section gets the page's form title (with selenium, not bs4)
    form_title = get_title(browser)
    
    # Gets the radio buttons for the options available
    #   with bs4, I can find the input with type="radio"
    options_select = browser.find_elements_by_name('id')

    # Gets the text (next to the radio buttons) for the options available. 
    options_text = browser.find_elements_by_class_name('option-label')    # radio button label

    # Gets the value of the category type
    category_type = give_options(browser, 2, form_title, options_select, options_text)
    
    # Selects the chosen option
    select(browser, options_select, category_type)    # select option associated with value
    return None
    
    #input("Enter anyting to continue: ")



def step3(browser):
    '''
    3rd Step of Create A Post - Create Posting
        Filling in the details
        these stay the same: (create a GUI? popup for this so User can edit without trouble)
            posting title
            price
            city or neighborhood
            postal code
            description
        
    '''


    input("Enter anything to continue.")





def get_title(browser):
    '''
    Returns a string value of the page's form title. 
    '''
    page_info = browser.find_element_by_class_name('formnote')
    for pos in range(len(page_info.text)):
        if page_info.text[pos] != ':':
            pass
        else:
            break
    title = page_info.text[:pos]
    return title


def give_options(browser, step_num, step_name, options_select, options_text):
    '''
    Goes through options and lists them for user to choose from.
     prints the following:
        Step (1/2/3): Page's Form Title
        Here are your options: (to choose an option, input its value when prompted)
            - Option 1, with a value of: 'value'
            - Option 2, with a value of: 'value'
            - etc....
    '''
    value = None
    
    print("Step " + str(step_num) + ":", end=' ')
    print(step_name + "?")
    print("Here are your options: (to choose an option, input its value when prompted)")
    for pos in range(len(options_text)):
        option = options_text[pos]
        option_value = options_select[pos].get_attribute('value') 
        print("\t- " + option.text + ", with a value of: " + option_value + "\n")
    
    # STEP 1 - Posting Type value = fso     
    if step_num == 1:
        print("Currently, only the 'for sale by owner' works.")
        value = input("Enter the posting option value: ")   # User enters posting type value
        if value != 'fso':
            print("Only 'for sale by owner' (value='fso') works. You inputted '" + value + "'.")
            value = 'fso'
            print("Changed the input to 'fso'")
            
    # STEP 2 - Category Type value = 145    
    if step_num == 2:
        print("Currently, only the 'cars & trucks - by owner' works.")
        value = input("Enter the category option value: ")  # User enters category type value
        if value != '145':
            print("Only 'cars & trucks - by owner' (value='145') works.", end=' ')
            print("You inputted '" + value + "'.")
            value = '145'
            print("Changed the input to '145'")
        
    return value
    
    

def select(browser, options, option_type):
    '''
    1st Step of Create A Post - Choose Type
        Selection of Type
            options = radio button WebElements
            option_type = value of radio button
    '''
    for option in options:
        if option.get_attribute('value') == option_type:  
            # 1st step: posting type, fso == for sale by owner
            # 2nd step: 
            break
        else:
            continue
    option.click()
    return None





# OTHER FUNCTIONS --- CHANGING THEM TO BE MORE GENERIC

def navigate_options(browser):
    ''' 
    Goes Through The Process Of Creating A Post
    # using requests and bs4 can allow the program to know exactly where to go and look
    '''         
    select_1st_option(browser)                  # 1st Step - 'what type of posting is this:' 
    select_2nd_option(browser)                  # 2nd Step - 'please choose a category:'
    fill_out_form(browser)                      # 3rd Step - fill in details of posting
    return None    

def select_2nd_option(browser):
    '''
    2nd Step of Create A Post - Choose Category
    '''
    options = browser.find_elements_by_class_name('option-label')
    for option in options:
        if (option.text == 'cars & trucks - by owner'):
            option.click()
            break           
    return None
 
def fill_out_form(browser):
    '''
    3rd Step of Create A Post - Create Posting
    '''
    json_inputs = browser.find_elements_by_class_name('json-form-input')
    for info in json_inputs:
        input_text = input("This input is for " + info.get_attribute('name') + ": ")
        
        if info.get_attribute('name') != 'language':
            info.clear()                                # for name="language",field cannot be cleared
        try:
            info.clear()                
            info.send_keys(input_text)
        except KeyboardInterrupt:
            raise
        except Exception as err:
            print("An exception occured: " + str(err))
            break    
    

#! /usr/bin/python3

# Craigslist Bot 
# Functions for Mechanical Soup 
import mechanicalsoup
import re
import clbot_GUI as GUI
from PyQt5.QtWidgets import (QDialog, QApplication)
import sys




            ####################### MECHANICAL SOUP ############################

def open(URL):
    """ New StatefulBroser object - open URL """
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    return browser


def create_post(browser):
    """ Create Post -- Hub for Steps """
    browser.follow_link(id='post')
    try:
        step1(browser)
        step2(browser)
        step3(browser)
    except Exception as err:
        print("An exception occurred: " + str(err)) 

def submit(browser):
    """
    Submits the current page's form.
        goes to button with 'continue' text if applicable
    """
    cont_text = ['continue','Continue','CONTINUE','submit','Submit','SUBMIT']
    button = browser.get_current_page().find('button')
    if type(button) == type(None):
        print("A button tag was not found.")
        form = browser.select_form()
        browser.submit_selected()
        
    else:
        while button.text not in cont_text:
            if type(button.find_next('button')) == type(None):
                print("No more buttons. Meaning no continue on this page. Better luck next time.")
                break
            else:
                button = button.find_next('button')
        form = browser.select_form()
        form.choose_submit(button)
        browser.submit_selected()                   # prompts a follow_link (new page) as well
    


def step1(browser):
    """
    Step 1 - Choose Type of Posting
        job offered, gig offered, resume/job wanted, housing offered,
        housing wanted, for sale by owner, for sale by dealer,
        wanted by owner, wanted by dealer, service offered,
        community, event/class
    """
    form = browser.select_form()
    data = {'id':'fso'}                     # {name:value, name:value, ...}
    form.set_radio(data)                # check radio button with value='fso' 
    browser.submit_selected()           # submit form         



def step2(browser):
    """
    Step 2 - Choose A Category
    """
    form_label = 'label[class="json-form-item select id category-select variant-radio"]'
    form = browser.select_form(form_label)
    soup = browser.get_current_page()                       # returns a beautiful soup object
    options = soup.find_all('input', "json-form-input id")  # radio buttons (tags)
    option_labels = soup.find_all('span', "option-label")   # radio button labels
    category = 'User chosen category; "cars & trucks - by owner" for now.'
    cate = 'cars'
    if len(options) == len(option_labels):
        for x in range(len(options)):
            if cate in option_labels[x].text:           # finds label with text containing 'cars'
                radio_tag = str(options[x]).split('"')       
                radio_value = radio_tag[-2]             # value of radio_tag is second from the end
                data = {'id':radio_value}               # radio_value = 145
                form.set_radio(data)
                break
        # can check radio tag string
        # for type="radio"
        # then determine how to select value
    submit(browser)


def step3(browser):
    """ Step 3 - Create Posting - Enter Details """
    soup = browser.get_current_page()
    form = browser.select_form()

    #window = createGUI(soup)
    enter = input('Enter anything to continue')
    
    #lang = {'language':'5'}
    #form.set_select(lang)       # select 'en' (value='5') within name="language"
    
    # search for check boxes later
    # checkboxes = soup.find_all(type="checkbox")
    


############################################## GUI ##################################################
# GUI CREATION:
#   Step 1:
#       call createGUI() function
#   Step 2:
#       
#   Step 3:


def createGUI(soup):
    """
    Create a GUI for the tags with input forms
        Make the GeneralDetails Inputs
        Make the Grouping Widgets
            Group tags with same names
    Returns a Widget object
    """
    fields = soup.find_all('fieldset')
    legends = soup.find_all('legend')
    groupings = []
    # MAIN WINDOW CREATED HERE
    app = QApplication([])
    post = GUI.PostWidget()             # create GeneralDetails Widget
    post.show()
    # create Widget Groupings
    for field in fields:                        
        groupings.append(GroupTags(field))          # list of dictionarys for each grouping
    for x,legend in enumerate(legends):
        grouping_name = capitalize(legend.string)       # get grouping text
        group_window = GUI.GroupWidget()                # widget for extra iformation
        group_window.throwin_info(groupings[x], legend.string)
        group_window.show()
        #post.createGroup(groupings[x], legend.string)      # add roup to main window
        break
    #return grouping  # returns a list of dictionaries; each field (grouping) having its own dict
    
    sys.exit(app.exec_())
    return app
    
    
def capitalize(string1):
    for x in range(len(string1)):
        if (x == 0) or (string1[x-1] == ' '):
            string1 = string1[:x] + string1[x].upper() + string1[x+1:]            


def GroupTags(field):
    """
    Create a Group Widget from field (tags)
        for tags with a class containing "json-form-input"
    Return a dictionary of tag names with their respective tags    
    """
    tags = []
    tag_dict = {}
    tag_names = ['input', 'select', 'textarea']
    for name in tag_names:
        tags.append(field.find_all(name, class_=re.compile("json-form-input")))
    tags = remove_emptys(tags)
    tag_names = return_groups(tags)
    for index,key in enumerate(tag_names):  
        tag_dict[key] = tags[index]
    return tag_dict



def remove_emptys(list1):
    """ Return a list without any empty indexes."""
    new_list = []
    for x in range(len(list1)):
        if len(list1[x]) != 0:
            new_list.append(list1[x])
    return new_list
        
    
def return_groups(tags):
    """ Print Groups and Return a list of tag names"""
    names = []
    #print("These are the groupings inside this field: ")
    for x in range(len(tags)):
        #print("\tThis is the grouping for " + tags[x][0].name + " tags: ")
        names.append(tags[x][0].name)
        for y in range(len(tags[x])):
            name = tags[x][y].get_attribute_list('name')[0]
            #print("\t\t " + name)
    return names
    


                     ########################## Drop Down List #########################
# Selects Options in DropDown   
def select_opt(browser):
    soup = browser.get_current_page()
    form = browser.select_form()
    select_tags = soup.find_all('select')        # 11 on Create Posting
    tag_inputs = dropdown(select_tags)
    print(tag_inputs)
    
    
    
def dropdown(tags):
    """
    Returns a dictionary {tag_name-attribute:real_value, ...}
        for ex: {'language':'2', 'condition':'10', ...}
            # 'language':'2'    refers to 'ca'
            # 'condition':'10'  refers to 'new'

     give_dropdown_options(tag):
        prints options          # for ex: 'language' options are: 'af','ca','da','de','en'
        return user's input     # for ex: user_input = 'en' for english
        
     get_values(tag):
        creates a dictionary of a tag's options:  string to values 
            # for ex: {'ca':'2', 'en':'5',...}
        return dictionary of option strings and values
     
     tag_dict[tag_name] = real_values[user_input] 
        # {'language':'5', 'condition':'10',...
    """
    tag_dict = {}
    real_values = {}
    for tag in tags:
        try:
            tag_name = tag.get_attribute_list('name')[0]
            user_input = give_dropdown_options(tag)
            print("Chosen option for " + tag_name + "is: " + user_input)
            real_values = get_values(tag)                   # gives real values for available dropdown
                                                              # options, e.g. 'en' has a value of '5'
            tag_dict[tag_name] = real_values[user_input]    # throw in user_input as key to get 
                                                              # real value as above ^
        except KeyboardInterrupt:
            print("Interupted!")
            print("Continue with return, please.")
            break
        except Exception as err:
            print("Exception occured: " + str(err))
    return tag_dict

def give_dropdown_options(tag):
    """
    Prints dropdown options
    Return the user's input for drop down options
    """
    undesirable = ['\n','-']
    list_ = []
    print("These are your options for: " + tag.get_attribute_list('name')[0])
    for child in tag.children:
        if child.string not in undesirable:
            list_.append(child.string)
    for y in range(len(list_)):
        print("\t"+ list_[y])
    ans = input("Enter the desired option: ")
    #if len(ans) != 2:              # this is for the language dropdown options
        #ans = ans[:2]
    return ans

### get value from select options
def get_values(tag):
    """
    Returns a dictionary {option_string:option_value, ...}
        {'ca':'2', 'af':'1'
    """
    undesirable = ['\n','-']
    list_ = []
    dict_ = {}
    for content in tag.contents:
        if content not in undesirable:
            if '-' not in content:
                list_.append(content)
    for x in range(len(list_)):
        dict_[list_[x].string] = list_[x].get_attribute_list('value')[0]
    return dict_



###########################################################################################
############################    Functions With Comments    ################################

def _step3(browser):
    """
    Step 3 - Create Posting - Enter Details
    """
    soup = browser.get_current_page()
    form = browser.select_form()
    
    tags = soup.find_all(class_=re.compile("json-form-input"))  # tags that information to input
    input_list, text_list, select_list = step3_sort_tags(tags)

    # Create GUI from these lists
    #   already have grouping for general inputs:
    #       Posting Title, Price, City or Neighborhood, Postal Code, Description
        
    #   look at <fieldset> tags for groupings
    #       then within fieldset grouping,
    #       group the tags with others that have the same tag.name
    #   ex:
    #       fieldset = posting details
    #           inputs = VIN, odometer, make and model
    #           select = language, condition, fuel, model year
    #               if special type, such as 'checkbox'
    #               then group these exclusive from other select tags
    
    fields = soup.find_all('fieldset')
    window = createGUI(soup)
    # select 'en' within name="language"
    lang = {'language':'5'}
    form.set_select(lang)
    
    # search for check boxes later
    # checkboxes = soup.find_all(type="checkbox")


def _createGUI(soup):
    """
    Create a GUI for the tags with input forms
        Make the GeneralDetails Inputs
        Make the Grouping Widgets
            Group tags with same names
    Returns a Widget object
    """
    groupings = []
    fields = soup.find_all('fieldset')
    # MAIN WINDOW CREATED HERE
    app = QApplication([])
    post = GUI.PostWidget()             # create GeneralDetails Widget
    # create Widget Groupings
    for field in fields:                        # for each fieldset tag, make a Group Widget
        groupings.append(GroupTags(field))  # add dictionary to list
        # the main indexes of groupings, e.g. groupings[0], groupings[1], and so on.
        #   are the dictionary themselves
        #   to access information inside dictionary, enter command like this:
        #     groupings[0]['select'] (first field accessing key 'select' to get list of select tags)
        #     groupings[1]['input']  (second field accessing key 'input' to get list of input tags)
    return groupings  # returns a list of dictionaries; each field (grouping) having its own dict


def _GroupTags(field):
    """
    Create a Group Widget from field (tags)
        for tags with a class containing "json-form-input"
    """
    tag_dict = group_tags(field)        # dictionary of tags; 
    return tag_dict


def _group_tags(field):
    tags = []
    tag_dict = {}
    tag_names = ['input', 'select', 'textarea']
    for name in tag_names:
        tags.append(field.find_all(name, class_=re.compile("json-form-input")))
        # each index of tags, has a list with tags named one of these:
        #   input
        #   select
        #   textarea
    tags = remove_emptys(tags)                  # remove empty indexes in list
    tag_names = print_groups(tags)              # gives index for tag_names
    # creates dictionary of tag names and their respective tags
    for index,key in enumerate(tag_names):  
        tag_dict[key] = tags[index]
        # {'tag name': [list of tags with 'tag name'], ... }
        # ex:   {'input':[<input class="json-form-input"... />, ..., <input ... />],
        #       'select': [<select class="json-form-input"...>, ... </select>] }
    return tag_dict


def _remove_emptys(list1):
    new_list = []
    for x in range(len(list1)):
        if len(list1[x]) != 0:
            new_list.append(list1[x])
    return new_list



def _print_groups(tags):
    """
    Print the following:
        This is the grouping for 'input' tags: 
            auto_vin
            ...
        This is the grouping for 'select' tags:
            language
            ...
    Returns a list with the tag name groups
        names = ['input','select']
        # giving the index of that tag's groupings
    """
    names = []
    print("These are the groupings inside this field: ")
    for x in range(len(tags)):
        print("\tThis is the grouping for " + tags[x][0].name + " tags: ")
        names.append(tags[x][0].name)                   # tag name; e.g. <input>
        for y in range(len(tags[x])):
            name = tags[x][y].get_attribute_list('name')[0] # tag attribute 'name='
            print("\t\t " + name)
    return names

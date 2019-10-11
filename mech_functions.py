#! /usr/bin/python3

# Craigslist Bot 
# Functions for Mechanical Soup 
import mechanicalsoup
import clbot_GUI as GUI
import re, sys, threading
from bs4 import BeautifulSoup


            ####################### MECHANICAL SOUP ############################
def create_a_post_process():
    """
    The process of the mechanicalsoup implementation of 'Create A Post'.

    Step 1: Choose Type of Posting
    Step 2: Choose A Category
    Step 3: Create Posting - Enter Details 
    Step 4: Add Map - Adding Location to Post
    Step 5: Add Images
    Step 6: Unpublished Draft of Posting
        - ask user if they want to edit:
            # post
            # location
            # images
        - or finish and publish draft
    Step 7: ? email phase
    To Do: 
        - add GUI functionality. 
        - add a way to save data. 
        - add a way for bot to access email. 
        - continue to edit functions. 
    """
    help(create_a_post_process)
    return None

# quick create_post
def create_posting():
    """Quick Way to go to 'create a post' on craigslist site."""
    URL = "https://batonrouge.craigslist.org/"
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    browser.follow_link(id='post')
    return browser

def open(URL):
    """New StatefulBroser object - open URL."""
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    return browser

def create_a_post(browser):
    """Hub for 'Create A Post' Process."""
    browser.follow_link(id='post')            # follow link for 'create a post'
    try:
        choose_type_of_posting(browser)
        choose_category(browser)
        add_details(browser)
        add_location(browser)
        add_images(browser)
        edit_draft_of_posting(browser)
    except Exception as err:
        print("An exception occurred: " + str(err)) 

# submit page using 'continue' button
def submit(browser):
    """
    Submits the current page's form.
    
    Looks for a button 'continue' text, if applicable, and uses that button for submission.
    """
    button = find_button_with_type(browser, 'submit')
    form = browser.select_form()

    if type(button) != type(None):          # a button was found.
        form.choose_submit(button)
    
    browser.submit_selected()       # prompts a follow_link (new page) as well
    return None


# quick walkthrough
def steps1_5(browser):
    """Quick Way to move through steps while debugging."""
    try:
        print("Step 1 - Choose Type of Posting")
        choose_type_of_posting(browser)

        print("Step 2 - Choose A Category")
        choose_category(browser)

        print("Step 3 - Create Posting - Enter Details")
        add_gaming_details(browser)

        print("Step 4 - Add Map - Adding Location to Post")
        add_location(browser)

        print("Step 5 - Add Images")
        add_images(browser)

        browser.launch_browser()
    except Eception as err:
        print("An exception occurred: " + str(err))

# step 1
def choose_type_of_posting(browser):
    """
    Step 1 - Choose Type of Posting.

    posting types: job offered, gig offered, resume/job wanted, 
        housing offered, housing wanted, for sale by owner, for sale by dealer,
        wanted by owner, wanted by dealer, service offered, community, event/class
    """
    form = browser.select_form()
    user_input = select_from_radio_options(browser)    # dictionary = {name_attr:value}
    form.set_radio(user_input)                    # check radio button with value chosen by user
    submit(browser)                    # submit form    

# step 2
def choose_category(browser):
    """
    Step 2 - Choose Category.

    Given a choice of 'for sale by owner' from Step 1, select the option with:
        'cars & trucks'
        'video gaming'  - currently using this
    """
    form = browser.select_form()
    user_input = select_from_radio_options(browser)    # dictionary = {name_attr:value}
    form.set_radio(user_input)
    submit(browser)

# step 3
def add_details(browser):
    """
    Step 3 - Create Posting - Enter Details.
    
    General Required Information:
        Posting Title (name attribute='PostingTitle'):
        Postal Code ('postal'):
        Description ('PostingBody'):
        email ('FromEMail'):
    """
    form = browser.select_form()

    user_inputs = input_values_for_add_details(browser) # dictionary of tag name attributes and values(= user inputs)
    set_user_inputs(form, user_inputs)          # sets the user inputs into browser
    
    # have to choose a privacy option for email 
    email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
    form.set_radio(email_privacy)

    submit(browser)
    # search for check boxes later
    # checkboxes = soup.find_all(type="checkbox")
    if details_have_missing_information(browser):
        input_missing_details(browser)


# step 4
def add_location(browser):
    """
    Step 4 - Add Map - Adding Location to Post.
    
    If the zip code (postal code) is not entered then ask for address.
    The address is then inputted into the browser.
    """
    soup = browser.get_current_page()
    form = browser.select_form()

    find = soup.find('button', id='search_button')        # button for finding location
    location_inputs = soup.find_all('input', type=False)
    if location_is_set(location_inputs) is False:
        # if zip code does not have a value: ask for address
        location_tag_dict = get_user_inputs_for(location_inputs)
        set_inputs(form, location_tag_dict) 

    form.choose_submit(find)
    browser.submit_selected()

# step 5
def add_images(browser):
    """
    Step 5 - Add Images.
        # look up how to use PyQt to upload images or drag and drop files

    User is able to upload a total of 24 maximum images.
    Upload the best image first - it will be featured. 
    """
    soup = browser.get_current_page()

    confirmed = ask_for_confirmation("Would you like to add images? ")
    image_count = 0
    if confirmed:
        add_images_until_limit_or_done(browser, button)

    # continues on to next step
    #form = browser.select_form('form',2)        # third form on page; 'done with images'
    button = soup.find('button', attrs={'class':'done bigbutton'})  # finish with uploading images
    form = browser.select_form(button.parent)
    form.choose_submit(button)
    browser.submit_selected()


# step 6    
def edit_draft_of_posting(browser):
    """
    Step 6 - Unpublished Draft of Posting.
    
    During this step, the webpage gives the following information:
        gives user the option to edit:
            - post
            - location
            - images
        shows the draft
        publish button
    User is able to choose between editing and publishing draft
    """
    soup = browser.get_current_page()
    forms = soup.find_all('form')
    edit_ans = input("Would you like to edit: post, location, or images? ")
    edit_ans_list = edit_ans.lower().split()
    negative_ans = ['no','nah','nope','n', 'non', 'n0']
    # if user answers in the negative, program continues and publishes the draft.
    if any(x for x in negative_ans if x in edit_ans):
        print("No Edits? Okay. Publishing the draft now.")
        button = soup.find('button', attrs={'value':'Continue'})
        # publishes the post
        # email gets sent to given email address
    else:
        if any(x for x in edit_ans_list if 'post' in x):
            # edit post
            button = soup.find('button', attrs={'value':'Edit Post'})
            print(button.text)
        elif any(x for x in edit_ans_list if 'location' in x):
            # edit location
            button = soup.find('button', attrs={'value':'Edit Location'})
            print(button.text)
        elif any(x for x in edit_ans_list if 'images' in x):
            button = soup.find('button', attrs={'value':'Edit Images'})
            print(button.text)
    form = browser.select_form(button.parent)
    form.choose_submit(button)
    browser.submit_selected()
    goto_step(browser, button.text)

# editing other pages (details, location, images)
def goto_step(browser, text):
    """
    Takes the user back to different steps depending on editing choice.

    Depending on text given, this function will call:
        add_details
        add_location
        add_images
    After the step function is called, edit_draft_of_posting is called again
        going back to the draft, to ask the user 
        if they would like to edit anything else
    # Edit step functions to allow users to edit the available information
    """
    if text == 'edit post':
        add_details(browser)
        edit_draft_of_posting(browser)
    elif text == 'edit location':
        add_location(browser)
        edit_draft_of_posting(browser)
    elif text == 'edit images':
        add_images(browser)
        edit_draft_of_posting(browser)
    else:
        # not editing post, location or images
        # page was already submitted so do nothing
        print("Further Action Required To Complete Request")
        print("You should receive an email shortly, with a link to:")
        print("\t- publish your ad")
        print("\t- edit (or confirm an edit to) your ad")
        print("\t- verify your email address")
        print("\t- delete your ad")


################################## GENERAL FUNCTIONS ######################################
def print_name_attrs(tags):
    for tag in tags:
        print(tag.get_attribute_list('name'))

def find_button_with_type(browser, text):
    """Find button with text given. 
    The text will be the filter for the type attribute."""
    soup = browser.get_current_page()
    button = soup.find('button', type=text)
    if type(button) == type(None):
        print("A button tag with attribute type " + text + " does not exist.")
    return button

def find_button_with_text(browser, text):
    """Find button that has the given text."""
    button = browser.get_current_page().find('button')
    if type(button) == type(None):
        print("A button tag was not found.")
        return None

    text_variations = different_versions_of_string(text)    # different variations of text
    while (button.text not in text_variations):             
        if type(button.find_next('button')) == type(None):  # next button does not exist.
            print("There are no buttons with text='" + text + "' on this page.")
            return None
        else:
            button = button.find_next('button')             # otherwise, keeping searching
    return button

def find_button_with_keyword(**kwargs):
    """Find a button that has the given keyword."""
    print(len(kwargs))
    # delete the keywords that aren't provided as arguments
    # for key in kwags,items():
    soup = browser.get_current_page()

    for key,value  in kwargs.items():
        if key == 'type':
            button = soup.find('button',type=value)
            return button

        elif key == 'name':
            button = soup.find('button',attrs={'name':value})
            return button

        elif key == 'value':
            button = soup.find('button',attrs={'value':value})
            return button

        elif key=='id':
            button = soup.find('button',id=value)
            return button

    button = browser.get_current_page().find('button')
    return button

    # learn how to use this instead of a bunch of if statements
    name_value = kwargs.pop('name','')
    type_value = kwargs.pop('type','')
    value_value = kwargs.pop('value','')
    id_value = kwargs.pop('id', None)
    print(name_value, type_value, value_value, id_value)

def ask_for_confirmation(text):
    """Ask a user if they would like to do something or not. Returns True or False."""
    affirmative = ['yes','ya','ye','y','oui','si','mhm','mmhmm', '']
    answer = input(text)
    if answer in affirmative:
        return True
    else:
        return False

#### string functions #####
def put_strings_together_from_list(a_list):
    """
    Return a string comprised from list indices. List must be comprised of strings.
    """
    text = ""
    if is_every_index_a_string(a_list):
        for value in a_list:
            text = text + value + " "
        text = remove_whitespace_at_either_end(text)
        return text
    else:
        print("This list contains an element that is not a string.")
        confirmed = ask_for_confirmation("Would you like to keep the first element? ")
        if confirmed:
            return a_list[0]
        else:
            return a_list

def is_every_index_a_string(a_list):
    """
    Returns True if every element in a_list is a string. Otherwise returns False.
    """
    for item in a_list:
        if type(item) != str:
            return False
    return True

def capitalize_each_word2(text):
    # mutates the given string.
    for x in range(len(text)):
        if (x == 0) or (text[x-1] == ' '):
            text = text[:x] + text[x].upper() + text[x+1:]

def capitalize_each_word(text):
    new_string = ""
    for word in text.split():
        new_string = new_string + word.capitalize() + " "
    new_string = remove_whitespace_at_either_end(new_string)
    return new_string


def remove_non_space_whitespace(text):
    """Takes out whitespace that isn't a space ' '."""
    whitespace = ['\n','\t','\r','\x0b','\x0c']
    if type(text) != str:
        print("Argument is not a string.")    
    else:
        while has_non_space_whitespace(text):
            for x in whitespace:
                text_index = text.find(x)
                if text_index != -1:
                    text = text[:text_index] + text[text_index+1:]
    return text

def has_non_space_whitespace(text):
    """Returns True if text has non-space whitespace."""
    whitespace = ['\n','\t','\r','\x0b','\x0c']
    for x in whitespace:
        if x in text:
            return True
    return False

def remove_whitespace_at_either_end(text):
    """Takes out whitespace at the start and end of a text."""
    whitespace = ['\n','\t',' ']
    if type(text) != str:
        print("Argument is not a string.")
    else:
        while starts_or_ends_with_whitespace(text):
            for x in whitespace:
                if text.startswith(x):
                    text = text[1:]
                if text.endswith(x):
                    text = text[:-1]
    return text

def starts_or_ends_with_whitespace(text):
    """Returns True if text starts or ends with whitespace."""
    whitespace = ['\n','\t',' ','\r','\x0b','\x0c']
    for x in whitespace:
        if text.startswith(x):
            return True
        elif text.endswith(x):
            return True
    return False

# string variation
def different_versions_of(item):
    """Returns a list containing the different versions of a data type.
    Most notably a string."""
    if type(item) == str:
        return different_versions_of_string(text)
    else:
        print("Only able to provide different versions of a string type.")
        return item

def different_versions_of_string(text):
    """Returns a list containing the different versions of a string.

    ex: text = 'continue'
        'continue' can be written as 'Continue', 'CONTINUE', 'cont.', 'CONT.'
    """
    string_list = [text, text.upper(), text.capitalize()]
    return string_list


#### list functions ####
def remove_empty_indexes(list1):
    """Return a list without any empty indexes."""
    new_list = []
    for x in range(len(list1)):
        if len(list1[x]) != 0:
            new_list.append(list1[x])
    return new_list

#### soup.find_all() filter functions ####
# filter functions
def not_radio(type_):
    return type_ and not type_ == 'radio'

def not_hidden(type_):
    return type_ and not type_ == 'hidden'

def is_radio_checkbox_or_tel(type_):
    types = ['radio','checkbox','tel']
    return (type_ in types)

def not_unwanted_type(type_):
    # 'tel' is for telephone numbers
    unwanted_types = ['radio','checkbox','hidden','tel']
    return type_ and not (type_ in unwanted_types)

def type_is_text_or_number(type_):
    types = ['text','number']
    return type_ in types

def input_tags_not_in_fieldset(tag):
    """Returns a input tag that is not within a fieldset tag."""
    return tag.name == 'input' and not within_fieldset(tag)

def textarea_tags_not_in_fieldset(tag):
    """Returns a textarea tag that is not within a fieldset tag."""
    return tag.name == 'textarea' and not within_fieldset(tag)

def select_tags_not_in_fieldset(tag):
    """Returns a select tag that is not within a fieldset tag."""
    return tag.name == 'select' and not within_fieldset(tag)

def within_fieldset(tag):
    """Returns True if the tag is within a fieldset tag. Otherwise returns False."""
    for parent in tag.parents:
        if parent is None:
            return False
        elif parent.name == 'fieldset':
            return True

def select_from_radio_options(browser):
    """
    Gives the user the current page's radio buttons and the text accompanying them.

    The radio buttons and the text are both within span tags.
    The radio buttons within span tags with class="left-side",
    and the text within span tags with class="right-side".

    Asks for user's input to choose a specific radio button.

    Returns a dictionary with a name attribute as key and a value determined by user.
        ex: return {name_attr:value}
            name_attr = 'id'
            value = 'res'
    """
    soup = browser.get_current_page()
    span_left = soup.find_all('span',class_="left-side")    # contains radio buttons
    span_right = soup.find_all('span',class_="right-side")  # contains text for radio buttons

    radio_buttons = tags_within_list_of_tags(span_left) # list of input tags with type='radio'
    labels = text_from_tags(span_right)                   # list of text describing radio buttons

    button_list = list(zip(radio_buttons,labels))   # list of radio butons and the text accompanying them

    user_input = select_radio_option(button_list)

    return user_input

def select_radio_option(a_list):
    """Print the text assocaited with a tag and the tag's value attribute.
    Each index of a_list is a tuple containing the tag and the text associated with it. 
        ex: a_list = [(tag,text), (tag,text)]

    Return the user's input
    """
    print("These are the options for the categories (marked with **): ")
    for item in a_list:
        value = item[0].get_attribute_list('value') # value for radio button
        value = put_strings_together_from_list(value)    # related to label of same index
        print("\t*" + item[1] + "*\t\twith a value of: " + value)

    user_input = input("Enter the text or the value associated with it: ")
    user_input = determine_user_input_for_radio_button(user_input, a_list)

    return user_input

def determine_user_input_for_radio_button(user_input, tag_list):
    """Determines what the user input indicates. 
    
    user_input = 'some string'
    tag_list = list of tags.
        ex: tag_list = [(tag, text), (tag,text)]

    Given a list of tags and the user's input,
    determine if the user input is the actual value of a tag,
    or the user input is, in some form, the text associated with a tag.    
    """
    name_attr = tag_list[0][0].get_attribute_list('name')   # name attribute of radio button
    name_attr = put_strings_together_from_list(name_attr)

    if len(user_input) < 4:
        # user inputted value instead of text
        # all input radio values are less than 4 characters and are lowercase
        return {name_attr:user_input.lower()}

    for item in tag_list:
        if user_input.lower() in item[1].lower():
            value = item[0].get_attribute_list('value')
            value = put_strings_together_from_list(value)
            return {name_attr:value}

    print("Inputted value does not refer to anything.")
    # not the best return
    return {}           # form.set_radio() uses a dictionary as its argument


# STEP 1 - Choose Type of Posting - FUNCTIONS
def text_from_tags(tags):
    """Returns a list of strings containing text for options."""
    text_list = []
    for tag in tags:
        text = remove_whitespace_at_either_end(tag.text)
        text = remove_non_space_whitespace(text)
        text_list.append(text)
    return text_list

def tags_within_list_of_tags(tags):
    """
    Returns a list of tags.

    From a given list of tags, 
    find the children of each tag:
        if the child is a tag,
        then add it to list.
    """
    tag_list = []
    for tag in tags:
        for child in tag.children:
            if type(child) == type(tags[0]):
                tag_list.append(child)
    return tag_list

# STEP 3 - Add Details - FUNCTIONS
# dictionary from list of tags
def dict_of_name_attributes_and_values_from(tags):
    """
    Returns a dictionary containing tag name attributes (attrs) and their values.

    tags = list of tags with the same tag name.
    Depending on name of tags (i.e. <input>, <select>):
        a different function is called to return a dictionary from the given list of tags.
        If the names of the tags are select (i.e. <select>):
            dict_of_select_options() is called on the list
        else:
            dict_of_general_inputs()
    """
    if len(tags) == 0:
        print("The given list is empty.")
        return {}

    print("\t\tThese are **" + tags[0].name + "** tags.")
    if tags[0].name == 'select':
        return dict_of_select_options(tags)
    else:
        return dict_of_general_inputs(tags)

def dict_of_general_inputs(tags):
    """
    Returns a dictionary containing the name attributes of tags and their values.

    Given a list of tags, tags:
        Find the name attribute of a tag
        Find the value of the tag.
        Add the name attribute and value to the dictionary (tag_dict)
    ex: tag_dict = {'name':value, 'name':value}
    """
    tag_dict = {}
    for tag in tags:
        name = tag.get_attribute_list('name')
        name = put_strings_together_from_list(name)

        value = tag.get_attribute_list('value')
        if type(value[0]) == type(None):        # tag does not have 'value' attribute
            tag_dict[name] = ""
        else:
            value = put_strings_together_from_list(value)
            tag_dict[name] = value
    return tag_dict

def dict_of_select_options(tags):
    """
    Returns a dictionary of dictionaries.

    Given a list of tags.
    The main dictionary contains the tags' name attributes (as keys) and their values = their choices.
    the values are a dictionary themselves, containing the choices and their actual value in the tag. 
        ex: returns {tag_name_attr:{choices}, tag_name:choices}
            # dictionary of options and their 'actual' values (for selecting them)
            choices = {'choice1':'value1', 'choice2':'value2'}  
    """
    tag_dict = {}
    for tag in tags:
        choices = {}
        name = tag.get_attribute_list('name')
        name = put_strings_together_from_list(name)
        for child in tag.children:
            if (str(type(child)) == "<class 'bs4.element.Tag'>") and (child.string != '\n'):
                value = child.get_attribute_list('value')        # actual value for given option
                value = put_strings_together_from_list(value)    # (child.string = option)
                choices[child.string] = value
        tag_dict[name] = choices
    return tag_dict

# user inputs
def tag_dict_of_user_inputs(tag_dict):
    """Returns a dictionary containing user inputs for tags."""
    if len(tag_dict) == 0:
        print("The given dictionary is empty.")
        return {}

    name = list(tag_dict)[0]        # the first key of the given dictionary (tag_dict)
    if type(tag_dict[name]) == type({}):     
        # if the value is a dictionary then it holds options for a select tag.
        return dict_of_user_inputs_for_select_tags(tag_dict)
    else:
        return dict_of_user_inputs_for_general_inputs(tag_dict)

def dict_of_user_inputs_for_general_inputs(tag_dict):
    """
    Return a dictionary containing the user inputted values.
    
    tag_dict = {'name_attr':value, 'name_attr':value}
    Given a dictionary of tag name attributes and their values (tag_dict),
        if a value is not empty (""), 
            then the user has the opporunity to keep the value or enter a new one.
        if a value is empty,
            then the user enters a value for themselves (can be empty, unless stated)
    user_dict = {'name_attr':'user_input', 'name_attr':'user_input'}
    Returns a dictionary of tag name attributes and the user's inputs as values. 
    """
    user_dict = {}
    for name in tag_dict:
        if tag_dict[name] != "":    # name attribute already has a value associated with it
            text = "This tag already has a value of '" + str(tag_dict[name]) + "' for " + name
            text = text + ". Would you like to keep it? "
            confirmed = ask_for_confirmation(text)
            if confirmed:                         # user wants to keep value already there
                user_dict[name] = tag_dict[name]
            else:
                user_dict[name] = input("Enter info for " + name + ": ")
        else:
            user_dict[name] = input("Enter info for " + name + ": ")
    return user_dict

def dict_of_user_inputs_for_select_tags(tag_dict):
    """
    Returns a dictionary containing the user selected values.
    
    tag_dict = {tag_name_attr:choices, tag_name:options}
        option = {'option1':'value1', 'option2':'value2'}
    Given a dictionary, tag_dict, of tag name attributes and their options,
    the options dictionary gives the actual value of the chosen option.
    
    ex: return user_dict = {'name_attr':'value','name_attr':'value'}
    """
    user_dict = {}
    for name in tag_dict:
        print("\tOptions for " + name + ": ")
        select_options = tag_dict[name]             # dictionary of options
        for option in select_options:               # lists the options for a given select tag
            print("\t" + option)
        user_input = input("Enter the desired option: ")
        for key in select_options:          # if the user input matches one of the keys (option text)
            if user_input in key:               # then make the user input equal to the option text
                user_input = key
                break
        user_dict[name] = tag_dict[name][user_input]          # the actual value of user input
    return user_dict

# inputting user info
def set_user_inputs(form, user_dict):
    """Sets the values, given from user_dict, inside form."""
    print("Inputting the values.")
    for name in user_dict:
        form.set(name, user_dict[name])

# gives user the inputs on current browser page.
# user is then able to input values.
def input_values_for_add_details(browser):
    """
    Returns a dictionary with name attribute as key and value determined by user.
    """
    soup = browser.get_current_page()
    fields = soup.find_all('fieldset')
    legends = []                        # legend tags give name for fieldset tags

    # find input, textarea, and select tags outside fieldset tags
    # (including input tags with radio/checkbox/hidden type)
    class_value = re.compile("json-form-input")
    inputs = soup.find_all(input_tags_not_in_fieldset,class_=class_value)
    description = soup.find(textarea_tags_not_in_fieldset,class_=class_value)
    selects = soup.find_all(select_tags_not_in_fieldset,class_=class_value)

    # put the list of tags into a dictionary of tag name attributes and their values.
    print("\t\tTHESE ARE THE INPUTS OUTSIDE OF A FIELDSET TAG")
    user_inputs = get_user_inputs_for(inputs + [description])
    user_inputs.update(get_user_inputs_for(selects))

    # fieldset inputs
    print("\t\tTHESE ARE THE INPUTS INSIDE THE FIELDSET TAGS")
    for field in fields:
        field_soup = BeautifulSoup(str(field))
        user_inputs.update(get_fieldset_user_inputs_for(field_soup))
        legends.append(field_soup.select_one('legend'))
    return user_inputs

# get the user inputs for the tags
def get_user_inputs_for(tags):
    """
    Returns a dictionary containing the tag name attributes and user's inputted values for those tags.
    """
    dict_inputs = dict_of_name_attributes_and_values_from(tags)
    user_input_dict = tag_dict_of_user_inputs(dict_inputs)    # user inputs info for tags
    return user_input_dict

# get the user inputs for the tags inside a fieldset tag.
def get_fieldset_user_inputs_for(field_soup):
    """
    Returns a dictionary containing the tag name attributes and user's inputted values for those tags.
    """
    inputs = field_soup.select('fieldset input')
    selects = field_soup.select('fieldset select')
    user_inputs = {}
    if len(inputs) != 0:
        user_inputs.update(get_user_inputs_for(inputs))
    if len(selects) != 0:
        user_inputs.update(get_user_inputs_for(selects))
    return user_inputs

def add_job_details(browser):
    form = browser.select_form()
    info_input = {'PostingTitle':'Selling', 'postal':70808, 'FromEMail':'email@protonmail.com'}
    info_checkbox = {'resumes_available_morning':'1'}
    info_select = {'education_level_completed':'5'}
    description = {'PostingBody':'Selling'}
    form.set_input(info_input)
    form.set_textarea(description)
    form.set_select(info_select)
    form.set_checkbox(info_checkbox)
    # have to choose a privacy option for email 
    email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
    form.set_radio(email_privacy)
    m.submit(browser)

def add_gaming_details(browser):
    """Subsitute for Step 3 - Quick Information Input."""
    form = browser.select_form()
    info_input = {'PostingTitle':'Selling PS4', 'price':200, 'postal':70808, 'FromEMail':'email@protonmail.com'}
    description = {'PostingBody':'Selling PS4 for $200'}
    info_select = {'language':'5', 'condition':'10'}

    form.set_input(info_input)
    form.set_textarea(description)
    form.set_select(info_select)
    submit(browser)

def details_have_missing_information(browser):
    """
    Checks that the required details were entered. 

    Returns False for no missing information. 
    Returns True for missing information.
    """
    soup = browser.get_current_page()
    highlight_error =  soup.find('div', class_="highlight")
    if type(highlight_error) == type(None):
        return False
    for child in highlight_error.children:
        if type(child) == type(highlight_error):
            print(child.text)
    return True


# STEP 4 - Add Location - FUNCTIONS
def location_is_set(ilist):
    """ 
    Returns True or False depending on existence of postal code.

        ilist = list of inputs
    Returns True
        if zip code (postal code) is already entered
    Returns False
        if zip code is not entered
    """
    name_attrs = ['city','geographic','area','street']
    for item in ilist:
        name = item.get_attribute_list('name')[0].lower()
        if any(x for x in name_attrs if x in name):
            value = item.get_attribute_list('value')[0]
            if value not in ['', None]:
                return True
    return False


# STEP 5 - Add Images - FUNCIONS
def form_without_class(forms_list):
    """ 
    Step 5 Function - Find Form Tag Without A Class. 

    Form tag needed for selecting button, does not have a class/
    Other form tags have classes with values: 'add' and 'delete ajax'.
    
    Returns a form tag.
    """
    for num,form in enumerate(forms_list):
        if form.get_attribute_list('class')[0] == None:
            return form                 # returns form with no class
    return form

def determine_tag_within(tag, tag_name, distinction):
    """
    Finds the tag that fits within the given parameters.

    CURRENTLY DOES NOT WORK; does not really find the tag.
    Given a tag containing other tags, desired tag name and distinction.
        a distinction being: type="whatever", name="tagname"
        a distinction will be put into a dictionary called attrs (attributes)
    Return a tag fitting the description.
    """
    attrs = distinction.split(" ")
    # should take the string before the '=' as the key
    # and the string after the '=' as the value.
    for child in tag.children:
        if type(child) == type(tag):
            if child.name == tag_name:
                for key in attrs:
                    if child.get_attribute_list(key)[0] == attrs[key]:
                        return child
            #if child.get_attribute_list('type')

def add_images_until_limit_or_done(browser, button):
    """Add images until limit is reached or user is done uploading images."""
    img_count = browser.get_current_page().find('span',class_="imgcount")   # tag containing image count limit
    limit = int(img_count.text)
    print("Upload the best image first - it will be featured.")
    button = soup.find('button', class_="addbtn")    # button for adding images to form
    while confirmed and limit > 0:
        limit -= 1
        add_file(browser, button)        # add image (file) to browser using button
        confirmed = ask_for_confirmation("Would you like to add another image? ")

def add_file(browser, button):
    """
    Adds a file to a form.
    
    Given a browser and its button associated with the submission of a file.
    Find the form that the button is held in and find the input tag with type="file".
    Once the input tag is found, use the form to set the value to the file path.
    """
    path_to_file = input("Copy and Paste the file location: ")
    form = browser.select_form(button.parent)            # select form containing button
    for child in form.children:
        if type(child) == type(button):                    # must be type 'bs4.element.Tag'
            if child.get_attribute_list('type')[0] == 'file':        # tag must have type attribute = 'file'
                    # gets the name attribute of tag, in a list
                    name_attribute = child.get_attribute_list('name')
                    name_attribute = put_strings_together_from_list(name_attribute)
                    break
    form.set(name_attribute, path_to_file)        # add file to form
    form.choose_submit(button)                    # button for adding files (not submiting whole page)
    browser.submit_selected()
    print("File: " + path_to_file + " has been added.")
    return None


#! /usr/bin/python3

# Craigslist Bot 
# Functions for Mechanical Soup 
import mechanicalsoup
import clbot_GUI as GUI
import re, sys, threading
from PyQt5.QtWidgets import (QDialog, QApplication)


            ####################### MECHANICAL SOUP ############################
def process():
    """
    This is the step by step process of the mechanicalsoup implementation of 'Create A Post'.

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

def create_post(browser):
    """Hub for 'Create A Post' Steps."""
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
    is_button_there = True
    cont_text = ['continue','Continue','CONTINUE','submit','Submit','SUBMIT']
    button = browser.get_current_page().find('button')
    if type(button) == type(None):
        print("A button tag was not found.")
        form = browser.select_form()
        browser.submit_selected()
        
    else:
        # look for button with text signifying next step
        # or look for button with name attribute = 'go'
        while (button.text not in cont_text) or (button.get_attribute_list('name')[0] != 'go'):     
            if type(button.find_next('button')) == type(None):
                print("No more buttons. Meaning no continue on this page. Better luck next time.")
                is_button_there = False
                break
            else:
                button = button.find_next('button')
        if is_button_there:
            form = browser.select_form()
            form.choose_submit(button)
            browser.submit_selected()                   # prompts a follow_link (new page) as well   

# quick walkthrough
def steps1_5(browser):
    """Quick Way to move through steps while testing."""
    try:
        print("Step 1 - Choose Type of Posting")
        choose_type_of_posting(browser)
        print("Step 2 - Choose A Category")
        choose_category(browser)
        print("Step 3 - Create Posting - Enter Details")
        add_needed_details(browser)
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
    soup = browser.get_current_page()
    form = browser.select_form()
    
    user_input = give_radio_options(browser)		# dictionary = {name_attr:value}
    form.set_radio(user_input)					# check radio button with value chosen by user
    browser.submit_selected()					# submit form    

# step 2
def choose_category(browser):
	"""
	Step 2 - Choose Category.

	Given a choice of 'for sale by owner' from Step 1, select the option with:
        'cars & trucks'
        'video gaming'  - currently using this
	"""
	soup = browser.get_current_page()
	form = browser.select_form()
	user_input = give_radio_options(browser)
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
    soup = browser.get_current_page()
    form = browser.select_form()
    inputs = soup.find_all('input',class_=re.compile("json-form-input"),type=not_radio)        # input tags
    description = soup.find('textarea',class_=re.compile("json-form-input"))    # description input
    selects = soup.find_all('select',class_=re.compile("json-form-input"))      # select tags

    # dictionary of input tags(and textarea tag)'s name attributes and values
    dict_inputs = dict_from_list(inputs + [description])    # treating description as part of the inputs
    
    # dictionary of select tags' name attributes and values
    dict_selects = dict_from_list(selects)

    user_ans_dict = user_dict_of_inputs(dict_inputs)       # user inputs info for input tags
    user_ans_dict.update(user_dict_of_inputs(dict_selects))     # user selects an option for select tags
    
    # inputs the information into the browser
    set_user_inputs(form, user_ans_dict)
    # have to choose a privacy option for email
    email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
    form.set_radio(email_privacy)
    
    browser.launch_browser()
    #window = createGUI(soup)
    enter = input('Enter anything to continue')
    submit(browser)
    # search for check boxes later
    # checkboxes = soup.find_all(type="checkbox")
    if check_details_for_error(browser):
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
    if not check_zip(location_inputs):
        # if zip code does not have a value: ask for address
        local_inputs = list_inputs_keep_value(location_inputs)
        local_ans_dict = dict_inputs_keep_value(local_inputs)

        set_inputs(form, local_ans_dict) 
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
    forms = soup.find_all('form')

    ans = ask_for_confirmation("Would you like to add images? ")
    image_count = 0
    if ans:
        print("Upload the best image first - it will be featured.")
        button = soup.find('button', class_="addbtn")    # button for adding images to form
        while ans and image_count < 24:
            add_file(browser, button)            # add image (file) to browser using button
            image_count = image_count + 1            
            ans = ask_for_confirmation("Would you like to add another image? ")

    # continues on to next step
    #form = browser.select_form('form',2)        # third form on page; 'done with images'
    form = browser.select_form(form_without_class(forms))
    button = soup.find('button', attrs={'class':'done bigbutton'})
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


############################################## GUI ##################################################
# GUI CREATION:
#   Step 1:
#       call createGUI() function
#   Step 2:
#       
#   Step 3:
def createGUI(soup):
    """
    Create a GUI for the tags with input forms.
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
        grouping_name = capitalize_each_word(legend.string)       # get grouping text
        group_window = GUI.GroupWidget()                # widget for extra iformation
        group_window.throwin_info(groupings[x], legend.string)
        group_window.show()
        #post.createGroup(groupings[x], legend.string)      # add roup to main window
        break
    #return grouping  # returns a list of dictionaries; each field (grouping) having its own dict
    
    sys.exit(app.exec_())
    return app


################################## GENERAL FUNCTIONS ######################################

def capitalize_each_word(string1):
    for x in range(len(string1)):
        if (x == 0) or (string1[x-1] == ' '):
            string1 = string1[:x] + string1[x].upper() + string1[x+1:]

def capitalize_each_word2(a_string):
    new_string = ""
    for word in a_string.split():
        new_string = new_string + word + " "
    return new_string

def GroupTags(field):
    """
    Create a Group Widget from field (tags).
        for tags with a class containing "json-form-input"
    Return a dictionary of tag names with their respective tags    
    """
    tags = []
    tag_dict = {}
    tag_names = ['input', 'select', 'textarea']
    for name in tag_names:
        tags.append(field.find_all(name, class_=re.compile("json-form-input")))
    tags = remove_empty_indexes(tags)
    tag_names = return_groups(tags)
    for index,key in enumerate(tag_names):  
        tag_dict[key] = tags[index]
    return tag_dict

def remove_empty_indexes(list1):
    """Return a list without any empty indexes."""
    new_list = []
    for x in range(len(list1)):
        if len(list1[x]) != 0:
            new_list.append(list1[x])
    return new_list
    
def return_groups(tags):
    """Returns a list of tag names."""
    names = []
    #print("These are the groupings inside this field: ")
    for x in range(len(tags)):
        #print("\tThis is the grouping for " + tags[x][0].name + " tags: ")
        names.append(tags[x][0].name)
        for y in range(len(tags[x])):
            name = tags[x][y].get_attribute_list('name')[0]
            #print("\t\t " + name)
    return names

def give_radio_options(browser):
	"""
	Returns a dictionary with a name attribute as key and a value determined by user.
		ex: return {name_attr:value}
			name_attr = 'id'
			value = 'res'
	"""
	soup = browser.get_current_page()
    span_left = soup.find_all('span',class_="left-side") # contains radio buttons for options
    span_right = soup.find_all('span',class_="right-side")	# contains tags that have text for options

    options = tags_within_list_of_tags(span_left)    # list of radio button tags 
    labels = labels_of_tags(span_right)            # list of text describing options

    name_attr = options[0].get_attribute_list('name')		# name attribute of radio button
    name_attr = put_strings_together_from_list(name_attr)

    print("These are the options for the categories (marked with **): ")
    for x in range(len(options)):
    	value = options[x].get_attribute_list('value') # value for radio button
        value = put_strings_together_from_list(value)	# related to label of same index
        print("\t*" + labels[x] + "*\t\twith a value of: " + value)
    user_ans = input("Enter either the type of posting or the value: ")

    if len(user_ans) < 4:
    	# user inputted value instead of label
    	# all values are less than 4 characters
        return {name_attr:user_ans}
    else:
        for label in labels:
            if user_ans.lower() in label:
                label_index = labels.index(label)
                value = options[label_index].get_attribute_list('value')
                value = put_strings_together_from_list(value)
                return {name_attr:value}
        print("Inputted value does not refer to anything.")
    # not the best return
    return {name_attr:user_ans}

# STEP 1 - Choose Type of Posting - FUNCTIONS
def labels_of_tags(tags):
    """Returns a list of strings containing text for options."""
    text_list = []
    for tag in tags:
        text = take_out_whitespace_at_start_and_end(tag.text)
        text = take_out_non_space_whitespace(text)
        text_list.append(text)
    return text_list

def tags_within_list_of_tags(tags):
    """
    Returns a list of tags.

    From a given list of tags, 
    find the children of each tag and if the child is a tag,
    then add it to list.
    """
    tag_list = []
    for tag in tags:
        for child in tag.children:
            if type(child) == type(tags[0]):
                tag_list.append(child)
    return tag_list

def take_out_non_space_whitespace(text):
    """Takes out whitespace that isn't a space ' '."""
    whitespace = ['\n','\t','\r','\x0b','\x0c']
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

def take_out_whitespace_at_start_and_end(text):
    """Takes out whitespace at the start and end of a text."""
    whitespace = ['\n','\t',' ']
    while starts_or_ends_with_whitespace(text)
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

# STEP 3 - Add Details - FUNCTIONS
    # dictionary from list of tags
def dict_from_list(tags):
    """
    Returns a dictionary containing tag name attributes (attrs) and their values.

    tags = list of tags with the same tag name.
    Depending on name of tags (i.e. <input>, <select>):
        a different function is called to return a dictionary from the given list of tags.
        If the names of the tags are select (i.e. <select>):
            dict_of_select_options() is called on the list
        else:
            dict_of_tag_name_attrs_and_values()
    """
    print("These are *" + tags[0].name + "* tags.")
    if tags[0].name == 'select':
        return dict_of_select_options(tags)
    else:
        return dict_of_tag_name_attrs_and_values(tags)

def dict_of_tag_name_attrs_and_values(tags):
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
def user_dict_of_inputs(tag_dict):
    """Returns a dictionary containing user inputs for tags."""
    name = list(tag_dict)[0]        # the value of the given dictionary (tag_dict)
    if type(tag_dict[name]) == type({}):     # if the value is a dictionary then it holds options for a select tag.
        return dict_of_user_select_values(tag_dict)
    else:
        return dict_of_user_values(tag_dict)

def dict_of_user_values(tag_dict):
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
            ans = ask_for_confirmation(text)
            if ans:                         # user wants to keep value already there
                user_dict[name] = tag_dict[name]
            else:
                user_dict[name] = input("Enter info for " + name + ": ")
        else:
            user_dict[name] = input("Enter info for " + name + ": ")
    return user_dict

def dict_of_user_select_values(tag_dict):
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
        print("Options for " + name + ": ")
        select_options = tag_dict[name]             # dictionary of options
        for option in select_options:               # lists the options for a given select tag
            print("\t" + option)
        user_ans = input("Enter the desired option: ")
        user_dict[name] = tag_dict[name][user_ans]          # the actual value of user input
    return user_dict

    # inputting user info
def set_user_inputs(form, user_dict):
    """Sets the values, given from user_dict, inside form."""
    print("Inputting the values.")
    for name in user_dict:
        form.set(name, user_dict[name])

def not_radio(type_):
    return type_ and not type_ == 'radio'

def not_hidden(type_):
    return type_ and not type_ == 'hidden'

def add_needed_details(browser):
    """Subsitute for Step 3 - Quick Information Input."""
    form = browser.select_form()
    info_input = {'PostingTitle':'Selling PS4', 'price':200, 'postal':70808, 'FromEMail':'email@protonmail.com'}
    description = {'PostingBody':'Selling PS4 for $200'}
    info_select = {'language':'5', 'condition':'10'}
    form.set_input(info_input)
    form.set_textarea(description)
    form.set_select(info_select)
    submit(browser)

def check_details_for_error(browser):
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
def check_zip(ilist):
    """ 
    Returns True or False depending on existence of postal code.

        ilist = list of inputs
    Returns True
        if zip code (postal code) is already entered
    Returns False
        if zip code is not entered
    """
    for item in ilist:
        if item.get_attribute_list('name')[0] == 'postal':
            if item.get_attribute_list('value')[0] != "":
                return True
    return False

def list_inputs_keep_value(ilist):
    """
    Returns a list of input tags and their name attributes.

        ilist = ResulSet of input tags
    Create a list that contains input tags:
        [(tag, {tag_name_attr:value}), (tag, {tag_name:value})]
    Returns a list containing: tags and dictionary of name_attribute and value.
    """
    input_list = []
    for item in ilist:
        name = item.get_attribute_list('name')[0]
        value = item.get_attribute_list('value')
        if value[0] != None:
            value_string = put_strings_together_from_list(value)
            input_list.append([item, {name:value_string}])
        else:
            input_list.append([item, {name:""}])
    return input_list

def dict_inputs_keep_value(ilist):
    """
    Returns a dictionary of input tags' name attributes and their values.

    ilist = list of inputs containing tags and dictionaries
        [(tag, {tag_name:value}), (tag, {tag_name:value})]
    Return a dictionary with values for inputs based on attribue name
        {name:ans, name:value}
    """
    print("These are the location inputs.")
    input_ans_dict = {}
    for item in ilist:
        name = list(item[1])[0]
        if item[1][name] == "":
            input_ans_dict[name] = input("Enter info for " + name + ": ")
        else:
            input_ans_dict[name] = item[1][name]
    return input_ans_dict

def put_strings_together_from_list(a_list):
    """
    Return a string comprised from list indices. List must be comprised of strings.
    """
    text = ""
    if is_every_index_a_string(a_list):
        for value in a_list:
            text = text + value + " "
        text = remove_trailing_whitespace(text)
        return text
    else:
        print("This list contains an element that is not a string.")
        ans = ask_for_confirmation("Would you like to keep the first element? ")
        if ans:
            return a_list[0]
        else:
            return a_list

def remove_trailing_whitespace(a_string):
    """
    Remove trailing whitespace in a string.
    """
    if type(a_string) != str:
        print("Argument is not a string.")
        return a_string
    elif a_string.endswith(" "):
        a_string = a_string[:-1]
    return a_string

def is_every_index_a_string(a_list):
    """
    Returns True if every element in a_list is a string. Otherwise returns False.
    """
    for item in a_list:
        if type(item) != str:
            return False
    return True

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

def ask_for_confirmation(text):
    """Ask a user if they would like to do something or not. Returns True or False."""
    affirmative = ['yes','ya','ye','y','oui','si','mhm','mmhmm']
    answer = input(text)
    if answer in affirmative:
        return True
    else:
        return False

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

def add_file(browser, button):
    """
    Adds a file to a form.
    
    Given a browser and its button associated with the submission of a file.
    Find the form that the button is held in and find the input tag with type="file".
    Once the input tag is found, use the form to set the value to the file path.
    """
    path_to_file = input("Copy and Paste the file location.")
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
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
    browser.follow_link(id='post')
    try:
        Step1(browser)
        Step2(browser)
        Step3(browser)
        Step4(browser)
        Step5(browser)
        Step6(browser)
    except Exception as err:
        print("An exception occurred: " + str(err)) 

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

def steps1_5(browser):
    """Quick Way to move through steps while testing."""
    try:
        print("Step 1 - Choose Type of Posting")
        Step1(browser)
        print("Step 2 - Choose A Category")
        Step2(browser)
        print("Step 3 - Create Posting - Enter Details")
        Step3_enter_needed_info(browser)
        print("Step 4 - Add Map - Adding Location to Post")
        Step4(browser)
        print("Step 5 - Add Images")
        Step5(browser)
        browser.launch_browser()
    except Eception as err:
        print("An exception occurred: " + str(err))

def Step1(browser):
    """
    Step 1 - Choose Type of Posting.

    posting types: job offered, gig offered, resume/job wanted, 
        housing offered, housing wanted, for sale by owner, for sale by dealer,
        wanted by owner, wanted by dealer, service offered, community, event/class
    """
    form = browser.select_form()
    data = {'id':'fso'}                     # {name:value, name:value, ...}
    form.set_radio(data)                # check radio button with value='fso' 
    browser.submit_selected()           # submit form         


def Step2(browser):
    """
    Step 2 - Choose A Category.
    
    Given a choice of 'for sale by owner' from Step 1, select the option with:
        'cars & trucks'
        'video gaming'  - currently using this
    """
    form_label = 'label[class="json-form-item select id category-select variant-radio"]'
    form = browser.select_form(form_label)
    soup = browser.get_current_page()                       # returns a beautiful soup object
    options = soup.find_all('input', "json-form-input id")  # radio buttons (tags)
    option_labels = soup.find_all('span', "option-label")   # radio button labels
    category = 'User chosen category; "cars & trucks - by owner" for now.'
    cate = 'gaming'
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


def Step3(browser):
    """Step 3 - Create Posting - Enter Details."""
    soup = browser.get_current_page()
    form = browser.select_form()
    inputs = soup.find_all('input',class_=re.compile("json-form-input"),type=not_radio)        # input tags
    description = soup.find('textarea',class_=re.compile("json-form-input"))    # description input
    selects = soup.find_all('select',class_=re.compile("json-form-input"))      # select tags
    # create a list that contains input tags:
        # [(tag, {tag_name_attr:value}), (tag, {tag_name:value})]
    input_list = list_inputs(inputs + [description])    # treating description as part of the inputs
    
    # create a list that contains select tags and their options:
        # [(tag, {tag_name_attr:choices}, {choice1:value1, choice2:value2}), 
        #  (tag, {tag_name:choices}, {choice1:value1, choice2:value2})]       
    select_list = list_selects(selects)
    input_ans_dict = dict_inputs(input_list)        # user inputs info for input tags
    select_ans_dict = dict_selects(select_list)     # user inputs info for select tags
    # inputs the information into the browser
    set_inputs(form, input_ans_dict)
    set_selects(form, select_ans_dict)
    # have to choose a privacy option for email
    email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
    form.set_radio(email_privacy)
    
    browser.launch_browser()
    #window = createGUI(soup)
    enter = input('Enter anything to continue')
    submit(browser)
    # search for check boxes later
    # checkboxes = soup.find_all(type="checkbox")
    

def Step4(browser):
    """
    Step 4 - Add Map - Adding Location to Post.
    
    If the zip code (postal code) is not entered then ask for address.
    The address is then inputted into the browser.
    """
    soup = browser.get_current_page()
    form = browser.select_form()
    find = soup.find('button', id='search_button')		# button for finding location
    location_inputs = soup.find_all('input', type=False)
    if not check_zip(location_inputs):
        # if zip code does not have a value: ask for address
        local_inputs = list_inputs_keep_value(location_inputs)
        local_ans_dict = dict_inputs_keep_value(local_inputs)

        set_inputs(form, local_ans_dict) 
    form.choose_submit(find)
    browser.submit_selected()

    
def Step5(browser):
    """
    Step 5 - Add Images.
        # look up how to use PyQt to upload images or drap and drop files
    """
    soup = browser.get_current_page()
    forms = soup.find_all('form')

    ans = ask_for_confirmation("Would you like to add images? ")
    if ans:
    	button = soup.find('button', class_="addbtn")	# button for adding images to form
    	while ans:
    		add_file(browser, button)					# add file to browser using button
    		ans = ask_for_confirmation("Would you like to add another image? ")

    # continues on to next step
    #form = browser.select_form('form',2)        # third form on page; done with images
    form = browser.select_form(form_no_class(forms))
    button = soup.find('button', attrs={'class':'done bigbutton'})
    form.choose_submit(button)
    browser.submit_selected()


def Step6(browser):
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


def goto_step(browser, text):
    """
    Takes the user back to different steps depending on editing choice.

    Depending on text given, this function will call:
        Step3
        Step4
        Step5
    After the step function is called, Step6 is called again
        going back to the draft, to ask the user 
        if they would like to edit anything else
    # Edit step functions to allow users to edit the available information
    """
    if text == 'edit post':
        Step3(browser)
        Step6(browser)
    elif text == 'edit location':
        Step4(browser)
        Step6(browser)
    elif text == 'edit images':
        Step5(browser)
        Step6(browser)
    else:
        # not editing post, location or imags
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

def capitalize_each_word2(string_):
    new_string = ""
    for word in string_.split():
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

# STEP 3 - FUNCTIONS
def list_inputs(ilist):
    """
    Returns a list of input tags and their name attributes.

        ilist = ResulSet of input tags
    Create a list that contains input tags:
        [(tag, {tag_name_attr:value}), (tag, {tag_name:value})]
    """
    input_list = []
    value = ''
    for item in ilist:
        name = item.get_attribute_list('name')[0]
        input_list.append([item, {name:""}])
    return input_list
    
def dict_inputs(ilist):
    """
    Returns a dictionary of input tags' name attributes and their values.

        ilist = list of inputs
    Returns a dictionary with values for inputs based on attribute name
        {name:ans, name:value, name:value}
    """
    print("These are the input tags.")
    input_ans_dict = {}
    for item in ilist:
        name = list(item[1])[0]
        ans = input("Enter info for " + name + ": ")
        input_ans_dict[name] = ans
    return input_ans_dict

def set_inputs(form, idict):
    """
    Sets the input tag value for the tag with name attribute 'key'.
    Special case for inputting the description, which is a textarea tag.
        name attribute of this textarea tag = "PostingBody"
    """
    print("Inputting in the values.")
    for key in idict:
        if key != 'PostingBody':
            dict_input = {key:idict[key]}
            form.set_input(dict_input)
        else:
            dict_input = {key:idict[key]}
            form.set_textarea(dict_input)

def list_selects(slist):
    """
    Returns a list of select tags with their name attributes.

    # create a list that contains select tags and their options:
    # [(tag, {tag_name_attr:choices}, {choice1:value1, choice2:value2}), 
    #  (tag, {tag_name:choices}, {choice1:value1, choice2:value2})]
    # 1st position == tag itself
    # 2nd position == dictionary of tag attribute name:choices
    # 3rd position == dictionary of choices and their actual value
    """
    select_list = []
    for item in slist:
        choices = []
        dict_choices = {}
        for child in item.children:
            if child.string != '\n':
                choices.append(child.string)
            if str(type(child)) == "<class 'bs4.element.Tag'>":
                value = child.get_attribute_list('value')[0]            
                dict_choices[child.string] = value
        name = item.get_attribute_list('name')[0]
        select_list.append([item, {name:choices}, dict_choices])
    return select_list

def dict_selects(slist):
    """
    Returns a dictionary of select tags' name attributes and their values.

    slist - list of: select tags, their name attributes, and their choices
        ex: [(tag, {tag_name_attr:choices}, {choice1:value1, choice2:value2}), 
            (tag, {tag_name:choices}, {choice1:value1, choice2:value2})]
            # within an index of slist:
                # 1st position == tag itself
                # 2nd position == dictionary of tag attribute name:choices
                # 3rd position == dictionary of choices and their actual value
        
    Returns a dictionary with values for select tags
    """
    print("These are the select tags and their options.")
    select_ans_dict = {}
    for item in slist:
        name = list(item[1])[0]     # gets key values of dictionary as a list
        print("Options for " + name + ": ")
        select_options = item[1][name]
        for option in select_options:
            print(option)
        ans = input("Enter the desired option: ")
        actual_value = item[2][ans]
        select_ans_dict[name] = actual_value
    return select_ans_dict

def set_selects(form, sdict):
    """Set the value for select tag with name attribute 'key'."""
    print("Choosing the options.")
    for key in sdict:
        dict_select = {key:sdict[key]}
        form.set_select(dict_select)

def not_radio(type_):
    return type_ and not type_ == 'radio'

def not_hidden(type_):
    return type_ and not type_ == 'hidden'

def Step3_enter_needed_info(browser):
    """Subsitute for Step 3 - Quick Information Input."""
    form = browser.select_form()
    info_input = {'PostingTitle':'Selling PS4', 'price':200, 'postal':70808, 'FromEMail':'emailtimenow@protonmail.com'}
    description = {'PostingBody':'Selling PS4 for $200'}
    info_select = {'language':'5', 'condition':'10'}
    form.set_input(info_input)
    form.set_textarea(description)
    form.set_select(info_select)
    submit(browser)

# STEP 4 - FUNCTIONS
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
            value_string = remove_trailing_whitespace(value_string)
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
            ans = input("Enter info for " + name + ": ")
            input_ans_dict[name] = ans
        else:
            input_ans_dict[name] = item[1][name]
    return input_ans_dict

def put_strings_together_from_list(list_):
    """Return a string comprised from list indices. List must be comprised of strings."""
    text = ""
    for string_ in list_:
        text = text + string_ + " "
    return text

def remove_trailing_whitespace(string_):
    """Removes trailing whitespace in a string."""
    if string_.endswith(" "):
        string_ = string_[:-1]
    return string_

# STEP 5 - FUNCIONS
def form_no_class(forms_list):
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
	affirmative = ['yes','ya','ye','oui','si', 'mhm', 'mmhmm']
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

	Return a tag fitting the description."""
	attrs = distinction.split(" ")
	# should take the string before the '=' as the key
	# and the string after the '=' as the value.
	for child in tag.children:
		if type(child) == type(tag):
			if child.name = tag_name:
				for key in attrs:
					if child.get_attribute_list(key)[0] == attrs[key]:
						return child
			if child.get_attribute_list('type')

def add_file(browser, button):
	"""
	Adds a file to a form.
	
	Given a browser and its button associated with the submission of a file.
	Find the form that the button is held in and find the input tag with type="file".
	Once the input tag is found, use the form to set the value to the file path.
	"""
	path_to_file = input("Copy and Paste the file location.")
	form = browser.select_form(button.parent)			# select form containing button
	for child in form.children:
		if type(child) == type(button):					# must be type 'bs4.element.Tag'
			if child.get_attribute_list('type')[0] == 'file':		# tag must have type attribute = 'file'
					# gets the name attribute of tag, in a list
					name_attribute = child.get_attribute_list('name')
					name_attribute = remove_trailing_whitespace(put_strings_together_from_list(name_attribute))
					break
	form.set(name_attribute, path_to_file)		# add file to form
	form.choose_submit(button)					# button for adding files (not submiting whole page)
	browser.submit_selected()
	print("File: " + path_to_file + " has been added.")
	return None


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

def _Step3(browser):
    """ 
    Step 3 - Create Posting - Enter Details 
    """
    soup = browser.get_current_page()
    form = browser.select_form()
    inputs = soup.find_all('input',class_=re.compile("json-form-input"),type=not_radio)        # input tags
    description = soup.find('textarea',class_=re.compile("json-form-input"))    # description input
    selects = soup.find_all('select',class_=re.compile("json-form-input"))      # select tags
    # create a list that contains input tags:
        # [(tag, {tag_name_attr:value}), (tag, {tag_name:value})]
    # list of inputs
    input_list = list_inputs(inputs + [description])    # treating description as part of the inputs

    ##### ADD MULTITHREADING #####
    # create a list that contains select tags and their options:
        # [(tag, {tag_name_attr:choices}, {choice1:value1, choice2:value2}), 
        #  (tag, {tag_name:choices}, {choice1:value1, choice2:value2})]        
    # list of selects:
    select_list = list_selects(selects)

    # start a new thread for multiprocessing
    # once input answers are given, program can begin to input the text
        # and continue to ask for inputs for select tags
    input_ans_dict = dict_inputs(input_list)        # user inputs info for input tags

    # start a new thread for multiprocessing
    select_ans_dict = dict_selects(select_list)     # user inputs info for select tags
    
    # set the input tag value for the tag with name attribute 'key'
    set_inputs(form, input_ans_dict)
    set_selects(form, select_ans_dict)
    
    # have to choose a privacy option for email
    email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
    form.set_radio(email_privacy)
    
    browser.launch_browser()
    #window = createGUI(soup)
    enter = input('Enter anything to continue')
    submit(browser)
    #lang = {'language':'5'}
    #form.set_select(lang)       # select 'en' (value='5') within name="language"
    
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
    tags = remove_empty_indexes(tags)                  # remove empty indexes in list
    tag_names = print_groups(tags)              # gives index for tag_names
    # creates dictionary of tag names and their respective tags
    for index,key in enumerate(tag_names):  
        tag_dict[key] = tags[index]
        # {'tag name': [list of tags with 'tag name'], ... }
        # ex:   {'input':[<input class="json-form-input"... />, ..., <input ... />],
        #       'select': [<select class="json-form-input"...>, ... </select>] }
    return tag_dict

def _remove_empty_indexes(list1):
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
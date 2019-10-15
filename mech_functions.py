#! /usr/bin/python3

# Craigslist Bot 
# Functions for Mechanical Soup 
import mechanicalsoup
import clbot_GUI as GUI
import fields as fs
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
def quick_create_a_post():
    """Quick Way to go to 'create a post' on craigslist site."""
    URL = "https://batonrouge.craigslist.org/"
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    browser.follow_link(id='post')          # follow link for 'create a post'

    return browser

def open(URL):
    """New StatefulBroser object - open URL."""
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    return browser


def create_a_post(browser):
    """Hub for 'Create A Post' Process."""            
    try:
        determine_page(browser)

    except Exception as err:
        print("An exception occurred: " + str(err))
    return None

def determine_page(browser):
    """
    Determines the type of function to call based on title of page. 
    Hard to distiquish between (the same title)
        'add_details_to_post'
        'add_location_to_post'
        'add_images_to_post'
    """
    soup = browser.get_current_page()
    forms = soup.find_all('form')        # length of forms gives a hint towards page
    title_text = soup.title.text

    if 'type' in title_text or 'category' in title_text:
        choose_category(browser)
        determine_page(browser)

    elif 'map' in title_text:
        add_location_to_post(browser)
        determine_page(browser)

    # 'baton rouge | create posting' is included in the below titles
    # length of forms tells us what page the browser is on.
    elif 'posting' in title_text and len(forms) == 1:
        add_details_to_post(browser)
        determine_page(browser)
    
    elif ('posting' in title_text) and (len(forms) == 3):
        add_images_to_post(browser)
        determine_page(browser)

    elif ('posting' in title_text) and (len(forms) == 8):
        edit_draft_of_posting(browser)

    return None

# submit page using 'continue' button
def submit(browser):
    """
    Submits the current page's form.
    
    Looks for a button 'continue' text, if applicable, and uses that button for submission.
    """
    button = find_button_with_type(browser, 'submit')
    form = browser.select_form()

    if button != None:          # a button was found.
        form.choose_submit(button)
    
    browser.submit_selected()       # prompts a follow_link (new page) as well
    return None


# quick walkthrough
def game_post(browser):
    """Quick Way to move through steps while debugging."""
    try:
        choose_type_of_posting_gaming(browser)
        print("Step 1 - Choose Type of Posting")

        choose_category_gaming(browser)
        print("Step 2 - Choose A Category")

    except Exception as err:
        print("An exception occurred: " + str(err))
    return None

def gaming_post(browser):
    """Quick Way to move through steps while debugging."""
    try:
        choose_type_of_posting_gaming(browser)
        print("Step 1 - Choose Type of Posting")

        choose_category_gaming(browser)
        print("Step 2 - Choose A Category")

        add_details_gaming(browser)
        print("Step 3 - Create Posting - Enter Details")

        add_location_to_post(browser)
        print("Step 4 - Add Map - Adding Location to Post")

        add_images_to_post(browser)
        print("Step 5 - Add Images")

        browser.launch_browser()

    except Exception as err:
        print("An exception occurred: " + str(err))
    return None

# step 1 and step 2
# Choose Type of Posting and Choose Category are basically the same
def choose_category(browser):
    """
    Step 1 & 2 - Choose Type of Posting or Choose Category.
    """
    print(browser.get_current_page().title.text)
    form = browser.select_form()
    user_input = select_from_radio_options(browser)    # dictionary = {name_attr:value}
    form.set_radio(user_input)
    submit(browser)
    return None

# step 1
def choose_type_of_posting(browser):
    """
    Step 1 - Choose Type of Posting.

    posting types: job offered, gig offered, resume/job wanted, 
        housing offered, housing wanted, for sale by owner, for sale by dealer,
        wanted by owner, wanted by dealer, service offered, community, event/class
    """
    print(browser.get_current_page().title.text)
    form = browser.select_form()
    user_input = select_from_radio_options(browser)    # dictionary = {name_attr:value}
    form.set_radio(user_input)                    # check radio button with value chosen by user
    submit(browser)                    # submit form    
    return None


# step 2
def choose_category_of_type(browser):
    """
    Step 2 - Choose Category.

    Given a choice of 'for sale by owner' from Step 1, select the option with:
        'cars & trucks'
        'video gaming'  - currently using this
    """
    print(browser.get_current_page().title.text)
    form = browser.select_form()
    user_input = select_from_radio_options(browser)    # dictionary = {name_attr:value}
    form.set_radio(user_input)
    submit(browser)
    return None


# step 3
def add_details_to_post(browser):
    """
    Step 3 - Create Posting - Enter Details.
    
    General Required Information:
        Posting Title (name attribute='PostingTitle'):
        Postal Code ('postal'):
        Description ('PostingBody'):
        email ('FromEMail'):
    """
    form = browser.select_form()

    input_details(browser)
    
    # have to choose a privacy option for email 
    email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
    form.set_radio(email_privacy)

    submit(browser)
    # search for check boxes later
    # checkboxes = soup.find_all(type="checkbox")
    if details_have_missing_information(browser):
        input_missing_details(browser)
    return None


# step 4
def add_location_to_post(browser):
    """
    Step 4 - Add Map - Adding Location to Post.
    
    If the zip code (postal code) is not entered then ask for address.
    The address is then inputted into the browser.
    """
    soup = browser.get_current_page()
    form = browser.select_form()

    find = soup.find('button', id='search_button')        # button for finding location
    location_inputs = soup.find_all('input', type=False)  # inputs for location
    if location_is_set(location_inputs) is False:         # ask for address if not entered
        user_inputs = get_user_inputs_for(location_inputs)  # dictionary of user_inputs
        set_user_inputs(form, user_inputs) 

    form.choose_submit(find)
    browser.submit_selected()
    return None

# step 5
def add_images_to_post(browser):
    """
    Step 5 - Add Images.
        # look up how to use PyQt to upload images or drag and drop files

    User is able to upload a total of 24 maximum images.
    Upload the best image first - it will be featured. 
    """
    confirmed = ask_for_confirmation("Would you like to add images? ")
    if confirmed:
        add_images_until_limit_or_done(browser)

    # continues on to next page 
    #form = browser.select_form('form',2)        # third form on page; 'done with images'
    button = find_button_with_text(browser, 'done with images') # finish with uploading images
    form = browser.select_form(button.parent)
    form.choose_submit(button)
    browser.submit_selected()
    return None

# step 6    
def edit_draft_of_posting(browser):
    """
    Step 6 - Unpublished Draft of Posting.
    
    The webpage gives the following information:
        gives user the option to edit:
            - post
            - location
            - images
        shows unpublished draft
        publish button
    User is able to choose between editing and publishing draft
    """
    soup = browser.get_current_page()
    forms = soup.find_all('form')

    confirmed = ask_for_confirmation("Would you like to edit: post, location, or images? ")
    if confirmed:
        button = get_edit_button(browser)

    else:
        # publishes the post
        # email gets sent to given email address
        print("No Edits? Okay. Publishing the draft now.")
        submit(browser)
        return None

    form = browser.select_form(button.parent)
    form.choose_submit(button)
    browser.submit_selected()
    goto_edit_page(browser, button.text)
    return None


# editing other pages (details, location, images)
def get_edit_button(browser):
    """Return a button that refers to the user's choice."""
    user_input = input("What would you like to edit? Post? Location? Images? Pick One: ")
    if 'post' in user_input:
        button = find_button_with_text(browser, 'edit post')

    elif 'location' in user_input:
        button = find_button_with_text(browser, 'edit location')

    elif 'image' in user_input:
        button = find_button_with_text(browser, 'edit images')

    return button


# FIX THIS UP -- Use determine_page(browser)
def goto_edit_page(browser, text):
    """
    Takes the user back to different steps depending on editing choice.

    Depending on text given, this function will call:
        add_details_to_post
        add_location_to_post
        add_images_to_post
    After the step function is called, edit_draft_of_posting is called again
        going back to the draft, to ask the user 
        if they would like to edit anything else
    # Edit step functions to allow users to edit the available information
    """
    if text == 'edit post':
        add_details_to_post(browser)
        edit_draft_of_posting(browser)

    elif text == 'edit location':
        add_location_to_post(browser)
        edit_draft_of_posting(browser)

    elif text == 'edit images':
        add_images_to_post(browser)
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
    return None


###### Quick Walkthrough ########
def choose_type_of_posting_gaming(browser):
    """
    Step 1 - Choose Type of Posting - for sale by owner
    """
    form = browser.select_form()
    user_input = {'id':'fso'}
    form.set_radio(user_input)
    submit(browser)                    
    return None

def choose_category_gaming(browser):
    """
    Step 2 - Choose Category.

    Given a choice of 'for sale by owner' from Step 1, select the option with:
        'cars & trucks'
        'video gaming'  - currently using this
    """
    form = browser.select_form()
    user_input = {'id':'151'}
    form.set_radio(user_input)
    submit(browser)
    return None

def add_general_details(browser):
    """Subsitute for add_details_to_post - Quick Information Input."""
    form = browser.select_form()
    info_input = {'PostingTitle':'Selling', 'postal':70808, 'FromEMail':'email@protonmail.com'}
    description = {'PostingBody':'Selling'}
    info_select = {'language':'5'}
    email_privacy = {'Privacy':'C'}

    form.set_input(info_input)
    form.set_textarea(description)
    form.set_select(info_select)
    form.set_radio(email_privacy)
    submit(browser)

def add_details_job(browser):
    """Subsitute for add_details_to_post - Quick Information Input."""
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
    submit(browser)

def add_details_gaming(browser):
    """Subsitute for add_details_to_post - Quick Information Input."""
    form = browser.select_form()
    info_input = {'PostingTitle':'Selling PS4', 'price':200, 'postal':70808, 'FromEMail':'email@protonmail.com'}
    description = {'PostingBody':'Selling PS4 for $200'}
    info_select = {'language':'5', 'condition':'10'}

    form.set_input(info_input)
    form.set_textarea(description)
    form.set_select(info_select)
    submit(browser)


################################## GENERAL FUNCTIONS ######################################
def merge_dict(dict1, dict2):
	"""Merge two dictionaries together."""
	res = {**dict1, **dict2}
	return res

def print_name_attrs(tags):
	"""Prints the name attributes of the tags."""
	for tag in tags:
		print(tag.get_attribute_list('name'))

def get_name_attributes(tags):
	"""Returns a list of name attributes from tags."""
	name_list = []
	for tag in tags:
		name = tag.get_attribute_list('name')
		name = put_strings_together_from_list(name)
		name_list.append(name)
	return name_list

def remove_tags_with_name_attributes(tags, exclude_values):
	"""Remove tags from a list of tags using an attribute as a filter.

	The tag with a name attribute that is in exlcude_values,
	will not be added to the new list of tags. 
	
	Returns a list of tags that do not have a name attribute in exlcude_values
	"""
	new_tags = []
	for tag in tags:
		value = tag.get_attribute_list('name')
		value = put_strings_together_from_list(value)
		if value not in exclude_values:
			new_tags.append(tag)
	return new_tags

def remove_tags_with_same_name_attr(tags):
	"""Removes tags that have the same name attribute."""
	new_tags = []
	name_list = get_name_attributes(tags)
	for tag in tags:
		name = tag.get_attribute_list('name')
		name = put_strings_together_from_list(name)
		while name_list.count(name) > 1:	# removes duplicate names
			name_list.remove(name)
		if name in name_list:				# tag has name attribute in name list
			new_tags.append(tag)			# only this tag can be added with this name attribute
			name_list.remove(name)		# remove name from name list 
											# no more tags with the same name can be added
	return new_tags


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
def different_versions_of_string(text):
    """Returns a list containing the different versions of a string.
    ex: text = 'continue'
        'continue' can be written as 'Continue', 'CONTINUE', 'cont.', 'CONT.'
    """
    string_list = [text, text.upper(), text.capitalize(), capitalize_each_word(text)]
    return string_list

# Button Functions - Find 
def find_button_with_type(browser, text):
    """Find button with text given. 
    The text will be the filter for the type attribute."""
    soup = browser.get_current_page()
    button = soup.find('button', type=text)
    if button == None:
        print("A button tag with attribute type " + text + " does not exist.")
    return button

def find_button_with_text(browser, text):
    """Find button that has the given text."""
    button = browser.get_current_page().find('button')
    if button == None:
        print("A button tag was not found.")
        return None

    text_variations = different_versions_of_string(text)    # different variations of text
    while (button.text not in text_variations):             
        if button.find_next('button') == None:  # next button does not exist.
            print("There are no buttons with text='" + text + "' on this page.")
            return None
        else:
            button = button.find_next('button')             # otherwise, keeping searching
    return button

def ask_for_confirmation(text):
    """Ask a user if they would like to do something or not. Returns True or False."""
    affirmative = ['yes','ya','ye','y','oui','si','mhm','mmhmm', '']
    answer = input(text)
    if answer in affirmative:
        return True
    else:
        return False

#### soup.find_all() filter functions ####
# filter functions
def fieldset_not_within_fieldset(tag):
	"""Returns tag if it is a fieldset tag not within a fieldset tag."""
	if tag.name == "fieldset":
		if tag.find_parent('fieldset') == None:
			return tag

def not_hidden(a_type):
	"""Returns a type that is not equal to hidden."""
	return a_type != "hidden"


################################## STEP FUNCTIONS ######################################
# STEP 1 - Choose Type of Posting - FUNCTIONS
def text_from_tags(tags):
    """Returns a list of strings containing text for options."""
    text_list = []
    for tag in tags:
        text = remove_whitespace_at_either_end(tag.text)
        text = remove_non_space_whitespace(text)
        text_list.append(text)
    return text_list

# Step 1 & Step 2 - Selecting Radio Option
def select_from_radio_options(browser):
    """
    Gives the user the current page's radio buttons and the text accompanying them.

    Determine the radio button structure:
        the input radio tags within either:
            label tags
            span tags
        return a list containing tags and text accompanying them
            ex: [(tag, text), (tag, text)]

    Asks for user's input to choose a specific radio button.

    Returns a dictionary with a name attribute as key and a value determined by user.
        ex: return {name_attr:value}
            name_attr = 'id'
            value = 'res'
    """
    tags_and_text = determine_radio_buttons_and_text(browser) # list of tags and text accompanying them
    user_input = select_radio_option_from_list(tags_and_text) # dictionary of user input

    return user_input

def determine_radio_buttons_and_text(browser):
    """Gives the radio button options based on which tags they are in.
    
    Returns a list containing the radio buttons and text describing them.
        ex: buttons_and_text = [(tag, text), (tag, text)]
    """
    soup = browser.get_current_page()
    radio_buttons = soup.find_all('input',type="radio")
    parent = radio_buttons[0].parent
    p_class = parent.get_attribute_list('class')[0]
    name = parent.name
    if name == 'label' and p_class == 'radio-option':
        radio_labels = soup.find_all('span',class_="option-label")    # tags holding text describing radio buttons

    elif name == 'span' and p_class == 'left-side':
        radio_labels = soup.find_all('span',class_="right-side")

    else:
        print("Radio buttons do not lie within label or span tags.")
        return []           # return empty list

    text_of_labels = text_from_tags(radio_labels)     # list of text describing radio buttons
    buttons_and_text = list(zip(radio_buttons, text_of_labels))  # list of radio butons and the text accompanying them
    return buttons_and_text

def select_radio_option_from_list(a_list):
    """Print the text assocaited with a tag and the tag's value attribute.
    Each index of a_list is a tuple containing the tag and the text associated with it. 
        ex: a_list = [(tag,text), (tag,text)]

    Return the user's input as a dictionary.
    """
    if len(a_list) == 0:        # list is empty
        return {}

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
    
    Returns a dictonary of user input.

    user_input = 'some string'
    tag_list = list of tags.
        ex: tag_list = [(tag, text), (tag,text)]

    Given a list of tags and the user's input,
    determine if the user input is the actual value of a tag,
    or the user input is, in some form, the text associated with a tag.    
    """
    name_attr = tag_list[0][0].get_attribute_list('name')   # name attribute of radio button
    name_attr = put_strings_together_from_list(name_attr)

    for item in tag_list:
        value = item[0].get_attribute_list('value')
        value = put_strings_together_from_list(value)
        if (user_input.lower() in item[1].lower()) or (user_input in value):
            return {name_attr:value}

    print("Inputted value does not refer to anything.")
    # not the best return
    return {}           # form.set_radio() uses a dictionary as its argument

# STEP 3 - Add Details - FUNCTIONS
def input_details(browser):
	"""User inputs values for page."""
	soup = browser.get_current_page()

	# input general details (Title, Description, Zip Code, etc.)
	name_attrs = input_general_details(browser)		# list of name attributes

	# input fieldset details ('posting details', 'contact info', 'location info')
	name_attrs = input_fieldset_details(browser, name_attrs)

	# leftover tags are put into their own "custom_fieldset"
		# finds all inputs (type != hidden)
		# (select tags are only within fieldset tags)
	custom_fieldset = soup.find_all('input', type=not_hidden)
	custom_fieldset = remove_tags_with_name_attributes(custom_fieldset, name_attrs)

	# what am I trying to do?

def input_fieldset_details(browser, name_attrs):
	"""User inputs details inside fieldset tags for post.

	Returns a list of name attributes used.
	"""
	form = browser.select_form()
	soup = browser.get_current_page()

	# split tags into their fieldsets
	fieldsets = soup.find_all(fieldset_not_within_fieldset)
	fieldset_objects = fs.create_fieldset_objects(fieldsets, name_attrs)

	for field in fieldset_objects:
		name_attrs = name_attrs + field.return_name_attributes() # name attributes of tags used
		user_inputs = field.input_values()	# user inputs for tags inside fieldset
		user_inputs.update(field.input_other_values())

		set_user_inputs(form, user_inputs)	# sets the user inputs into browser

	return name_attrs

def input_general_details(browser):
	"""User inputs general details for post.
	
	Sets the values for the name attributes with user input.
	Returns a dictionary of name attributes that were used to set a value.
		# not all name attributes will be on page
	"""
	form = browser.select_form()
	soup = browser.get_current_page()

	# tag name attributes
	name_attributes = ['PostingTitle', 'price','GeographicArea',
	'postal','FromEMail','PostingBody']
	name_attrs_used = []		# actual list of name attributes used

	for name in name_attributes:
		tag = soup.find(attrs={'name':name})
		if tag != None:							# found a tag with name_attribute=name
			name_attrs_used.append(name)		# adds name attribute to list
			text = find_parent_sibling_text(tag)	# returns string or None

			if text != None:					# found text describing tag
				user_input = input("Input {0}: ".format(text))

			else:
				user_input = input("Input " + name + ": ")

			form.set(name, user_input)			# sets the user's input for tag
	return name_attrs_used


# input details - functions
def find_parent_sibling_text(tag):
	"""Finds the parent's sibling that contains text that accompanies tag.
	
	This is for Step 3 - Add Details to Post
	Tries to find the span tag with class="label" that describes the tag given.

	the 'textarea' tag does not have a similar parent tag structure as the others.
	so, the function 'find_siblings_text' is called on itself.

	Returns a string or None.
	"""
	if tag.name == 'textarea': # tag doesn't have a similar parent tag as the others
		return find_siblings_text(tag)
	else:
		return find_siblings_text(tag.parent)


def find_siblings_text(tag):
	"""Given a tag, go through its previous and next siblings to find a span tag.
	
	Returns a string or None.
	"""
	# previous siblings
	for sibling in tag.previous_siblings:
		text = find_span_text(sibling)	# determines if sibling is a tag
		if text != None:				# (if sibling is a tag and has a span tag)
			return text 				# returns span tag's string; otherwise no return
	
	# next siblings
	for sibling in tag.next_siblings:
		text = find_span_text(sibling)
		if text != None:
			return text
	return None


def find_span_text(sibling):
	"""Returns a span tag's text if the sibling is a tag. 

	Given a tag's sibling, determine if said sibling is a tag itself.
		if so, find a span tag with class="label".
		if a span tag is found, return the text accompanying it.
	
	Returns a string or None.
	"""
	if str(type(sibling)) == "<class 'bs4.element.Tag'>":	# sibling is a Tag
		span = sibling.find('span', class_=re.compile("label"))	# finds the span tag within sibling tag
		if span != None:				
			return span.text 			# return span tag's string if span tag exists
	return None

def remove_tags_with_attribute(tags, exclude_values):
    """Remove tags from a list of tags using an attribute as a filter.

    exclude_values is a dictionary. 
    {'attribute':[list of values for attribut]}

    The tag with an attribute = attribute and a value that is in values,
    will not be added to the new list of tags. 
    
    Returns a list of tags that don't have the attribue = one of values
    """
    new_tags = []
    attribute = list(exclude_values)[0]

    for tag in tags:
        value = tag.get_attribute_list(attribute)
        value = put_strings_together_from_list(value)

        if value not in exclude_values[attribute]:
            new_tags.append(tag)

    return new_tags

# get the user inputs for the tags
def get_user_inputs_for(tags):
    """
    Returns a dictionary containing the tag name attributes and user's inputted values for those tags.
    	dict_inputs = {name:value, name:value, name:options}
    	user_input_dict ={'name_attr':'user_input', 'name_attr':'user_input'}
    """
    dict_inputs = dict_of_name_attributes_and_values_from(tags)
    user_input_dict = dict_of_user_inputs_from(dict_inputs)    # user inputs info for tags
    return user_input_dict

# new dictionary of tags # 0
def dict_of_name_attributes_and_values_from(tags):
    """Returns a dictionary containing tag name attributes and their values.

    if 'select' tag:
    	dict_of_select(tag) = {name:options}
			options = {'choice1':'value1', 'choice2':'value2'}
	else:
		dict_of_general_input(tag) = {name:value}

	tag_dict = {name:value, name:value, name:options}
    """
    tag_dict = {}
    for tag in tags:
    	print("\t\t**" + tag.name + "** tag.")

    	if tag.name == 'select':
    		tag_dict.update( dict_of_select(tag) )

    	else:
    		tag_dict.update( dict_of_general_input(tag) )

    return tag_dict

# 0 > 1.1
def dict_of_general_input(tag):
    """
    Returns a dictionary of tag's name attribute and value associated with it.
    ex: return {name:value}
        name = tag's name attribute
        value = tag's value attribute
    """
    name = tag.get_attribute_list('name')
    name = put_strings_together_from_list(name)
    value = tag.get_attribute_list('value')
    
    if value[0] == None:        # tag does not have 'value' attribute
        value = ""

    else:
        value = put_strings_together_from_list(value)

    return {name:value}

# 0 > 1.2
def dict_of_select(tag):
    """
    Returns a dictionary of tag's name attribute and options associated with tag.
    ex: return {name:options}
        options = dictionary
            options = {'choice1':'value1', 'choice2':'value2'}
    """
    name = tag.get_attribute_list('name')
    name = put_strings_together_from_list(name)
    options = dict_options_of_select_tag(tag)

    return {name:options}

# 1.2 > 1.2.1
def dict_options_of_select_tag(tag):
    """Returns a dictionary of options.

    The options have a text value and a real value (when selecting an option)
        options = {'choice1':'value1', 'choice2':'value2'}
    """
    options = {}
    for child in tag.children:
        # obtain the actual value for a option given by select tag
        if (type(child) == type(tag)) and (child.string != '\n'):
            value = child.get_attribute_list('value')        # actual value for given option
            value = put_strings_together_from_list(value)    # (child.string = option)
            options[child.string] = value

    return options

# new dictionary of user inputs # 00
def dict_of_user_inputs_from(a_dict):
    """
    Returns a dictionary containing user inputs for tags.
    
    Given a dictionary (a_dict) containing name attributes and their values (or choices),
    tag_dict = {'name_attr':'user_input', 'name_attr':'user_input'}
    """
    tag_dict = {}

    for name in a_dict:
        value = a_dict[name]
        tag_dict.update( user_input_for(name, value) )

    return tag_dict

# 00 > 1
def user_input_for(name, value):
    """Returns a dictionary containing a tag's name attribute and user input for it."""
    if type(value) == type({}):
        print("Options for " + name + ": ")
        user_input = user_select_option(value)

    else:
        user_input = user_general_input(name, value)

    return {name:user_input}

# 1 > 2.1
def user_general_input(name, value):
    """Returns the user's input for a tag with name attribute = name."""
    if len(value) > 1:
        info_text = "This tag already has a value of '" + value + "' for " + name + "."
        print(info_text)
        confirmed = ask_for_confirmation("Would you like to keep it? ")

        if confirmed:
            return value            # user keeps value already available
    
    user_input = input("Enter info for " + name + ": ")
    return user_input

# 1 > 2.2
def user_select_option(options):
    """Returns the user's input for a selected option in options (dictionary)."""
    print_options(options)

    user_input = input("Enter the desired option: ")
    user_input = get_real_option_value(user_input, options)

    return user_input

# 2.2 >
def get_real_option_value(user_input, options):
    """
    Return the real value of the user inputted option.

    If a match cannot be found from user input. Return the original input back.
    """
    for key in options:
        # user input contains a string that matches option text (key).
        if (user_input in key) or (key in user_input):
            return options[key]

    return user_input

# 2.2 >
def print_options(options):
    """Given a dictionary of options. Print the options (keys)."""
    for option in options:
        print("\t" + option)
    return None

# inputting user info
def set_user_inputs(form, user_dict):
    """Sets the values, given from user_dict, inside form.
	
	user_dict = {'name_attr':'user_input', 'name_attr':'user_input'}
    """
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
        field_soup = BeautifulSoup(str(field), 'lxml')
        user_inputs.update(get_fieldset_user_inputs_for(field_soup))
        legends.append(field_soup.select_one('legend'))
    return user_inputs

def details_have_missing_information(browser):
    """
    Checks that the required details were entered. 

    Returns False for no missing information. 
    Returns True for missing information.
    """
    soup = browser.get_current_page()
    highlight_error =  soup.find('div', class_="highlight")
    if highlight_error == None:
        return False
    for child in highlight_error.children:
        if type(child) == type(highlight_error):
            print(child.text)
    return True

def input_missing_details(browser):
	browser.launch_browser()
	form = browser.select_form()
	info_input = {'FromEMail':'email@protonmail.com'}
	email_privacy = {'Privacy':'C'}
	form.set_input(info_input)
	form.set_radio(email_privacy)
	submit(browser)

# STEP 4 - Add Location - FUNCTIONS
def location_is_set(ilist):
    """ 
    Returns True location has at least one value inputted. Otherwise returns False.

        ilist = list of inputs
    Returns True
        if a location already entered
        if one value is entered then the location is set.
    Returns False
        if a location is not entered
    """
    name_attrs = ['city','geographic','area','street']
    location_values = []
    for item in ilist:
        value = item.get_attribute_list('value')[0]
        if value not in ["",None]:
            location_values.append(True)
    if True in location_values:
        return True
    else:
        return False


# STEP 5 - Add Images - FUNCIONS

def add_images_until_limit_or_done(browser):
    """Add images until limit is reached or user is done uploading images."""
    img_count = browser.get_current_page().find('span',class_="imgcount")   # tag containing image count limit
    limit = int(img_count.text)
    confirmed = True

    print("Upload the best image first - it will be featured.")
    button = find_button_with_text(browser, 'add image')    # button for adding images to form
    
    while confirmed and limit > 0:
        limit -= 1
        add_file(browser, button)        # add image (file) to browser using button
        confirmed = ask_for_confirmation("Would you like to add another image? ")

def add_file(browser, button):
    """
    Adds a file to a form.
    
    Given a browser and its button associated with the submission of a file.
    Find the form that the button is held in, 
    and find the input tag associated with button (type="file")
    Once the input tag is found, use the form to set the value to the file path.
    """
    path_to_file = input("Copy and Paste the file location: ")
    form = browser.select_form(button.parent)            # select form containing button

    name_attribute = find_name_attr_for_add_file_input(button)

    form.set(name_attribute, path_to_file)        # add file to form
    form.choose_submit(button)                    # button for adding files (not submiting whole page)
    browser.submit_selected()
    
    print("File: " + path_to_file + " has been added.")
    return None

def find_name_attr_for_add_file_input(button):
    """Returns name attribute for input associated with add file."""
    soup = BeautifulSoup(str(button.parent),'lxml')
    input_tag = soup.find('input',type="file")
    name_attribute = input_tag.get_attribute_list('name')
    name_attribute = put_strings_together_from_list(name_attribute)
    return name_attribute

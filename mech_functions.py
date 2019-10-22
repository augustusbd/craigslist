#! /user/bin/python3

# Craigslist Bot
# Mechanical Soup Implementation
# Functions 

import mechanicalsoup

import fields as fs
import general_functions as gen

######## MechanicalSoup Functions ########
def set_user_inputs(form, user_dict):
    """
    Sets the values, given from user_dict, inside form.
    
    user_dict = {'name_attr':'user_input', 'name_attr':'user_input'}
    """
    print("Inputting the values.")
    for name in user_dict:
        form.set(name, user_dict[name])
    return None

#0 and #00
def get_user_inputs_for(tags):
    """
    Returns a dictionary containing the tag name attributes and user's inputted values for those tags.
        dict_inputs = {name:value, name:value, name:options}
        user_input_dict ={'name_attr':'user_input', 'name_attr':'user_input'}
    """
    dict_inputs = dict_of_name_attributes_and_values_from(tags)     #0
    user_input_dict = dict_of_user_inputs_from(dict_inputs)         #00
    return user_input_dict

#   dictionary of tags #0
def dict_of_name_attributes_and_values_from(tags):
    """
    Returns a dictionary containing tag name attributes and their values.

    if 'select' tag:
        dict_of_select(tag) = {name:options}
            options = {'choice1':'value1', 'choice2':'value2'}
    else:
        dict_of_general_input(tag) = {name:value}

    tag_dict = {name:value, name:value, name:options}
    """
    tag_dict = {}
    for tag in tags:
        if tag.name != 'select':
            tag_dict.update(dict_of_general_input(tag)) # 1.1
        else:
            tag_dict.update(dict_of_select_tag(tag))        # 1.2
            
    return tag_dict

#       0 > 1.1
def dict_of_general_input(tag):
    """
    Returns a dictionary of tag's name attribute and value associated with it.
    ex: return {name:value}
        name = tag's name attribute
        value = tag's value attribute
    """
    name = tag.get_attribute_list('name')
    name = gen.add_strings_together_from_list(name)
    value = tag.get_attribute_list('value')
    
    if value[0] == None:        # tag does not have 'value' attribute
        value = ""

    else:
        value = gen.add_strings_together_from_list(value)

    return {name:value}

#       0 > 1.2
def dict_of_select_tag(tag):
    """
    Returns a dictionary of tag's name attribute and options associated with tag.
    ex: return {name:options}
        options = dictionary
            options = {'choice1':'value1', 'choice2':'value2'}
    """
    name = tag.get_attribute_list('name')
    name = gen.add_strings_together_from_list(name)
    options = dict_options_of_select_tag(tag)       # 1.2.1

    return {name:options}

#       1.2 > 1.2.1
def dict_options_of_select_tag(tag):
    """
    Returns a dictionary of options.

    The options have a text value and a real value (when selecting an option)
        options = {'choice1':'value1', 'choice2':'value2'}
    """
    options = {}
    for child in tag.children:
        # obtain the actual value for an option given by select tag
        if (type(child) == type(tag)) and (child.string != '\n'):
            value = child.get_attribute_list('value')       # actual value for given option
            value = gen.add_strings_together_from_list(value)    
            options[child.string] = value                   # (child.string = option)

    return options


#   dictionary of user inputs #00
def dict_of_user_inputs_from(a_dict):
    """
    Returns a dictionary containing user inputs for tags.
    
    Given a dictionary (a_dict) containing name attributes and their values (or choices),
    tag_dict = {'name_attr':'user_input', 'name_attr':'user_input'}
    """
    tag_dict = {}

    for name in a_dict:
        value = a_dict[name]
        tag_dict.update(user_input_for(name, value))

    return tag_dict

#       00 > 1
def user_input_for(name, value):
    """Returns a dictionary containing a tag's name attribute and user input for it."""
    if type(value) != type({}):
        user_input = user_general_input(name, value)    # 2.1

    else:
        # select tag's options
        print(f"Options for {name}: ")
        user_input = user_select_option(value)          # 2.2

    return {name:user_input}

#       1 > 2.1
def user_general_input(name, value):
    """Returns the user's input for a tag (with name attribute = name)."""
    if len(value) > 1:
        print(f"This tag already has a value of '{value}' for {name}")

        confirmed = gen.ask_for_confirmation("Would you like to keep it? ")
        if confirmed:
            return value            # user keeps value already available
    
    user_input = input(f"Enter info for {name}: ")
    return user_input

#       1 > 2.2
def user_select_option(options):
    """Returns the user's input for a selected option in options (dictionary)."""
    print_options(options)
    user_input = input("Enter the desired option: ")
    user_input = get_real_option_value(user_input, options)

    return user_input

#       2.2 >
def print_options(options):
    """Given a dictionary of options. Print the options (keys)."""
    for option in options:
        print(f"\t{option}")
    return None

#       2.2 >
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



# STEP 1 & 2 - Selecting Radio Option
def text_from_tags(tags):
    """Returns a list of strings containing text for options."""
    text_list = []
    for tag in tags:
        text = gen.remove_whitespace_at_either_end(tag.text)
        text = gen.remove_non_space_whitespace(text)
        text_list.append(text)
    return text_list

#   input radio options and user input
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

#   give radio options
def determine_radio_buttons_and_text(browser):
    """
    Gives the input radio options.
    
    Input radio options (buttons) will have labels within different tags.
    Returns a list containing the radio buttons and text describing them.
        ex: buttons_and_text = [(tag, text), (tag, text)]
    """
    soup = browser.get_current_page()
    radio_buttons = soup.find_all('input', type="radio")

    # parent tag name and class
    parent = radio_buttons[0].parent
    p_class = parent.get_attribute_list('class')[0]
    p_name = parent.name

    if p_name == 'label' and p_class == 'radio-option':
        # tags holding text describing radio buttons
        radio_labels = soup.find_all('span',class_="option-label")

    elif p_name == 'span' and p_class == 'left-side':
        radio_labels = soup.find_all('span',class_="right-side")

    else:
        print("Radio buttons do not lie within label or span tags.")
        return []           # return empty list

    # list of text describing radio buttons
    texts = text_from_tags(radio_labels)

    # list of radio butons and the text accompanying them
    #  ex: [(tag, text), (tag, text)]
    buttons_and_texts = list(zip(radio_buttons, texts))

    return buttons_and_texts

#   user input (selection) of radio option
def select_radio_option_from_list(a_list):
    """
    User selects a radio option.

    Print the text assocaited with a tag and the tag's value attribute.
    Each index of a_list is a tuple containing the tag and the text associated with it. 
        ex: a_list = [(tag,text), (tag,text)]

    Return the user's input as a dictionary.
    """
    if len(a_list) == 0:        # empty list
        return {}

    print("These are the options for the categories (marked with **): ")
    for item in a_list:
        value = item[0].get_attribute_list('value') # value for radio button
        value = gen.add_strings_together_from_list(value)
        print(f"\t*{item[1]}*\twith a value of: {value}")

    user_input = input("Enter the text or the value associated with it: ")
    user_input = determine_user_input_for_radio_button(user_input, a_list)

    return user_input


def determine_user_input_for_radio_button(user_input, tag_list):
    """
    Determines what the user input refers to. 
    
    Returns a dictonary of user input.

    user_input = 'some string'
    tag_list = list of tags.
        ex: tag_list = [(tag, text), (tag,text)]

    Given a list of tags and the user's input,
    determine if the user input is the actual value of a tag,
    or the user input is, in some form, the text associated with a tag.    
    """
    # name attribute of radio tags
    name_attr = tag_list[0][0].get_attribute_list('name')
    name_attr = gen.add_strings_together_from_list(name_attr)

    for item in tag_list:
        value = item[0].get_attribute_list('value')
        value = gen.add_strings_together_from_list(value)

        if (user_input.lower() in item[1].lower()) or (user_input in value):
            return {name_attr:value}

    print("Inputted value does not refer to anything.")
    # not the best return
    return {}           # form.set_radio() uses a dictionary as its argument


# STEP 3 - Add Details
def input_details(browser):
    """User inputs values for page."""
    soup = browser.get_current_page()

    # input general details (Title, Description, Zip Code, etc.)
    name_attrs = input_general_details(browser)     # list of name attributes

    # input fieldset details ('posting details', 'contact info', 'location info')
    name_attrs = input_fieldset_details(browser, name_attrs)

    # leftover tags are put into their own "custom_fieldset"
        # finds all inputs (type != hidden)
        # (select tags are only within fieldset tags)
    custom_fieldset = soup.find_all('input', type=gen.not_hidden)
    custom_fieldset = gen.remove_tags_with_name_attributes(custom_fieldset, name_attrs)

    # what am I trying to do?
    return None


#   input details functions
#       general details - functions
def input_general_details(browser):
    """
    User inputs general details for post.
    
    Sets the values for the name attributes with user input.
    Returns a list of name attributes that were used to set a value.
        # not all name attributes will be on page
    """
    # tag name attributes for general details required
    name_attributes = ['PostingTitle', 'price','GeographicArea',
    'postal','FromEMail','PostingBody']

    name_attrs_used = general_details(browser, name_attributes)

    return name_attrs_used

def general_details(browser, names):
    """
    Return a list of name attributes used to set a value.
    
    Goes through the name attributes given (names) and inputs the user's values.
    """
    form = browser.select_form()
    soup = browser.get_current_page()

    name_attrs_used = []        # actual list of name attributes used

    # FOR textarea, the VALUE DOES NOT EXIST
    # the input is set to the paragraph's text

    for name in names:
        tag = tag = soup.find(attrs={'name':name})
        if tag != None:
            name_attrs_used.append(name)
            # returns string describing tag or None
            tag_text = gen.find_parent_sibling_text(tag)    

            # tag has a value inputted
            if (tag_text != None) and gen.value_exists(tag):    
                user_input = gen.existing_value_input(tag, tag_text)

            elif (tag_text == None) and gen.value_exists(tag):
                user_input = gen.existing_value_input(tag, name)

            # tag does not have a value inputted
            elif tag_text != None:                          
                user_input = input(f"Input {tag_text}: ")

            else:
                user_input = input(f"Input {name}: ")

            form.set(name, user_input)  
    return name_attrs_used

#       fieldset details - functions
def input_fieldset_details(browser, name_attrs):
    """
    User inputs details inside fieldset tags for post.

    Returns a list of name attributes used.
    """
    form = browser.select_form()
    soup = browser.get_current_page()

    # split tags into their fieldsets
    fieldsets = soup.find_all(gen.fieldset_not_within_fieldset)
    fieldset_objects = fs.create_fieldset_objects(fieldsets, name_attrs)

    for field in fieldset_objects:
        name_attrs = name_attrs + field.return_name_attributes() # name attributes of tags used
        user_inputs = field.input_values()  # user inputs for tags inside fieldset
        user_inputs.update(field.input_other_values())

        set_user_inputs(form, user_inputs)  # sets the user inputs into browser

    return name_attrs


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
    # tag containing image count limit
    img_count = browser.get_current_page().find('span',class_="imgcount")   
    limit = int(img_count.text)
    confirmed = True

    print("Upload the best image first - it will be featured.")
    button = gen.find_button_with_text(browser, 'add image')    # button for adding images to form
    
    while confirmed and (limit > 0):
        limit -= 1
        add_file(browser, button)        # add image (file) to browser using button
        confirmed = gen.ask_for_confirmation("Would you like to add another image? ")

def add_file(browser, button):
    """
    Adds a file to a form.
    
    Given a browser and its button associated with the submission of a file.
    Find the form that the button is held in, 
    and find the input tag associated with button (type="file")
    Once the input tag is found, use the form to set the value to the file path.
    """
    path_to_file = input("Copy and Paste the file location: ")

    if len(path_to_file) < 3:
        return None

    name_attribute = find_name_attr_for_add_file_input(button)
    
    form = browser.select_form(button.parent)     # select form containing button
    form.set(name_attribute, path_to_file)        # add file to form
    form.choose_submit(button)                    # button for adding files (not submiting whole page)
    browser.submit_selected()
    
    print("File:'{path_to_file}'' has been added.")
    return None

def find_name_attr_for_add_file_input(button):
    """Returns name attribute for input associated with add file."""
    soup = button.parent
    input_tag = soup.find('input',type="file")
    name_attribute = input_tag.get_attribute_list('name')
    name_attribute = gen.add_strings_together_from_list(name_attribute)
    return name_attribute



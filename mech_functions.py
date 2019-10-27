#! /user/bin/python3

# Craigslist Bot
# Mechanical Soup Implementation
# Functions 

import mechanicalsoup
from PyQt5.QtWidgets import (QDialog, QApplication, QLabel,
                             QGridLayout)

import general_functions as gen


# Add Details - Fieldset Tags - Classes
class Fieldset():
    """
    Structure containing a fieldset tag and its inputs.
    """
    def __init__(self, fieldset, exclude_name_attrs):
        self.Title = gen.capitalize_each_word(fieldset.find('legend').text)
        self._field = fieldset
        self.subfield_exists = False

        # determines if fieldset exists within fieldset
        subfield = self.does_subfield_exist(fieldset)
        if subfield != False:
            self.subfield_exists = True
            self.create_subfieldset(subfield, exclude_name_attrs)
            # exlcude now includes the name attributes of the SubField
            exclude_name_attrs = exclude_name_attrs + self.SubField.name_attributes

        self.field_inputs(exclude_name_attrs)
    
    def __str__(self):
        return f"{self.Title} grouping of tags."

    def __repr__(self):
        return f"Contains the tags of {self.Title}."

    def field_inputs(self, exclude_name_attrs):
        """Field inputs."""
        input_tags = self._field.find_all('input', type=gen.not_checkbox_or_radio)
        select_tags = self._field.find_all('select')
        regular_tags = input_tags + select_tags

        self.tags = gen.remove_tags_with_name_attributes(regular_tags, exclude_name_attrs)
        self.name_attributes = gen.get_name_attributes(self.tags)    # list of name attributes from tags

        other_inputs = self._field.find_all('input', type=gen.checkbox_or_radio)
        self.other_tags = gen.remove_tags_with_same_name_attr(other_inputs)

    def create_subfieldset(self, field, exclude_name_attrs):
        """Creates the SubField object using the fieldset tag within fieldset tag."""
        # this is a grouping within Fieldset GUI,
        self.SubField = SubFieldset(field, exclude_name_attrs)
        #group = QGroupBox()
    
    def input_values(self):
        """User inputs values for field's tags."""
        if self.subfield_exists:
            inputs = get_user_inputs_for(self.tags)                # Field inputs
            sub_inputs = get_user_inputs_for(self.SubField.tags)    # SubField inputs
            self.user_inputs = gen.merge_dict(inputs, sub_inputs)

        else:
            self.user_inputs = get_user_inputs_for(self.tags)

        return self.user_inputs

    def input_other_values(self):
        """User inputs values for field's other tags (radio and checkboxes)."""
        if len(self.other_tags) == 0:
            return {}

        else:
            inputs = get_user_input_for_others(self.other_tags)
            return inputs

    def return_name_attributes(self):
        """Returns the field's name attributes as a list."""
        if self.subfield_exists:
            return self.name_attributes + self.SubField.name_attributes
        
        else:
            return self.name_attributes

    def does_subfield_exist(self, fieldset):
        """Returns the subfield if it exists; otherwise returns False."""
        subfield = fieldset.find('fieldset') # finds fieldset tag within fieldset tag
        if subfield == None:
            return False
        else:
            return subfield

    def create_window(self):
        """creates Fieldset GUI for inputting values."""
        #self.window = QDialog()
        #self.window.setWindowTitle(self.Title)
        #self.MainLayout = QGridLayout()
        pass



class SubFieldset(Fieldset):
    """
    Structure containing a fieldset tag (and its inputs) 
    that is within another fieldset tag.
    """
    pass
    #def __init__(self, fieldset, exclude_name_attrs):
        # this is a child of Fieldset object
        # how do I get the same self.variables initialized
        #super().__init__(self)



def create_fieldset_objects(fieldsets, exclude_name_attrs):
    """Using the fieldsets to create their own groupings."""
    fieldset_objects = []

    for field in fieldsets:
        fieldset_objects.append(Fieldset(field, exclude_name_attrs))
        
    return fieldset_objects


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
    name = gen.get_attribute_string(tag, 'name')
    value = gen.get_attribute_string(tag, 'value')
    
    if value == None:        # tag does not have 'value' attribute
        value = ""

    return {name:value}

#       0 > 1.2
def dict_of_select_tag(tag):
    """
    Returns a dictionary of tag's name attribute and options associated with tag.
    ex: return {name:options}
        options = dictionary
            options = {'choice1':'value1', 'choice2':'value2'}
    """

    name = gen.get_attribute_string(tag, 'name')
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

            # actual value for given option
            value = gen.get_attribute_string(child, 'value')

            # (child.string = option)
            options[child.string] = value                   

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


#X and #XX
def get_user_input_for_others(tags):
    """
    Returns a dictionary containing the name attributes and values for tags.

    tags = list of input tags that have type = 'checkbox' or 'radio'
    """

    tag_dict = {}
    for tag in tags:
        type_ = gen.get_attribute_string(tag, 'type')

        if type_ == 'checkbox':
            tag_dict.update(checkbox_input(tag))    #X

        elif type_ == 'radio':
            tag_dict.update(radio_input(tag))       #XX

    return tag_dict

#X
def checkbox_input(tag):
    """
    User checks the checkbox if desired.
    
    Ask user if they want to check checkbox
        if yes,
            return {name:value}
        else
            return {}
    """
    name = gen.get_attribute_string(tag, 'name')
    value = gen.get_attribute_string(tag, 'value')

    text = gen.find_parent_sibling_text(tag)

    if text != None:
        confirmed = gen.ask_for_confirmation(f"Would you like to check checkbox of {text}? ")

    else:
        confirmed = gen.ask_for_confirmation(f"Would you like to check checkbox of {name}? ")

    if confirmed:
        return {name:value}

    else:
        return {}

#XX
def radio_input(tag):
    """
    User selects the desired radio option.

    Find other radio inputs with same name,
    Give user the options of radio inputs,
    Ask user which one they would like to select

    Return {name:value_of_radio_option}
    """
    name = gen.get_attribute_string(tag, 'name')

     # gets the full html tag without needing browser
    soup = tag.find_parent('html') 
    
    # find input radio tags with same name attribute
    radios = soup.find_all('input', attrs={'name':name, 'type':'radio'})
    
    print(gen.find_parent_sibling_text(radios[0]))    # describes the radio options

    radio_dict = {}

    print("These are the radio options: ")
    for radio in radios:
        pos = radios.index(radio) + 1          # position of radio button in dictionary
        title = gen.get_attribute_string(radio, 'title')
        
        # value of radio button (browser uses this to select option)
        value = gen.get_attribute_string(tag, 'value')     
        
        radio_dict[str(pos)] = value                # store value of radio button

        print(f"\tOption #{pos}: {title}")    # gives radio button info
        print(f"\t\tBasically means: {gen.find_siblings_text(radio)}\n")

    user_input = input("Which option would you like to select? (enter option #): ")

    return {name:radio_dict[user_input]}



# STEP 1 & 2 - Selecting Radio Option

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
        value = gen.get_attribute_string(item[0], 'value')# value for radio button
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
    name_attr = gen.get_attribute_string(tag_list[0][0], 'name')

    for tag,text in tag_list:
        value = gen.get_attribute_string(tag, 'value')

        if (user_input.lower() in text.lower()) or (user_input.lower() in value.lower()):
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
    fieldset_objects = create_fieldset_objects(fieldsets, name_attrs)

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
    name_attribute = gen.get_attribute_string(input_tag, 'name')
    return name_attribute
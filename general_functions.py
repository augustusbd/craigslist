#! /user/bin/python3

# Craigslist Bot
# Functions 
import mechanicalsoup
import re

#abcdefghijklmnopqrstuvwxyz

############### General Functions ###############
def ask_for_confirmation(text):
    """Ask a user if they would like to do something or not. Returns True or False."""
    affirmative = ['yes','ya','ye','y','oui','si','mhm','mmhmm']
    answer = input(text)
    if answer in affirmative:
        return True
    else:
        return False

def merge_dict(dict1, dict2):
	"""Merge two dictionaries together."""
	res = {**dict1, **dict2}
	return res


#	string functions #
def add_strings_together_from_list(a_list):
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

def capitalize_each_word(text):
    new_string = ""
    for word in text.split():
        new_string = new_string + word.capitalize() + " "
    new_string = remove_whitespace_at_either_end(new_string)
    return new_string

def different_versions_of_string(text):
    """
    Returns a list containing the different versions of a string.
    ex: text = 'continue'
        'continue' can be written as 'Continue', 'CONTINUE', 'cont.', 'CONT.'
    """
    string_list = [text, text.upper(), text.capitalize(), capitalize_each_word(text)]
    return string_list

def is_every_index_a_string(a_list):
    """
    Returns True if every element in a_list is a string. Otherwise returns False.
    """
    for item in a_list:
        if type(item) != str:
            return False
    return True

def put_strings_together(a_list):
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
        print("Returning the first element of list.")
        return a_list[0]


#		whitespace
def has_non_space_whitespace(text):
    """Returns True if text has non-space whitespace."""
    whitespace = ['\n','\t','\r','\x0b','\x0c']
    for x in whitespace:
        if x in text:
            return True
    return False

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



######### BeautifulSoup Functions #########
def get_name_attributes(tags):
	"""Returns a list of name attributes from tags."""
	name_list = []
	for tag in tags:
		name = tag.get_attribute_list('name')
		name = add_strings_together_from_list(name)
		name_list.append(name)
	return name_list

def print_name_attrs(tags):
	"""Prints the name attributes of the tags."""
	for tag in tags:
		print(tag.get_attribute_list('name'))

# 	filter functions #
def fieldset_not_within_fieldset(tag):
	"""Returns tag if it is a fieldset tag not within a fieldset tag."""
	if tag.name == "fieldset":
		if tag.find_parent('fieldset') == None:
			return tag

def not_hidden(a_type):
	"""Returns a type that is not equal to hidden."""
	return a_type != "hidden"

# 	find button functions #
def find_button_with_type(browser, text):
    """Find button with text given. 
    The text will be the filter for the type attribute."""
    soup = browser.get_current_page()
    button = soup.find('button', type=text)
    if button == None:
        print(f"A button tag with attribute type '{text}' does not exist.")
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
            print("There are no buttons with text='{text}' on this page.")
            return None
        else:
            button = button.find_next('button')             # otherwise, keeping searching
    return button

#	find text functions #
def find_parent_sibling_text(tag):
    """
    Finds the parent's sibling that contains text that accompanies tag.
    
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
    """
    Given a tag, go through its previous and next siblings to find a span tag.
    
    Returns a string or None.
    """
    # previous siblings
    for sibling in tag.previous_siblings:
        text = find_span_text(sibling)  # finds the span tag's text within sibling
        if text != None:                # text was found within span tag
            return text
    
    # next siblings
    for sibling in tag.next_siblings:
        text = find_span_text(sibling)
        if text != None:
            return text

    return None

def find_span_text(sibling):
    """
    Find a span tag within sibling and return its text.

    Given a tag's sibling, determine if said sibling is a tag itself.
        if so, find a span tag with class="label".
        if a span tag is found, return the text accompanying it.
    
    Returns a string or None.
    """
    if str(type(sibling)) == "<class 'bs4.element.Tag'>":   # sibling is a Tag
        span = sibling.find('span', class_=re.compile("label"))
        if span != None:                
            return span.text
    return None

#	remove tags #
def remove_tags_with_name_attributes(tags, exclude_values):
	"""Remove tags from a list of tags using an attribute as a filter.

	The tag with a name attribute that is in exlcude_values,
	will not be added to the new list of tags. 
	
	Returns a list of tags that do not have a name attribute in exlcude_values
	"""
	new_tags = []
	for tag in tags:
		value = tag.get_attribute_list('name')
		value = add_strings_together_from_list(value)
		if value not in exclude_values:
			new_tags.append(tag)
	return new_tags

def remove_tags_with_same_name_attr(tags):
	"""Removes tags that have the same name attribute."""
	new_tags = []
	name_list = get_name_attributes(tags)
	for tag in tags:
		name = tag.get_attribute_list('name')
		name = add_strings_together_from_list(name)
		while name_list.count(name) > 1:	# removes duplicate names
			name_list.remove(name)
		if name in name_list:				# tag has name attribute in name list
			new_tags.append(tag)			# only this tag can be added with this name attribute
			name_list.remove(name)		# remove name from name list 
											# no more tags with the same name can be added
	return new_tags

#   tag value functions
def existing_value_input(tag, tag_text):
    """
    Asks user if they would like to change the tag's value or keep it the same. 

    Returns the user's input.
    """
    tag_text = capitalize_each_word(tag_text)

    if tag.name == 'textarea':
    	value = tag.text

    else:
    	value = tag.get_attribute_list('value')
    	value = add_strings_together_from_list(value)

    message = (f"{tag_text}: {value}   (already entered).\n"
                f"\tenter another value to change {tag_text}: "
            )
    user_input = input(message)

    if user_input == "":
        return value

    return user_input

def value_exists(tag):
    """Returns True if the tag has a value."""
    value_list = ['',None]
    if tag.name == 'textarea':
    	value = tag.text

    else:
    	value = tag.get_attribute_list('value')[0]

    if value in value_list:
        return False

    else:
        return True


#! /usr/bin/python3

# Craigslist Bot 
# Add Details - Fieldset Tags
from PyQt5.QtWidgets import (QDialog, QApplication, QLabel,
        					 QGridLayout)

import mech_functions as m
import general_functions as gen

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
        input_tags = self._field.find_all('input', type=not_checkbox_or_radio)
        select_tags = self._field.find_all('select')
        regular_tags = input_tags + select_tags

        self.tags = gen.remove_tags_with_name_attributes(regular_tags, exclude_name_attrs)
        self.name_attributes = gen.get_name_attributes(self.tags)    # list of name attributes from tags

        other_inputs = self._field.find_all('input', type=checkbox_or_radio)
        self.other_tags = gen.remove_tags_with_same_name_attr(other_inputs)

    def create_subfieldset(self, field, exclude_name_attrs):
        """Creates the SubField object using the fieldset tag within fieldset tag."""
        # this is a grouping within Fieldset GUI,
        self.SubField = SubFieldset(field, exclude_name_attrs)
        #group = QGroupBox()
    
    def input_values(self):
        """User inputs values for field's tags."""
        if self.subfield_exists:
            inputs = m.get_user_inputs_for(self.tags)                # Field inputs
            sub_inputs = m.get_user_inputs_for(self.SubField.tags)    # SubField inputs
            self.user_inputs = gen.merge_dict(inputs, sub_inputs)

        else:
            self.user_inputs = m.get_user_inputs_for(self.tags)

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
        self.window = QDialog()
        self.window.setWindowTitle(self.Title)
        self.MainLayout = QGridLayout()



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



def get_user_input_for_others(tags):
    """
    Returns a dictionary containing the name attributes and values for tags.

    tags = list of input tags that have type = 'checkbox' or 'radio'
    """

    tag_dict = {}
    for tag in tags:
        type_ = tag.get_attribute_list('type')
        type_ = gen.add_strings_together_from_list(type_)

        if type_ == 'checkbox':
            tag_dict.update( checkbox_input(tag) )

        elif type_ == 'radio':
            tag_dict.update( radio_input(tag) )

    return tag_dict


def checkbox_input(tag):
    """User checks the checkbox if desired.
    # ask user if they want to check checkbox
    # if yes,
        # return {name:value}
    # else
        # return {}
    """
    name = tag.get_attribute_list('name')
    name = gen.add_strings_together_from_list(name)
    value = tag.get_attribute_list('value')
    value = gen.add_strings_together_from_list(value)

    text = gen.find_parent_sibling_text(tag)
    if text != None:
        confirmed = gen.ask_for_confirmation("Would you like to check checkbox of " + text + "? ")

    else:
        confirmed = gen.ask_for_confirmation("Would you like to check checkbox of " + name + "? ")

    if confirmed:
        return {name:value}

    else:
        return {}

def radio_input(tag):
    """User selects the desired radio option"""
    # find other radio inputs with same name
    # give user the options of radio inputs
    # ask user which one they would like to select
    # return {name:value_of_radio_option}
    name = tag.get_attribute_list('name')
    name = gen.add_strings_together_from_list(name)

    soup = tag.find_parent('html')  # gets the full html tag without needing browser
    
    # find tags with same name attribute
    radios = soup.find_all('input', attrs={'name':name, 'type':'radio'})
    
    print(gen.find_parent_sibling_text(radios[0]))    # describes the radio options

    radio_dict = {}
    print("These are the radio options: ")
    for radio in radios:
        pos = radios.index(radio) + 1               # position of radio button
        title = radio.get_attribute_list('title')
        title = gen.add_strings_together_from_list(title)
        value = tag.get_attribute_list('value')     # value of radio button (to select)
        value = gen.add_strings_together_from_list(value)
        
        radio_dict[str(pos)] = value                # store value of radio button

        print(f"\tOption #{pos}: {title}")    # gives radio button info
        print(f"\t\tBasically means: {gen.find_siblings_text(radio)}\n")

    user_input = input("Which option would you like to select? (enter option #): ")
    return {name:radio_dict[user_input]}

def create_fieldset_objects(fieldsets, exclude_name_attrs):
    """Using the fieldsets to create their own groupings."""
    fieldset_objects = []
    for field in fieldsets:
        fieldset_objects.append(Fieldset(field, exclude_name_attrs))
        
    return fieldset_objects

# exclusive or: lists of tags
def compare_lists_of_tags_remove_indentical(tags1, tags2):
    """Remove tags that are in both list of tags."""
    new_tags = xor(tags1, tags2) 


# SOUP FIND FILTER
def checkbox_or_radio(a_type):
    """Return type != 'radio' or 'checkbox'"""
    types = ['checkbox', 'radio']
    return a_type in types

def not_checkbox_or_radio(a_type):
    """Return type != 'radio' or 'checkbox'"""
    types = ['checkbox', 'radio']
    return a_type and not (a_type in types)

def fieldset_not_within_fieldset(tag):
    """Returns tag if it is a fieldset tag not within a fieldset tag."""
    if tag.name == "fieldset":
        if tag.find_parent('fieldset') == None:
            return tag
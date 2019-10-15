import mech_functions as m
from PyQt5.QtWidgets import (QDialog, QApplication, QLabel,
		QGridLayout)



class Fieldset():
	"""
	Structure containing a fieldset tag and its inputs.
	"""
	def __init__(self, fieldset):
		self.Title = m.capitalize_each_word(fieldset.find('legend').text)

		input_tags = fieldset.find_all('input')
		select_tags = fieldset.find_all('select')
		self.tags = input_tags + select_tags

		self.name_attributes = get_name_attributes(self.tags)	# list of name attributes from tags


	def create_window(self):
		# creates Fieldset GUI for inputting values
		self.window = QDialog()
		self.window.setWindowTitle(self.Title)

		self.MainLayout = QGridLayout()


	def create_subfieldset(self, field):
		# this is a grouping within Fieldset GUI,
		# self.subfield = SubFieldset(self, field)
		self.subfield = SubFieldset(self, field)

		group = QGroupBox()


	def input_values_for(self):
		self.user_inputs = m.get_user_inputs_for(self.tags)




class SubFieldset(Fieldset):
	"""
	Structure containing a fieldset tag (and its inputs) 
	that is within another fieldset tag.
	"""
	def __init__(self, fieldset):
		# this is a child of Fieldset object
		# how do I get the same self.variables initialized
		super().__init__(self)



def create_fieldset_objects(fieldsets):
	"""Using the fieldsets to create their own groupings."""
	fieldset_objects = []
	for field in fieldsets:
		fieldset_objects.append(Fieldset(field))
		
	return fieldset_objects

# exclusive or: lists of tags
def compare_lists_of_tags_remove_indentical(tags1, tags2):
	"""Remove tags that are in both list of tags."""
	new_tags = xor(tags1, tags2) 


def get_name_attributes(tags):
	name_list = []
	for tag in tags:
		name = tag.get_attribute_list('name')
		name = put_strings_together_from_list(name)
		name_list.append(name)
	return name_list

# SOUP FIND FILTER
def fieldset_not_within_fieldset(tag):
	"""Returns tag if it is a fieldset tag not within a fieldset tag."""
    if tag.name == 'fieldset':
        if tag.find_parent('fieldset') == None:
            return tag
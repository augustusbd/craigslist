from bs4 import BeautifulSoup
import mech_functions as m


class Fieldset():
	"""
	Structure containing a fieldset tag and its inputs.
	"""
	def __init__(self, fieldset):
		self.soup = BeautifulSoup(str(fieldset), 'lxml')
		input_tags = self.soup.find_all('input')
		select_tags = self.soup.find_all('select')
		self.tags = input_tags + select_tags

	def create_window(self):
		# creates Fieldset GUI for inputting values
		self.MainLayout = None

	def create_subfieldset(self, field):
		# this is a grouping within Fieldset GUI,
		# self.subfield = SubFieldset(self, field)
		self.subfield = SubFieldset(self, field)

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
		self.tags = []


def create_fieldset_objects(fieldsets):
	"""Using the fieldsets to create their own groupings."""
	fieldset_objects = []
	for field in fieldsets:
		fieldset_objects.append(Fieldset(field))
		
	return fieldset_objects

# exclusive or: lists of tags
def compare_lists_of_tags_remove_indentical(tags1, tags2):
	new_tags = xor(tags1, tags2) 

# SOUP FIND FILTER
def fieldset_not_within_fieldset(tag):
	if tag.name == 'fieldset':
		if tag.find_parent('fieldset') == None:
			return tag
	return tag and not str(tag)

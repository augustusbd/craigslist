#! /usr/bin/python3

# Craigslist Bot
# Mechanical Soup Implementation
import mechanicalsoup
from PyQt5.QtWidgets import QApplication

import mech_functions as m
import general_functions as gen



class Browser(mechanicalsoup.StatefulBrowser):
    """
    Contains the methods used to 'Create A Post' on Craigslist.
    """
    def __init__(self, type_='post'):
        super().__init__()
        
        if type_ == 'post': 
            self.initPostBrowser()

        else:
            self.initBrowser()

    def __str__(self):
        return f"This object browses and handles the craigslist site."

    def __repr__(self):
        return f"Contains the browser and methods for controlling craigslist site."


    def initPostBrowser(self):
        """Browser will be used to 'create a post'."""
        self.open("https://batonrouge.craigslist.org/")
        self.follow_link(id='post')        # 'create a post' link
        self.in_progress = True

        return None


    def initBrowser(self):
        """Browser is meant to browse through site."""
        self.open("https://batonrouge.craigslist.org/")
        return None


    def create_a_post_process(self):
        MESSAGE = """
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
        print(MESSAGE)
        return None


    def publish_draft_message(self):
        MESSAGE = (
            f"Further Action Required To Complete Request\n"
            f"You should receive an email shortly, with a link to:\n"
            f"publish your ad\n"
            f"\tedit (or confirm an edit to) your ad\n"
            f"\tverify your email address\n"
            f"\tdelete your ad"
            )
        print(MESSAGE)
        return None

    def determine_page(self):
        """
        Determines which function to call based on title of page and number of forms.
        """
        soup = self.get_current_page()
        forms = soup.find_all('form')        # length of forms gives a hint towards page
        title_text = soup.title.text
        #print(title_text)

        if 'type' in title_text or 'category' in title_text:
            # self.choose_category_of_post()
            return 'category'
            
        elif 'map' in title_text:
            # self.add_location_to_post()
            return 'map'


        elif ('posting' in title_text) and (len(forms) == 1):
            # self.add_details_to_post()
            return 'details'
        
        elif ('posting' in title_text) and (len(forms) == 3):
            # self.add_images_to_post()
            return 'images'

        elif ('posting' in title_text) and (len(forms) == 8):
            # self.edit_draft_of_posting()
            return 'edit'

        else:
            # not editing post, location or images
            # page was already submitted so only print message
            self.publish_draft_message()

        self.in_progress = False
        return None


    def submit_(self):
        """
        Submits the current page's form.
        
        Looks for a button 'continue' text, if applicable, and uses that button for submission.
        """
        button = self.get_current_page().find('button', type='submit')
        form = self.select_form()

        if button != None:          # a button was found.
            form.choose_submit(button)
        
        self.submit_selected()       # prompts a follow_link (new page) as well
        return None


    ## STEP 1 - radio buttons and labels
    def display_categories_of_post(self):
        """
        Return the radio buttons of page to display through GUI.

        reimplementation of: self.determine_radio_buttons()
        """
        soup = self.get_current_page()
        radio_buttons = soup.find_all('input', type="radio")

        # parent tag name and class
        parent = radio_buttons[0].parent
        parent_class = parent.get_attribute_list('class')[0]

        if parent_class == 'radio-option':
            # tags containing text describing radio buttons
            radio_labels = soup.find_all('span',class_="option-label")

        elif parent_class == 'left-side':
            radio_labels = soup.find_all('span',class_="right-side")

        else:
            print("Radio buttons' labels could not be found.")
            return [], []

        # list of labels describing radio buttons
        labels = gen.text_from_tags(radio_labels)
        return radio_buttons, labels

    ## STEP 1 - select radio button using Browser
    def select_radio_button2(self, tag, selection):
        """
        Select radio option with form (Browser).
        """
        name_attribute = gen.get_attribute_string(tag, 'name')
        form = self.select_form()
        form.set_radio({name_attribute:selection})

        self.submit_()
        return None


    # step 1 and step 2
    # Choose Type of Posting and Choose Category are basically the same
    
    # STEP 3
    def add_details_to_post(self):
        """
        Step 3 - Create Posting - Enter Details.
        
        General Required Information:
            Posting Title (name attribute='PostingTitle'):
            Postal Code ('postal'):
            Description ('PostingBody'):
            email ('FromEMail'):
        """
        form = self.select_form()

        self.input_details()
        
        # have to choose a privacy option for email 
        email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
        form.set_radio(email_privacy)

        self.submit_()

        if details_have_missing_information(self.browser):
            input_missing_details(self.browser)

        return None

    #   step 3 - Add Details
    def input_details(self):
        """User inputs values for page."""
        soup = self.get_current_page()

        # input general details (Title, Description, Zip Code, etc.)
        name_attrs = self.input_general_details()     # list of name attributes used

        # input fieldset details ('posting details', 'contact info', 'location info')
        name_attrs = self.input_fieldset_details(name_attrs)

        # leftover tags are put into their own "custom_fieldset"
            # finds all inputs (type != hidden)
            # (select tags are only within fieldset tags)
        custom_fieldset = soup.find_all('input', type=gen.not_hidden)
        custom_fieldset = gen.remove_tags_with_name_attributes(custom_fieldset, name_attrs)

        # what am I trying to do?
        return None

    #   input details functions
    #       general details - functions
    def input_general_details(self):
        """
        User inputs general details for post.
        
        Sets the values for the name attributes with user input.
        Returns a list of name attributes that were used to set a value.
            # not all name attributes will be on page
        """
        # tag name attributes for general details required
        name_attributes = ['PostingTitle', 'price','GeographicArea',
        'postal','FromEMail','PostingBody']

        name_attrs_used = self.general_details(name_attributes)

        return name_attrs_used


    def general_details(self, names):
        """
        Return a list of name attributes used to set a value.
        
        Goes through the name attributes given (names) and inputs the user's values.
        """
        form = self.select_form()
        soup = self.get_current_page()

        name_attrs_used = []        # actual list of name attributes used

        # FOR textarea, the input is set to the paragraph's text
        for name in names:
            tag = soup.find(attrs={'name':name})
            if tag != None:
                name_attrs_used.append(name)

                # returns string describing tag or None
                tag_text = gen.find_parent_sibling_text(tag)
                # either the tag text or the name attribute
                text = gen.first_string_if_not_empty(tag_text, name)  

                # tag has a value inputted
                if gen.value_exists(tag):
                    user_input = gen.existing_value_input(tag, text)

                # tag does not have a value inputted
                else:
                    user_input = input(f"Input {text}: ")

                form.set(name, user_input)  

        return name_attrs_used

    #       fieldset details - functions
    def input_fieldset_details(self, name_attrs):
        """
        User inputs details inside fieldset tags for post.

        Returns a list of name attributes used.
        """
        form = self.select_form()
        soup = self.get_current_page()

        # split tags into their fieldsets
        fieldsets = soup.find_all(gen.fieldset_not_within_fieldset)
        fieldset_objects = create_fieldset_objects(fieldsets, name_attrs)

        for field in fieldset_objects:
            name_attrs = name_attrs + field.return_name_attributes()
            # user inputs for tags inside fieldset
            user_inputs = field.input_values()  
            # inputs for radio and checkbox types
            user_inputs.update(field.input_other_values()) 

            m.set_user_inputs(form, user_inputs)  # sets the user inputs into browser

        return name_attrs



    # STEP 4
    def add_location_to_post(self):
        """
        Step 4 - Add Map - Adding Location to Post.
        
        If the zip code (postal code) is not entered then ask for address.
        The address is then inputted into the browser.
        """
        soup = self.get_current_page()
        form = self.select_form()

        find = soup.find('button', id='search_button')        # button for finding location
        location_inputs = soup.find_all('input', type=False)  # inputs for location

        if m.location_is_set(location_inputs) is False:         # ask for address if not entered
            user_inputs = m.get_user_inputs_for(location_inputs)  # dictionary of user_inputs
            m.set_user_inputs(form, user_inputs) 

        form.choose_submit(find)
        self.submit_selected()
        return None

    
    # STEP 5
    def add_images_to_post(self):
        """
        Step 5 - Add Images.
            # look up how to use PyQt to upload images or drag and drop files

        User is able to upload a total of 24 maximum images.
        Upload the best image first - it will be featured. 
        """
        confirmed = gen.ask_for_confirmation("Would you like to add images? ")
        if confirmed:
            self.add_images_until_limit()

        # finish with uploading images
        button = gen.find_button_with_text(self, 'done with images')

        # continues on to next page
        form = self.select_form(button.parent)
        form.choose_submit(button)
        self.submit_selected()
        return None


    #   step 5 - Add Images - FUNCIONS
    def add_images_until_limit(self):
        """Add images until limit is reached or user is done uploading images."""
        # tag containing image count limit
        img_count = self.get_current_page().find('span', class_="imgcount")   
        limit = int(img_count.text)
        confirmed = True

        
        # button for adding images to form
        button = gen.find_button_with_text(self, 'add image')
        print("Upload the best image first - it will be featured.") 
        
        while confirmed and (limit > 0):
            limit -= 1
            self.add_file(button)        # add image (file) to browser using button
            confirmed = gen.ask_for_confirmation("Would you like to add another image? ")

        return None


    def add_file(self, button):
        """
        Adds a file to a form.
        
        Given a browser and its button associated with the submission of a file.
        Find the form that the button is held in, 
        and find the input tag associated with button (type="file")
        Once the input tag is found, use the form to set the value to the file path.
        """
        path_to_file = input("Copy and Paste the file location: ")

        # simple check: is the value long enough for a file location?
        if len(path_to_file) < 3:
            return None

        name_attribute = gen.find_name_attr_for_add_file_input(button)
        
        # select form containing button
        form = self.select_form(button.parent)     
        form.set(name_attribute, path_to_file)        # add file to form
        form.choose_submit(button)                    # submit file through button
        self.submit_selected()
        
        print(f"File:'{path_to_file}'' has been added.")
        return None


    # STEP 6    
    def edit_draft_of_posting(self):
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
        soup = self.get_current_page()
        forms = soup.find_all('form')

        confirmed = gen.ask_for_confirmation("Would you like to edit draft? ")
        if confirmed:
            button = self.get_edit_button()

        else:
            # publishes the post
            # email gets sent to given email address
            print("No Edits? Okay. Publishing the draft now!")
            # self.submit_()
            print("\tthe post is not being submitted.")
            return None

        # select form containing button
        form = self.select_form(button.parent)
        form.choose_submit(button)
        self.submit_selected()

        self.determine_page()
        return None

    #   editing other pages (details, location, images)
    def get_edit_button(self):
        """Return a button that refers to the user's choice."""
        edit_text = (f"What would you like to edit? (please choose only one)\n"
                        f"\tpost, location, or images?\t")
        user_input = input(edit_text)

        if 'post' in user_input:
            button = gen.find_button_with_text(self, 'edit post')

        elif 'location' in user_input:
            button = gen.find_button_with_text(self, 'edit location')

        elif 'image' in user_input:
            button = gen.find_button_with_text(self, 'edit images')

        return button



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
        self.name_attributes = gen.get_name_attributes(self.tags)

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



class CreatePost():
    """
    Contains the methods used to 'Create A Post' on Craigslist.
    """
    def __init__(self, browser=mechanicalsoup.StatefulBrowser()):
        self.browser = browser
        self.browser.open("https://batonrouge.craigslist.org/")
        self.browser.follow_link(id='post')        # 'create a post' link

        # start GUI stuff
        #self.app = QApplication([])
        #self.window = GUI.Window(browser)
        #self.app.exec_()


class QuickCreatePost(CreatePost):
    """
    Contains the methods used to quickly 'Create A Post' on Craigslist.
    For Sale By Owner - Video Games - Post
    """
    def game_post(self, step_num):
        """Quick Way to move through steps while debugging."""
        if step_num >= 1:
            print("Step 1 - Choose Type of Posting")
            self.choose_type_of_posting_gaming()
            
        if step_num >= 2:
            print("Step 2 - Choose A Category")
            self.choose_category_gaming()
            
        if step_num >= 3:
            print("Step 3 - Create Posting - Enter Details")
            self.add_details_gaming()
            
        if step_num >= 4:
            print("Step 4 - Add Map - Adding Location to Post")
            self.add_location_to_post()
            
        if step_num >= 5:
            print("Step 5 - Add Images")
            self.add_images_to_post()
            
        return None

    def gaming_post(self):
        """Quick Way to move to Step 6 - Edit Draft - while debugging."""
        try:
            print("Step 1 - Choose Type of Posting")
            self.choose_type_of_posting_gaming()
            
            print("Step 2 - Choose A Category")
            self.choose_category_gaming()

            print("Step 3 - Create Posting - Enter Details")
            self.add_details_gaming()

            print("Step 4 - Add Map - Adding Location to Post")
            self.add_location_to_post()
            
            print("Step 5 - Add Images")
            self.add_images_to_post()
            
            self.browser.launch_browser()

        except Exception as error:
            print(f"An error occurred: {str(error)}")

        return None

    def choose_type_of_posting_gaming(self):
        """
        Step 1 - Choose Type of Posting - for sale by owner
        """
        form = self.browser.select_form()
        user_input = {'id':'fso'}
        form.set_radio(user_input)
        self.submit_()                    
        return None

    def choose_category_gaming(self):
        """
        Step 2 - Choose Category.

        Given a choice of 'for sale by owner' from Step 1, select the option with:
            'cars & trucks'
            'video gaming'  - currently using this
        """
        form = self.browser.select_form()
        user_input = {'id':'151'}
        form.set_radio(user_input)
        self.submit_()
        return None

    def add_details_gaming(self):
        """Subsitute for add_details_to_post - Quick Information Input."""
        form = self.browser.select_form()
        info_input = {'PostingTitle':'Selling PS4', 'price':200, 'postal':70808, 'FromEMail':'email@protonmail.com'}
        description = {'PostingBody':'Selling PS4 for $200'}
        info_select = {'language':'5', 'condition':'10'}

        form.set_input(info_input)
        form.set_textarea(description)
        form.set_select(info_select)
        self.submit_()




# functions
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
    """Adds in general missing details."""
    browser.launch_browser()
    form = browser.select_form()

    info_input = {'FromEMail':'email@protonmail.com'}
    email_privacy = {'Privacy':'C'}
    form.set_input(info_input)
    form.set_radio(email_privacy)

    browser.submit_selected()
    return None
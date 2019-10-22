#! /usr/bin/python3

# Craigslist Bot
# Mechanical Soup Implementation
import mechanicalsoup

import mech_functions as m
import general_functions as gen


class CreatePost():
    """
    Contains the methods used to 'Create A Post' on Craigslist.
    """
    def __init__(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.browser.open("https://batonrouge.craigslist.org/")
        self.browser.follow_link(id='post')        # 'create a post' link

        #self.determine_page()                    # starts process            


    def __str__(self):
        return f"This is the object for creating a post on craigslist"

    def __repr__(self):
        return f"Contains the browser and methods for creating a post on craigslist."

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
    
    def create_post(self):
    	"""Starts the process of 'Create A Post'."""
    	self.determine_page()
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
        soup = self.browser.get_current_page()
        forms = soup.find_all('form')        # length of forms gives a hint towards page
        title_text = soup.title.text

        if 'type' in title_text or 'category' in title_text:
            self.choose_category()
            self.determine_page()

        elif 'map' in title_text:
            self.add_location_to_post()
            self.determine_page()

        elif 'posting' in title_text and len(forms) == 1:
            self.add_details_to_post()
            self.determine_page()
        
        elif ('posting' in title_text) and (len(forms) == 3):
            self.add_images_to_post()
            self.determine_page()

        elif ('posting' in title_text) and (len(forms) == 8):
            self.edit_draft_of_posting()

        else:
            # not editing post, location or images
            # page was already submitted so only print message
            self.publish_draft_message()

        return None


    def submit(self):
        """
        Submits the current page's form.
        
        Looks for a button 'continue' text, if applicable, and uses that button for submission.
        """
        button = self.browser.get_current_page().find('button', type='submit')
        form = self.browser.select_form()

        if button != None:          # a button was found.
            form.choose_submit(button)
        
        self.browser.submit_selected()       # prompts a follow_link (new page) as well
        return None

    
    # step 1 and step 2
    # Choose Type of Posting and Choose Category are basically the same
    def choose_category(self):
        """
        Step 1 & 2 - Choose Type of Posting or Choose Category.
        """
        print(self.browser.get_current_page().title.text)
        # dictionary = {name_attr:value}
        user_input = m.select_from_radio_options(self.browser)

        form = self.browser.select_form()
        form.set_radio(user_input)
        
        self.submit()
        return None

    
    # step 3
    def add_details_to_post(self):
        """
        Step 3 - Create Posting - Enter Details.
        
        General Required Information:
            Posting Title (name attribute='PostingTitle'):
            Postal Code ('postal'):
            Description ('PostingBody'):
            email ('FromEMail'):
        """
        form = self.browser.select_form()

        m.input_details(self.browser)
        
        # have to choose a privacy option for email 
        email_privacy = {'Privacy':'C'} # CL mail relay (recommended)
        form.set_radio(email_privacy)

        self.submit()

        if details_have_missing_information(self.browser):
            input_missing_details(self.browser)

        return None

    
    # step 4
    def add_location_to_post(self):
        """
        Step 4 - Add Map - Adding Location to Post.
        
        If the zip code (postal code) is not entered then ask for address.
        The address is then inputted into the browser.
        """
        soup = self.browser.get_current_page()
        form = self.browser.select_form()

        find = soup.find('button', id='search_button')        # button for finding location
        location_inputs = soup.find_all('input', type=False)  # inputs for location

        if m.location_is_set(location_inputs) is False:         # ask for address if not entered
            user_inputs = m.get_user_inputs_for(location_inputs)  # dictionary of user_inputs
            m.set_user_inputs(form, user_inputs) 

        form.choose_submit(find)
        self.browser.submit_selected()
        return None

    
    # step 5
    def add_images_to_post(self):
        """
        Step 5 - Add Images.
            # look up how to use PyQt to upload images or drag and drop files

        User is able to upload a total of 24 maximum images.
        Upload the best image first - it will be featured. 
        """
        confirmed = gen.ask_for_confirmation("Would you like to add images? ")
        if confirmed:
            m.add_images_until_limit_or_done(self.browser)

        # continues on to next page
        button = gen.find_button_with_text(self.browser, 'done with images') # finish with uploading images
        form = self.browser.select_form(button.parent)
        form.choose_submit(button)
        self.browser.submit_selected()
        return None
    

    # step 6    
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
        soup = self.browser.get_current_page()
        forms = soup.find_all('form')

        confirmed = gen.ask_for_confirmation("Would you like to edit draft? ")
        if confirmed:
            button = self.get_edit_button()

        else:
            # publishes the post
            # email gets sent to given email address
            print("No Edits? Okay. Publishing the draft now!")
            self.submit()
            return None

        form = self.browser.select_form(button.parent)
        form.choose_submit(button)
        self.browser.submit_selected()

        self.determine_page()
        return None
    

    # editing other pages (details, location, images)
    def get_edit_button(self):
        """Return a button that refers to the user's choice."""
        edit_text = (f"What would you like to edit? (please choose only one)\n"
                        f"\tpost, location, or images?\t")
        user_input = input(edit_text)

        if 'post' in user_input:
            button = gen.find_button_with_text(self.browser, 'edit post')

        elif 'location' in user_input:
            button = gen.find_button_with_text(self.browser, 'edit location')

        elif 'image' in user_input:
            button = gen.find_button_with_text(self.browser, 'edit images')

        return button




class QuickCreatePost(CreatePost):
    """
    Contains the methods used to quickly 'Create A Post' on Craigslist.
    For Sale By Owner - Video Games - Post
    """
    def __init__(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.browser.open("https://batonrouge.craigslist.org/")
        self.browser.follow_link(id='post')        # 'create a post' link


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
        self.submit()                    
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
        self.submit()
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
        self.submit()




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
# GUI Classes (and their Methods) and Functions
import PyQt5.QtWidgets as Qt
import mechanicalsoup
import sys


import mech_class as mech
import general_functions as gen


class Window(Qt.QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.initVariables()
        self.initUI()

        self.continueButton.clicked.connect(self.Continue)
        self.chooseButton.clicked.connect(self.begin_from_scratch)

        self.resize(self.sizeHint())
        self.show()


    def initVariables(self):
        """
        Initialized variables for use through process.

        # maybe, instead initialize variables during the step needed.
        """
        # list containing pairs of Labels and QWidgets (Label, QWidget)
        self.labels_and_widgets = [] 
        # user inputted data 
        self.selected_options = []
        # user dictionary
        self.user_dict = {}


    def initUI(self):
        """
        Initialize UI

        Posting Group:
            General Information for Post

        Alternative Button:
            A Button "Start With 'Choose Type'" (disregards inputted general info)

        Continue Button:
            With inputted general information, the Bot will determine what the user
            wants to post and ask for more information if needed. 
        """
        self.setWindowTitle("Craigslist Bot")
        self.mainlayout = Qt.QGridLayout()

        # Central Widget - Needed for QMainWindow
        central_widget = Qt.QWidget()
        central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(central_widget)

        self.createPostingGroup()
        self.createContinueButton()
        self.createAlternativeButton()

        self.mainlayout.addWidget(self.postingGroup, 0, 0, 1, -1)
        self.mainlayout.addWidget(self.chooseButton, 1, 0)
        self.mainlayout.addWidget(self.continueButton, 1, 1)


    def createContinueButton(self):
        """
        Create Continue Button
        """
        self.continueButton = Qt.QPushButton('&Continue')
        self.continueButton.setDefault(True)
        self.continueButton.resize(self.continueButton.sizeHint())


    def createAlternativeButton(self):
        """
        Create button 'Choose Type of Posting' for starting 'create a post' process.
        """
        self.chooseButton = Qt.QPushButton("Choose Type of Posting")
        self.chooseButton.resize(self.chooseButton.sizeHint())


    def createPostingGroup(self):
        """
        Group for:
            Posting Title
            Price    (if 0, no price)
            City or Neighborhood
            Postal Code
            Description

        For each item in group, there is a QLabel and a QWidget.
        """
        self.postingGroup = Qt.QGroupBox('General Posting Details')

        titles = ['Posting Title', 'Price', 'City or Neighborhood', 'Postal Code']
        description = 'Description'
        posting_inputs = []

        grid_layout = Grid()
        grid_layout.addInputs_Labels(titles)
        grid_layout.addInputs_Labels(description)

        self.postingGroup.setLayout(grid_layout)

        self.labels_and_widgets += grid_layout.pairs     # .pairs variable of Grid()


    def createCategoryGroup(self, tags_and_text, title):
        """
        Group is for Choose Type or Category of Posting.

        The group will contain radio buttons for the options given.        

        tags_and_text = [(tag, text), (tag, text)]
        """
        options = Options(tags_and_text, title)

        # Controls when the application takes the selected option
        # when the options widget is closed, then the application can take it
        if options.exec_():
            print(options.selected)
            self.selected_options.append((title, options.selected))

        #self.mainLayout.addWidget(self.categoryGroup)


    def Continue(self):
        """Determine the type of post the user wants from the inputted information."""
        print("User chooses to continue with inputted information.")
        self.gather_info(self.labels_and_widgets)
        self.determine_type_of_posting()

        return None


    def gather_info(self, widget_list):
        """
        Gather info from QLineEdits, QPlainText, and QSpinBox

        widget_list = [(label, widget), (label, widget), ..., (label, widgets)]
        """
        for label,widget in widget_list:
            lower_label = label.lower()

            if 'price' in lower_label:
                value = widget.value()
                if value != 0:
                    self.user_dict.update({label:value})

            elif 'description' in lower_label:
                self.user_dict.update({label:widget.toPlainText()})

            else:
                self.user_dict.update({label:widget.text()})

        return None


    def determine_type_of_posting(self):
        """
        Determine type of posting with user inputted values.

        Along with user inputs, 
        go through saved data of previous postings.
        """
        # do something with browser
        pass


    def begin_from_scratch(self):
        """Go to 'Choose Type of Posting' for 'create a post' process.

        Have to find a way to tell 'CreatePost' object to move to
        the 'choose type of posting' step of process.
        then call the createCategoryGroup() function to create radio options within GUI.
        """
        self.browser = mech.Browser()
        self.gather_info(self.labels_and_widgets)
        self.create_a_post_loop()
        return None


    def create_a_post_loop(self):
        """Starts the process for 'Create A Post'.

        Main Loop - New Page Equal New Round
            Gather info (input tags) from browser page
            determine action to take (based on input tags)
            create new object (window) for inputting/selecting values
        """
        print("create a post loop")
        while self.browser.in_progress:
            function_name = self.browser.determine_page()
            self.browser_function(function_name)
        return None


    def browser_function(self, function_name):
        """
        Hub for calling browser functions.
        """
        print("\tBrowser function")
        if function_name == 'category':
            self.browser_choose_category()

        elif function_name == 'details':
        	self.browser_add_details()

        elif function_name == 'map':
        	self.browser_add_location()

        elif function_name == 'images':
        	self.browser_add_images()

        elif function_name == 'edit':
        	self.browser_edit_draft()

        else:
            print("end of 'create a post' process")

        return None


    def browser_choose_category(self):
        """
        Browser function for 'Choose Type' or 'Choose Category of Post'
        """
        print("\t\tBrowser choose category")
        title = self.browser.get_current_page().title.text
        tags, labels = self.browser.display_categories_of_post()

        popup = Options(tags, labels, title)
        popup.exec_()
        #selection = (title, popup.selected)
        self.browser.select_radio_button2(tags[0], popup.selection)

        return None


    def browser_add_details(self):
    	pass

    def browser_add_images(self):
    	pass

    def browser_add_location(self):
    	pass

    def browser_edit_draft(self):
    	pass


    def close_application(self):
        """Closes program."""
        choice = Qt.QMessageBox.question(self, 'Exit!', 
                                            "Would you like to exit?",
                                            Qt.QMessageBox.No | Qt.QMessageBox.Yes)
        if choice == Qt.QMessageBox.Yes:
            print("Exit Now!")
            sys.exit()
        else:
            pass





# USED FOR RADIO BUTTON OPTIONS
class Options(Qt.QDialog):

    def __init__(self, tags=[], labels=[], 
                 title='select one of the options', parent=None):

        super().__init__()
        self.tags = tags
        self.labels = labels
        self.title = title
        self.selection = '' # selected option (real value)

        self.options_layout = Qt.QVBoxLayout()

        self.createRadioButtons()
        self.createValueDictionary()
        self.createContinueButton()
        self.setLayout(self.options_layout)

        self.resize(self.sizeHint())
        #self.show()

        self.continueButton.clicked.connect(self.submitChoice)


    def createRadioButtons(self):
        """
        Create Radio Buttons

        Limit Size of Widget depending on length of tags
        """
        layout = determine_layout(len(self.tags))
        radioGroup = Qt.QGroupBox(self.title)

        self.radioButtonGroup = Qt.QButtonGroup()
        self.radioButtonGroup.setExclusive(True)

        if type(layout) != type(Qt.QVBoxLayout()):
            layout = self.createRadioButtonsGrid(layout)

        else:
            layout = self.createRadioButtonsVBox(layout)

        radioGroup.setLayout(layout)
        self.options_layout.addWidget(radioGroup)
        return None


    def createRadioButtonsGrid(self, layout):
        """Split radio buttons into columns of 10."""
        local_layout = Qt.QVBoxLayout()
        column = 0

        for id_num, label in enumerate(self.labels):
            radio_button = Qt.QRadioButton(label)
            self.radioButtonGroup.addButton(radio_button, id_num)

            if local_layout.count() < 12:
                local_layout.addWidget(radio_button)

            else:
                layout.addLayout(local_layout, 0, column)
                column += 1
                local_layout = Qt.QVBoxLayout()
                local_layout.addWidget(radio_button)

        layout.addLayout(local_layout, 0, column)
        return layout


    def createRadioButtonsVBox(self, layout):
        """Add all radio buttons under one QVBoxLayout"""
        for id_num, label in enumerate(self.labels):
            radio_button = Qt.QRadioButton(label)
            layout.addWidget(radio_button)
            self.radioButtonGroup.addButton(radio_button, id_num)
        return layout


    def createValueDictionary(self):
        """
        Create dictionary of radio button labels and their 'real' value.
        """
        self.dictionary = {}
        for x in range(len(self.tags)):
            real_value = gen.get_attribute_string(self.tags[x], 'value')
            self.dictionary.update({self.labels[x]:real_value})
        return None


    def createContinueButton(self):
        """
        Create Continue Button
        """
        self.continueButton = Qt.QPushButton('&Continue')
        self.continueButton.setDefault(True)
        self.continueButton.resize(self.continueButton.sizeHint())

        self.options_layout.addWidget(self.continueButton)


    def submitChoice(self):
        """Set the Selected Radio Button."""
        radio_button = self.radioButtonGroup.checkedButton()

        if radio_button != None:
            # obtain real value of selected radio button
            self.selection = self.dictionary[radio_button.text()]
            self.close_application()

        else:
            print('Nothing to submit.\tSelect an option to continue.')


    def close_application(self):
        """Closes this widget."""
        choice = Qt.QMessageBox.question(self, 'Next Step!', 
                                         "Would you like to continue to next step?",
                                         Qt.QMessageBox.Yes | Qt.QMessageBox.No)
        if choice == Qt.QMessageBox.Yes:
            print("Continuing to next step!")
            self.done(0)
        else:
            pass


def determine_layout(length):
    if length > 12:
        return Qt.QGridLayout()
    else:
        return Qt.QVBoxLayout()

def split_pairs(list1):
    first = []
    second = []
    for element in list1:
        first.append(element[0])
        second.append(element[1])
    return first, second

def remove_text(orginal, remove_string):
    """Remove a subset of the original string."""
    if remove_string in original:
       pass 
    else:
        print(f"{remove_string} is not a subset of {original}")




class Grid(Qt.QGridLayout):
    def __init__(self):
        super().__init__()
        self.pairs = []


    def addInputs_Labels(self, labels):
        """
        Create Labels and Inputs for given list of labels.

        1st Row Added - QLabel
        2nd Row Added - QWidget

        Add (Label, QWidget) to list of pairs (self.pairs)

        Return None
        """
        row = determine_row(self)

        if type(labels) == type(''):
            self.addLabel(labels, row)
            widget = self.addInput(labels, row+1)

            self.pairs.append((labels, widget))
            return None

        for column,label in enumerate(labels):
            self.addLabel(label, row, column)
            widget = self.addInput(label, row+1, column)

            self.pairs.append((label, widget))         

        return None



    def addLabel(self, label, row=0, column=0):
        """
        Add QLabel to Grid Layout
        """
        self.addWidget(Qt.QLabel(label), row, column)

        return None


    def addInput(self, label, row=0, column=0):
        """
        Add QWidget to Grid Layout

        Return QWidget
        """
        text = label.lower()

        if 'description' in text:
            widget = Qt.QPlainTextEdit()
            # .addWidget(QWidget, int row, int column, int rowSpan, int columnSpan)
            #     rowSpan = 1 (widget spans only one row)
            #     columnSpan = -1 (widget spans to the right edge)
            self.addWidget(widget, row, column, 1, -1)

        elif 'price' in text:
            widget = Qt.QSpinBox()
            widget.setRange(0,10000)
            self.addWidget(widget, row, column)

        elif 'title' in text:
            widget = Qt.QLineEdit()
            self.addWidget(widget, row, column)
            self.setColumnStretch(column, 3)

        else:
            widget = Qt.QLineEdit()
            self.addWidget(widget, row, column)
        
        return widget



def determine_row(layout):
    """
    Given a Grid layout, find which row to add to. 
    """
    count = layout.count()
    row = layout.rowCount()

    # add to first row (0) when there are no items in layout
    if (row == 1) and (count == 0):
        return 0

    # add to second row (1) when there are items in layout and row is still 1.
    elif (row == 1) and (count > 0):
        return 1

    # add to given row
    else:
        return row

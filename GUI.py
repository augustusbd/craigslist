# GUI Classes (and their Methods) and Functions
import PyQt5.QtWidgets as Qt
import sys

class Window(Qt.QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        # pairs of Labels and QWidgets
        self.labels_and_widgets = []
        self.selected_options = []

        self.mainlayout = Qt.QGridLayout()
        self.initUI()
        # Central Widget - Needed for QMainWindow
        central_widget = Qt.QWidget()
        central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(central_widget)

        self.continueButton.clicked.connect(self.NextStep)
        self.chooseButton.clicked.connect(self.Beginning)

        self.resize(self.sizeHint())
        self.show()


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

        layout = Grid()
        layout.addInputs_Labels(titles)
        layout.addInputs_Labels(description)

        self.postingGroup.setLayout(layout)

        self.labels_and_widgets += layout.pairs


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


    def NextStep(self):
    	"""Determine the type of post the user wants from the inputted information."""
    	print("User chooses to continue with inputted information.")


    def Beginning(self):
    	"""Go to 'Choose Type of Posting' for 'create a post' process.

		Have to find a way to tell 'CreatePost' object to move to
		the 'choose type of posting' step of process.
		then call the createCategoryGroup() function to create radio options within GUI.
    	"""
    	print("Choose type of posting from radio button options.")


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

    def __init__(self, tags_and_labels, 
                    title='select one of the options', parent=None):

        super().__init__()
        self.title = title
        self.tags, self.labels = split_pairs(tags_and_labels)

        self.selected = []

        self.options_layout = Qt.QVBoxLayout()

        self.createRadioButtons()
        self.createContinueButton()
        self.setLayout(self.options_layout)

        self.resize(self.sizeHint())
        self.show()

        self.continueButton.clicked.connect(self.submitChoice)


    def createRadioButtons(self):
        """
        Create Radio Buttons
        """
        layout = Qt.QVBoxLayout()
        radioGroup = Qt.QGroupBox(self.title)

        self.radioButtonGroup = Qt.QButtonGroup()
        self.radioButtonGroup.setExclusive(True)

        if self.labels and len(self.labels) >= 1:

            for id_num, label in enumerate(self.labels):
                radio_button = Qt.QRadioButton(label)
                layout.addWidget(radio_button)
                self.radioButtonGroup.addButton(radio_button, id_num)

        radioGroup.setLayout(layout)
        self.options_layout.addWidget(radioGroup)
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
            self.selected = radio_button.text()
            self.close_application()

        else:
            print('Nothing to submit.')


    def close_application(self):
        """Closes this widget."""
        choice = Qt.QMessageBox.question(self, 'Exit!', 
                                            "Would you like to exit?",
                                            Qt.QMessageBox.Yes | Qt.QMessageBox.No)
        if choice == Qt.QMessageBox.Yes:
            print("Exit Now!")
            self.accept()
        else:
            pass




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

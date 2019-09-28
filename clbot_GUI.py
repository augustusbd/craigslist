#! /usr/bin/python3

# Craigslist Bot
# GUI Class and Methods

from PyQt5.QtWidgets import (QDialog, QApplication, QLabel,
        QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout,
        QLineEdit, QPlainTextEdit, QSpinBox, QPushButton,
        QComboBox )
import sys
import math



class StartWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Craigslist Bot")
        #self.resize(800,400)
        
        layout = QVBoxLayout()
        
        intro = QLabel("Hello, I'm the Craigslist Bot!")
        question = QLabel("Would you like to make a post?")
        
        self.create_yes_no()
        
        layout.addWidget(intro)
        layout.addWidget(question)
        layout.addWidget(self.yes_no)
        self.setLayout(layout)
        # Hello, I'm the Craigslist Bot!
        # Would you like to make a post?
        #   No - I'm sorry, I can only make posts for now. Goodbye!
        #   Yes - What type of program?
        #       [m]echanicalsoup or [s]elenium?
        
        self.yes_no.currentIndexChanged.connect(self.answer)
        
        
    def create_yes_no(self):
        self.yes_no = QComboBox()
        self.yes_no.addItems(['yes','no'])   
    
    def answer(self, index):
        print(self.yes_no.itemText(index))


###################################

class PostWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Create A Post")
        self.resize(800,400)
        self.all_pairs = []
        
        # Create Top Group For:
        # Posting Title, Price, City, Postal Code, Description
        self.createTopGroup()

        # Create Submit Button
        self.createSubmit()
        
        # MAIN GROUP - Top Layer
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.topGroup)         # add Top Group - Price, City, Description
        self.mainLayout.addWidget(self.submitButton)     # add Submit Button
        self.setLayout(self.mainLayout)
        #self.current_row = 2                              # always start adding to grid at column 0
        # Check For Submission
        self.submitButton.clicked.connect(self.submitDetails)
        
        
    def createSubmit(self):
        """ Submit Posting Details """
        self.submitButton = QPushButton('&Submit')
        self.submitButton.setDefault(True)

    def submitDetails(self):
        """ Grabs the Inputted Details """
        print("Submit Connection Worked!")
        self.InputText = self.grabText(self.all_pairs)  # create dictionary pairs of labels and inputs
        
        # Adds Description to dictionary pairs
        print(self.InputText)
        
    
    def createTopGroup(self):
        """
        QLabel for titles
            Posting Title           - QLineEdit
            Price                   - QSpinBox
            City or Neighborhood    - QLineEdit
            Postal Code             - QLineEdit
            Description             - QPlainTextEdit
        """
        self.topGroup = QGroupBox()             # general info for post
        titles = ['Posting Title', 'Price', 'City or Neighborhood', 'Postal Code']
        description = 'Description'
        layout = QGridLayout()
        # Labels and Inputs for: Posting Title, Price, City, Postal Code
        self.addGridLabels(layout,0,titles)                 # QLabels to 1st row
        top_inputs = self.addGridInputs(layout,1,titles)    # QLineEdits & QSpinBox to 2nd row
        # Label and Input for: Description
        self.addGridLabels(layout,2,description)            # QLabel to 3rd row
        top_inputs = top_inputs + self.addGridInputs(layout,3,description) #QPlainTextEdit to 4th row
        
        self.topGroup.setLayout(layout)
        # Pairing Labels with Inputs
        # [(label, input), (title,input), ...]
        labels = titles + [description]
        top_pairs = list(group_list(pair(labels, top_inputs), 2))
        
        # Add Input Pairs to Main Pairs
        self.all_pairs = self.all_pairs + top_pairs

    def createGroup(self, group, group_name):
        """
        Given a dictionary (group), and its title (group_name)
            For each key in group, there is a value containing a list
            e.g.
                group = {'key1': ['value1','value2','value3'],
                         'key2': ['value4','value5','value5'] }
        Create A QGroupBox
            a layout of QGridLayout  # nx2 Grid
              - each index of grid belongs to one key from group
              e.g. the dictionary is divided by its keys into a grid
                grid[0][0] = group['key1']
                grid[0][1] = group['key2']  
            within each index of grid, there is a subgroup
              - subgroups are created from the values of group[key]
              e.g. 
                value = group['key1']
                subGroup = self.createSubGroup(value)    
            once the subgroup is created, it is added to the grid layout
            this occurs for each key within group.
            
        All SubGroups Created and Added to GridLayout of GroupBox
        Add GroupBox to MainLayout
        Set the Layout of the Main Window to MainLayout again
        """
        box = QGroupBox(group_name)
        num = len(group)
        num_of_rows = math.ceil(num/2)       # number of rows from length of group
        pure_rows = math.floor(num/2)        # whole number; # of rows with 2 columns used
        unpure_rows = math.ceil(num_of_rows - pure_rows) # either 0 or 1; a row with one column used 

        layout = QGridLayout()        
        names = list(group)         # list of tag names; e.g. ['input', 'select']
        pos = 0                     # position of tag name; 0 for 'input', 1 for 'select'
        # Create SubGroup per key of group  
        x = 0                                   # row number
        while x < pure_rows:                    # create rows with 2 columns
            for y in range(2):
                key = names[pos]
                value = group[key]
                subGroup = self.createSubGroup(value)
                #print("Row: " + str(x) + "& Col: " + str(y))                
                layout.addLayout(subGroup,x,y)   # add subGroup to GridLayout
                pos = pos + 1
            x = x + 1
        for y in range(unpure_rows):            # create a 1 column row or nothing
            key = names[pos]
            value = group[key]
            subGroup = self.createSubGroup(value)
            layout.addLayout(subGroup,x,y)
            #print("Extra row of " + str(y) + " column(s)")
        box.setLayout(layout)
        self.mainLayout.addWidget(box)
        self.setLayout(self.mainLayout)


    def createSubGroup(self, group_items):
        """ 
        Given a list.
            For each index of list
                creat a QWidget
                add it to QLayout
            e.g.
                group_items = list of tags with same name;
                [<input ... />, <input ... />, <input ... />]
        Create A QVBoxLayout
            for each item in the list:
                create a QLabel and add it to the box layout
                create a QWidget and add it to the box layout
        Retuns a QVBoxLayout 
        """ 
        sub_inputs = []
        sub_labels = []
        sublayout = QVBoxLayout()
        if group_items[0].name == 'input':
            for x,item in enumerate(group_items):
                # Add Label
                name = item.get_attribute_list('name')[0]  # list; first index for string value
                sublayout.addWidget(QLabel(name))
                sub_labels.append(name)                     # add text not actually QLabel
                # Add LineEdit (Input)
                sub_inputs.append(QLineEdit())
                sublayout.addWidget(sub_inputs[x])
                 
        elif group_items[0].name == 'select':
            # for each tag in the 'select' list
            for item in group_items:
                # create a dropdown menu widget
                dropdown = QComboBox()
                # Add Label                  
                name = item.get_attribute_list('name')[0]
                sublayout.addWidget(QLabel(name))           # label the dropdown menu
                sub_labels.append(name)
                # Drop Down Options
                options_list = give_dropdown_options(item) # get a list of dropdown options w/in tag
                options_list = remove_emptys(options_list) # list without empty indexes
                dropdown.addItems(options_list)            # adds list of strings as drop down items
                # Add Drop Down Menu (Input)
                sublayout.addWidget(dropdown)
                sub_inputs.append(dropdown)
        # Pairing Labels (text) with Inputs
        # [(label,input), (label,input)]
        sub_pairs = list(group_list(pair(sub_labels, sub_inputs), 2))
        self.all_pairs = self.all_pairs + sub_pairs
        return sublayout


    def grabText(self, pairs):
        """"
        Grabs the information entered into GUI
            Takes a list of tuples (pairs)
                [('Posting Title', QLineEdit()), ('Price', QSpinBox()), ...]
            Splits the labels and input text into a dictionary
                {'Posting Title':'Selling Car', 'Price':2000, ...}
        Returns a dictionary of pairs
        """
        inputText = {}
        for x in range(len(pairs)):
            label = pairs[x][0]
            # Grabs Input Text from QLineEdit & QPlainText
            if label != 'Price':
                if label == 'Description':
                    text = self.description.toPlainText()
                    inputText[label] = text
                else:
                    text = pairs[x][1].text()
                    inputText[label] = text
            else:
                text = pairs[x][1].value()
                inputText[label] = text
        return inputText
        

    def addGridLabels(self, layout, row, label_text):
        """
         Add Labels to a Specific Row in Grid Layout
            - using the layout given, 
              add Widgets of created QLabels using label_text
        """
        labels = []
        if type(label_text) == type(labels):
            for column,string in enumerate(label_text):
                layout.addWidget(QLabel(string), row, column)
        elif type(label_text) == type('string'):
            if label_text == 'Description':
                layout.addWidget(QLabel(label_text), row, 0)
            else:
                print("This is a string type but not 'Description'.")
        else:
            print("This is not a list type or string type.")
        return None



    def addGridInputs(self, layout, row, label_text):
        """
        Add Inputs to a Specific Row within Grid Layout
        Returns a list of QWidgets
        """
        input_boxes = []
        if type(label_text) == type(input_boxes): 
            for column,string in enumerate(label_text):
                if string == 'Price':
                    priceBox = QSpinBox()
                    priceBox.setRange(100,10000)
                    priceBox.setValue(2000)
                    input_boxes.append(priceBox)
                    layout.addWidget(input_boxes[column], row, column)
                elif string == 'Posting Title':
                    input_boxes.append(QLineEdit())
                    layout.addWidget(input_boxes[column], row, column)
                    layout.setColumnStretch(column,3)
                else:
                    input_boxes.append(QLineEdit())
                    layout.addWidget(input_boxes[column], row, column)
        elif type(label_text) == type('string'):
            if label_text == 'Description':
                # self.description = QPlainTextEdit(self)
                # layout.addWidget(self.description, row, 0)    add to 'row' row, and 0 column
                # layout.setColumnStretch(0
                self.description = QPlainTextEdit(self)
                input_boxes.append(self.description)
                layout.addWidget(self.description, row, 0, 1, -1)  # textedit at row,column=0
                                                 # rowSpan=1 (should be only one row)
                                                 # columnSpan=-1 (should extend to right edge)
        return input_boxes
        
############################## END OF POST WIDGET CLASS ############################################


class GroupWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        # Create Group
        self.groupLayout = QGridLayout()
        self.all_pairs = []
        
    def throwin_info(self, grouping, group_name):
        self.setWindowTitle(group_name)
        self.createWindow(grouping)

    def createWindow(self, group):
        num = len(group)
        num_of_rows = math.ceil(num/2)
        pure_rows = math.floor(num/2)
        unpure_rows = math.ceil(num_of_rows - pure_rows)
        names = list(group)
        pos = 0
        x = 0
        while x < pure_rows:
            for y in range(2):
                key = names[pos]
                value = group[key]
                subGroup = self.createSubGroup(value)
                self.groupLayout.addLayout(subGroup,x,y)
                pos = pos + 1
            x = x + 1
        for y in range(unpure_rows):
            key = names[pos]
            value = group[key]
            subGroup = self.createSubGroup(value)
            self.groupLayout.addLayout(subGroup,x,y)
        self.setLayout(self.groupLayout)

    def createSubGroup(self, group_items):
        sub_inputs = []
        sub_labels = []
        sublayout = QVBoxLayout()
        if group_items[0].name == 'input':
            for x,item in enumerate(group_items):
                # Add Label
                name = item.get_attribute_list('name')[0]  # list; first index for string value
                sublayout.addWidget(QLabel(name))
                sub_labels.append(name)                     # add text not actually QLabel
                # Add LineEdit (Input)
                sub_inputs.append(QLineEdit())
                sublayout.addWidget(sub_inputs[x])  
        elif group_items[0].name == 'select':
            # for each tag in the 'select' list
            for item in group_items:
                # create a dropdown menu widget
                dropdown = QComboBox()
                # Add Label                  
                name = item.get_attribute_list('name')[0]
                sublayout.addWidget(QLabel(name))           # label the dropdown menu
                sub_labels.append(name)
                # Drop Down Options
                options_list = give_dropdown_options(item) # get a list of dropdown options w/in tag
                options_list = remove_emptys(options_list) # list without empty indexes
                dropdown.addItems(options_list)            # adds list of strings as drop down items
                # Add Drop Down Menu (Input)
                sublayout.addWidget(dropdown)
                sub_inputs.append(dropdown)
        # Pairing Labels (text) with Inputs
        # [(label,input), (label,input)]
        sub_pairs = list(group_list(pair(sub_labels, sub_inputs), 2))
        self.all_pairs = self.all_pairs +  sub_pairs
        return sublayout


############################ END OF GROUP WIDGET CLASS ##############################################



############### General Functions #############################
def group_list(list1, n):
    """
    Items in a list are grouped together
        group an iterable into an n-tuples iterable.
        incomplete tuples are discared. e.g.:
            >>> list(group(range(10), 3))
            [(0,1,2), (3,4,5), (6,7,8)]
        Yields a list of n-tuples
    """
    for x in range(0, len(list1), n):
        val = list1[x:x+n]
        if len(val) == n:
            yield tuple(val)

def pair(list1, list2):
    """
    Takes two lists and pairs their indexes together
        Returns a list (combination of both lists)
        ex:
            list1 = ['a', 'b', 'c']
            list2 = [1, 2, 3]
            pairs = ['a', 1, 'b', 2, 'c', 3]    
    """
    pairs = []
    for x in range(len(list1)):
        pairs.append(list1[x])
        pairs.append(list2[x])
    return pairs

def determine_rows(num_of_items, num_of_cols):
    """ 
    Return 3 variables determing rows:
        num_rows = number of rows
        pure_rows = number of rows with maximum # of columns (num_of_cols)
        unpure_rows = number of rows without max # of cols
    """
    num_of_rows = math.ceil(num_of_items/num_of_cols)
    pure_rows = math.floor(num_of_items/num_of_cols)
    unpure_rows = math.ceil(num_of_rows - pure_rows)
    return num_rows, pure_rows, unpure_rows
    
def give_dropdown_options(tag):
    """ Returns the drop down options of tag """
    list_ = []
    for child in tag.children:
        list_.append(child.string)
    return list_

def remove_emptys(list1):
    """ Return a list without any empty indexes."""
    new_list = []
    for x in range(len(list1)):
        if (len(list1[x])) != 0 and (list1[x] != '\n'):
            new_list.append(list1[x])
    return new_list

#################################### Testing PostWidet() #########################################
def main():
    app = QApplication([])
    post = PostWidget()
    post.show()
    enter = input("Enter anyting to contine. ")
    #group = {'key1': ['value1','value2','value3'], 'key2': ['value4','value5','value6'] }
    #post.createGroup(group, 'GROUP')
    sys.exit(app.exec_())  


if __name__ == '__main__':
    main()
    


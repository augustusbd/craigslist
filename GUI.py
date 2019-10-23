# GUI Class and Methods
from PyQt5.QtWidgets import (QDialog, QApplication, QLabel,
							QGroupBox, QGridLayout, QVBoxLayout,
							QButtonGroup, QRadioButton,
							QSpinBox, QLineEdit, QPlainTextEdit
							)

class Main(QDialog):

	def __init__(self, parent=None):
		super().__init__()
		# pairs of Labels and QWidgets
		self.labels_and_widgets = []
		self.buttons = []

		self.initUI()

		self.buttons.buttonClicked()

	def initUI(self):
		self.setWindowTitle("Craigslist Bot")

		# Posting Group - Posting Title, Description, City, etc.
		self.createPostingGroup()

		# MAIN LAYOUT 
		self.mainLayout = QGridLayout()
		self.mainLayout.addWidget(self.postingGroup)

		self.setLayout(self.mainLayout)


	def createCategoryGroup(self, title, tags_and_text):
		"""
		Group for: listing radio options

		Choose Type or Category of Posting

		tags_and_text = [(tag, text), (tag, text)]
		"""
		self.categoryGroup = QGroupBox(title)
		self.buttonGroup = QButtonGroup()
		layout QVBoxLayout()

		for x,(tag, text) in enumerate(tags_and_text):
			# recommended to assign only positive ids
			rb = QRadioButton(text)
			buttonGroup.addButton(rb, x+1)
			layout.addWidget(rb)

		self.buttons.append(buttonGroup)

		self.categoryGroup.setLayout(layout)
		self.mainLayout.addWidget(self.categoryGroup)




	def createPostingGroup(self):
		"""
		Group for:
			Posting Title
			Price	(if 0, no price)
			City or Neighborhood
			Postal Code
			Description
		"""
		self.postingGroup = QGroupBox()

		titles = ['Posting Title', 'Price', 'City or Neighborhood', 'Postal Code']
		description = 'Description'
		posting_inputs = []

		layout = Grid()
		layout.addInputs_Labels(titles)
		layout.addInputs_Labels(description)

		self.postingGroup.setLayout(layout)

		self.labels_and_widgets += layout.pairs



class Grid(QGridLayout):
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
		self.addWidget(QLabel(label), row, column)

		return None


	def addInput(self, label, row=0, column=0):
		"""
		Add QWidget to Grid Layout

		Return QWidget
		"""
		text = label.lower()

		if 'description' in text:
			widget = QPlainTextEdit()
			# .addWidget(QWidget, int row, int column, int rowSpan, int columnSpan)
			# 	rowSpan = 1 (widget spans only one row)
			# 	columnSpan = -1 (widget spans to the right edge)
			self.addWidget(widget, row, column, 1, -1)

		elif 'price' in text:
			widget = QSpinBox()
			widget.setRange(0,10000)
			self.addWidget(widget, row, column)

		elif 'title' in text:
			widget = QLineEdit()
			self.addWidget(widget, row, column)
			self.setColumnStretch(column, 3)

		else:
			widget = QLineEdit()
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
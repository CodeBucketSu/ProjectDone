

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from TodoItemModel import *

class ProjectDoneWin(QMainWindow):
	''' '''
	def __init__(self, parent=None):
		super(ProjectDoneWin, self).__init__(parent)

		#=======================================
		# Set central widget
		#=======================================
		self.setWindowTitle('Project Done')
		self.setWindowIcon(QIcon('icon/ProjectDone.png'))
		centralWidget = QWidget()
		self.hbox = QHBoxLayout()
		
		# set the treeView
		self.treeView = QTreeView()
		model = TodoItemModel()
		model.load()
		self.treeView.setModel(model)

		# add the treeview to layout
		self.hbox.addWidget(self.treeView)	
		centralWidget.setLayout(self.hbox)
		self.setCentralWidget(centralWidget)

		#=======================================
		# Set statusbar
		#=======================================
		self.statusbar = self.statusBar()

		#=======================================
		# Set actions
		#=======================================
		# Add a new todo item.
		tipText = 'New todo item.'
		newAction = self.createAction('&New todo item', \
				self.newItem, 'Ctrl+N', 'icon/newItem.png',\
				tipText, False)

		# Add a new sub item.
		tipText = 'Add sub item.'
		addSubAction = self.createAction('&Add sub item', \
				self.addSubItem, 'Ctrl+A', 'icon/newSubItem.png',\
				tipText, False)

		# Check the item.
		tipText = 'Todo item finished.'
		checkAction = self.createAction('&Check todo item', \
				self.checkItem, 'Ctrl+C', 'icon/check.png',\
				tipText, False)

		# Delete the item.
		tipText = 'Delete todo item.'
		deleteAction = self.createAction('&Delete todo item', \
				self.deleteItem, 'Ctrl+D', 'icon/deleteItem.png',\
				tipText, False)

		# Save the edits.
		tipText = 'Save the edits.'
		saveAction = self.createAction('&Save the edits', \
				self.saveEdit, 'Ctrl+S', 'icon/saveEdit.png',\
				tipText, False)
		
		#=============================================
		# Set the tool bar
		#=============================================
		itemToolBar = self.addToolBar("Item")
		itemToolBar.setObjectName("ItemToolBar")
		self.addActions(itemToolBar, (newAction, addSubAction, \
						checkAction, deleteAction, saveAction))


	def createAction(self, text, slot, shortcut=None, 
						icon=None, tip=None, checkable=False, 
						signal="triggered()"):
		'''This is a action_helper helps to create an action'''
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(icon))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			self.connect(action, SIGNAL(signal), slot)
		if checkable:
			action.setCheckable(True)
		return action


	def addActions(self, target, actions):
		'''helps add actions to the target, which 
		is either a menubar or a toolbar.
		'''
		for action in actions:
			if action is None:    
				target.addSeparator()
			else:
		   		target.addAction(action)
		   		

	def newItem(self):
		print 'newItem'


	def addSubItem(self):
		print 'addSubItem'


	def checkItem(self):
		print 'checkItem'


	def deleteItem(self):
		print 'deleteItem'


	def saveEdit(self):
		print 'saveItem'


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = ProjectDoneWin()
	win.show()
	app.exec_()
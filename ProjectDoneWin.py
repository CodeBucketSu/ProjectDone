

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from TodoItemModel import *

class ProjectDoneWin(QMainWindow):
	''' '''
	def __init__(self, parent=None):
		super(ProjectDoneWin, self).__init__(parent)
		self.treeView = QTreeView()
		model = TodoItemModel()
		model.load()
		self.treeView.setModel(model)

		self.setCentralWidget(self.treeView)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = ProjectDoneWin()
	win.show()
	app.exec_()
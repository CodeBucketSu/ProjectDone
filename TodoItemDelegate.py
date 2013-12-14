''' This is the delegate for the todoList '''
import sys
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from TodoItem import *
from SqlHelper import *

class TodoItemDelegate(QtItemDelegate):

	def __init__(self):

''' This is the todoItem class'''

import sys
import bisect
import time

KEY, ITEM = range(2)
maxtime = 29999999999

def cmp(a, b):
	if a < b:
		return -1
	elif a == b:
		return 0
	else:
		return 1




class TodoItem():
	def __init__(self, ID, finish=0, what = 'What to do',\
				 when=maxtime, notes = 'NULL', \
				 where='NULL', remindTime=0, \
				 context='NULL', fatherID=0, \
				 ancesters = '0'):
		'''Initialzer of TodoItem class.'''
		self.ID = ID
		self.what = what
		self.finish = finish
		self.remindTime = remindTime
		self.when = when
		self.notes = notes
		self.where = where
		self.context = context
		self.fatherID = fatherID
		self.ancesters = ancesters
		self.children = []
		#self.parent is set in addTodoItem() method

	def __repr__(self):
		return (str(self.ID) +' '+ str(self.finish) +' '
				+ self.what +' '+ str(self.when) +' '
				+ self.where +' '+ str(self.where) +' '
				+ str(self.remindTime) +' '+ self.context +' '
				+ str(self.fatherID) +' '+ self.ancesters +'\n'
				+ '	' + str(self.children)) + '\n'

	def __cmp__(self, other):
		''' Used by mode to sort its data.
		Compared under the key ancesters.'''
		if not isinstance(other, TodoItem):
			return -1
		key_self = self.ancesters.split('_')
		key_other = other.ancesters.split('_')
		if len(key_self) == len(key_other):
			return cmp(key_self, key_other)
		else:
			return cmp(len(key_self), len(key_other))



	def childOrderKey(self):
		''' Used by parent to sort its children.
		The key of sorting is: finish --> deadline --> ID'''
		key = str(self.finish) + str(int(self.when)) \
					+ str(self.ID)
		return key


	#def cmpByAncesters(self, other):
		''' Used by model when load all the data into a tree.'''


	
	def childAtRow(self, row):
		''' Return the rowth child item.'''
		if 0 <= row < len(self.children):
			return self.children[row][ITEM]

	
	def rowOfChild(self, child):
		''' Return the order of given child in self.children.'''
		if not self.children:
			return -1
		if isinstance(child, TodoItem):
			i = bisect.bisect_left(self.children, \
								(child.childOrderKey(), child))
			if 0 <= i < len(self.children):
				return i
			else:
				return -1


	def lenOfChildren(self):
		''' Used by model.rowCount method. '''
		return len(self.children)

	'''
	def IDOfParent(self):
		if self.fatherID = None:	#????
			return None;
		return self.fatherID
	'''

	def addChild(self, child):
		''' Only add a child to the current item.
		Will not change the child.'''
		if isinstance(child, TodoItem):
			row = bisect.bisect(self.children, \
				(child.childOrderKey(), child))
			bisect.insort(self.children, \
				(child.childOrderKey(), child))
			return row


	def appendNewChild(self, child):
		''' Used when add new todo item to the parent.'''
		self.children.append((child.childOrderKey(), child))


	def getAncestersList(self):
		list = self.ancesters.split('_')
		return [int(id) for id in list]


	def getChildByID(self, ID):
		if not self.children:
			return None
		for item in self.children:
			if item[ITEM].ID == ID:
				return item[ITEM]
		return None


	def setCheckState(self, value):
		if value:
			self.finish = 1
		else:
			self.finish = 0


	def dataToUpdate(self):
		return (self.ID, self.finish, self.what, self.when, \
			self.notes, self.where, self.remindTime, self.context, \
			self.fatherID, self.ancesters)

	def sortChildren(self):
		if not self.children:
			return 
		old = self.children
		self.children = []
		for child in old:
			self.addChild(child[1])

	def updateOrderKeys(self):
		if not self.children:
			return
		for i, child in enumerate(self.children):
			self.children[i] = (child[1].childOrderKey(), child[1])


	def deleteChild(self, row):
		''' Called by model when deleting an item.'''
		if 0 <= row < self.lenOfChildren():
			IDlist = self.allIDsInSubTree(row)
			print 'DELETE item: ', self.children.pop(row)
			return IDlist


	def allIDsInSubTree(self, row):
		''' Return all the IDs of all the nodes in a subTree, 
		whose root is the rowth	child of current item's children. '''
		if 0 <= row <self.lenOfChildren():
			IDlist = []
			for i in range(self.children[row][ITEM].lenOfChildren()):
				IDlist.extend(self.children[row][ITEM]\
									.allIDsInSubTree(i))
			IDlist.append(self.children[row][ITEM].ID)
			return IDlist
		else:
			return []
''' This is the model for the todoList '''
import sys
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from TodoItem import *
from SqlHelper import *

#ID, FINISH, WHAT, WHEN, NOTES, WHERE, REMINDTIME, CONTEXT, \
#    FATHERID, ANCESTERS = range(10)
WHAT, WHEN, FINISH = range(3)


class TodoItemModel(QAbstractItemModel):

    def __init__(self):
        super(TodoItemModel, self).__init__()
        self.root = TodoItem(0, 0, 'root', 0, '', '', 0, '', 0, '')
        self.root.parent = None
        self.headers = ['Task', 'Time', 'Finish']
        self.context = set()
        self.whereTodo = set()
        self.SqlHlp = SqliteHelper()
        self.SqlHlp.initDatabase()


    def flags(self, index):
    	''' 
    	Returns the item flags for the given index.
    	All the items is editable and drag & drop enabled.
    	'''
    	if not index.isValid():
    		return (Qt.ItemIsEnabled | Qt.ItemIsDropEnabled)
    	return (QAbstractItemModel.flags(self, index) 
    		| Qt.ItemIsEditable | Qt.ItemIsDragEnabled \
    		| Qt.ItemIsDropEnabled )

    def load(self):
        items = [TodoItem(*item) for item \
                            in self.SqlHlp.getAllTodoItems()]
        items.sort()
        for todoItem in items:
            #print todoItem
            self.addTodoItem(todoItem)
            

    def addTodoItem(self, todoItem):
        '''
        Add a todo item into the datas in memor.
        Build a tree from the root node.
        '''
        root = self.root
        ancesters = todoItem.getAncestersList()
        print ancesters
        if ancesters == [0]:
            self.root.addChild(todoItem)
            todoItem.parent = self.root
        else:
            for ancstID in ancesters:
                ancst = root.getChildByID(ancstID)
                if not ancst:
                    # The path of ancesters does not exist!
                    self.root.addChild(todoItem) # Add the item to root
                    todoItem.fatherID = root.ID
                    todoItem.ancesters = str(root.ID)
                    todoItem.parent = self.root
                    self.SqlHlp.updateTodoItem(todoItem.ID, \
                                t_father_id=todoItem.fatherID,\
                                t_ancesters=todoItem.ancesters)
                else:
                    root = ancst
            root.addChild(todoItem)
            todoItem.parent = root



    #def asRecord(self, index):


    def nodeFromIndex(self, index):
        return index.internalPointer() \
            if index.isValid() else self.root

    def index(self, row, column, parent):
        assert self.root
        father = self.nodeFromIndex(parent)
        assert father is not None
        return self.createIndex(row, column, \
                                father.childAtRow(row))


    def parent(self, child):
        ''' If the child is the top level, i.e., its 
        parent is self.root, return None. '''
        child = self.nodeFromIndex(child)
        if child is None:
            return QModelIndex()
        parent = child.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != -1
        return self.createIndex(row, 0, parent)

    def data(self, index, role=Qt.DisplayRole):
        item = self.nodeFromIndex(index)
        if not item:
            return QVariant()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == FINISH:
                return QVariant(item.finish)
            if column == WHAT:
                return QVariant(item.what)
            if column == WHEN:
                timeFomat = '%Y-%m-%d %H-%m'
                sTime = time.strftime(timeFomat, time.gmtime(item.when))
                return QVariant(sTime)
        return QVariant()


    def headerData(self, section, orientation, \
                    role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and \
                role == Qt.DisplayRole:
            assert 0<= section < len(self.headers)
            return QVariant(self.headers[section])
        return QVariant()

    def rowCount(self, index=QModelIndex()):
        item = self.nodeFromIndex(index)
        if item is None:
            return 0
        return item.lenOfChildren()


    def columnCount(self, index=QModelIndex()):
        ''' The columns to show are: FINISH, WHAT, WHEN. '''
        return len(self.headers)
'''
    #def setData(self, index, value, role=Qt.EditRole):


    #def save(self):

    #def sortByName(self):

'''

if __name__ == '__main__':
    model = TodoItemModel()
    model.load()
    print model.root
'''This is the SQLiteHelper class.'''
import sys

import sqlite3
import time

'''
todo_table:
+---------------+
| t_id 			|
|---------------|
| t_finish		|
| t_what		|
| t_when		|
|---------------|
| t_notes		|
| t_where		|
| t_remindTime	|
| t_context		|
|---------------|
| t_father_id	|
| t_ancesters	|
+---------------+

context_table
+---------------+
| c_id 			|
|---------------|
| c_name		|
+---------------+

location_table
+---------------+
| l_id 			|
|---------------|
| l_name		|
+---------------+
'''
maxtime = 29999999999

initDBScript = '''
	create table todo_table(
		t_id integer not null primary key,
		t_finish integer not null default 0,
		t_what text not null,
		t_when real default 10675199167,
		t_notes text, 
		t_where text,
		t_remindTime real default 10675199167,
		t_context text,
		t_father_id integer not null default 0,
		t_ancesters text not null default '0'
		);
	create table context_table(
		c_id integer not null primary key,
		c_name text not null
		);
	create table location_table(
		l_id integer not null primary key, 
		l_name text not null
		);
	'''
newTodoItemSql = '''
	insert into todo_table (
		t_finish, 
		t_what, 
		t_when, 
		t_notes,
		t_where, 
		t_remindTime, 
		t_context, 
		t_father_id, 
		t_ancesters) 
	values (
		?, ?, ?, ?, ?, ?, ?, ?, ?);
	'''
getAllTodoItemsSql = '''
	select * from todo_table 
	order by t_finish, t_when, t_id;
	'''
updateTodoItemSql = '''
	update todo_table 
		set t_finish = ?,
		t_what = ?, 
		t_when = ?,
		t_notes = ?,
		t_where = ?,
		t_remindTime = ?,
		t_context = ?,
		t_father_id = ?,
		t_ancesters = ?
	where
		t_id = ? ;
	'''
isTableExistSql = '''
	select name from sqlite_master where type = 'table' order by name;
	'''
deleteTodoItemSql = '''
	delete from todo_table where t_id = ? ;
	'''
getNewestItemIDSql = '''
	select t_id from todo_table order by t_id desc limit 3
	'''

class SqliteHelper(object):
	'''Sqlite Helper.'''
	def __init__(self):
		self.connector = sqlite3.connect('ProjectDone.db')
		self.cursor = self.connector.cursor()

	def initDatabase(self):
		connector = sqlite3.connect('ProjectDone.db')
		cur = connector.cursor()
		cur.execute(isTableExistSql)
		tables = cur.fetchall()
		if not tables:
			cur.executescript(initDBScript)
			connector.commit()
		else:
			print tables
		connector.close()

	def newTodoItem(self, t_finish=0, t_what = 'What to do', \
					t_when=maxtime, t_notes = 'NULL', \
					t_where='NULL', t_remindTime=0,\
					t_context='NULL', t_father_id=0, \
					t_ancesters = '0' , ):
		self.cursor.execute(newTodoItemSql, (t_finish, t_what,\
					t_when, t_notes, t_where, t_remindTime, \
					t_context, t_father_id, t_ancesters))
		self.cursor.execute(getNewestItemIDSql)
		self.connector.commit()
		return self.cursor.fetchone()[0]

	def getAllTodoItems(self):
		self.cursor.execute(getAllTodoItemsSql)
		todoItems = self.cursor.fetchall()
		return todoItems

	def updateTodoItem(self, t_id, t_finish=0, t_what = 'What to do',\
					t_when=maxtime, t_notes = 'NULL', \
					t_where='NULL', t_remindTime=0, \
					t_context='NULL', t_father_id=0, \
					t_ancesters = '0'):
		self.cursor.execute(updateTodoItemSql, (t_finish, \
					t_what, t_when, t_notes, t_where, \
					t_remindTime, t_context, \
					t_father_id, t_ancesters, \
					t_id))
		self.connector.commit()

	def deleteTodoItem(self, t_id):
		self.cursor.execute(deleteTodoItemSql, (t_id, ))
		self.connector.commit()

	def deleteTodoItems(self, t_id_list):
		for t_id in t_id_list:
			self.deleteTodoItem(t_id)

	def close(self):
		self.connector.close()

if __name__ == '__main__':
	sqlh = SqliteHelper()
	sqlh.initDatabase()
	#sqlh.newTodoItem(0, 'aaa', t_father_id = 0)
	#sqlh.newTodoItem(0, 'bbb', t_father_id = 1, t_ancesters = '1')
	#sqlh.newTodoItem(0, 'ccc', t_father_id = 2, t_ancesters = '1_2')
	#sqlh.newTodoItem(0, 'aaa', t_father_id = 0)
	#sqlh.newTodoItem(0, 'bbb', t_father_id = 4, t_ancesters = '4')
	#sqlh.newTodoItem(0, 'ccc', t_father_id = 5, t_ancesters = '4_5')
	#sqlh.newTodoItem(0, 'ccc', t_father_id = 5, t_ancesters = '3_5')
	print sqlh.newTodoItem()
	#for record in sqlh.getAllTodoItems():
	#	print type(record), record
	sqlh.close()


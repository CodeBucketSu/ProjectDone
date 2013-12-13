import sys
import bisect
import random


class A():
	def __init__(self, id):
		self.id = id

	
	def orderKey(self):
		return self.id
	

	def __repr__(self):
		return ('A: ' + str(self.id))

l = []
for i in range(5):
	r = random.randint(1, 100)
	a = A(r)
	bisect.insort_left(l, (a.id, a))
	print bisect.bisect_left(l, (a.id, a))
	print ' ', r, ' ', l



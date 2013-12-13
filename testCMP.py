import sys
import random

def cmp(a, b):
	if a < b:
		return -1
	elif a == b:
		return 0
	else:
		return 1

class Test():
	def __init__(self, a):
		self.ancesters = a

	def __cmp__(self, other):
		''' Used by mode to sort its data.
		Compared under the key ancesters.'''
		if not isinstance(other, Test):
			return -1
		key_self = self.ancesters.split('_')
		key_other = other.ancesters.split('_')
		if len(key_self) == len(key_other):
			return cmp(key_self, key_other)
		else:
			return cmp(len(key_self), len(key_other))

	def __repr__(self):
		return self.ancesters


if __name__ == '__main__':
	list = []
	for i in range(10):
		cnt = random.randint(1,4)
		s = ''
		for c in range(cnt):
			sp = random.randint(1,4)
			s += str(sp)
			s += '_' 
		#print s[:-1]
		t = Test(s[:-1])
		list.append(t)
	list.sort()
	for i in list:
		print i
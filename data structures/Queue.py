class Queue:
	"""
	Очередь 
	[<значение>, <следущий эл.>, <первый эл.>]
	
	>>> A = Queue()
	>>> A.add(1)
	>>> A.add(2)
	>>> A.add(3)
	>>> A.pop()
	1
	>>> A.pop()
	2
	>>> A.pop()
	3
	>>> A.add(3)
	>>> A.clear()
	>>> A.len()
	0
	>>> A.add(1)
	>>> A.add(2)
	>>> A.pop()
	1
	>>> A.pop()
	2
	>>> A._next
	>>> A._first
	>>> A.add('right')
	>>> A.add('right')
	>>> A.pop()
	'right'
	>>> A.pop()
	'right'
	
	"""
	
	def __init__(self):
		self._next = None
		self._first = None
		self.size = 0
	
	def add(self, x):
		if self._first is None:
			self._first = [x, self._next, self._first]
		elif self._first[1] is None:
			self._next = [x, None, self._first]
			self._first[1] = self._next
		else:
			tmp = self._next
			self._next = [x, None, self._first]
			tmp[1] = self._next
		self.size += 1
	
	def pop(self):
		assert self.size, "Очередь пуста"
		x = self._first[0]
		self._first = self._first[1]
		if self._first is not None:
			self._first[2] = None
		else:
			self._next = None
		self.size -= 1
		
		return x
	
	def clear(self):
		self._next = None
		self._first = None
		self.size = 0		
		
	def len(self):
		return self.size


if __name__ == "__main__":
	import doctest
	doctest.testmod()

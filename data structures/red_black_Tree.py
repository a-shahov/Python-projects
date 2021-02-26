class Node:
	
	def __init__(self, key, value):
		
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self._depth = 0


class RedBlackNode(Node):
	
	def __init__(self, key, value):
		
		Node.__init__(self, key, value)
		self.color = "red"


class Tree:
	
	def __init__(self):
		
		self.root = None
		self.size = 0
		self._height = 0


	def __bool__(self):
		
		return bool(self.size)


	def __len__(self):
		
		return self.size


	def __str__(self):
		
		if self.root is None:
			return "Tree is empty!"
		tmp = self.root
		return self._BFS(tmp)


	def _BFS(self, tmp, string="", depth=0):
		
		tmp._depth = depth
		flag = True
		for number, child in (0, tmp.left), (1, tmp.right):
			if child is not None:
				string = self._BFS(child, string, depth+1)
				if flag:
					string += "{}({}, {})\n".format("---"*(depth), tmp.key, tmp.value)
					flag = False
			else:
				if not number:
					flag = False
					string += "{}({}, {})\n".format("---"*(depth), tmp.key, tmp.value)
		return string
			

	def _create_node(self, key, value):
		
		return Node(key, value)


	def _balance_push(self, x):
		
		pass


	def push(self, key, value=None):
		
		x = self._create_node(key, value)
		if self.root is None:
			self.root = x
			self.size += 1
		else:
			tmp = self.root
			while True:
				if x.key == tmp.key:
					tmp.key, tmp.value = x.key, x.value
					break
				elif x.key > tmp.key:
					if tmp.right is None:
						tmp.right = x
						x.parent = tmp
						self.size += 1
						self._balance_push(x)
						break
					else:
						tmp = tmp.right
				elif x.key < tmp.key:
					if tmp.left is None:
						tmp.left = x
						x.parent = tmp
						self.size += 1
						self._balance_push(x)
						break
					else:
						tmp = tmp.left


	def get(self, key):
		
		if self.root is None:
			return None
		tmp = self.root
		while True:
			if key == tmp.key:
				return tmp.key, tmp.value
			elif key > tmp.key:
				if tmp.right is None:
					return None
				else:
					tmp = tmp.right
			elif key < tmp.key:
				if tmp.left is None:
					return None
				else:
					tmp = tmp.left

A = Tree()
A.push(10)
A.push(5)
A.push(7)
A.push(4)
A.push(15)
A.push(14)
A.push(16)
A.push(17)
A.push(18)
A.push(19)
print(A)


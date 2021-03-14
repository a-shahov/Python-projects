class Node:
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self._depth = 0
	
	
	def __str__(self):
		return str((self.key, self.value))


class RedBlackNode(Node):
	def __init__(self, key, value):
		Node.__init__(self, key, value)
		self.color = "red"


class Tree:
	def __init__(self):
		self.root = None
		self.size = 0


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
					string += "{}{}\n".format("---"*(depth), tmp)
					flag = False
			else:
				if not number:
					flag = False
					string += "{}{}\n".format("---"*(depth), tmp)
		return string
			

	def _create_node(self, key, value):
		return Node(key, value)


	def _balance_push(self, tmp):
		pass


	def _balance_pop(self, tmp):
		pass


	def _find(self, key):
		if self.root is None:
			return None
		tmp = self.root
		while True:
			if key == tmp.key:
				return tmp
			elif key > tmp.key:
				if tmp.right is None:
					return None
				tmp = tmp.right
			else:
				if tmp.left is None:
					return None
				tmp = tmp.left


	def _find_min(self, tmp):
		while True:
			if tmp.left is None:
				return tmp
			tmp = tmp.left


	def get_min(self):
		assert self.root, "Tree is empty!" 
		tmp = self.root
		while True:
			if tmp.left is None:
				return tmp.key, tmp.value
			tmp = tmp.left

	
	def get_max(self):
		assert self.root, "Tree is empty!" 
		tmp = self.root
		while True:
			if tmp.right is None:
				return tmp.key, tmp.value
			tmp = tmp.right


	def clear(self):
		self.root = None
		self.size = 0


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
	
	
	def pop(self, key):
		tmp = self._find(key)
		assert tmp is not None
		couple = (tmp.key, tmp.value)
		self.size -= 1
		if tmp.right is None:
			if tmp.left is None:
				if tmp.parent is None:
					self.clear()
				else:
					if tmp.parent.left is tmp:
						tmp.parent.left = None
					elif tmp.parent.right is tmp:
						tmp.parent.right = None
			else:
				if tmp.parent is None:
					tmp.left.parent = None
					self.root = tmp.left
				else:
					if tmp.parent.left is tmp:
						tmp.parent.left = tmp.left
						tmp.left.parent = tmp.parent
					elif tmp.parent.right is tmp:
						tmp.parent.right = tmp.left
						tmp.left.parent = tmp.parent
		else:
			tmp_min = self._find_min(tmp.right)
			if tmp_min.parent is tmp:
				if tmp.parent is None:
					tmp_min.parent = None
					tmp_min.left = tmp.left
					if tmp.left is not None:
						tmp.left.parent = tmp_min
					self.root = tmp_min
				else:
					tmp_min.parent = tmp.parent
					tmp_min.left = tmp.left
					if tmp.left is not None:
						tmp.left.parent = tmp_min
					if tmp.parent.right is tmp:
						tmp.parent.right = tmp_min
					elif tmp.parent.left is tmp:
						tmp.parent.left = tmp_min
			else:
				if tmp.parent is None:
					tmp_min.parent.left = tmp_min.right
					if tmp_min.right is not None:
						tmp_min.right.parent = tmp_min.parent
					tmp_min.parent = None
					tmp.right.parent = tmp_min
					tmp_min.right = tmp.right
					tmp_min.left = tmp.left
					if tmp.left is not None:
						tmp.left.parent = tmp_min
					self.root = tmp_min
				else:
					tmp_min.parent.left = tmp_min.right
					if tmp_min.right is not None:
						tmp_min.right.parent = tmp_min.parent
					tmp_min.parent = tmp.parent
					if tmp.parent.right is tmp:
						tmp.parent.right = tmp_min
					elif tmp.parent.left is tmp:
						tmp.parent.left = tmp_min
					tmp.right.parent = tmp_min
					tmp_min.right = tmp.right
					tmp_min.left = tmp.left
					if tmp.left is not None:
						tmp.left.parent = tmp_min
		return couple


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
A.pop(4)
print(A)

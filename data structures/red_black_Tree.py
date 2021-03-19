class Node:
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
	
	
	def __str__(self):
		return str((self.key, self.value))
	
	
	def copy(self, obj):
		self.key = obj.key
		self.value = obj.value


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
		for first, child in (True, tmp.right), (False, tmp.left):
			if child is not None:
				string = self._BFS(child, string, depth+1)
				if flag:
					string += "{}{}\n".format("---"*(depth), tmp)
					flag = False
			else:
				if first:
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


	def _get_min(self, tmp): 
		while True:
			if tmp.left is None:
				return tmp
			tmp = tmp.left

	
	def _get_max(self, tmp):
		while True:
			if tmp.right is None:
				return tmp
			tmp = tmp.right


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
			self._balance_push(x)
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
		if tmp.right is None and tmp.left is None:
			if tmp is self.root:
				self.root = None
			else:
				if tmp.parent.right is tmp:
					tmp.parent.right = None
				else:
					tmp.parent.left = None
		elif tmp.right is None:
			tmp_max = self._get_max(tmp.left)
			tmp.copy(tmp_max)
			if tmp_max.parent.left is tmp_max:
				tmp_max.parent.left = tmp_max.left
				if tmp_max.left is not None:
					tmp_max.left.parent = tmp_max.parent
			else:
				tmp_max.parent.right = tmp_max.left
				if tmp_max.left is not None:
					tmp_max.left.parent = tmp_max.parent
		else:
			tmp_min = self._get_min(tmp.right)
			tmp.copy(tmp_min)
			if tmp_min.parent.left is tmp_min:
				tmp_min.parent.left = tmp_min.right
				if tmp_min.right is not None:
					tmp_min.right.parent = tmp_min.parent
			else:
				tmp_min.parent.right = tmp_min.right
				if tmp_min.right is not None:
					tmp_min.right.parent = tmp_min.parent
		return couple


	def pop_irrelevant(self, key):
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


class RBTree(Tree):
	def __init__(self):
		Tree.__init__(self)


	def _create_node(self, key, value):
		return RedBlackNode(key, value)


	def _recolour(self, node):
		father = node.parent
		grfather = father.parent
		if father is grfather.left:
			uncle = grfather.right
		else:
			uncle = grfather.left
		
		father.color = "black"
		grfather.color = "red"
		uncle.color = "black"
		
		self._balance_push(grfather)


	def _big_right_rotation(self, node):
		father = node.parent
		grfather = father.parent
		
		grfather.left = father.right
		if father.right is not None:
			father.right.parent = grfather
		
		father.parent = grfather.parent
		if grfather.parent is not None:
			if grfather.parent.left is grfather:
				grfather.parent.left = fatherr
			else:
				grfather.parent.right = father
		grfather.parent = father
		father.right = grfather
		
		if grfather is self.root:
			self.root = father
		
		grfather.color = "red" 
		father.color = "black"


	def _big_left_rotation(self, node):
		father = node.parent
		grfather = father.parent
		
		grfather.right = father.left
		if father.left is not None:
			father.left.parent = grfather
		
		father.parent = grfather.parent
		if grfather.parent is not None:
			if grfather.parent.left is grfather:
				grfather.parent.left = father
			else:
				grfather.parent.right = father
		grfather.parent = father
		father.left = grfather
		
		if grfather is self.root:
			self.root = father
		
		grfather.color = "red" 
		father.color = "black"


	def _small_left_rotation(self, node):
		father = node.parent
		grfather = father.parent
		
		grfather.left = node
		node.parent = grfather
		
		father.right = node.left
		if node.left is not None:
			node.left.parent = father
		
		node.left = father
		father.parent = node
		
		self._big_right_rotation(father)


	def _small_right_rotation(self, node):
		father = node.parent
		grfather = father.parent
		
		grfather.right = node
		node.parent = grfather
		
		father.left = node.right
		if node.right is not None:
			node.right.parent = father
		
		node.right = father
		father.parent = node
		
		self._big_left_rotation(father)


	def _balance_push(self, node):
		if node is self.root:
			node.color = "black"
		elif node.parent.color == "black":
			pass
		else:
			father = node.parent
			grfather = father.parent
			if grfather.left is father:
				uncle = grfather.right
			else:
				uncle = grfather.left
			if father.color == "red" and uncle is not None and uncle.color == "red":
				self._recolour(node)
			elif father.color == "red" and (uncle is None or uncle.color == "black"):
				if grfather.left is father and father.right is node:
					self._small_left_rotation(node)
				elif grfather.right is father and father.left is node:
					self._small_right_rotation(node)
				elif grfather.left is father and father.left is node:
					self._big_rigкht_rotation(node)
				elif grfather.right is father and father.right is node:
					self._big_left_rotation(node)





A = Tree()
A.push(10)
A.push(11)
A.push(12)
A.push(13)
A.push(14)
A.push(15)
A.push(16)
A.push(17)
A.push(18)
A.push(19)
A.push(20)
A.push(21)
print(A)
A.pop(18)
A.pop(14)
A.pop(10)
print(A)

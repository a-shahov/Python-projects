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
		if tmp.right is None: #There is no right subtree
			if tmp.left is None: #The element to remove (tmp) - sheet
				#No need to change coefficients skew, h_r_tree, h_l_tree
				if tmp.parent is None: #The removed item is the root, size = 1
					self.clear()
					tmp_transit = None #For function __count_skew_delete
					orientation = "None" #For function __count_skew_delete
				#It is necessary to change the coefficients skew, h_r_tree, h_l_tree
				else: #The element to be removed (tmp) has a parent
					#we come to the left, that is, +1 to skew, at tmp.parent
					if tmp.parent.left is tmp:
						tmp.parent.left = None
						orientation = "left"
					#we come to the right, that is, -1 to skew, for tmp.parent
					elif tmp.parent.right is tmp:
						tmp.parent.right = None
						orientation = "right"
					tmp_transit = tmp.parent
			else: #The item being removed(tmp) has a left child
				#No need to change coefficients skew, h_r_tree, h_l_tree
				if tmp.parent is None: #The removed item(tmp) is the root, size = 2
					tmp.left.parent = None
					self.root = tmp.left
					tmp_transit = None #For function __count_skew_delete
					orientation = "None"
				#It is necessary to change the coefficients skew, h_r_tree, h_l_tree
				else: #The element to be removed(tmp) has a parent
					#we come to the left, that is, +1 to skew, at tmp.parent
					if tmp.parent.left is tmp:
						tmp.parent.left = tmp.left
						orientation = "left"
					#we come to the right, that is, -1 to skew, for tmp.parent
					elif tmp.parent.right is tmp:
						tmp.parent.right = tmp.left
						orientation = "right"
					tmp.left.parent = tmp.parent
					tmp_transit = tmp.parent
		else: #The item being removed(tmp) has a right subtree
			tmp_min = self.__find_min(tmp)
			if tmp_min.parent is tmp:
				#we come to the right, that is, -1 to skew, to tmp_min(after reassignments)
				if tmp.parent is None: #The item to remove(tmp) is the root
					tmp_min.parent = None
					self.root = tmp_min
				else: #The element to be removed(tmp) has a parent
					tmp_min.parent = tmp.parent
					if tmp.parent.right is tmp:
						tmp.parent.right = tmp_min
					elif tmp.parent.left is tmp:
						tmp.parent.left = tmp_min
						
				if tmp.left is not None:
					tmp.left.parent = tmp_min
				tmp_min.left = tmp.left
				
				#tmp_min replaces tmp and gets its old attributes
				#which will be adjusted in __count_skew_delete
				tmp_min.skew = tmp.skew
				tmp_min.h_r_tree = tmp.h_r_tree
				tmp_min.h_l_tree = tmp.h_l_tree
				
				orientation = "right"
				tmp_transit = tmp_min
			else:
				#we come to the left, that is, +1 to skew, in tmp_min.parent(before reassignments)
				orientation = "left"
				tmp_transit = tmp_min.parent
				
				if tmp.parent is None: #The item to remove (tmp) is the root
					tmp_min.parent.left = tmp_min.right
					if tmp_min.right is not None:
						tmp_min.right.parent = tmp_min.parent
					tmp_min.parent = None
					self.root = tmp_min
				else: #The element to be removed (tmp) has a parent
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
				#tmp.left is not None because tmp has a right subtree
				#which consists of at least two elements
				tmp.left.parent = tmp_min
				tmp_min.left = tmp.left
		
		self._balance_pop(tmp_transit, orientation)
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


class Node:

	def __init__(self, key, value):
		
		self.skew = 0 #main attribute for balancing
		self.h_r_tree = 0 #height of the right subtree
		self.h_l_tree = 0 #height of the left subtree
		
		self.key = key 
		self.value = value
		self.right = None #link to the right child
		self.left = None #link to the left child
		self.parent = None #parent link

class Tree:
	"""
	AVL - tree

	push(key, value) - add a key (key) with value (value),
	value by default None

	find(key) - search by key, if present returns True
	otherwise False, can return a reference to the searched object, 
	see documentation

	delete(key) - deletes an element from the tree by key

	clear() - Makes the tree empty

	is_empty() - Returns True if the tree is empty,
	otherwise False

	get_list_keys() - Returns an ordered list of keys
	
	get_min() - Returns the minimum key and its value
	
	get_max() - Returns the maximum key and its value

	The size attribute contains the size of the tree
	"""
	def __init__(self):
		self.root = None
		self.size = 0
	

	def __small_left_rotation(self, tmp):
		"""
		gets a reference to an object tmp where
		tmp.parent has a skew overflow
		"""
		#Link reassignment
		top = tmp.parent.parent
		a = tmp.parent
		b = tmp
		
		if top is None:
			b.parent = top
			self.root = b
		elif top.right is a:
			b.parent = top
			top.right = b
		elif top.left is a:
			b.parent = top
			top.left = b
			
		a.parent = b
		a.right = b.left
		if b.left is not None:
			b.left.parent = a
		b.left = a
		
		#Recalculation of coefficients
		a.h_r_tree = b.h_l_tree
		b.h_l_tree = 1 + max(a.h_r_tree, a.h_l_tree)
		a.skew = a.h_r_tree - a.h_l_tree
		b.skew = b.h_r_tree - b.h_l_tree

	
	def __big_left_rotation(self, tmp):
		"""
		gets a reference to an object tmp where
		tmp.parent has a skew overflow
		"""
		#Link reassignment
		top = tmp.parent.parent
		a = tmp.parent
		b = tmp
		c = tmp.left
		
		if top is None:
			c.parent = top
			self.root = c
		elif top.right is a:
			c.parent = top
			top.right = c
		elif top.left is a:
			c.parent = top
			top.left = c
			
		a.parent = c
		a.right = c.left
		if c.left is not None:
			c.left.parent = a
		b.parent = c
		b.left = c.right
		if c.right is not None:
			c.right.parent = b
		c.left = a
		c.right = b

		#Recalculation of coefficients
		a.h_r_tree = c.h_l_tree
		b.h_l_tree = c.h_r_tree
		c.h_l_tree = 1 + max(a.h_l_tree, a.h_r_tree)
		c.h_r_tree = 1 + max(b.h_l_tree, b.h_r_tree)
		a.skew = a.h_r_tree - a.h_l_tree
		b.skew = b.h_r_tree - b.h_l_tree
		c.skew = c.h_r_tree - c.h_l_tree
	
	
	def __small_right_rotation(self, tmp):
		"""
		gets a reference to an object tmp where
		tmp.parent has a skew overflow
		"""
		#Link reassignment
		top = tmp.parent.parent
		a = tmp.parent
		b = tmp
		
		if top is None:
			b.parent = top
			self.root = b
		elif top.right is a:
			b.parent = top
			top.right = b
		elif top.left is a:
			b.parent = top
			top.left = b
			
		a.parent = b
		a.left = b.right
		if b.right is not None:
			b.right.parent = a
		b.right = a
		
		#Recalculation of coefficients
		a.h_l_tree = b.h_r_tree
		b.h_r_tree = 1 + max(a.h_l_tree, a.h_r_tree)
		a.skew = a.h_r_tree - a.h_l_tree
		b.skew = b.h_r_tree - b.h_l_tree
	

	def __big_right_rotation(self, tmp):
		"""
		gets a reference to an object tmp where
		tmp.parent has a skew overflow
		"""
		#Link reassignment
		top = tmp.parent.parent
		a = tmp.parent
		b = tmp
		c = tmp.right
		
		if top is None:
			c.parent = top
			self.root = c
		elif top.right is a:
			c.parent = top
			top.right = c
		elif top.left is a:
			c.parent = top
			top.left = c
		
		a.parent = c
		a.left = c.right
		if c.right is not None:
			c.right.parent = a
		b.parent = c
		b.right = c.left
		if c.left is not None:
			c.left.parent = b
		c.right = a
		c.left = b
		
		#Recalculation of coefficients
		a.h_l_tree = c.h_r_tree
		b.h_r_tree = c.h_l_tree
		c.h_r_tree = 1 + max(a.h_l_tree, a.h_r_tree)
		c.h_l_tree = 1 + max(b.h_l_tree, b.h_r_tree)
		a.skew = a.h_r_tree - a.h_l_tree
		b.skew = b.h_r_tree - b.h_l_tree
		c.skew = c.h_r_tree - c.h_l_tree


	def __count_skew_push(self, tmp):
		"""
		This function recalculates the skew coefficient 
		for all parents who need it. Runs every time push is called
		
		tmp - This is a link to the current object, 
		recalculation is performed in tmp.parent
		"""
		if tmp.parent is None:
			return
		elif tmp.parent.right is tmp:
			corrective = 1
		elif tmp.parent.left is tmp:
			corrective = -1	
		else:
			raise Warning("Algorithm failure, invalid program location")
		#valid values for tmp.parent.skew are -1, 0, 1
		if tmp.parent.skew + corrective == 2: #was 1 now 2
			tmp.parent.h_r_tree += 1
			if tmp.parent.h_l_tree + 1 == max(tmp.h_r_tree, tmp.h_l_tree):
				#Condition for small left rotation
				if tmp.h_l_tree <= tmp.h_r_tree:
					self.__small_left_rotation(tmp)
				#Condition for big left rotation
				elif tmp.h_l_tree > tmp.h_r_tree:
					self.__big_left_rotation(tmp)
			else:
				raise Warning("Algorithm failure, invalid program location")
			return
		elif tmp.parent.skew + corrective == 1: #was 0 now 1
			tmp.parent.skew += corrective
			tmp.parent.h_r_tree += 1
			tmp = tmp.parent
			self.__count_skew_push(tmp)
			return
		elif tmp.parent.skew + corrective == 0: #was -1 or 1 now 0
			tmp.parent.skew += corrective
			if tmp.parent.right is tmp:
				tmp.parent.h_r_tree += 1
			else:
				tmp.parent.h_l_tree += 1
			return
		elif tmp.parent.skew + corrective == -1: #was 0 now -1
			tmp.parent.skew += corrective
			tmp.parent.h_l_tree += 1
			tmp = tmp.parent
			self.__count_skew_push(tmp)
			return
		elif tmp.parent.skew + corrective == -2: #was -1 now -2
			tmp.parent.h_l_tree += 1
			if tmp.parent.h_r_tree + 1 == max(tmp.h_r_tree, tmp.h_l_tree):
				#Condition for small right rotation
				if tmp.h_l_tree >= tmp.h_r_tree:
					self.__small_right_rotation(tmp)
				#Condition for big right rotation
				elif tmp.h_l_tree < tmp.h_r_tree:
					self.__big_right_rotation(tmp)
			else:
				raise Warning("Algorithm failure, invalid program location")
			return
		else:
			raise Warning("Algorithm failure, invalid program location")
	
	def push(self, key, value=None):
		"""
		add a key (key) with value (value),
		value by default None
		"""
		notice = "An element with such a key is already contained in the tree"
		assert not self.find(key), notice
		if self.root is None:
			self.root = Node(key, value)
		else:
			x = Node(key, value)
			tmp = self.root
			while True:
				if x.key > tmp.key:
					if tmp.right is None:
						tmp.right = x
						x.parent = tmp
						tmp = x
						break
					else:
						tmp = tmp.right
				else:
					if tmp.left is None:
						tmp.left = x
						x.parent = tmp
						tmp = x
						break
					else:
						tmp = tmp.left
			self.__count_skew_push(tmp)
		self.size += 1

	
	def find(self, key, from_the_inside=False):
		"""
		If the item is in the tree:
		can return a link to the element you are looking for,
		if from_the_inside == True,
		otherwise returns True
		"""
		if self.root is None:
			return False
		tmp = self.root
		while True:
			if key == tmp.key:
				if from_the_inside:
					return tmp
				else:
					return True
			elif key > tmp.key:
				if tmp.right is None:
					return False
				tmp = tmp.right
			else:
				if tmp.left is None:
					return False
				tmp = tmp.left


	def clear(self):
		"""
		Resets all values in the tree
		"""
		self.root = None
		self.size = 0

	
	def __find_min(self, tmp):
		"""
		tmp - link to the item to remove
		"""
		tmp = tmp.right
		while True:
			if tmp.left is None:
				return tmp
			tmp = tmp.left


	def delete(self, key):
		"""
		deletes an element from the tree by key
		"""
		tmp = self.find(key, True) #Returns a reference to the searched object or False
		assert tmp is not False, "There is no such element in the tree"
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
		
		self.__count_skew_delete(tmp_transit, orientation)


	def __count_skew_delete(self, tmp_transit, orientation):
		"""
		orientation - came from the right "right", came from the left "left",
		no need to change coefficients "None"
		"right" - tmp_transit has -1 to skew, -1 to h_r_tree
		"left" - tmp_transit has +1 to skew, -1 to h_l_tree
		tmp_transit - change attributes in this object
		"""
		if orientation == "None":
			return
		elif orientation == "right":
			corrective = -1
		elif orientation == "left":
			corrective = 1
		
		if tmp_transit.skew + corrective == 2: #was 1 now 2
			
			tmp_transit.h_l_tree -= 1
			if tmp_transit.h_l_tree + 1 == \
					max(tmp_transit.right.h_r_tree, tmp_transit.right.h_l_tree):
				#Condition for small left rotation
				if tmp_transit.right.h_l_tree < tmp_transit.right.h_r_tree:
					#The height continues to shrink to the root !!!!
					#You need to keep calling the function __count_skew_delete
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
						
					self.__small_left_rotation(tmp_transit.right)
						
					#continue to call the function
					self.__count_skew_delete(tmp_next, orientation)
				#Condition for big left rotation
				elif tmp_transit.right.h_l_tree > tmp_transit.right.h_r_tree:
					#The height continues to shrink to the root !!!!
					#You need to keep calling the function __count_skew_delete
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
							
					self.__big_left_rotation(tmp_transit.right)
						
					#continue to call the function
					self.__count_skew_delete(tmp_next, orientation)
						
				elif tmp_transit.right.h_l_tree == tmp_transit.right.h_r_tree:
					#A special case!!!
					self.__small_left_rotation(tmp_transit.right)
						
		elif tmp_transit.skew + corrective == 1: #was 0 now 1
			
			tmp_transit.skew += corrective
			tmp_transit.h_l_tree -= 1
			
		elif tmp_transit.skew + corrective == 0:
			
			tmp_transit.skew += corrective
			if corrective == -1:
				tmp_transit.h_r_tree -= 1
			elif corrective == 1:
				tmp_transit.h_l_tree -= 1
				
			if tmp_transit.parent is not None:
				if tmp_transit.parent.right is tmp_transit:
					orientation = "right"
				elif tmp_transit.parent.left is tmp_transit:
					orientation = "left"
				self.__count_skew_delete(tmp_transit.parent, orientation)
				
		elif tmp_transit.skew + corrective == -1: #was 0 now -1
			
			tmp_transit.skew += corrective
			tmp_transit.h_r_tree -= 1
			
		elif tmp_transit.skew + corrective == -2: #was -1 now -2
			
			tmp_transit.h_r_tree -= 1
			if tmp_transit.h_r_tree + 1 == \
					max(tmp_transit.left.h_r_tree, tmp_transit.left.h_l_tree):
				#Condition for small right rotation
				if tmp_transit.left.h_l_tree > tmp_transit.left.h_r_tree:
					#The height continues to shrink to the root !!!!
					#You need to keep calling the function __count_skew_delete
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
							
					self.__small_right_rotation(tmp_transit.left)
						
					#continue to call the function
					self.__count_skew_delete(tmp_next, orientation)
				# Condition for big right rotation
				elif tmp_transit.left.h_l_tree < tmp_transit.left.h_r_tree:
					#The height continues to shrink to the root !!!!
					#You need to keep calling the function __count_skew_delete
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
							
					self.__big_right_rotation(tmp_transit.left)
						
					#continue to call the function
					self.__count_skew_delete(tmp_next, orientation)
					
				elif tmp_transit.left.h_l_tree == tmp_transit.left.h_r_tree:
					#A special case!!!
					self.__small_right_rotation(tmp_transit.left)
		return


	def is_empty(self):
		"""
		Returns True if the tree is empty,
		otherwise False
		"""
		if self.root is None:
			return True
		return False


	def get_list_keys(self):
		"""
		Returns an ordered list of keys,
		if Tree is empty, return None
		"""
		if self.root is None:
			return None
		tmp = self.root
		while True:
			if tmp.left is not None:
				tmp = tmp.left
			else:
				break
		return self.__craft(tmp)


	def __craft(self, tmp):
		"""
		uses an algorithm similar 
		to depth-first traversal to create 
		an ordered list of keys
		"""
		Keys = [None]*self.size
		Keys[0] = tmp.key
		used = {tmp.key}
		count = 1
		while count < self.size: 
			
			if tmp.right is not None and tmp.right.key not in used:
				tmp = self.__find_min(tmp)
				Keys[count] = tmp.key
				used.add(tmp.key)
				count += 1
				continue
				
			if tmp.parent is not None and tmp.parent.key not in used:
				tmp = tmp.parent
				Keys[count] = tmp.key
				used.add(tmp.key)
				count += 1
				continue
				
			tmp = tmp.parent
		return Keys


	def _test(self):
		"""
		Returns an ordered list of keys,
		the tree becomes empty.
		The function tests the delete option
		"""
		B = [None]*self.size
		tmp = self.root
		i = 0
		while True:
			if tmp.left is None:
				B[i] = tmp.key
				i += 1
				self.delete(tmp.key)
				if self.root is not None:
					tmp = self.root
				else:
					return B
			else:
				tmp = tmp.left
	
	
	def get_min(self):
		"""
		Returns the minimum key and its value
		"""
		assert self.root, "Tree is empty!" 
		tmp = self.root
		while True:
			if tmp.left is None:
				return tmp.key, tmp.value
			tmp = tmp.left

	
	def get_max(self):
		"""
		Returns the maximum key and its value
		"""
		assert self.root, "Tree is empty!" 
		tmp = self.root
		while True:
			if tmp.right is None:
				return tmp.key, tmp.value
			tmp = tmp.right


if __name__ == "__main_":	
	import random
	"""
	A list of fixed
	length (you can make a random length it doesn't matter)
	from random numbers from 0 to 100, these numbers are also added to the tree.
	Next, the list is displayed and using the show () method, it is displayed
	list of tree keys. Since the show () method empties the tree,
	then by the ordering of the list of keys one can judge about
	correct / incorrect operation of the tree.
	I have no proof that this way of testing the code,
	guarantees the absolute correctness of the code.
	"""
	N = 3000
	for p in range(N):
		tree = Tree()
		A = []
		
		for i in range(25):
			x = random.randint(0,100)
			while x in A:
				x = random.randint(0,100)
			tree.push(x)
			A.append(x)
			
		try:
			print(A)
			B = tree._test()
			print(B)
			if sorted(A) == B:	
				print("Ok")
			else:
				print("Failure")
				print("Tests passed",p ,"of", N)
				break
				
		except:
			print(A)
			print("Failure")
			print("Tests passed",p ,"of", N)
			break
		if p+1 == N:
			print("Tests passed",p+1 ,"of", N)

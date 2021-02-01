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

	show() - Returns an ordered list of keys, the tree becomes empty

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
		assert tmp is not False, "Такого элемента в дереве нету"
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
					"""
					приходим слева то есть +1 к skew, у tmp.parent
					"""
					if tmp.parent.left is tmp:
						tmp.parent.left = None
						orientation = "left"
						"""
						приходим справа то есть -1 к skew, у tmp.parent
						"""
					elif tmp.parent.right is tmp:
						tmp.parent.right = None
						orientation = "right"
					tmp_transit = tmp.parent
			else:#У удаляемого элемента(tmp) есть левый потомок
				""" Не нужно менять коэффициенты skew, h_r_tree, h_l_tree """
				if tmp.parent is None:#Удалаемый элемент это корень size = 2
					tmp.left.parent = None
					self.root = tmp.left
					tmp_transit = None#Для функции count_skew_delete
					orientation = "None"
					""" Нужно менять коэффициенты skew, h_r_tree, h_l_tree """
				else:#У удаляемого элемента(tmp) есть родитель
					"""
					приходим слева то есть +1 к skew, у tmp.parent
					"""
					if tmp.parent.left is tmp:
						tmp.parent.left = tmp.left
						orientation = "left"
						"""
						приходим справа то есть -1 к skew, у tmp.parent
						"""
					elif tmp.parent.right is tmp:
						tmp.parent.right = tmp.left
						orientation = "right"
					tmp.left.parent = tmp.parent
					tmp_transit = tmp.parent
		else:#У удаляемого элемента(tmp) есть правое поддерево
			tmp_min = self.__find_min(tmp)
			if tmp_min.parent is tmp:
				""" 
				приходим справа то есть -1 к skew, в tmp_min(после переназначений)
				"""
				if tmp.parent is None:#Удаляемый элемент(tmp) это корень 
					tmp_min.parent = None
					self.root = tmp_min
				else:#У удаляемого элемента(tmp) есть родитель
					tmp_min.parent = tmp.parent
					if tmp.parent.right is tmp:
						tmp.parent.right = tmp_min
					elif tmp.parent.left is tmp:
						tmp.parent.left = tmp_min
						
				if tmp.left is not None:
					tmp.left.parent = tmp_min
				tmp_min.left = tmp.left
				
				#tmp_min встаёт на место tmp и получает её старые атрибуты
				#которые будут откорректированы в count_skew_delete
				tmp_min.skew = tmp.skew
				tmp_min.h_r_tree = tmp.h_r_tree
				tmp_min.h_l_tree = tmp.h_l_tree
				
				orientation = "right"
				tmp_transit = tmp_min
			else:
				"""
				приходим слева то есть +1 к skew, в tmp_min.parent(до переназначений)
				"""
				orientation = "left"
				tmp_transit = tmp_min.parent
				
				if tmp.parent is None:#Удаляемый элемент(tmp) это корень 
					tmp_min.parent.left = tmp_min.right
					if tmp_min.right is not None:
						tmp_min.right.parent = tmp_min.parent
					tmp_min.parent = None
					self.root = tmp_min
				else:#У удаляемого элемента(tmp) есть родитель
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
				#tmp.left не None потому что у tmp правое поддерево 
				#состоит минимум из двух элементов
				tmp.left.parent = tmp_min
				tmp_min.left = tmp.left
		
		self.__count_skew_delete(tmp_transit, orientation)


	def __count_skew_delete(self, tmp_transit, orientation):
		"""
		orientation - пришли справа "right", пришли слева "left", 
		не надо менять коэффициенты "None"
		"right" - у tmp_transit -1 к skew, -1 к h_r_tree
		"left" - у tmp_transit +1 к skew, -1 к h_l_tree
		tmp_transit - в этом объекте изменяем атрибуты
		"""
		if orientation == "None":
			return
		elif orientation == "right":
			corrective = -1
		elif orientation == "left":
			corrective = 1
		
		if tmp_transit.skew + corrective == 2: #было 1 стало 2
			
			tmp_transit.h_l_tree -= 1
			if tmp_transit.h_l_tree + 1 == \
					max(tmp_transit.right.h_r_tree, tmp_transit.right.h_l_tree):
				#Условие для малого левого вращения
				if tmp_transit.right.h_l_tree < tmp_transit.right.h_r_tree:
					#Высота сокращается до корня!!!!
					#Нужно продолжать вызывать функцию
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
						
					self.__small_left_rotation(tmp_transit.right)
						
					#продолжаем вызывать функцию
					self.__count_skew_delete(tmp_next, orientation)
				#Условие для большого левого вращения
				elif tmp_transit.right.h_l_tree > tmp_transit.right.h_r_tree:
					#Высота сокращается до корня!!!!
					#Нужно продолжать вызывать функцию
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
							
					self.__big_left_rotation(tmp_transit.right)
						
					#продолжаем вызывать функцию
					self.__count_skew_delete(tmp_next, orientation)
						
				elif tmp_transit.right.h_l_tree == tmp_transit.right.h_r_tree:
					#Особый случай!!!
					self.__small_left_rotation(tmp_transit.right)
						
		elif tmp_transit.skew + corrective == 1: #было 0 стало 1
			
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
				
		elif tmp_transit.skew + corrective == -1: #было 0 стало -1
			
			tmp_transit.skew += corrective
			tmp_transit.h_r_tree -= 1
			
		elif tmp_transit.skew + corrective == -2: #было -1 стало -2
			
			tmp_transit.h_r_tree -= 1
			if tmp_transit.h_r_tree + 1 == \
					max(tmp_transit.left.h_r_tree, tmp_transit.left.h_l_tree):
				#Условие для малого правого вращения
				if tmp_transit.left.h_l_tree > tmp_transit.left.h_r_tree:
					#Высота сокращается до корня!!!!
					#Нужно продолжать вызывать функцию
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
							
					self.__small_right_rotation(tmp_transit.left)
						
					#продолжаем вызывать функцию
					self.__count_skew_delete(tmp_next, orientation)
				#Условие для большого правого вращения
				elif tmp_transit.left.h_l_tree < tmp_transit.left.h_r_tree:
					#Высота сокращается до корня!!!!
					#Нужно продолжать вызывать функцию
					tmp_next = tmp_transit.parent
					if tmp_transit.parent is not None:
						if tmp_transit.parent.right is tmp_transit:
							orientation = "right"
						elif tmp_transit.parent.left is tmp_transit:
							orientation = "left"
					else:
						orientation = "None"
							
					self.__big_right_rotation(tmp_transit.left)
						
					#продолжаем вызывать функцию
					self.__count_skew_delete(tmp_next, orientation)
					
				elif tmp_transit.left.h_l_tree == tmp_transit.left.h_r_tree:
					#Особый случай!!!
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


	def show(self):
		"""
		Returns an ordered list of keys,
		the tree becomes empty
		"""
		B = [0]*self.size
		i = 0
		tmp = self.root
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


if __name__ == "__main__":	
	import random
	"""
	Создается список фиксированной 
	длины(можно сделать случайной длины это не принципиально)
	из случайных чисел от 0 до 100, также эти числа добавляются в дерево.
	Далее выводится список и с помощью метода show(), выводится
	список ключей дерева. Так как метод show() опусташает дерево,
	то по упорядоченности списка ключей можно судить о 
	правильной/неправильной работе дерева.
	У меня нету доказательства, что этот способ тестирования кода, 
	гарантирует абсолютную правильность кода.
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
			B = tree.show()
			print(B)
			if sorted(A) == B:	
				print("Ok")
			else:
				print("Failure")
				print("Пройдено тестов",p+1 ,"из", N)
				break
				
		except:
			print(A)
			print("Failure")
			print("Пройдено тестов",p ,"из", N)
			break
		if p+1 == N:
			print("Пройдено тестов",p+1 ,"из", N)

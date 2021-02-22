class Node:
	
	def __init__(self, key, value):
		
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None


class RedBlackNode(Node):
	
	def __init__(self, key, value):
		
		Node.__init__(self, key, value)
		self.color = "red"


class Tree:
	
	def __init__(self):
		
		self.root = None
		self.size = 0
	
	def create_node(self, key, value):
		
		return Node(key, value)
		
		
	def push(self, key, value=None):
		
		x = self.create_node(key, value)

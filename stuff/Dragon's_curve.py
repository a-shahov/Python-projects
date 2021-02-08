import turtle
import math as m


def draw_right(length, depth):
	
	if depth == 0:
		turtle.forward(length)
	else:
		turtle.right(45)
		draw_right(length/m.sqrt(2), depth-1)
		turtle.left(90)
		draw_left(length/m.sqrt(2), depth-1)
		turtle.right(45)
		

def draw_left(length, depth):
		
	if depth == 0:
		turtle.forward(length)
	else:
		turtle.left(45)
		draw_right(length/m.sqrt(2), depth-1)
		turtle.right(90)
		draw_left(length/m.sqrt(2), depth-1)
		turtle.left(45)
		

def draw(length, depth):
	"""
	LOL!
	"""
	draw_right(length, depth)


turtle.penup()
turtle.goto(-200,0)
turtle.pendown()
turtle.speed('fastest')
turtle.shape('turtle')
turtle.width(3)

draw(300,10)

a = input()

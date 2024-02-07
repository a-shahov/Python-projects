import turtle


def draw(length, depth):
	
	if depth == 0:
		turtle.forward(length)
	else:
		turtle.left(45)
		draw(length/2, depth-1)
		turtle.right(90)
		draw(length/2, depth-1)
		turtle.left(45)
		
	
turtle.penup()
turtle.goto(-200,-100)
turtle.pendown()
turtle.speed('fastest')
turtle.shape('turtle')
turtle.width(3)

draw(5000,10)

a = input()

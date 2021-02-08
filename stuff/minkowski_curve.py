import turtle


def draw(length, depth):
	
	if depth == 0:
		turtle.forward(length)
	else:
		draw(length/4, depth-1)
		turtle.left(90)
		draw(length/4, depth-1)
		turtle.right(90)
		draw(length/4, depth-1)
		turtle.right(90)
		draw(length/4, depth-1)
		draw(length/4, depth-1)
		turtle.left(90)
		draw(length/4, depth-1)
		turtle.left(90)
		draw(length/4, depth-1)
		turtle.right(90)
		draw(length/4, depth-1)


turtle.penup()
turtle.goto(-280,0)
turtle.pendown()
turtle.speed('fastest')
turtle.shape('turtle')
turtle.width(3)

draw(540,3)

a = input()

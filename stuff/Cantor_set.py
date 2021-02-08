import turtle


def draw(length, depth, x, y):
	
	if depth == 0:
		turtle.forward(length)
	else:
		turtle.forward(length)
		turtle.penup()
		turtle.goto(x,y-15)
		turtle.pendown()
		draw(length/3, depth-1, x, y-15)
		turtle.penup()
		turtle.goto(x + 2*length/3, y-15)
		turtle.pendown()
		draw(length/3, depth-1, x + 2*length/3, y-15)

	
x, y = -350, 0
turtle.penup()
turtle.goto(x, y)
turtle.pendown()
turtle.speed('fastest')
turtle.shape('turtle')
turtle.width(1)

draw(700, 6, x, y)

a = input()


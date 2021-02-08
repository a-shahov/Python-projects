import turtle


def draw(length, depth):
	
	if depth == 0: 
		turtle.forward(length)
	else:
		draw(length/3, depth-1)
		turtle.left(60)
		draw(length/3, depth-1)
		turtle.right(120)
		draw(length/3, depth-1)
		turtle.left(60)
		draw(length/3, depth-1)
	

def draw_snow(length, depth):
	
	draw(length, depth)
	turtle.right(120)
	draw(length, depth)
	turtle.right(120)
	draw(length, depth)


turtle.speed('fastest')
turtle.shape('turtle')
turtle.penup()
turtle.goto(-280,160)
turtle.pendown()
turtle.color("black", "red")
turtle.width(3)
turtle.begin_fill()
draw_snow(540, 3)
turtle.end_fill()
	
a = input()

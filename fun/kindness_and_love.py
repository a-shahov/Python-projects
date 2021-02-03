import graphics as gr
import time
import math


class Line:
	
	def __init__(self, size, point_start, point_finish, window):
		
		loc_param = 0.225 #line length to width ratio
		_line = gr.Line(point_start, point_finish)
		_line.setWidth(loc_param * size)
		_line.setOutline("black")
		_line.draw(window)


def love(size):
	
	win_size = 1.3 * math.sqrt(2) * 2 * size
	window = gr.GraphWin("LOVE", 1.4 * win_size, win_size)
	
	time.sleep(1.2)
	background(size, win_size, window)
	time.sleep(1.5)
	vertical_line(size, win_size, window)
	horizontal_line(size, win_size, window)
	window.getMouse()
	window.close()
	

def background(size, win_size, window):
	
	sieg_background = gr.Rectangle(gr.Point(0, 0),
		gr.Point(1.4*win_size, win_size))
	sieg_background.setFill("red")
	sieg_background.draw(window)
	
	sieg_circle = gr.Circle(gr.Point(1.4*win_size/2, win_size/2),
		win_size/2.4)
	sieg_circle.setOutline("red")
	sieg_circle.setFill("white")
	sieg_circle.draw(window)


def vertical_line(size, win_size, window):
	
	loc_iter = 50
	step = size/loc_iter
	point_start = gr.Point(1.4*win_size/2, win_size/2)
	x1, y1 = 1.4*win_size/2, win_size/2
	x2, y2 = 1.4*win_size/2, win_size/2
	x3, y3 = 1.4*win_size/2, win_size/2
	x4, y4 = 1.4*win_size/2, win_size/2

	
	for i in range(loc_iter):
		
		x1 += step/math.sqrt(2)
		y1 += step/math.sqrt(2)
		x2 += step/math.sqrt(2)
		y2 -= step/math.sqrt(2)
		x3 -= step/math.sqrt(2)
		y3 += step/math.sqrt(2)
		x4 -= step/math.sqrt(2)
		y4 -= step/math.sqrt(2)
		point_finish_1 = gr.Point(x1, y1)
		point_finish_2 = gr.Point(x2, y2)
		point_finish_3 = gr.Point(x3, y3)
		point_finish_4 = gr.Point(x4, y4)
		first_line = Line(size, point_start, point_finish_1, window)
		second_line = Line(size, point_start, point_finish_2, window)
		third_line = Line(size, point_start, point_finish_3, window)
		fourth_line = Line(size, point_start, point_finish_4, window)
		
	
	
def horizontal_line(size, win_size, window):
	
	cor = 0.225*0.5*size/math.sqrt(2)
	loc_iter = 50
	step = size/loc_iter
	point_start_1 = gr.Point(1.4*win_size/2+size/math.sqrt(2)-cor,
		win_size/2+size/math.sqrt(2)-cor)
	point_start_2 = gr.Point(1.4*win_size/2+size/math.sqrt(2)-cor,
		win_size/2-size/math.sqrt(2)+cor)
	point_start_3 = gr.Point(1.4*win_size/2-size/math.sqrt(2)-cor,
		win_size/2+size/math.sqrt(2)-cor)
	point_start_4 = gr.Point(1.4*win_size/2-size/math.sqrt(2)+cor,
		win_size/2-size/math.sqrt(2)-cor)
	x1, y1 = 1.4*win_size/2+size/math.sqrt(2)-cor, \
		win_size/2+size/math.sqrt(2)-cor
	x2, y2 = 1.4*win_size/2+size/math.sqrt(2)-cor, \
		win_size/2-size/math.sqrt(2)+cor
	x3, y3 = 1.4*win_size/2-size/math.sqrt(2)-cor, \
		win_size/2+size/math.sqrt(2)-cor
	x4, y4 = 1.4*win_size/2-size/math.sqrt(2)+cor, \
		win_size/2-size/math.sqrt(2)-cor
	
	for i in range(loc_iter):
		
		x1 += step/math.sqrt(2)
		y1 -= step/math.sqrt(2)
		x2 -= step/math.sqrt(2)
		y2 -= step/math.sqrt(2)
		x3 += step/math.sqrt(2)
		y3 += step/math.sqrt(2)
		x4 -= step/math.sqrt(2)
		y4 += step/math.sqrt(2)
		point_finish_1 = gr.Point(x1, y1)
		point_finish_2 = gr.Point(x2, y2)
		point_finish_3 = gr.Point(x3, y3)
		point_finish_4 = gr.Point(x4, y4)
		first_line = Line(size, point_start_1, point_finish_1, window)
		second_line = Line(size, point_start_2, point_finish_2, window)
		third_line = Line(size, point_start_3, point_finish_3, window)
		fourth_line = Line(size, point_start_4, point_finish_4, window)


love(211)

import graphics as gr
import time
import math


class Line:
	
	def __init__(self, size, point_start, point_finish, window):
		
		loc_param = 0.225 #line length to width ratio
		self._line = gr.Line(point_start, point_finish)
		self._line.setWidth(loc_param * size)
		self._line.setOutline("black")
		self._line.draw(window)
	
	def undraw(self):
		self._line.undraw()


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
	
	loc_iter = 35
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
		
		try:
			first_line_ = first_line
			second_line_ = second_line
			third_line_ = third_line
			fourth_line_ = fourth_line
		except:
			pass
			
		first_line = Line(size, point_start, point_finish_1, window)
		second_line = Line(size, point_start, point_finish_2, window)
		third_line = Line(size, point_start, point_finish_3, window)
		fourth_line = Line(size, point_start, point_finish_4, window)
		
		try:
			first_line_.undraw()
			second_line_.undraw()
			third_line_.undraw()
			fourth_line_.undraw()
		except:
			pass
		
		time.sleep(0.03)
	
	
def horizontal_line(size, win_size, window):
	
	cor = 0.225*0.5*size/math.sqrt(2)
	loc_iter = 35
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
		
		try:
			first_line_ = first_line
			second_line_ = second_line
			third_line_ = third_line
			fourth_line_ = fourth_line
		except:
			pass
		
		first_line = Line(size, point_start_1, point_finish_1, window)
		second_line = Line(size, point_start_2, point_finish_2, window)
		third_line = Line(size, point_start_3, point_finish_3, window)
		fourth_line = Line(size, point_start_4, point_finish_4, window)
		
		try:
			first_line_.undraw()
			second_line_.undraw()
			third_line_.undraw()
			fourth_line_.undraw()
		except:
			pass
		
		time.sleep(0.03)


love(211)

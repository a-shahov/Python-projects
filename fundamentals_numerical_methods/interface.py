import tkinter as tk
from inspect import isfunction

class Interface(tk.Frame):
	
	def __init__(self, parent=None, width=800, height=700):
		tk.Frame.__init__(self, parent)
		self.rlwidth = (0.05, 0.25, 0.05, 0.60, 0.05) #относительные размеры основных виджетов в ширину с учётом отступов
		self.rlheight = (0.05, 0.18, 0.05, 0.67, 0.05) #относительные размеры основных виджетов в высоту с учётом отступов
		self.btn1_x = None #координаты клика мышкой по объекту canvas
		self.btn1_y = None #они не равны None только в случае нажатой кнопки
		self.set_settigs(width, height)
		self.rollbox_res = list(self.standardbox_res) #(x1,y1,x2,y2)
		self.rollbox_func = list(self.standardbox_func) #(x1,y1,x2,y2)
		
		out_result = self.makeOutputWidget("Result:", "res") #res and func - идентификаторы для обработчиков!
		out_function = self.makeOutputWidget("Function:", "func")
		frm_result = out_result[0] #фрейм для компоновщика
		frm_function = out_function[0] #фрейм для компоновщика
		frm_canvas = self.makeCanvasButtons() #фрейм для компоновщика
		self.canv_result = out_result[1]
		self.canv_function = out_function[1]
		
		self.master.geometry("{}x{}".format(width, height))
		self.master.title("Numerical methods")
		self.placer(frm_canvas, frm_result, frm_function)
		
		self.bind("<Configure>", self.resize_buttons)
	
	def set_settigs(self, width, height):
		self.width = width #размеры фрейма в целом
		self.height = height #размеры фрейма в целом
		
		#Инициализация атрибутов необходимых для перемещения объекта внутри canvas
		self.standardbox_res = (0+2, 0+2, self.width*self.rlwidth[3]-2, self.height*self.rlheight[1]-2) #(x1,y1,x2,y2)
		self.standardbox_func = (0+2, 0+2, self.width*self.rlwidth[3]-2, self.height*self.rlheight[3]-2) #(x1,y1,x2,y2)
	
	def placer(self, frm_canv, frm_res, frm_func):
		"""
		self.rlwidth = (0.05, 0.25, 0.05, 0.60, 0.05)
		self.rlheight = (0.05, 0.15, 0.05, 0.70, 0.05)
		"""
		canv_x = self.rlwidth[0]
		canv_y = self.rlheight[0]
		canv_rwidth = self.rlwidth[1]
		canv_rheight = 1 - (self.rlheight[0] + self.rlheight[4])
		
		res_x = canv_x + canv_rwidth + self.rlwidth[2]
		res_y = canv_y
		res_rwidth = self.rlwidth[3]
		res_rheight = self.rlheight[1]
		
		func_x = res_x
		func_y = res_y + res_rheight + self.rlheight[2]
		func_rwidth = res_rwidth
		func_rheight = self.rlheight[3]
		
		frm_canv.place(relx=canv_x, rely=canv_y, relwidth=canv_rwidth, relheight=canv_rheight)
		frm_res.place(relx=res_x, rely=res_y, relwidth=res_rwidth, relheight=res_rheight)
		frm_func.place(relx=func_x, rely=func_y, relwidth=func_rwidth, relheight=func_rheight)
	
	def resize_buttons(self, event):
		self.set_settigs(event.width, event.height)
		self.makeButtons(self.button_canvas, self.functions)
		
	def _button1(self, event):
		self.btn1_x = event.x
		self.btn1_y = event.y
	
	def _button1_motion(self, event, identifier):
		"""
		sbox and rbox = (x1, y1, x2, y2)
		"""
		if (self.btn1_x is None) or (self.btn1_y is None):
			return
		if identifier == "func":
			rbox = self.rollbox_func
			sbox = self.standardbox_func
		elif identifier == "res":
			rbox = self.rollbox_res
			sbox = self.standardbox_res

		displacement_vector = (event.x - self.btn1_x, event.y - self.btn1_y)
		self.btn1_x = event.x
		self.btn1_y = event.y
		for axis, offset in zip(["x", "y"], displacement_vector):
			if axis == "x":
				rbox_c1, rbox_c2 = rbox[0], rbox[2] #x1, x2
				sbox_c1, sbox_c2 = sbox[0], sbox[2] #x1, x2
				tuple_offset = (offset, 0)
			elif axis == "y":
				rbox_c1, rbox_c2 = rbox[1], rbox[3] #y1, y2
				sbox_c1, sbox_c2 = sbox[1], sbox[3] #y1, y2
				tuple_offset = (0, offset)
			if (offset >= 0) and (offset <= (sbox_c1 - rbox_c1)):
				event.widget.move("all", *tuple_offset)
				self._mover_rbox(offset, axis, identifier)
			elif (offset < 0) and (abs(offset) <= (rbox_c2 - sbox_c2)):
				event.widget.move("all", *tuple_offset)
				self._mover_rbox(offset, axis, identifier)
	
	def _mover_rbox(self, offset, axis, identifier):
		if axis == "x":
			indexes = (0, 2)
		elif axis == "y":
			indexes = (1, 3)
		if identifier == "func":
			for i in indexes:
				self.rollbox_func[i] += offset
		elif identifier == "res":
			for i in indexes:
				self.rollbox_res[i] += offset
	
	def _button_release(self, event):
		self.btn1_x = None
		self.btn1_y = None
	
	def makeOutputWidget(self, name, identifier):
		frm = tk.Frame(self)
		tk.Label(frm, text=name).pack(anchor="w")
		canv = tk.Canvas(frm, bg="white", bd=2, relief="groove")
		canv.bind("<Button-1>", self._button1)
		canv.bind("<B1-Motion>", lambda event: self._button1_motion(event, identifier))
		canv.bind("<ButtonRelease-1>", self._button_release)
		canv.pack(fill="both", expand="yes")
		return frm, canv
	
	def makeCanvasButtons(self):
		frm = tk.Frame(self)
		functions = self.find_functions()
		canvas = tk.Canvas(frm, bg="white", bd=2, relief="groove")
		canvas.bind("<Button-4>", lambda event:canvas.yview("scroll", "-5", "units"))
		canvas.bind("<Button-5>", lambda event:canvas.yview("scroll", "5", "units"))
		sbar = tk.Scrollbar(frm, command=canvas.yview, width=13)
		canvas.config(yscrollcommand=sbar.set)
		sbar.pack(side="right", fill="y")
		canvas.pack(side="left", fill="both", expand="yes")
		self.makeButtons(canvas, functions)
		self.button_canvas = canvas
		self.functions = functions
		return frm 
	
	def makeButtons(self, canvas, functions):
		"""
		functions = {"number": {"name": "string", "function": <function>, "content": "string"}}
		"""
		canvas.delete("all")
		btn_height = 50 #высота кнопки в пикселях
		canvas.config(scrollregion=(0,0,int(self.rlwidth[1]*self.width)-15, 15 + len(functions)*(15+btn_height)))
		i = 0
		for key in sorted(functions):
			btn = tk.Button(canvas, text="{} ({})".format(functions[key]["name"], key))
			btn.config(command=lambda key=key: self.handler(functions[key]["function"], functions[key]["content"]))
			btn.bind("<Button-4>", lambda event:canvas.yview("scroll", "-5", "units"))
			btn.bind("<Button-5>", lambda event:canvas.yview("scroll", "5", "units"))
			x = int((self.rlwidth[1]*self.width-15)*0.5)
			y = int(15+btn_height*0.5 + i*(btn_height+15))
			id_btn = canvas.create_window(x, y, window=btn)
			canvas.itemconfig(id_btn, width=int((self.rlwidth[1]*self.width-15)*0.8), height=btn_height)
			i += 1
	
	def handler(self, function, content):
		"""
		meaning of the names
		result = function() - what the function returns
		function = function content 
		"""
		self._handler(self.canv_result, function(), "res")
		self._handler(self.canv_function, content, "func")
	
	def _handler(self, canv, text, identifier):
		if identifier == "func":
			sbox = self.standardbox_func
		elif identifier == "res":
			sbox = self.standardbox_res
		canv.delete("all")
		id_obj = canv.create_text(0, 0, text=text+"\n") #поправка из-за подписей Result и Function
		x1, y1, x2, y2 = canv.bbox(id_obj)
		canv.move(id_obj, (x2-x1)*0.5+3, (y2-y1)*0.5+3) #кухонная поправка из-за границы
		for i, cord1, cord2 in (2, x1, x2), (3, y1, y2):
			if (cord2-cord1) > sbox[i]:
				self._setter_rbox(cord2-cord1 + 8, i, identifier) #кухонная поправка из-за границы
			else:
				self._setter_rbox(sbox[i], i, identifier) 
		
	def _setter_rbox(self, offset, axis, identifier):
		if identifier == "func":
			self.rollbox_func[axis-2] = 0 + 2 #кухонная поправка из-за границы
			self.rollbox_func[axis] = offset 
		elif identifier == "res":
			self.rollbox_res[axis-2] = 0 + 2 #кухонная поправка из-за границы
			self.rollbox_res[axis] = offset

	def find_functions(self, name_file="functions"):
		"""
		return dictionary = {"number": {"name": "string", "function": <function>, "content": "string"}}
		"""
		dict_func = {}
		list_functions = __import__(name_file)
		content_functions = self.file_analysis(name_file)
		for name in dir(list_functions):
			if isfunction(getattr(list_functions, name)):
				func = getattr(list_functions, name)
				dict_func[func.__doc__] = {"name": name, "function": func, "content": content_functions[name]}
		return dict_func
								
	def file_analysis(self, name_file):
		"""
		return dictionary = {"name": "string"}
		"""
		with open(name_file + ".py", "r") as file_functions:
			content_functions = {}
			new_func = False
			for line in file_functions:
				if not new_func and line.startswith("def"):
					new_func = not new_func
					tmp_name = line.split()[1].split("(")[0]
					tmp_content = line
					continue
				elif new_func and line.startswith("def"):
					content_functions[tmp_name] = tmp_content.strip()
					tmp_name = line.split()[1].split("(")[0]
					tmp_content = line
					continue
				if new_func and (line.startswith("\t") or line.startswith(" ") or line.startswith("")):
					tmp_content += line
				elif new_func and not (line.startswith("\t") or line.startswith(" ") or line.startswith("")):
					new_func = not new_func
					content_functions[tmp_name] = tmp_content.strip() 
			else:
				if new_func:
					content_functions[tmp_name] = tmp_content.strip()
			return content_functions
					
if __name__ == "__main__":
	Interface().pack(fill="both", expand="yes")
	tk.mainloop()

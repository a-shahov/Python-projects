import numpy as np
import matplotlib.pyplot as plt
import math

def bisection():
	"1.1"
	f = lambda x: np.exp(-x) - np.sin(x)
	a, b = 0, 2
	e = 0.0001
	
	x = np.linspace(a, b, 200)
	figure = plt.figure()
	plt.xlabel("x")
	plt.ylabel("f(x)")
	plt.plot(x, f(x))
	figure.savefig("bisection.png")
	
	n = 0
	while True:
		n += 1
		c = a + (b-a)/2
		if f(a)*f(c) < 0:
			b = c
		elif f(c)*f(b) < 0:
			a = c 
		elif f(c) == 0:
			return "solution: {0}\nerror: {1}\nn = {2}".format(c, e, n)
		if (b-a) <= e:
			return "solution: {0}\nerror: {1}\nn = {2}".format((b-a)/2 + a, e, n)

def chord_method():
	"1.2"
	f = lambda x: 5*np.exp(x) - 7*np.power(x, 2) + 15
	a, b = -2, 0
	e = 0.0000001
	
	x = np.linspace(a, b, 200)
	figure = plt.figure()
	plt.xlabel("x")
	plt.ylabel("f(x)")
	plt.plot(x, f(x))
	figure.savefig("chord_method.png")
	
	def check(a, b, f):
		x = a - f(a) / (f(b) - f(a)) * (b - a)
		if f(x) > 0:
			return False
		return True
	
	n = 0
	sequence = []
	kind = check(a, b, f)
	while True: 
		n += 1
		if kind: #если True то вогнута, иначе выгнута
			sequence.append(a)
			x = a - f(a) / (f(b) - f(a)) * (b - a)
			a = x 
		else:
			sequence.append(b)
			x = a - f(a) / (f(b) - f(a)) * (b - a)
			b = x 
		if n >= 2:
			err = (x - sequence[-1]) / (1 - (x - sequence[-1]) / (sequence[-2] - sequence[-1]))
			if abs(err) < e:
				return "solution: {0}\nerror: {1}\nn = {2}".format(x, e, n)

def newton():
	"1.3"
	f = lambda x: 5*np.exp(x) - 7*np.power(x, 2) + 15
	f1 = lambda x: 5*np.exp(x) - 14*x
	a, b = -2, 0
	e = 0.0000001
	
	x = np.linspace(a, b, 200)
	figure = plt.figure()
	plt.xlabel("x")
	plt.ylabel("f(x)")
	plt.plot(x, f(x))
	figure.savefig("newton.png")
	
	n = 0
	sequence = [a]
	while True:
		n += 1
		x = sequence[-1] - f(sequence[-1]) / f1(sequence[-1])
		if n >= 2:
			err = (x - sequence[-1]) / (1 - (x - sequence[-1]) / (sequence[-2] - sequence[-1]))
			if abs(err) < e:
				return "solution: {0}\nerror: {1}\nn = {2}".format(x, e, n)
		sequence.append(x)

def iteration():
	"1.4"
	f = lambda x: 3*np.exp(x+2) - 7*np.power(x-1, 2) + 25*np.sin(x+3) - 5
	a, b = -2, 2
	e = 0.00001

	x = np.linspace(a, b, 200)
	figure = plt.figure()
	plt.xlabel("x")
	plt.ylabel("f(x)")
	plt.plot(x, f(x))
	figure.savefig("iteration.png")	
	
	fi = lambda x: x - f(x)/70 #Максимум производной примерно равен 130
	n = 0
	sequence = [a]
	while True:
		n += 1
		x = fi(sequence[-1])
		if n >= 2:
			err = (x - sequence[-1]) / (1 - (x - sequence[-1]) / (sequence[-2] - sequence[-1]))
			if abs(err) < e:
				return "solution: {0}\nerror: {1}\nn = {2}".format(x, e, n)
		sequence.append(x)

def gauss():
	"2.1"
	A = np.array([[0.68, 0.05, -0.11, 0.08, 2.15],
			[-0.11, 0.84, 0.28, 0.06, -0.83],
			[-0.08, 0.15, 1, -0.12, 1.16], 
			[0.21, -0.13, 0.27, 1, 0.44]], dtype=np.float64)
	
	result = str(A) + "\n"
	n = len(A[:, 0])
	for i in range(n):
		for k in range(n-(i+1)):
			koeff = -(A[i+k+1, i] /  A[i, i])
			A[i+k+1] = A[i+k+1] + A[i] * koeff
			
	for i in range(n-1, -1, -1):
		for k in range(1, i+1):
			koeff = -(A[i-k, i] / A[i, i])
			A[i-k] = A[i-k] + A[i] * koeff
	
	index = [i for i in range(n)]
	x = A[:, n] / A[index, index]
	print(A)
	for i in range(n):
		result += "x{}={}  ".format(i+1, round(x[i], 3))
	return result

def iteration_matrix():
	"2.2"
	A = np.array([[0.68, 0.05, -0.11, 0.08, 2.15],
			[-0.11, 0.84, 0.28, 0.06, -0.83],
			[-0.08, 0.15, 1, -0.12, 1.16], 
			[0.21, -0.13, 0.27, 1, 0.44]], dtype=np.float64)
	result = str(A) + "\n"
	e = 0.000001
	
	def check(matrix):
		n = matrix.shape[0]
		mat_kf = matrix[:, :-1].copy() #только коэффициенты 
		mat_b = matrix[:, -1].copy().reshape((n, 1)) #свободные члены
		for i in range(n):
			kf = mat_kf[i,i]
			mat_kf[i,i] = 0
			mat_b[i] = mat_b[i] / kf 
			for j in range(n):
				mat_kf[i, j] = mat_kf[i, j] / kf
		tmp = [np.add.reduce(abs(mat_kf[i])) for i in range(n)]
		q = max(tmp)
		if q < 1:
			metrika = lambda x, y: abs(x - y).max()
			return np.concatenate([-mat_kf, mat_b], axis=1), q, metrika
		
		mat_kf = matrix[:, :-1].copy() #только коэффициенты 
		mat_b = matrix[:, -1].copy().reshape((n, 1)) #свободные члены
		for i in range(n):
			kf = mat_kf[i,i]
			mat_kf[i,i] = 0
			mat_b[i] = mat_b[i] / kf 
			for j in range(n):
				mat_kf[i, j] = mat_kf[i, j] / kf
		tmp = [np.add.reduce(abs(mat_kf[:, i])) for i in range(n)]
		q = max(tmp)
		if q < 1:
			metrika = lambda x, y: abs(x - y).sum()
			return np.concatenate([-mat_kf, mat_b], axis=1), q, metrika
		
		mat_kf = matrix[:, :-1].copy() #только коэффициенты 
		mat_b = matrix[:, -1].copy().reshape((n, 1)) #свободные члены
		for i in range(n):
			kf = mat_kf[i,i]
			mat_kf[i,i] = 0
			mat_b[i] = mat_b[i] / kf 
			for j in range(n):
				mat_kf[i, j] = mat_kf[i, j] / kf
		q = np.add.reduce(mat_kf ** 2) ** (0.5)
		if q < 1:
			metrika = lambda x, y: (((x - y) ** 2).sum()) ** (0.5)
			return np.concatenate([-mat_kf, mat_b], axis=1), q, metrika
		return False, False, False
	
	matrix, q, metrika = check(A)
	if matrix is False:
		return "Матрица не подходит для метода итераций"	
	
	length = matrix.shape[0] 
	sequence = [matrix[:, -1]] #первое приближение
	n = 0
	while True:
		n += 1
		x_k = sequence[-1]
		x_k1 = []
		for i in range(length):
			tmp = 0
			for j in range(length):
				tmp += matrix[i, j] * x_k[j]
			tmp += matrix[i, -1] #свободный член
			x_k1.append(tmp)
		sequence.append(np.array(x_k1))
		if metrika(sequence[-1], sequence[-2]) * q / (1 - q) < e:
			for i in range(length):
				result += "x{}={}  ".format(i+1, round(sequence[-1][i], 4))
			return result + "\nn = {}".format(n)

def seidel():
	"2.3"
	A = np.array([[0.68, 0.05, -0.11, 0.08, 2.15],
			[-0.11, 0.84, 0.28, 0.06, -0.83],
			[-0.08, 0.15, 1, -0.12, 1.16], 
			[0.21, -0.13, 0.27, 1, 0.44]], dtype=np.float64)
	result = str(A) + "\n"
	e = 0.000001
	
	def check(matrix):
		n = matrix.shape[0]
		mat_kf = matrix[:, :-1].copy() #только коэффициенты 
		mat_b = matrix[:, -1].copy().reshape((n, 1)) #свободные члены
		for i in range(n):
			kf = mat_kf[i,i]
			mat_kf[i,i] = 0
			mat_b[i] = mat_b[i] / kf 
			for j in range(n):
				mat_kf[i, j] = mat_kf[i, j] / kf
		tmp = [np.add.reduce(abs(mat_kf[i])) for i in range(n)]
		q = max(tmp)
		if q < 1:
			metrika = lambda x, y: abs(x - y).max()
			return np.concatenate([-mat_kf, mat_b], axis=1), q, metrika
		
		mat_kf = matrix[:, :-1].copy() #только коэффициенты 
		mat_b = matrix[:, -1].copy().reshape((n, 1)) #свободные члены
		for i in range(n):
			kf = mat_kf[i,i]
			mat_kf[i,i] = 0
			mat_b[i] = mat_b[i] / kf 
			for j in range(n):
				mat_kf[i, j] = mat_kf[i, j] / kf
		tmp = [np.add.reduce(abs(mat_kf[:, i])) for i in range(n)]
		q = max(tmp)
		if q < 1:
			metrika = lambda x, y: abs(x - y).sum()
			return np.concatenate([-mat_kf, mat_b], axis=1), q, metrika
		
		mat_kf = matrix[:, :-1].copy() #только коэффициенты 
		mat_b = matrix[:, -1].copy().reshape((n, 1)) #свободные члены
		for i in range(n):
			kf = mat_kf[i,i]
			mat_kf[i,i] = 0
			mat_b[i] = mat_b[i] / kf 
			for j in range(n):
				mat_kf[i, j] = mat_kf[i, j] / kf
		q = np.add.reduce(mat_kf ** 2) ** (0.5)
		if q < 1:
			metrika = lambda x, y: (((x - y) ** 2).sum()) ** (0.5)
			return np.concatenate([-mat_kf, mat_b], axis=1), q, metrika
		return False, False, False
	
	matrix, q, metrika = check(A)
	if matrix is False:
		return "Матрица не подходит для метода итераций Зейделя"
		
	length = matrix.shape[0] 
	sequence = [matrix[:, -1]] #первое приближение
	n = 0
	while True:
		n += 1
		x_k = sequence[-1]
		x_k1 = []
		for i in range(length):
			tmp = 0
			for j in range(length):
				if len(x_k1) > j:
					tmp += matrix[i, j] * x_k1[j] #отличие методов
				else:
					tmp += matrix[i, j] * x_k[j]
			tmp += matrix[i, -1] #свободный член
			x_k1.append(tmp)
		sequence.append(np.array(x_k1))
		if metrika(sequence[-1], sequence[-2]) * q / (1 - q) < e:
			for i in range(length):
				result += "x{}={}  ".format(i+1, round(sequence[-1][i], 4))
			return result + "\nn = {}".format(n)

def determinant():
	"3.1"
	A = np.array([[12, 2, 2, 3],
			[2, 7, 3, 3],
			[11, 0, 34, 4],
			[11, 33, 21, 4]])
	result = str(A) + "\n"
	n = len(A[0])
	for i in range(n):
		for k in range(n-(i+1)):
			koeff = -(A[i+k+1, i] /  A[i, i])
			A[i+k+1] = A[i+k+1] + A[i] * koeff
			
	return result + "Det = {}".format(A.diagonal().prod())

def lagrange_pol():
	"4.1"
	A = np.array([[0.05, 0.050042],
				[0.10, 0.100335],
				[0.17, 0.171657],
				[0.25, 0.255342],
				[0.30, 0.309336],
				[0.36, 0.376403]])
	x = 0.263
	result = str(A) + "\nx={}\n".format(x)
	n = len(A[:, 0])
	k = np.zeros(n) #пустой массив для коэффициентов
	for i in range(n):
		tmp = A[i, 1] #значение yi
		for j in range(n):
			if i != j:
				tmp = tmp / (A[i, 0] - A[j, 0])
		k[i] = tmp
	
	summ = 0
	for i in range(n):
		tmp = k[i]
		for j in range(n):
			if i != j:
				tmp = tmp * (x - A[j, 0])
		summ += tmp
	
	return result + "F(x)={}".format(round(summ, 6))

def left_rect():
	"5.1"
	k = 0.75471
	f = lambda x: (1 - math.pow((k * math.sin(x)), 2)) ** (-0.5)
	a, b = 0, math.pi * 36 / 180
	e = 0.00001
	n = 8 #начальная сетка
	r = 2 #коэффициент сгущения сетки
	p = 1 #порядок сходимости
	q = 1 #разность степеней членов разложения в ряд
	
	def calc_s(n):
		x = np.linspace(a, b, n+1)
		h = (b-a)/n
		s = 0
		for i in range(n):
			s += f(x[i])
		return s * h
	
	def calc_er(n, u=None, er=None):
		if u is None:
			u = np.zeros((1,3))
			er = np.zeros((1,3))
			u[0, 0] = calc_s(n)
			return u, er
		size = u.shape[0]
		if size == 1:
			n *= r
			er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + er[0, 0]
			return np.concatenate([u, tmp_u]), er
		else: #size > 1 
			n *= r**size
			tmp_er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			tmp_er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + tmp_er[0, 0]
			tmp_er[0, 1] = (tmp_u[0, 1] - u[-1, 1]) / (r**(p+q) - 1)
			tmp_u[0, 2] = tmp_u[0, 1] + tmp_er[0, 1]
			return np.concatenate([u, tmp_u]), np.concatenate([er, tmp_er])
			
	u, er = calc_er(n)
	count = 0
	while True:
		count += 1
		u, er = calc_er(n, u, er)
		if u.shape[0] == 2:
			if abs(er[-1, 0]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 1], 6), e, count)
		else:
			if abs(er[-1, 1]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 2], 6), e, count)

def right_rect():
	"5.2"
	k = 0.75471
	f = lambda x: (1 - math.pow((k * math.sin(x)), 2)) ** (-0.5)
	a, b = 0, math.pi * 36 / 180
	e = 0.0000001
	n = 8 #начальная сетка
	r = 2 #коэффициент сгущения сетки
	p = 1 #порядок сходимости
	q = 1 #разность степеней членов разложения в ряд
	
	def calc_s(n):
		x = np.linspace(a, b, n+1)
		h = (b-a)/n
		s = 0
		for i in range(1, n+1):
			s += f(x[i])
		return s * h
	
	def calc_er(n, u=None, er=None):
		if u is None:
			u = np.zeros((1,3))
			er = np.zeros((1,3))
			u[0, 0] = calc_s(n)
			return u, er
		size = u.shape[0]
		if size == 1:
			n *= r
			er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + er[0, 0]
			return np.concatenate([u, tmp_u]), er
		else: #size > 1 
			n *= r**size
			tmp_er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			tmp_er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + tmp_er[0, 0]
			tmp_er[0, 1] = (tmp_u[0, 1] - u[-1, 1]) / (r**(p+q) - 1)
			tmp_u[0, 2] = tmp_u[0, 1] + tmp_er[0, 1]
			return np.concatenate([u, tmp_u]), np.concatenate([er, tmp_er])
			
	u, er = calc_er(n)
	count = 0
	while True:
		count += 1
		u, er = calc_er(n, u, er)
		if u.shape[0] == 2:
			if abs(er[-1, 0]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 1], 6), e, count)
		else:
			if abs(er[-1, 1]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 2], 6), e, count)

def average():
	"5.3"
	k = 0.75471
	f = lambda x: (1 - math.pow((k * math.sin(x)), 2)) ** (-0.5)
	a, b = 0, math.pi * 36 / 180
	e = 0.000001
	n = 8 #начальная сетка
	r = 2 #коэффициент сгущения сетки
	p = 2 #порядок сходимости
	q = 2 #разность степеней членов разложения в ряд
	
	def calc_s(n):
		x = np.linspace(a, b, n+1)
		h = (b-a)/n
		s = 0
		for i in range(n):
			s += f(x[i] + h/2)
		return s * h
	
	def calc_er(n, u=None, er=None):
		if u is None:
			u = np.zeros((1,3))
			er = np.zeros((1,3))
			u[0, 0] = calc_s(n)
			return u, er
		size = u.shape[0]
		if size == 1:
			n *= r
			er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + er[0, 0]
			return np.concatenate([u, tmp_u]), er
		else: #size > 1 
			n *= r**size
			tmp_er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			tmp_er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + tmp_er[0, 0]
			tmp_er[0, 1] = (tmp_u[0, 1] - u[-1, 1]) / (r**(p+q) - 1)
			tmp_u[0, 2] = tmp_u[0, 1] + tmp_er[0, 1]
			return np.concatenate([u, tmp_u]), np.concatenate([er, tmp_er])
			
	u, er = calc_er(n)
	count = 0
	while True:
		count += 1
		u, er = calc_er(n, u, er)
		if u.shape[0] == 2:
			if abs(er[-1, 0]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 1], 6), e, count)
		else:
			if abs(er[-1, 1]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 2], 6), e, count)

def trapeze():
	"5.4"
	k = 0.75471
	f = lambda x: (1 - math.pow((k * math.sin(x)), 2)) ** (-0.5)
	a, b = 0, math.pi * 36 / 180
	e = 0.0000001
	n = 8 #начальная сетка
	r = 2 #коэффициент сгущения сетки
	p = 2 #порядок сходимости
	q = 2 #разность степеней членов разложения в ряд
	
	def calc_s(n):
		x = np.linspace(a, b, n+1)
		h = (b-a)/n
		s = 0
		for i in range(1, n+1):
			s += (f(x[i]) + f(x[i-1]))/2
		return s * h
	
	def calc_er(n, u=None, er=None):
		if u is None:
			u = np.zeros((1,3))
			er = np.zeros((1,3))
			u[0, 0] = calc_s(n)
			return u, er
		size = u.shape[0]
		if size == 1:
			n *= r
			er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + er[0, 0]
			return np.concatenate([u, tmp_u]), er
		else: #size > 1 
			n *= r**size
			tmp_er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			tmp_er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + tmp_er[0, 0]
			tmp_er[0, 1] = (tmp_u[0, 1] - u[-1, 1]) / (r**(p+q) - 1)
			tmp_u[0, 2] = tmp_u[0, 1] + tmp_er[0, 1]
			return np.concatenate([u, tmp_u]), np.concatenate([er, tmp_er])
			
	u, er = calc_er(n)
	count = 0
	while True:
		count += 1
		u, er = calc_er(n, u, er)
		if u.shape[0] == 2:
			if abs(er[-1, 0]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 1], 6), e, count)
		else:
			if abs(er[-1, 1]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 2], 6), e, count)

def simpson():
	"5.5"
	k = 0.75471
	f = lambda x: (1 - math.pow((k * math.sin(x)), 2)) ** (-0.5)
	a, b = 0, math.pi * 36 / 180
	e = 0.0000001
	n = 8 #начальная сетка
	r = 2 #коэффициент сгущения сетки
	p = 4 #порядок сходимости
	q = 2 #разность степеней членов разложения в ряд
	
	def calc_s(n):
		x = np.linspace(a, b, n+1)
		h = (b-a)/n
		s = 0
		for i in range(0, n-2, 2):
			s += f(x[i]) + 4 * f(x[i+1]) + f(x[i+2])
		return s * h / 3
	
	def calc_er(n, u=None, er=None):
		if u is None:
			u = np.zeros((1,3))
			er = np.zeros((1,3))
			u[0, 0] = calc_s(n)
			return u, er
		size = u.shape[0]
		if size == 1:
			n *= r
			er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + er[0, 0]
			return np.concatenate([u, tmp_u]), er
		else: #size > 1 
			n *= r**size
			tmp_er = np.zeros((1,2))
			tmp_u = np.zeros((1,3))
			tmp_u[0, 0] = calc_s(n)
			tmp_er[0, 0] = (tmp_u[0, 0] - u[-1, 0]) / (r**p - 1)
			tmp_u[0, 1] = tmp_u[0, 0] + tmp_er[0, 0]
			tmp_er[0, 1] = (tmp_u[0, 1] - u[-1, 1]) / (r**(p+q) - 1)
			tmp_u[0, 2] = tmp_u[0, 1] + tmp_er[0, 1]
			return np.concatenate([u, tmp_u]), np.concatenate([er, tmp_er])
			
	u, er = calc_er(n)
	count = 0
	while True:
		count += 1
		u, er = calc_er(n, u, er)
		if u.shape[0] == 2:
			if abs(er[-1, 0]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 1], 6), e, count)
		else:
			if abs(er[-1, 1]) < e:
				return "Значение интеграла = {}\nточность = {}\nn = {}".format(round(u[-1, 2], 6), e, count)

def kotes():
	"5.6"
	C = [2857/89600, 15741/89600, 1080/89600, 19344/89600, 5778/89600,
		5778/89600, 19344/89600, 1080/89600, 15741/89600, 2857/89600]
	k = 0.75471
	f = lambda x: (1 - math.pow((k * math.sin(x)), 2)) ** (-0.5)
	a, b = 0, math.pi * 36 / 180
	n = 10
	x = np.linspace(a, b, n)
	s = 0
	
	for i in range(n):
		s += C[i] * f(x[i])
	s *= (b - a)
	return "Значение интеграла = {}\nКоличество узлов = {}".format(round(s, 6), n)

def euler():
	"6.1"
	f = lambda x, y: x**2 + y**2
	a, b = 1, 1.2
	n = 5
	h = (b - a) / n
	y = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		tmp = y[i] + h * f(x[i], y[i])
		y.append(tmp)
	n *= 2
	h = (b - a) / n
	y1 = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		tmp = y1[i] + h * f(x[i], y1[i])
		y1.append(tmp)
	e = abs(y1[-1] - y[-1])
	return "f({}) = {}\ne = {}".format(x[-1], y1[-1], e)

def euler_cauchy():
	"6.2"
	f = lambda x, y: x**2 + y**2
	a, b = 1, 1.2
	n = 5
	h = (b - a) / n
	y = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		tmp = y[i] + h * f(x[i], y[i])
		tmp = y[i] + (h / 2) * (f(x[i], y[i]) + f(x[i+1], tmp))
		y.append(tmp)
	n *= 2
	h = (b - a) / n
	y1 = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		tmp = y1[i] + h * f(x[i], y1[i])
		tmp = y1[i] + (h / 2) * (f(x[i], y1[i]) + f(x[i+1], tmp))
		y1.append(tmp)
	e = abs(y1[-1] - y[-1]) / 3
	return "f({}) = {}\ne = {}".format(x[-1], y1[-1], e)

def middle():
	"6.3"
	f = lambda x, y: x**2 + y**2
	a, b = 1, 1.2
	n = 5
	h = (b - a) / n
	y = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		tmp_x = x[i] + h / 2
		tmp_y = y[i] + (h / 2) * f(x[i], y[i])
		tmp_y = y[i] + h * f(tmp_x, tmp_y)
		y.append(tmp_y)
	n *= 2
	h = (b - a) / n
	y1 = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		tmp_x = x[i] + h / 2
		tmp_y = y1[i] + (h / 2) * f(x[i], y1[i])
		tmp_y = y1[i] + h * f(tmp_x, tmp_y)
		y1.append(tmp_y)
	e = abs(y1[-1] - y[-1]) / 3
	return "f({}) = {}\ne = {}".format(x[-1], y1[-1], e)

def runge_kutta():
	"6.4"
	f = lambda x, y: y * (1 - x)
	a, b = 0, 0.5
	n = 100
	h = (b - a) / n
	y = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	for i in range(n):
		k0 = f(x[i], y[i])
		k1 = f(x[i] + h/2, y[i] + (h/2)*k0)
		k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
		k3 = f(x[i] + h, y[i] + h*k2)
		tmp = y[i] + h * (k0 + 2*k1 + 2*k2 + k3) / 6
		y.append(tmp)
	return "f({}) = {}".format(x[-1], y[-1]) 

def adams():
	"6.5"
	f = lambda x, y: math.cos(1.5*x - y**2) - 1.3
	a, b = -1, 1
	n = 100
	h = (b - a) / n
	y = [0.2] #Начальные условия
	x = np.linspace(a, b, n+1)
	
	def runge_kutta(f, a, b, h, y, x):
		for i in range(3):
			k0 = f(x[i], y[i])
			k1 = f(x[i] + h/2, y[i] + (h/2)*k0)
			k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
			k3 = f(x[i] + h, y[i] + h*k2)
			tmp = y[i] + h * (k0 + 2*k1 + 2*k2 + k3) / 6
			y.append(tmp)
		return y
	
	y = runge_kutta(f, a, b, h, y, x)
	f_i = [f(x[i], y[i]) for i in range(len(y))]
	for i in range(3, n):
		tmp = y[i] + (h / 24) * (55*f_i[i] - 59*f_i[i-1] + 37*f_i[i-2] - 9*f_i[i-3])
		f_i.append(f(x[i+1], tmp))
		y.append(tmp)
	return "f({}) = {}".format(x[-1], y[-1])

def predict_correct():
	"6.6"
	f = lambda x, y: y * (1 - x)
	a, b = 0, 0.5
	n = 100
	h = (b - a) / n
	y = [1] #Начальные условия
	x = np.linspace(a, b, n+1)
	
	def runge_kutta(f, a, b, h, y, x):
		for i in range(3):
			k0 = f(x[i], y[i])
			k1 = f(x[i] + h/2, y[i] + (h/2)*k0)
			k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
			k3 = f(x[i] + h, y[i] + h*k2)
			tmp = y[i] + h * (k0 + 2*k1 + 2*k2 + k3) / 6
			y.append(tmp)
		return y
	
	y = runge_kutta(f, a, b, h, y, x)
	f_i = [f(x[i], y[i]) for i in range(len(y))]
	for i in range(3, n):
		tmp_y = y[i] + (h / 24) * (55*f_i[i] - 59*f_i[i-1] + 37*f_i[i-2] - 9*f_i[i-3])
		f_i.append(f(x[i+1], tmp_y))
		tmp_y = y[i] + (h / 24) * (9*f_i[i+1] + 19*f_i[i] - 5*f_i[i-1] + f_i[i-2])
		y.append(tmp_y)
	return "f({}) = {}".format(x[-1], y[-1])

def grad_descent():
	"7.1"
	f = lambda x, y: 5/y + y/x + 2*x
	f_x = lambda x, y: 2 - y / (x ** 2) #Производная по x
	f_y = lambda x, y: 1/x - 5 / (y ** 2) #Производная по y
	x, y = (0, 3), (0, 3) #область поиска минимума
	xk, yk = x[1], y[1]
	diag = ((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2) ** 0.5
	e = 0.00001
	while True:
		dx = f_x(xk, yk)
		dy = f_y(xk, yk)
		grad = ((dx) ** 2 + (dy) ** 2) ** 0.5
		if grad < e:
			return "x={}  y={}\nf = {}\ne = {}".format(round(xk, 6), round(yk, 6), f(xk, yk), e)
		k = e * diag / grad
		if k > 1: k = 1
		xk = xk - k*dx
		yk = yk - k*dy

def square_iт_ex():
	"7.2"
	f = lambda x, y: 3*x**2 - x*y + 2*y**2 - 2*x + y
	M = [0.5, -0.5] #Начальное приближение
	h = (0.01, 0.01)
	e = (0.001, 0.001)
	x_min = [None for t in range(len(M))]
	count = 0
	while True:
		count += 1
		for i in range(len(M)):
			x_c = [None for t in range(len(M))]
			x_l = [None for t in range(len(M))]
			x_r = [None for t in range(len(M))]
			x_c[i] = M[i]
			x_l[i] = M[i] - h[i]
			x_r[i] = M[i] + h[i]
			for k in range(len(M)):
				if k != i:
					x_c[k] = M[k]
					x_l[k] = M[k] 
					x_r[k] = M[k]
			y_c = f(*x_c)
			y_l = f(*x_l)
			y_r = f(*x_r)
			x_min[i] = (y_l*(x_c[i] + x_r[i]) - 2*y_c*(x_r[i] + x_l[i]) + y_r*(x_c[i] + x_l[i])) / (2*(y_l - 2*y_c + y_r))
		tmp = [abs(x_min[i] - M[i]) < e[i] for i in range(len(M))]
		if all(tmp):
			result = ""
			for i in range(len(M)):
				result += "x{} = {}  ".format(i, x_min[i])
			return result + "\nf = {}\ne = {}\nn = {}".format(f(*x_min), str(e), count)
		else:
			M = x_min
			x_min = [None for t in range(len(M))]

def plate_evid():
	"8.1"
	#Свинец, температура по краям 700К и 500К, начальная 400К
	#Толщина пластины 0.1м, время нагрева 50с
	t = 50
	H = 0.1
	T0, TH, Tst = 700, 500, 400
	ro = 600
	C = 1250
	k_heat = 0.15
	n, m = 30, 10 #Разбиение по толщине пластины и по времени (n, m)
	tay = t / (m - 1)
	h = H / (n - 1)
	T = np.zeros((m, n), dtype=np.float64)
	for i in range(m):
		for j in range(n):
			if j == 0:
				T[i, j] = T0
			elif j == n-1:
				T[i, j] = TH
			else:
				T[i, j] = Tst
	
	const = (tay * k_heat) / (ro * C * h ** 2)
	for i in range(1, m):
		for j in range(1, n-1):
			T[i, j] = T[i-1, j] + const * (T[i-1, j+1] - 2*T[i-1, j] + T[i-1, j-1])
	
	x = np.linspace(0, H, n) #Толщина
	y = T[-1, :] #Температура
	figure = plt.figure()
	plt.xlabel("Толщина")
	plt.ylabel("Температура")
	plt.plot(x, y)
	figure.savefig("plate_evidently.png")
	
	return "Смотри график!"

def plate_implicit():
	"8.2"
	#Свинец, температура по краям 700К и 500К, начальная 400К
	#Толщина пластины 0.1м, время нагрева 50с
	t = 50
	H = 0.1
	T0, TH, Tst = 700, 500, 400
	ro = 11300
	C = 140
	k_heat = 35.1
	n, m = 30, 10 #Разбиение по толщине пластины и по времени (n, m)
	tay = t / (m - 1)
	h = H / (n - 1)
	T = np.zeros((m, n), dtype=np.float64)
	for i in range(m):
		for j in range(n):
			if j == 0:
				T[i, j] = T0
			elif j == n-1:
				T[i, j] = TH
			else:
				T[i, j] = Tst
	A = k_heat / (h ** 2)
	B = (2 * k_heat) / (h ** 2) + ((ro * C) / tay)
	C1 = k_heat / (h ** 2)
	alfa = np.zeros(n-1) #Не зависит от временного шага
	alfa[0] = 0
	beta = np.zeros((m-1, n-1)) #Зависит от временного шага
	beta[:, 0] = T0
	for i in range(1, n-1):
		alfa[i] = A / (B - C1*alfa[i-1])

	for i in range(1, m):
		
		for k in range(1, n-1):
			D = -(ro * C * T[i-1, k]) / tay
			beta[i-1, k] = (C1*beta[i-1, k-1] - D) / (B - C1*alfa[k-1]) 
	
		for j in range(n-2, 0, -1):
			T[i, j] = alfa[j]*T[i, j+1] + beta[i-1, j]
	x = np.linspace(0, H, n) #Толщина
	y = T[-1, :] #Температура
	figure = plt.figure()
	plt.xlabel("Толщина")
	plt.ylabel("Температура")
	plt.plot(x, y)
	figure.savefig("plate_implicit.png")
	
	return "Смотри график!"

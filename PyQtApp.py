import sys, math, random, queue, threading, time
import pyautogui
import serial
import numpy	
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread
from scipy import zeros, signal, random, fft, arange
import matplotlib.pyplot as plt
from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
# from sklearn.linear_model import LinearRegression



WIDTH = 75
grid = []
intense = 80

xpos = 50
ypos = 50

def Extract(lst, ele): 
    return [item[ele] for item in lst]

class Cell():
	def __init__(self, i, j, intensity):
		self.i = i
		self.j = j
		self.walls = [1, 1, 1, 1]  # top, right, bottom, left
		self.intensity = intensity
		#print(intensity)
	def index(self, i, j, cols, rows):
		if (i < 0) or (j < 0) or (i > (cols - 1)) or (j > (rows - 1)):
			return None
		else:
			return i + j * cols
	def __str__(self):
		return("Cell at x:" + str(self.i) + " y:" + str(self.j) + " intensity: " + str(self.intensity))

class PressurePoint():
	def __init__(self, i, j, intensity):
		self.i = i
		self.j = j
		self.intensity = intensity

def plotSpectrum(y,Fs):
 """
 Plots a Single-Sided Amplitude Spectrum of y(t)
 """
 n = len(y) # length of the signal
 k = arange(n)
 T = n/Fs
 frq = k/T # two sides frequency range
 frq = frq[range(int(n/2))] # one side frequency range

 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(int(n/2))]
 
 plot(frq,abs(Y)) # plotting the spectrum
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')

class App(QWidget):
	def __init__(self):
		super().__init__()
		# self.WLS = LinearRegression()
		self.fitted = 0
		self.time = 0
		self.data1mem = []
		self.state = 0
		self.diffbuffer = []
		self.totalforcebuffer = []
		self.data = [0,0,0,0,0,0,0,0]
		self.databaseline = [0,0,0,0,0,0,0,0]
		self.dataout = [1,1,1,1,1,1,1,1] 
		self.datafiltered = [1,1,1,1,1,1,1,1] 
		self.first = 100
		self.ser = serial.Serial('COM4',timeout=5)
		self.ser.baudrate = 57600
		self.pressed = 0
		self.left = 0
		self.top = 0
		self.centerPressure = Cell(0,0,1)
		self.width = 1400
		self.height = 620
		self.color = 0
		self.point = (10,10)
		self.force = 80
		self.up = 0
		self.cols = math.floor(self.width / WIDTH)
		self.rows = math.floor(self.height / WIDTH)
		self.points = [[self.cols*1/8,self.rows/4],[self.cols*3/8,self.rows/4],[self.cols*5/8,self.rows/4],[self.cols*7/8,self.rows/4],\
		[self.cols*7/8,self.rows*3/4],[self.cols*5/8,self.rows*3/4],[self.cols*3/8,self.rows*3/4],[self.cols*1/8,self.rows*3/4]]
		self.active = False
		self.initui()
		self.init_cells(self.point, intense)

		# Filter Coeficients

		self.b, self.a = signal.butter(3, 3, fs=35)
		self.z0 = signal.lfilter_zi(self.b, self.a)
		self.z1 = signal.lfilter_zi(self.b, self.a)
		self.z2 = signal.lfilter_zi(self.b, self.a)
		self.z3 = signal.lfilter_zi(self.b, self.a)
		self.z4 = signal.lfilter_zi(self.b, self.a)
		self.z5 = signal.lfilter_zi(self.b, self.a)
		self.z6 = signal.lfilter_zi(self.b, self.a)
		self.z7 = signal.lfilter_zi(self.b, self.a)
		self.d, self.c = signal.butter(20, 3, fs=35)
		self.y = signal.lfilter_zi(self.d, self.c)

		# Midpoints

		self.midpoints = [None]*16


	def keyPressEvent(self, event):
		global intense
		if(event.text() == 'a'):
			intense = intense + 1
		if(event.text() == 'd'):
			intense = intense - 1

	def mousePressEvent (self, event):
		self.pressed = 0
	
	def mouseReleaseEvent(self, event):
		self.pressed = 0


	def findClosestPoint(self, i, j):
		
		closestDist = 100000
		
		if not self.points:
			return None
		closestPoint = self.points[0].copy()
		number = 0
		closestnumber = 0
		firstpoint = 1
		for p in self.points:
			if firstpoint == 1:
				closestPoint = p
				closestDist = math.sqrt((p[0] - i)**2 + (p[1] - j)**2)
				firstpoint = 0
			else:
				if (math.sqrt((p[0] - i)**2 + (p[1] - j)**2) < closestDist):
					closestPoint = p
					closestDist = math.sqrt((p[0] - i)**2 + (p[1] - j)**2)
					closestnumber = number
			number = number + 1
		# print(closestPoint.copy())
		return closestPoint.copy(), closestnumber



		return

	def init_cells(self, point, force):
		if not self.active:
			del grid[:]
			for j in range(self.rows):
				for i in range(self.cols):
					closestPoint, number = self.findClosestPoint(i,j)
					if closestPoint is None:
						cell = Cell(i, j, 0)
					else:
						cell = Cell(i, j, min(255 , 255- (int(math.sqrt(abs(closestPoint[0]-i)**2 + abs(closestPoint[1]-j)**2)*(20)))))
					grid.append(cell)
			QTimer.singleShot(1, self.go)

	def go(self):
		global xpos
		global ypos

		self.active = True
		diff = 0
		diffcounter = 0
		while True:
			self.update()

			temptime = time.time()
			if (temptime > self.time):
				hz = 1/(temptime - self.time)
			self.time = temptime
			#print(str(hz) + " Hz")
			
			while(self.ser.read() != b':'):
				pass

			self.ser.read()
			tdata = self.ser.read(81)

			charcounter = 0
			tempdata = []
			i = 0
			while(i < 71):
				try:
					self.data[charcounter] = float(bytes(tdata[i:i+11]).decode("utf-8"))
				except ValueError:
					pass
				
				charcounter = charcounter + 1
				i = i + 10

			# dataarray = np.array(self.data.copy()).reshape((1,8))
				

			if(self.first > 0):
				self.databaseline = self.data.copy()
				self.first = self.first - 1
				print(self.databaseline)
				print(self.data)		
				print(self.point)

			else:
				self.dataout = numpy.square([self.data[0]-self.databaseline[0],self.data[1]-self.databaseline[1],self.data[2]-self.databaseline[2],self.data[3]-self.databaseline[3], \
				self.data[4]-self.databaseline[4],self.data[5]-self.databaseline[5],self.data[6]-self.databaseline[6],self.data[7]-self.databaseline[7]])
				self.datafiltered[0], self.z0 = signal.lfilter(self.b, self.a, [self.dataout[0]], zi=self.z0)
				self.datafiltered[1], self.z1 = signal.lfilter(self.b, self.a, [self.dataout[1]], zi=self.z1)
				self.datafiltered[2], self.z2 = signal.lfilter(self.b, self.a, [self.dataout[2]], zi=self.z2)
				self.datafiltered[3], self.z3 = signal.lfilter(self.b, self.a, [self.dataout[3]], zi=self.z3)
				self.datafiltered[4], self.z4 = signal.lfilter(self.b, self.a, [self.dataout[4]], zi=self.z4)
				self.datafiltered[5], self.z5 = signal.lfilter(self.b, self.a, [self.dataout[5]], zi=self.z5)
				self.datafiltered[6], self.z6 = signal.lfilter(self.b, self.a, [self.dataout[6]], zi=self.z6)
				self.datafiltered[7], self.z7 = signal.lfilter(self.b, self.a, [self.dataout[7]], zi=self.z7)
				

				self.datafiltered[0] = self.datafiltered[0][0]
				self.datafiltered[1] = self.datafiltered[1][0]
				self.datafiltered[2] = self.datafiltered[2][0]
				self.datafiltered[3] = self.datafiltered[3][0]
				self.datafiltered[4] = self.datafiltered[4][0]
				self.datafiltered[5] = self.datafiltered[5][0]
				self.datafiltered[6] = self.datafiltered[6][0]
				self.datafiltered[7] = self.datafiltered[7][0]

				self.totalforcebuffer.append(sum(self.datafiltered))
				print(self.datafiltered)
				print(sum(numpy.sqrt(self.datafiltered)))

				self.data1mem.append(numpy.sqrt(self.datafiltered.copy()))
				# print(((Extract(self.data1mem,0))))
				# print(self.data1mem)
				# Plot Freq Spectrum and peform  filter

				if(len(self.data1mem) == 1000):

					# result1 = zeros(len(self.data1mem))
					# for i, x in enumerate(self.data1mem):
					# 	result1[i], self.z = signal.lfilter(self.b, self.a, [x], zi=self.z)
					# result2 = zeros(len(result1))
					# for i, x in enumerate(self.data1mem):
					# # 	result2[i], self.y = signal.lfilter(self.d, self.c, [x], zi=self.y)
					# plt.plot(Extract(self.data1mem,0))
					# plt.plot(Extract(self.data1mem,1))
					# plt.plot(Extract(self.data1mem,2))
					# plt.plot(Extract(self.data1mem,3))
					# plt.plot(Extract(self.data1mem,4))
					# plt.plot(Extract(self.data1mem,5))
					# plt.plot(Extract(self.data1mem,6))
					# plt.plot(Extract(self.data1mem,7))
					#plotSpectrum(self.data1mem,35)
					# plotSpectrum(result1[100:500],17.6)
					# plotSpectrum(result1[100:500],17.6)
					# plt.plot(result1)
					# plt.plot(result2)
					plt.plot(self.totalforcebuffer)
					plt.show()
				self.databaseline = numpy.subtract(self.databaseline, numpy.multiply(numpy.subtract(self.databaseline,self.data),0.0));
				if sum(self.dataout):
					self.point = [(self.datafiltered[0]*self.cols*1/8+ self.datafiltered[1]*self.cols*3/8+ self.datafiltered[2]*self.cols*5/8+ self.datafiltered[3]*self.cols*7/8+ \
							   self.datafiltered[4]*self.cols*7/8+ self.datafiltered[5]*self.cols*5/8+ self.datafiltered[6]*self.cols*3/8+ self.datafiltered[7]*self.cols*1/8)/sum(numpy.absolute(self.datafiltered)), \
							   (self.datafiltered[0]*self.rows/8+ self.datafiltered[1]*self.rows/8+ self.datafiltered[2]*self.rows/8+ self.datafiltered[3]*self.rows/8+ \
							   self.datafiltered[4]*self.rows*7/8+ self.datafiltered[5]*self.rows*7/8+ self.datafiltered[6]*self.rows*7/8+ self.datafiltered[7]*self.rows*7/8)/sum(numpy.absolute(self.datafiltered))]

					# Generate Midpoints

					k = 6

					self.midpoints[0] = Cell(int((self.datafiltered[0]*self.cols*1/8 + self.datafiltered[1]*self.cols*3/8)/(abs(self.datafiltered[0])+abs(self.datafiltered[1]))),int(self.rows/8),((self.datafiltered[0])+(self.datafiltered[1]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[1] = Cell(int((self.datafiltered[1]*self.cols*3/8 + self.datafiltered[2]*self.cols*5/8)/(abs(self.datafiltered[1])+abs(self.datafiltered[2]))),int(self.rows/8),((self.datafiltered[1])+(self.datafiltered[2]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[2] = Cell(int((self.datafiltered[2]*self.cols*5/8 + self.datafiltered[3]*self.cols*7/8)/(abs(self.datafiltered[2])+abs(self.datafiltered[3]))),int(self.rows/8),((self.datafiltered[2])+(self.datafiltered[3]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)

					self.midpoints[3] = Cell(int((self.datafiltered[4]*self.cols*7/8 + self.datafiltered[5]*self.cols*5/8)/(abs(self.datafiltered[4])+abs(self.datafiltered[5]))),int(self.rows*7/8),((self.datafiltered[4])+(self.datafiltered[5]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[4] = Cell(int((self.datafiltered[5]*self.cols*5/8 + self.datafiltered[6]*self.cols*3/8)/(abs(self.datafiltered[5])+abs(self.datafiltered[6]))),int(self.rows*7/8),((self.datafiltered[5])+(self.datafiltered[6]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[5] = Cell(int((self.datafiltered[6]*self.cols*3/8 + self.datafiltered[7]*self.cols*1/8)/(abs(self.datafiltered[6])+abs(self.datafiltered[7]))),int(self.rows*7/8),((self.datafiltered[6])+(self.datafiltered[7]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)

					self.midpoints[6] = Cell(int(self.cols/8),int((self.datafiltered[0]*self.rows*1/8 + self.datafiltered[7]*self.rows*7/8)/(abs(self.datafiltered[0])+abs(self.datafiltered[7]))),((self.datafiltered[0])+(self.datafiltered[7]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[7] = Cell(int(self.cols*3/8),int((self.datafiltered[1]*self.rows*1/8 + self.datafiltered[6]*self.rows*7/8)/(abs(self.datafiltered[1])+abs(self.datafiltered[6]))),((self.datafiltered[1])+(self.datafiltered[6]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[8] = Cell(int(self.cols*5/8),int((self.datafiltered[2]*self.rows*1/8 + self.datafiltered[5]*self.rows*7/8)/(abs(self.datafiltered[2])+abs(self.datafiltered[5]))),((self.datafiltered[2])+(self.datafiltered[5]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[9] = Cell(int(self.cols*7/8),int((self.datafiltered[3]*self.rows*1/8 + self.datafiltered[4]*self.rows*7/8)/(abs(self.datafiltered[3])+abs(self.datafiltered[4]))),((self.datafiltered[3])+(self.datafiltered[4]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)

					self.midpoints[10] = Cell(int((self.datafiltered[0]*self.cols*1/8 + self.datafiltered[6]*self.cols*3/8)/(abs(self.datafiltered[0])+abs(self.datafiltered[6]))),int((self.datafiltered[0]*self.rows*1/8 + self.datafiltered[6]*self.rows*7/8)/(abs(self.datafiltered[0])+abs(self.datafiltered[6]))),((self.datafiltered[0])+(self.datafiltered[6]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[11] = Cell(int((self.datafiltered[1]*self.cols*3/8 + self.datafiltered[7]*self.cols*1/8)/(abs(self.datafiltered[1])+abs(self.datafiltered[7]))),int((self.datafiltered[1]*self.rows*1/8 + self.datafiltered[7]*self.rows*7/8)/(abs(self.datafiltered[1])+abs(self.datafiltered[7]))),((self.datafiltered[1])+(self.datafiltered[7]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[12] = Cell(int((self.datafiltered[2]*self.cols*5/8 + self.datafiltered[6]*self.cols*3/8)/(abs(self.datafiltered[2])+abs(self.datafiltered[6]))),int((self.datafiltered[2]*self.rows*1/8 + self.datafiltered[6]*self.rows*7/8)/(abs(self.datafiltered[2])+abs(self.datafiltered[6]))),((self.datafiltered[2])+(self.datafiltered[6]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[13] = Cell(int((self.datafiltered[1]*self.cols*3/8 + self.datafiltered[5]*self.cols*5/8)/(abs(self.datafiltered[1])+abs(self.datafiltered[5]))),int((self.datafiltered[1]*self.rows*1/8 + self.datafiltered[5]*self.rows*7/8)/(abs(self.datafiltered[1])+abs(self.datafiltered[5]))),((self.datafiltered[1])+(self.datafiltered[5]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[14] = Cell(int((self.datafiltered[2]*self.cols*5/8 + self.datafiltered[4]*self.cols*7/8)/(abs(self.datafiltered[2])+abs(self.datafiltered[4]))),int((self.datafiltered[2]*self.rows*1/8 + self.datafiltered[4]*self.rows*7/8)/(abs(self.datafiltered[2])+abs(self.datafiltered[4]))),((self.datafiltered[2])+(self.datafiltered[4]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					self.midpoints[15] = Cell(int((self.datafiltered[3]*self.cols*7/8 + self.datafiltered[5]*self.cols*5/8)/(abs(self.datafiltered[3])+abs(self.datafiltered[5]))),int((self.datafiltered[3]*self.rows*1/8 + self.datafiltered[5]*self.rows*7/8)/(abs(self.datafiltered[3])+abs(self.datafiltered[5]))),((self.datafiltered[3])+(self.datafiltered[5]))/math.sqrt(sum(numpy.absolute(self.datafiltered)))*k)
					

					xpositions = numpy.empty([16,1])
					ypositions = numpy.empty([16,1])
					intensities = [None]*16
					count = 0
					for point in self.midpoints:
						xpositions[count,0] = point.i
						ypositions[count,0] = point.j
						intensities[count] = abs(point.intensity)
						count = count + 1
						
					#print(xpositions)

					# print(xpositions)
					# print(ypositions)
					# print(intensities)

					# self.WLS.fit(numpy.asarray(xpositions), numpy.asarray(ypositions), sample_weight=intensities)

					self.centerPressure = Cell(int(self.point[0]),int(self.point[1]),sum(numpy.square(self.datafiltered))/1000)

					#print(self.WLS.coef_[0])
					self.fitted = 1
					


				prevdiff = diff
				diff = (sum(numpy.absolute(self.datafiltered)))
				self.diffbuffer.append(diff)
				if(len(self.diffbuffer) > 10):
					self.diffbuffer.pop()
				if(self.state == 0):
					if(diff < 0.1):
						self.databaseline = self.data.copy()
					else:
						self.state = 1
				if(self.state == 1):
					if(diff - prevdiff < -diff/20):
						diffcounter = diffcounter + 1
						#print("diff")
					elif diffcounter > 0:
						diffcounter = diffcounter - 1
					if diffcounter > 20 or diff < 0.1:
						self.databaseline = self.data.copy()
						self.state = 0
				# print(self.state)

				# #print(diff)

				# print(self.databaseline)
				# print(self.data)	
				# print(self.dataout)
				#print(self.datafiltered)	
				#print(str(self.midpoints[0]))
				# print(sum(self.dataout))
				#print(self.dataout)
				#print(dataout)

			
			QApplication.processEvents()
			#QThread.msleep(1)
			if(self.pressed):
				self.points.append([xpos,ypos])
			if(self.up == 0):
				self.color = self.color + 1
				if self.color == 255:
					 self.up = 1
			else:
				self.color = self.color - 1
				if self.color == 0:
					 self.up = 0
		self.active = False

	def initui(self):
		QShortcut(QKeySequence('F5'), self, self.init_cells)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.lightGray)
		self.setPalette(p)
		self.show()

	def paintEvent(self, e):
		
		# Draw full grid

		# for c in grid:
		# 	closestPoint, number = self.findClosestPoint(c.i,c.j)
		# 	if closestPoint is not None:
		# 		c.intensity = min(255 , 255- min(255 ,(int(math.sqrt(abs(closestPoint[0]-c.i)**2 + abs(closestPoint[1]-c.j)**2)*(100-(self.dataout[number])*4)))))
		# 	self.draw_cell_manual(c)
		# self.draw_cell_manual(self.centerPressure)
		# qp.drawLine(0    , 400    , 4, 400 + (WLS.coef_[0]*10))
		#Draw Pressure
		for c in grid:
			c.intensity = 0


		for c in grid:
			if(sum(self.dataout) and self.state):
				#c.intensity = min(255 , 255- min(255 ,(int(math.sqrt(abs(self.centerPressure.i-c.i)**2 + abs(self.centerPressure.j-c.j)**2)*(60)))))
				for ele in self.midpoints:
					pass
					# c.intensity = min(255 , c.intensity + min(255 , int((1/(1+((abs(ele.i-c.i)**2 + abs(ele.j-c.j)**2)))*2*(ele.intensity)))))
					#print((int(10/(1+(math.sqrt(abs(ele.i-c.i)**2 + abs(ele.j-c.j)**2)*(ele.intensity))))))
					#c.intensity = 255

			else:
				c.intensity = 0
			self.draw_single_cell(c)



		outputs = "outputs: "
		if(self.midpoints[0]):
			for midpoint in self.midpoints:
				outputs = (outputs + str(midpoint.intensity) + " ")

		# print(outputs)

		if self.state and self.centerPressure.intensity>-10:
			self.draw_single_cell(self.centerPressure)
			self.draw_single_cell(self.midpoints[0])
			self.draw_single_cell(self.midpoints[1])
			self.draw_single_cell(self.midpoints[2])
			self.draw_single_cell(self.midpoints[3])
			self.draw_single_cell(self.midpoints[4])
			self.draw_single_cell(self.midpoints[5])

			self.draw_single_cell(self.midpoints[6])
			self.draw_single_cell(self.midpoints[7])
			self.draw_single_cell(self.midpoints[8])
			self.draw_single_cell(self.midpoints[9])

			self.draw_single_cell(self.midpoints[10])
			self.draw_single_cell(self.midpoints[11])
			self.draw_single_cell(self.midpoints[12])
			self.draw_single_cell(self.midpoints[13])
			self.draw_single_cell(self.midpoints[14])
			self.draw_single_cell(self.midpoints[15])
				
			# outputs = "outputs: "
			# for midpoint in self.midpoints:
			# 	outputs = (outputs + str(midpoint.intensity) + " ")
			# print(outputs)
			pass
		#print(self.centerPressure.i)
		#print(self.centerPressure.j)

		if(self.fitted):
			self.draw_line()


	def draw_line(self):

		qp = QPainter(self)
		qp.setPen(QPen(Qt.green, 1, Qt.SolidLine))
		# slope = (self.WLS.coef_[0])
		#print(slope[0])
		# qp.drawLine(self.centerPressure.i*WIDTH, self.centerPressure.j*WIDTH  , self.centerPressure.i*WIDTH + 200, self.centerPressure.j*WIDTH + int(200*slope[0]))



	def draw_cell_manual(self, cell):
		x = cell.i * WIDTH
		y = cell.j * WIDTH
		# LINES
		qp = QPainter(self)
		qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
		if cell.walls[0]:  # top
			qp.drawLine(x    , y    , x + WIDTH, y)
		if cell.walls[1]:  # right
			qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
		if cell.walls[2]:  # bottom
			qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
		if cell.walls[3]:  # left
			qp.drawLine(x    , y + WIDTH, x    , y)
		forcecolor = self.centerPressure.intensity / 5
		qp.setBrush(QColor(int(max(0,min(255,forcecolor*cell.intensity*self.centerPressure.intensity/10)), max(0,min(255,((1.0 - forcecolor) * cell.intensity*self.centerPressure.intensity/10))) , 0, 200)))
		qp.drawRect(x, y, WIDTH, WIDTH)

	def draw_single_cell(self, cell):
		x = cell.i * WIDTH
		y = cell.j * WIDTH
		# LINES
		qp = QPainter(self)
		qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
		if cell.walls[0]:  # top
			qp.drawLine(x    , y    , x + WIDTH, y)
		if cell.walls[1]:  # right
			qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
		if cell.walls[2]:  # bottom
			qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
		if cell.walls[3]:  # left
			qp.drawLine(x    , y + WIDTH, x    , y)
		forcecolor = 1
		qp.setBrush(QColor(int(max(0,min(255,forcecolor*cell.intensity))), int(max(0,min(255,((1.0 - forcecolor) * cell.intensity)))) , 0, 200))
		qp.drawRect(x, y, WIDTH, WIDTH)


	def draw_cell(self, cell):
		x = cell.i * WIDTH
		y = cell.j * WIDTH
		# LINES
		qp = QPainter(self)
		qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
		if cell.walls[0]:  # top
			qp.drawLine(x    , y    , x + WIDTH, y)
		if cell.walls[1]:  # right
			qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
		if cell.walls[2]:  # bottom
			qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
		if cell.walls[3]:  # left
			qp.drawLine(x    , y + WIDTH, x    , y)
			qp.drawRect(x, y, WIDTH, WIDTH)



if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())



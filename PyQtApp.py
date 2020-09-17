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


WIDTH = 40
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
		
		self.data1mem = []
		self.state = 0
		self.diffbuffer = []
		self.data = [0,0,0,0,0,0,0,0]
		self.databaseline = [0,0,0,0,0,0,0,0]
		self.dataout = [1,1,1,1,1,1,1,1] 
		self.datafiltered = [1,1,1,1,1,1,1,1] 
		self.first = 100
		self.ser = serial.Serial('COM4',timeout=5)
		self.ser.baudrate = 2000000
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

		current = grid[0]
		current.visited = 1
		current.currentCell = 1
		diff = 0
		diffcounter = 0
		while True:
			self.update()
			print(time.time())
			while(self.ser.read() != b'k'):
				pass
			self.ser.read()
					
			tdata = self.ser.read(63)
			#print (tdata)
			charcounter = 0
			tempdata = []
			for character in tdata:
				if charcounter == 92:
					self.data[charcounter] = float(bytes(tempdata).decode("utf-8"))
					break
				if character != 32:
					tempdata.append(character)
				else:
					if(not tempdata):
						continue
					if charcounter == 8:
						break	
					self.data[charcounter] = float(bytes(tempdata).decode("utf-8"))
					tempdata = []
					charcounter = charcounter + 1
					
					

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

				#print (self.datafiltered[0])

				self.data1mem.append(self.datafiltered.copy())
				# print(((Extract(self.data1mem,0))))
				# print(self.data1mem)
				# Plot Freq Spectrum and peform  filter

				if(len(self.data1mem) == 30000):

					# result1 = zeros(len(self.data1mem))
					# for i, x in enumerate(self.data1mem):
					# 	result1[i], self.z = signal.lfilter(self.b, self.a, [x], zi=self.z)
					# result2 = zeros(len(result1))
					# for i, x in enumerate(self.data1mem):
					# 	result2[i], self.y = signal.lfilter(self.d, self.c, [x], zi=self.y)
					plt.plot(Extract(self.data1mem,0))
					plt.plot(Extract(self.data1mem,1))
					plt.plot(Extract(self.data1mem,2))
					plt.plot(Extract(self.data1mem,3))
					plt.plot(Extract(self.data1mem,4))
					plt.plot(Extract(self.data1mem,5))
					plt.plot(Extract(self.data1mem,6))
					plt.plot(Extract(self.data1mem,7))
					plotSpectrum(self.data1mem,17.6)
					# plotSpectrum(result1[100:500],17.6)
					# plotSpectrum(result1[100:500],17.6)
					# plt.plot(result1)
					# plt.plot(result2)
					plt.show()
				self.databaseline = numpy.subtract(self.databaseline, numpy.multiply(numpy.subtract(self.databaseline,self.data),0.0));
				if sum(self.dataout):
					self.point = [(self.datafiltered[0]*self.cols*1/8+ self.datafiltered[1]*self.cols*3/8+ self.datafiltered[2]*self.cols*5/8+ self.datafiltered[3]*self.cols*7/8+ \
							   self.datafiltered[4]*self.cols*7/8+ self.datafiltered[5]*self.cols*5/8+ self.datafiltered[6]*self.cols*3/8+ self.datafiltered[7]*self.cols*1/8)/sum(numpy.absolute(self.datafiltered)), \
							   (self.datafiltered[0]*self.rows/8+ self.datafiltered[1]*self.rows/8+ self.datafiltered[2]*self.rows/8+ self.datafiltered[3]*self.rows/8+ \
							   self.datafiltered[4]*self.rows*7/8+ self.datafiltered[5]*self.rows*7/8+ self.datafiltered[6]*self.rows*7/8+ self.datafiltered[7]*self.rows*7/8)/sum(numpy.absolute(self.datafiltered))]

				self.centerPressure = Cell(int(self.point[0]),int(self.point[1]),sum(numpy.square(self.datafiltered))/1000)

				prevdiff = diff
				diff = (sum((numpy.subtract(self.data,self.databaseline))))
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
					if diffcounter > 3 or diff < 0.1:
						self.databaseline = self.data.copy()
						self.state = 0
				# print(self.state)

				# #print(diff)

				# print(self.databaseline)
				# print(self.data)	
				# print(self.dataout)
				#print(self.datafiltered)	
				print(self.point)
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

		#Draw Pressure

		for c in grid:
			if(sum(self.dataout) and self.state):
				c.intensity = min(255 , 255- min(255 ,(int(math.sqrt(abs(self.centerPressure.i-c.i)**2 + abs(self.centerPressure.j-c.j)**2)*(60)))))
			else:
				c.intensity = 0
			self.draw_cell_manual(c)

		if self.state and self.centerPressure.intensity>1:
			self.draw_cell_manual(self.centerPressure)
		#print(self.centerPressure.i)
		#print(self.centerPressure.j)



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
		qp.setBrush(QColor(max(0,min(255,forcecolor*cell.intensity*self.centerPressure.intensity/10)), max(0,min(255,((1.0 - forcecolor) * cell.intensity*self.centerPressure.intensity/10))) , 0, 200))
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
		if cell.visited:
			if cell.currentCell:
				qp.setBrush(QColor(0, 0 , 255, 100))
			else:
				qp.setBrush(QColor(255, 0, 255, 100))
			qp.drawRect(x, y, WIDTH, WIDTH)



if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())



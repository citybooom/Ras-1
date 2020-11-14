import xlrd
import numpy as np
import sys, math, random, queue, threading, time
import pyautogui
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread
from scipy import zeros, signal, random, fft, arange
import matplotlib.pyplot as plt
from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from sklearn.linear_model import LinearRegression


class App(QWidget):
	def __init__(self):
		super().__init__()
		self.WLS = LinearRegression()
		self.fitted = 0
		self.time = 0
		self.data1mem = []
		self.state = 0
		self.diffbuffer = numpy.array([[0 for x in range(8)] for y in range(1)])

		self.data = [0,0,0,0,0,0,0,0]
		self.databaseline = [0,0,0,0,0,0,0,0]
		self.dataout = [1,1,1,1,1,1,1,1] 
		self.datafiltered = [1,1,1,1,1,1,1,1] 
		self.first = 1000
		self.ser = serial.Serial('COM12',timeout=5)
		self.ser.baudrate = 115200
		self.pressed = 0
		self.left = 0
		self.top = 0
		self.centerPressure = Cell(0,0,1)
		self.width = 1400
		self.height = 620
		self.color = 0
		self.force = 80
		self.up = 0

		self.active = False
		self.initui()

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


	def keyPressEvent(self, event):
		global intense
		if(event.text() == 'a'):
			intense = intense + 1
		if(event.text() == 'd'):
			intense = intense - 1

	def init_cells(self, point, force):
		
	def go(self):

		self.active = True
		
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
			print(tdata)
			charcounter = 0
			tempdata = []
			i = 0
			while(i < 71):
				try:
					self.data[charcounter] = float(bytes(tdata[i:i+11]).decode("utf-8"))
				except:
					pass
				charcounter = charcounter + 1
				i = i + 10
			# print(self.data)
				

			if(self.first > 0):
				self.databaseline = self.data.copy()
				self.first = self.first - 1
				print(self.databaseline)
				print(self.data)		
				print(self.point)

			else:
				self.dataout = [self.data[0]-self.databaseline[0],self.data[1]-self.databaseline[1],self.data[2]-self.databaseline[2],self.data[3]-self.databaseline[3], \
				self.data[4]-self.databaseline[4],self.data[5]-self.databaseline[5],self.data[6]-self.databaseline[6],self.data[7]-self.databaseline[7]]

				self.datafiltered = self.data.copy()
				self.totalforcebuffer.append(sum(self.datafiltered))

				# print(self.datafiltered)

				#self.data1mem.append(numpy.sqrt(self.datafiltered.copy()))
				self.databaseline = numpy.subtract(self.databaseline, numpy.multiply(numpy.subtract(self.databaseline,self.data),0.0));
			
				

				if sum(self.dataout):
					self.point = [(self.datafiltered[0]*self.cols*1/8+ self.datafiltered[1]*self.cols*3/8+ self.datafiltered[2]*self.cols*5/8+ self.datafiltered[3]*self.cols*7/8+ \
						   self.datafiltered[4]*self.cols*7/8+ self.datafiltered[5]*self.cols*5/8+ self.datafiltered[6]*self.cols*3/8+ self.datafiltered[7]*self.cols*1/8)/sum(numpy.absolute(self.datafiltered)), \
						   (self.datafiltered[0]*self.rows/8+ self.datafiltered[1]*self.rows/8+ self.datafiltered[2]*self.rows/8+ self.dataout[3]*self.rows/8+ \
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
					
				self.WLS.fit(numpy.asarray(xpositions), numpy.asarray(ypositions), sample_weight=intensities)

				self.centerPressure = Cell(int(self.point[0]),int(self.point[1]),sum(numpy.square(self.datafiltered))/1000)

				self.fitted = 1
				


				prevdiff = diff
				diff = 0
				drift = 0

				self.diffbuffer = numpy.append(self.diffbuffer, numpy.array(self.datafiltered).reshape((1,8)), axis=0)
				if(numpy.size(self.diffbuffer) > 64):
					drift = sum(numpy.subtract(self.diffbuffer[0,:],self.diffbuffer[7,:]))
					diff = (sum(numpy.absolute(numpy.subtract(self.diffbuffer[0,:],self.diffbuffer[7,:]) - drift/8)))
					self.diffbuffer =  numpy.delete(self.diffbuffer ,0, 0)

					print(self.diffbuffer[0,:])
					print(self.diffbuffer[7,:])
					print(drift)
					print(diff)

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
		# QShortcut(QKeySequence('F5'), self, self.init_cells)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.lightGray)
		self.setPalette(p)
		self.show()

	def paintEvent(self, e):
		
		for c in grid:
			self.draw_single_cell(c)

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

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())






import sys, math, random, queue, threading, time
import pyautogui
import serial
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread
from scipy import zeros, signal, random, fft, arange

import matplotlib.pyplot as plt

from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from sklearn.linear_model import LinearRegression

timenow = 0
lasttime = 0
hz = 0
ser = serial.Serial('COM16',timeout=5)
ser.baudrate = 115200	
data = [0,0,0,0,0,0,0,0]
datamem = np.array([[0 for x in range(8)] for y in range(200)] )
dataout = np.array([[0 for x in range(8)] for y in range(200)] )
latchvalues =  np.array([0 for x in range(8)])
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
count = 1
ax.axis([0,200,0,100000])
ax2.axis([-0.35,0.35,-0.25,0.25])

plt.show(block=False)

points = [[1/8,1/4],[3/8,1/4],[5/8,1/4],[7/8,1/4],[7/8,3/4],[5/8,3/4],[3/8,3/4],[1/8,3/4]]



lines = [None]*8
# bar1, = ax.plot((100,100),(0,20000))
# bars = [bar1]

for i in range(0,8):
	lines[i], = ax.plot(np.zeros(200))

plotpoint, = ax2.plot(105,200,'ro') 

peakcounter = 0
state = 0

while(1):
	count = count + 1;
	timenow = time.time()
	if (timenow > lasttime):
		hz = 1/(timenow - lasttime)

	lasttime = timenow
	# print(str(hz) + " Hz")



	while(ser.read() != b':'):
		pass

	ser.read()
	tdata = ser.read(81)

	charcounter = 0
	tempdata = []
	i = 0
	while(i < 71):
		try:
			data[charcounter] = float(bytes(tdata[i:i+11]).decode("utf-8"))
		except ValueError:
			pass
		
		charcounter = charcounter + 1
		i = i + 10




	dataarray = np.array(data.copy()).reshape((1,8))
	datamem = np.append(datamem, dataarray, axis=0)
	#print(np.size(datamem[:,0]))



	if(len(datamem) > 200):
		datamem = np.delete(datamem,0, 0)

	if(len(dataout) > 199):
		dataout = np.delete(dataout,0, 0)


	# print(np.shape(np.append(dataout, dataarray - datamem[194,:].reshape((1,8)), axis=0)))


	if(state == 0):
		dataout = np.append(dataout, dataarray - datamem[196,:].reshape((1,8)), axis=0)
		# for i in range(0,8):
		# 	dataout[195,i] = datamem[195,i] - datamem[194,i]
		# 	dataout[196,i] = datamem[196,i] - datamem[194,i]
		# 	dataout[197,i] = datamem[197,i] - datamem[194,i]
		# 	dataout[198,i] = datamem[198,i] - datamem[194,i]
		# 	dataout[199,i] = datamem[199,i] - datamem[194,i]

	point  = [0,0]
	dataoutpoint = dataarray.copy()
	if(state == 1):
		dataoutpoint = dataarray - latchvalues.reshape((1,8))
		dataout = np.append(dataout, dataoutpoint, axis=0)
		for i in range(0,8):
			point = [point[0] + (dataoutpoint[0,i]-np.mean(dataoutpoint[0]))*points[i][0]/sum(np.absolute(dataoutpoint[0])), point[1] +(dataoutpoint[0,i]-np.mean(dataoutpoint[0]))*points[i][1]/sum(np.absolute(dataoutpoint[0]))]
		print(point)

		# for i in range(0,8):
		# 	dataout[195,i] = datamem[195,i] - latchvalues[i]
		# 	dataout[196,i] = datamem[196,i] - latchvalues[i]
		# 	dataout[197,i] = datamem[197,i] - latchvalues[i]
		# 	dataout[198,i] = datamem[198,i] - latchvalues[i]
		# 	dataout[199,i] = datamem[199,i] - latchvalues[i]

	#print(dataoutpoint[0,1])
	# print(points[0][1])



	peakness = 1
	i = 0
	for line in lines:
		line.set_ydata(dataout[:,i])
		peakness = peakness * (abs((datamem[196,i]-datamem[195,i])) + abs((datamem[198,i]-datamem[199,i])))/100
		i = i + 1

	if (peakness > 100):
		# bar, = ax.plot((197,197),(np.amin(datamem[197,:].copy()),np.amax(datamem[197,:].copy())))
		# bars.append(bar)
		
		peakcounter = 3
		if(state == 0):
			for i in range(0,8):
				latchvalues[i] = datamem[196,i];

		state = 1
			
	if (peakness < 5 and state == 1):
		peakcounter = peakcounter - 1
		if(peakcounter == 0):
			state = 0

	# for bar in bars:
	# 	xbar = bar.get_xdata()
	# 	bar.set_xdata([xbar[0] -1,xbar[0] -1])
	# 	if xbar[0] == 150:
	# 		bar.remove()
	# 		bars.remove(bar)


	#bar.set_ydata([np.amin(datamem)-500,np.amax(datamem)+500])
	ax.axis([0,200,min(-700,np.amin(dataout)-500),max(700, np.amax(dataout)+500)])
	

	plotpoint.set_xdata(-point[0])
	plotpoint.set_ydata(point[1])

	fig.canvas.draw()
	fig.canvas.flush_events()

	fig2.canvas.draw()
	fig2.canvas.flush_events()


	# print(peakness)


	# if(count > 2000):
	# 	plt.show()


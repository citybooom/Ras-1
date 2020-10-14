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
ser = serial.Serial('COM12',timeout=5)
ser.baudrate = 115200	
data = [0,0,0,0,0,0,0,0]
datamem = np.array([[0 for x in range(8)] for y in range(200)] )
fig, ax = plt.subplots()
count = 1
plt.axis([0,200,0,100000])
plt.show(block=False)


lines = [None]*8
bar1, = ax.plot((100,100),(0,20000))
bars = [bar1]

for i in range(0,8):
	lines[i], = ax.plot(np.zeros(200))

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



	peakness = 1
	i = 0
	for line in lines:
		line.set_ydata(datamem[:,i])
		peakness = peakness * (abs((datamem[196,i]-datamem[195,i])) + abs((datamem[198,i]-datamem[199,i])))/100
		i = i + 1

	if (peakness > 100):
		bar, = ax.plot((197,197),(np.amin(datamem[197,:].copy()),np.amax(datamem[197,:].copy())))
		bars.append(bar)
			
	for bar in bars:
		xbar = bar.get_xdata()
		bar.set_xdata([xbar[0] -1,xbar[0] -1])
		if xbar[0] == 1:
			bars.remove(bar)


	#bar.set_ydata([np.amin(datamem)-500,np.amax(datamem)+500])
	plt.axis([0,200,np.amin(datamem)-500,np.amax(datamem)+500])

	fig.canvas.draw()
	fig.canvas.flush_events()
	print(peakness)


	# if(count > 2000):
	# 	plt.show()


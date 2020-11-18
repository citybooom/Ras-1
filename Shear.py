import sys, math, random, queue, threading, time
import pyautogui
import serial
import xlrd
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread
from scipy import zeros, signal, random, fft, arange
import matplotlib.pyplot as plt
from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from sklearn.linear_model import LinearRegression
from pynput import keyboard

global state
def on_press(key):
	if(format(key) == "Key.space"):
		print("reset")
		global state
		state = 0
	# try:
	#     print('alphanumeric key {0} pressed'.format(
	#         key.char))
	# except AttributeError:
	#     print('special key {0} pressed'.format(
	#         key))

listener = keyboard.Listener(
    on_press=on_press)
listener.start()


timenow = 0
lasttime = 0
hz = 0
ser = serial.Serial('COM10',timeout=5)
ser.baudrate = 57600	
#ser.timeout = 0            # non blocking read	
data = [0,0,0,0,0,0,0,0]
datamem = np.array([[0 for x in range(8)] for y in range(200)] )
dataout = np.array([[0 for x in range(8)] for y in range(200)] )
latchvalues =  np.array([0 for x in range(8)])
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
count = 1
dim1 = 30; dim2 = 12; dim3 = 8
ax.axis([0,200,0,100000])
ax2.axis([-200000,200000, -200000, 200000])

plt.show(block=False)

loc = ("Calibration.xlsx")
 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)



Calibration = np.zeros((dim1, dim2, dim3))
Calibration [0][0][0] = 1

for i in range (0,dim1):
	for j in range (0,dim2):
		for k in range (0,dim3):
			Calibration[i][j][k] = sheet.cell_value( i,j+dim2*k)


lines = [None]*8
# bar1, = ax.plot((100,100),(0,20000))
# bars = [bar1]

shear, = ax2.plot([0,0],[0,0]) 

for i in range(0,8):
	lines[i], = ax.plot(np.zeros(200))

# plotpoint, = ax2.plot(105,200,'ro') 

xlist = zeros(dim1*dim2);
ylist = zeros(dim1*dim2);

for i in range (0,dim2):
	for j in range (0,dim1):
		xlist[i*dim1 +j] = j
		ylist[i*dim1 +j] = i
#scatterpoint = ax2.scatter(xlist,ylist, marker="s",s=900) 
#ax2.set_aspect('equal')

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
	dataoutpoint = dataarray.copy() 
	if(state == 0):
		dataoutpoint = dataarray - datamem[196,:].reshape((1,8))
		dataout = np.append(dataout,dataoutpoint, axis=0)

	point  = [0,0]
	if(state == 1):
		dataoutpoint = dataarray - latchvalues.reshape((1,8))
		dataout = np.append(dataout, dataoutpoint, axis=0)

	peakness = 1
	i = 0


	# print(dataoutpoint[0])

	datapoint = dataoutpoint[0]
	ratios = np.zeros(8)
	matchs = np.zeros((dim1,dim2))
	averageMatch = 0

	if 0 in dataoutpoint[0]:
		ratios = np.ones(8)
	else:
		for i in range (0,dim1):
			for j in range (0,dim2):
				average = 0
				for k in range (0,8):
					average = average + abs(datapoint[k]/8)
				for k in range (0,8):
					ratios[k] = datapoint[k] / average
				match = 0
				for k in range (0,8):
					match = match + abs(ratios[k] - Calibration[i][j][k])/8
				matchs[i][j] = match


	# if 0 in dataoutpoint[0]:
	# 	ratios = np.ones(8)
	# else:
	# 	for i in range (0,dim1):
	# 		for j in range (0,dim2):
	# 			Max = 0
	# 			for k in range (0,8):
	# 				if (datapoint[k]) > Max:
	# 					Max = datapoint[k]
	# 			for k in range (0,8):
	# 				ratios[k] = datapoint[k] / Max
	# 			match = 0
	# 			for k in range (0,8):
	# 				match = match + abs(Calibration[i][j][k] - ratios[k])/8
	# 			matchs[i][j] = match
				
	# print(matchs)

	highest = 10000000000
	pos = [0,0]
	for i in range (0,dim1):
		for j in range (0,dim2):
			if matchs[i][j] < highest:
				highest = matchs[i][j]
				pos = [i,j]

	intense = max(datapoint)

	intense = math.sqrt(math.sqrt(math.sqrt(abs(intense))))
	#print(intense)
	#print (intense)

	i = 0
	for line in lines:
		line.set_ydata(dataout[:,i])
		peakness = peakness * (abs((datamem[196,i]-datamem[195,i])) + abs((datamem[198,i]-datamem[199,i])))/100
		i = i + 1

	if (peakness > 10000):
		# bar, = ax.plot((197,197),(np.amin(datamem[197,:].copy()),np.amax(datamem[197,:].copy())))
		# bars.append(bar)
		
		peakcounter = 5
		if(state == 0):
			for i in range(0,8):
				latchvalues[i] = datamem[196,i]
		state = 1

		
			
                                              

	
	# for bar in bars:
	# 	xbar = bar.get_xdata()
	# 	bar.set_xdata([xbar[0] -1,xbar[0] -1])
	# 	if xbar[0] == 150:
	# 		bar.remove()
	# 		bars.remove(bar)
	# bar.set_ydata([np.amin(datamem)-500,np.amax(datamem)+500])
	ax.axis([0,200,min(-700,np.amin(dataout)-500),max(700, np.amax(dataout)+500)])
	
	colors = []
	worstmatch = 0
	for i in range (0,dim1):
		for j in range (0,dim2):
			if(matchs[i][j] > worstmatch):
				worstmatch = matchs[i][j]
	# unitmatchs = zeros((dim1,dim2))
	# for i in range (0,dim1):
	# 	for j in range (0,dim2):
	# 		unitmatchs[i][j] = highest / matchs[i][j]


	# unitbest = highest/worstmatch
	print(peakness)
	print(highest)
	print(intense)
	print(" ")


	intenseColor = min(1,intense*0.2)
	if (state == 1):
		for i in range (0,dim2):
			for j in range (0,dim1):
				if(pos[1] == i and pos[0] == j):
					colors.append((1,1,1))
				elif(matchs[j][i] > (1.3)):
					colors.append((0,0,0))	
				else:
					colors.append((0.8*intenseColor,0,1-0.8*intenseColor))
				# print(matchs[j][i])	
	else:
		for i in range (0,dim2):
			for j in range (0,dim1):
				colors.append((0,0,0))

	# print(colors)
	#rng = np.random.RandomState(0)
	#colors = rng.rand(240)
	#scatterpoint, = ax2.plot(xlist,ylist,'ro',  c = colors)

	# scatterpoint.set_color(colors)
	# plotpoint.set_ydata(pos[1])

	shear_x = datapoint[0]+datapoint[1]+datapoint[2]+datapoint[3]-(datapoint[4]+datapoint[5]+datapoint[6]+datapoint[7])
	shear_y = datapoint[0]+datapoint[1]+datapoint[6]+datapoint[7]-(datapoint[2]+datapoint[3]+datapoint[4]+datapoint[5])

	print(shear_x)
	print(shear_y)

	shear.set_xdata([0,shear_x])
	shear.set_ydata([0,shear_y])


	fig.canvas.draw()
	fig.canvas.flush_events()




	fig2.canvas.draw()
	fig2.canvas.flush_events()


	# print(peakness)


	# if(count > 2000):
	# 	plt.show()


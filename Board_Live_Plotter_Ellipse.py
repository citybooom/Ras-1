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
# from sklearn.linear_model import LinearRegression
from pynput import keyboard
from matplotlib.patches import Ellipse


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

ser = serial.Serial('COM9',timeout=5)

ser.baudrate = 57600	
#ser.timeout = 0            # non blocking read	
data = [0,0,0,0,0,0,0,0]
datamem = np.array([[0 for x in range(8)] for y in range(200)])
dataout = np.array([[0 for x in range(8)] for y in range(200)])
latchvalues =  np.array([0 for x in range(8)])
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
count = 1
dim1 = 31; dim2 = 12; dim3 = 8
ax.axis([0,200,0,100000])
ax2.axis([-1,dim1, -1, dim2])

plt.show(block=False)

loc = ("Calibration_S3.xlsx")
 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)



Calibration = np.zeros((dim1, dim2, dim3))
Calibration [0][0][0] = 1

for i in range (0,dim1):
	for j in range (0,dim2):
		for k in range (0,dim3):
			Calibration[i][j][k] = sheet.cell_value( i,j+dim2*k)


lines = [None]*8

for i in range(0,8):
	lines[i], = ax.plot(np.zeros(200))

# plotpoint, = ax2.plot(105,200,'ro') 

xlist = np.zeros(dim1*dim2);
ylist = np.zeros(dim1*dim2);
bottom_center = 1/2
top_center = 1/2
left_center = 1/2
right_center = 1/2
for i in range (0,dim2):
	for j in range (0,dim1):
		xlist[i*dim1 +j] = j
		ylist[i*dim1 +j] = i
scatterpoint = ax2.scatter(xlist,ylist, marker="s",s=900) 
ax2.set_aspect('equal')
# angle , = ax2.plot((dim1/2-1/2,dim1/2-1/2+5*np.cos(pi/4)),(dim2/2-1/2 ,dim2/2-1/2+5*np.cos(pi/4)))
vert_spine, = ax2.plot((bottom_center + dim1, top_center + dim1),(0, dim2-1))
hor_spine, = ax2.plot((0, dim1-1),(left_center + dim2, right_center + dim2))



forcePlot = Ellipse(xy=[4,5], width=10, height=4, angle=pi/4)
ax2.add_artist(forcePlot)
       
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


	high = 0
	wide = 0

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
	bestmatch = 100000
	pos = [0,0]
	worstmatch = 0
	average = 0

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
				maxk = 0
				penk = 0
				for k in range (1,8):
					match = match + (abs(ratios[k] - Calibration[i][j][k]))
				matchs[i][j] = match
				if matchs[i][j] > worstmatch:
					worstmatch = matchs[i][j]
				if matchs[i][j] < bestmatch:
					bestmatch = matchs[i][j]
					pos = [i,j]

	for i in range (0,dim1):
		for j in range (0,dim2):
			matchs[i][j] = (matchs[i][j] - bestmatch)/(worstmatch - bestmatch)

	#print(bestmatch)
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

		
			
	# if (peakness < 5000 and state == 1):
	# 	peakcounter = peakcounter - 1
	# 	if(peakcounter == 0):
	# 		state = 0
	# else:
	# 	peakcounter = 3

	ax.axis([0,200,min(-700,np.amin(dataout)-500),max(700, np.amax(dataout)+500)])
	
	colors = []
	# unitmatchs = zeros((dim1,dim2))
	# for i in range (0,dim1):
	# 	for j in range (0,dim2):
	# 		unitmatchs[i][j] = highest / matchs[i][j]


	# unitbest = highest/worstmatch
	# print(peakness)
	# print(highest)
	# print(intense)
	# print(" ")



	# print(colors)
	#rng = np.random.RandomState(0)
	#colors = rng.rand(240)
	#scatterpoint, = ax2.plot(xlist,ylist,'ro',  c = colors)


	points = [[-1/2,1/2],[-1/4,1/2],[1/4,1/2],[1/2,1/2],[1/2,-1/2],[1/4,-1/2],[-1/4,-1/2],[-1/2,-1/2 ]]

	leftshift = 0
	rightshift = 0
	upshift = 0
	downshift = 0

	ante_pos = [0,0];

	top_center =    (points[0][0] * datapoint[0] + points[1][0] * datapoint[1] + points[2][0] * datapoint[2] + points[3][0] * datapoint[3])    / (abs(datapoint[0]) + abs(datapoint[1]) + abs(datapoint[2]) + abs(datapoint[3]))*dim1 + dim1/2
	bottom_center = (points[4][0] * datapoint[4] + points[5][0] * datapoint[5] + points[6][0] * datapoint[6] + points[7][0] * datapoint[7])    / (abs(datapoint[4]) + abs(datapoint[5]) + abs(datapoint[6]) + abs(datapoint[7]))*dim1 + dim1/2

	left_center =    (points[0][1] * datapoint[0] + points[1][1] * datapoint[1] + points[4][1] * datapoint[4] + points[5][1] * datapoint[5])   / (abs(datapoint[0]) + abs(datapoint[1]) + abs(datapoint[4]) + abs(datapoint[5]))*dim2 + dim2/2
	right_center =   (points[2][1] * datapoint[2] + points[3][1] * datapoint[3] + points[6][1] * datapoint[6] + points[7][1] * datapoint[7])   / (abs(datapoint[2]) + abs(datapoint[3]) + abs(datapoint[6]) + abs(datapoint[7]))*dim2 + dim2/2


	
	if(average):
		for k in range (0,dim3):
			ante_pos[0] = ante_pos[0] + points[k][0]*datapoint[k]/(average*8);
			ante_pos[1] = ante_pos[1] + points[k][1]*datapoint[k]/(average*8);
		
		ante_pos[0] = min(dim1-1,max(0, round(ante_pos[0]*dim1) +dim1/2))
		ante_pos[1] = min(dim2-1,max(0, round(ante_pos[1]*dim2) +dim2/2))
		# print(ante_pos);


	

		# for k in range (0,dim3):
		# 	if((datapoint[k] > 0 and (ante_pos[0] > points[k][0]*dim1)) or (datapoint[k] < 0 and ante_pos[0] < points[k][0]*dim1)):
		# 		rightshift = rightshift + abs(datapoint[k]/average) *abs(ante_pos[0]-points[k][0]*dim1)/10
		# 	if((datapoint[k] > 0 and (ante_pos[0] < points[k][0]*dim1)) or (datapoint[k] < 0 and ante_pos[0] > points[k][0]*dim1)):
		# 		leftshift = leftshift + abs(datapoint[k]/average) *abs(ante_pos[0]-points[k][0]*dim1)/10
		# 	if((datapoint[k] > 0 and (ante_pos[1] > points[k][1]*dim2) or (datapoint[k] < 0 and ante_pos[1] < points[k][1]*dim2)):
		# 		downshift = downshift + abs(datapoint[k] / average)*abs(ante_pos[1]-points[k][1]*dim2)/10
		# 	if((datapoint[k] > 0 and (ante_pos[1] < points[k][1]*dim2)) or (datapoint[k] < 0 and ante_pos[1] > points[k][1]*dim2)):
		# 		upshift = upshift + abs(datapoint[k] / average) *abs(ante_pos[1]-points[k][1]*dim2)/10

		for k in range (0,dim3):
			points[k][0] = (points[k][0]+1/2)*dim1
			points[k][1] = (points[k][1]+1/2)*dim2

		# print(points)

		ante_pos = pos


		for k in range (0,dim3):
			if(datapoint[k] > 0 and (ante_pos[0] > points[k][0])):
				leftshift = leftshift   + abs(datapoint[k]/average) *abs(ante_pos[0]-points[k][0])/2
			if(datapoint[k] > 0 and (ante_pos[0] < points[k][0])):
				rightshift = rightshift + abs(datapoint[k]/average) *abs(ante_pos[0]-points[k][0])/2
			if(datapoint[k] > 0 and (ante_pos[1] > points[k][1])):
				upshift = upshift       + abs(datapoint[k]/average) *abs(ante_pos[1]-points[k][1])/2
			if(datapoint[k] > 0 and (ante_pos[1] < points[k][1])):
				downshift = downshift   + abs(datapoint[k]/average) *abs(ante_pos[1]-points[k][1])/2

		leftshift = round(leftshift)
		rightshift = round(rightshift)
		upshift = round(upshift)
		downshift = round(downshift)
		# print(leftshift)
		# print(rightshift)
		# print(upshift)
		# print(downshift)

		high = average/(abs((datapoint[7]-datapoint[0])/(datapoint[7]+datapoint[0])) + abs((datapoint[6]-datapoint[1])/(datapoint[6]+datapoint[1])) + abs((datapoint[5]-datapoint[2])/(datapoint[5]+datapoint[2])) + abs((datapoint[4]-datapoint[3])/(datapoint[4]+datapoint[3])))

		wide = average/(abs((datapoint[0]-datapoint[1])/(datapoint[0]+datapoint[1])) + abs((datapoint[2]-datapoint[3])/(datapoint[2]+datapoint[3])) + abs((datapoint[4]-datapoint[5])/(datapoint[4]+datapoint[5])) + abs((datapoint[6]-datapoint[7])/(datapoint[6]+datapoint[7])))


		# print(datapoint)
		# print(top_center)
		# print(bottom_center)
		
		# print(np.arctan)
		print("")

	intenseColor = min(1,intense*0.2)
	if (state == 1):
		for i in range (0,dim2):
			for j in range (0,dim1):
				if(pos[1] == i and pos[0] == j):
					colors.append((1,1,1))
				elif(ante_pos[1] == i and ante_pos[0] == j):
					colors.append((0,1,0))
				# elif(i < (ante_pos[1] +  upshift) and i > (ante_pos[1] - downshift) and j  < ( ante_pos[0] + rightshift) and j > (ante_pos[0] -  leftshift)) :
				# 	colors.append((0.5,0.5,0.5))
				
				else:
					colors.append((matchs[j][i] ,0,1-matchs[j][i] ))
				# print(matchs[j][i])	
	else:
		for i in range (0,dim1):
			for j in range (0,dim2):
				colors.append((0,0,0))

				

	theta = 0
	slope = 0
	sumweight = 0
	for k in range (0,dim3):
		unitweight = datapoint[k]/(np.sqrt((ante_pos[1] - points[k][1])**2+(ante_pos[0]-points[k][0])**2))
		if(ante_pos[0]-points[k][0]):
			slope = slope + (ante_pos[1] - points[k][1])/(ante_pos[0]-points[k][0])*unitweight
		sumweight = sumweight + unitweight
	if(sumweight):
		theta = np.arctan(slope/sumweight)
	else:
		theta = 0                                                                                                                                                                        

	scatterpoint.set_color(colors)
	# plotpoint.set_ydata(pos[1])


	forcePlot.set_angle(-np.arctan((top_center-bottom_center)/dim2)/pi*180+90)
	if(downshift + upshift):
		if((rightshift + leftshift)/(downshift + upshift) > 2):
			forcePlot.set_angle(np.arctan(dim1/(left_center-right_center)/pi*180))
			# print("horiz")
		else:
			pass
			# print("vert")
	forcePlot.set_center(ante_pos)
	forcePlot.set_height(upshift + downshift)
	forcePlot.set_width(rightshift + leftshift)


	# angle.set_ydata((dim2/2-1/2 ,dim2/2-1/2+5*np.sin(theta)))
	# angle.set_xdata((dim1/2-1/2,dim1/2-1/2+5*np.cos(theta)))
	vert_spine.set_xdata((bottom_center,top_center))
	hor_spine.set_ydata((left_center,right_center))


	fig.canvas.draw()
	fig.canvas.flush_events()
	print(Calibration)

	ser.flushInput()

	fig2.canvas.draw()
	fig2.canvas.flush_events()



	# print(peakness)


	# if(count > 2000):
	# 	plt.show()


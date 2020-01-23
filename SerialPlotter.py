
import serial
import time
import struct
import sys
import matplotlib.pyplot as plt
import numpy as np

print ("Begin")
ser = serial.Serial('COM3',timeout=5)  # open serial port
ser.baudrate = 2000000
count = 0
Data0 = np.zeros(100)
Data1 = []
Data2 = []
Data3 = []
Data4 = []
Data5 = []
Data6 = []
Data7 = []
Data8 = []
Data9 = []
DataA = []
DataB = []
DataC = []
DataD = []
DataE = []
DataF = []

plt.ion()		
fig = plt.figure()
ax1 = fig.add_subplot(111)
line1, = ax1.plot(np.linspace(count,100,count + 99) , Data0[count:count+99])

while(ser.read() != b'a'):
	pass
while 1: 
	
	count = count + 1;
	tdata = ser.read(131)             # Wait forever for anythingq
	#time.sleep(1)                   # Sleep (or inWaiting() doesn't give the correct value)
	# tdata += ser.readline(data_left) # Do the read and combine it with the first character
	# print(tdata)
	data0 = tdata[0:8]
	data1 = tdata[8:16]
	data2 = tdata[16:24]
	data3 = tdata[24:32]
	data4 = tdata[33:41]
	data5 = tdata[41:49]
	data6 = tdata[49:57]
	data7 = tdata[57:65]
	data8 = tdata[66:74]
	data9 = tdata[74:82]
	dataA = tdata[82:90]
	dataB = tdata[90:98]
	dataC = tdata[99:107]
	dataD = tdata[107:115]
	dataE = tdata[115:123]
	dataF = tdata[123:131]

	# print(data0)
	# print(data1)
	# print(data2)
	# print(data3)
	# print(data4)
	# print(data5)
	# print(data6)
	# print(data7)
	# print(data8)
	# print(data9)
	# print(dataA)
	# print(dataB)
	# print(dataC)
	# print(dataD)
	# print(dataE)
	# print(dataF)
	
	
	Data0 = np.append(Data0,[float(data0.decode("utf-8"))])
	Data1.append(float(data1.decode("utf-8")))
	Data2.append(float(data2.decode("utf-8")))
	Data3.append(float(data3.decode("utf-8")))
	Data4.append(float(data4.decode("utf-8")))
	Data5.append(float(data5.decode("utf-8")))
	Data6.append(float(data6.decode("utf-8")))
	Data7.append(float(data7.decode("utf-8")))
	Data8.append(float(data8.decode("utf-8")))
	Data9.append(float(data9.decode("utf-8")))
	DataA.append(float(dataA.decode("utf-8")))
	DataB.append(float(dataB.decode("utf-8")))
	DataC.append(float(dataC.decode("utf-8")))
	DataD.append(float(dataD.decode("utf-8")))
	DataE.append(float(dataE.decode("utf-8")))
	DataF.append(float(dataF.decode("utf-8")))

	line1.set_data(np.linspace(count,100,count + 99) , Data0[count:count+99])
	plt.show()
	#plt.pause(0.05)

	if(count == 100):
		print(Data0)
		break



print("End")



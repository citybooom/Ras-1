
import serial
import time
import struct
import sys
import matplotlib.pyplot as plt

print ("Begin")
ser = serial.Serial('COM3',timeout=5)  # open serial port
ser.baudrate = 500000
count = 0
Data = []
Data2 = []
Data3 = []
while(ser.read() != b'a'):
	pass
while 1: 
	
	tdata = ser.read(46)               # Wait forever for anythingq
	#time.sleep(1)                   # Sleep (or inWaiting() doesn't give the correct value)
	data_left = ser.inWaiting()      # Get the number of characters ready to be read
	# tdata += ser.readline(data_left) # Do the read and combine it with the first character
	print(tdata)
	if(sys.getsizeof(tdata) == 41):
		if(count == 0):
			Data.append(float(tdata.decode("utf-8")))
		if(count == 1):
			Data2.append(float(tdata.decode("utf-8")))
		if(count == 2):
			Data3.append(float(tdata.decode("utf-8")))
	if tdata == b'next\r\n':
		count = count + 1
	if count == 3:
		break


plt.plot(Data)
plt.plot(Data2)
plt.plot(Data3)
plt.show()
print("End")



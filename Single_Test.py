import serial


ser = serial.Serial('COM10',timeout=5)
ser.baudrate = 115200

f = open("Single_data_C1_30.txt", "a")

count = 0

while(1):

	while (ser.read() != b':'):
		pass
	tdata = ser.read(81)

	f.write(str(tdata))
	f.write("\n")
	count = count + 1
	print(count)
	if(count == 300):
		f.close()
		break
import serial


ser = serial.Serial('COM10',timeout=5)
ser.baudrate = 115200

ser2 = serial.Serial('COM11', timeout=0)
ser2.baudrate = 115200

f = open("Test5.txt", "a")

trial_pos = '0_0'
count = 0

while(1):

	if (ser2.read() == b':'):
		new_pos = (ser2.read(5)).decode('ascii')
		if(new_pos != trial_pos):
			f.write(new_pos)
			f.write("\n")
			trial_pos = new_pos
	while (ser.read() != b':'):
		pass
	tdata = ser.read(81)
	# data = [0,0,0,0,0,0,0,0]
	# charcounter = 0
	# tempdata = []
	# i = 0
	# while(i < 71):
	# 	try:
	# 		data[charcounter] = float(bytes(tdata[i:i+11]).decode("utf-8"))
	# 	except ValueError:
	# 		pass
		
	# 	charcounter = charcounter + 1
	# 	i = i + 10

	# f.write(str(data).strip('[]'))
	f.write(str(tdata))
	f.write("\n")
	count = count + 1
	print(trial_pos)
	if(trial_pos == '10_10'):
		f.close()
		break
	

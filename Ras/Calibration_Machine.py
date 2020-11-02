import serial


ser = serial.Serial('COM17',timeout=5)
ser.baudrate = 115200

ser2 = serial.Serial('COM9', timeout=100)
ser2.baudrate = 115200

trial_pos = '4_8'

while(1):

	while(ser.read() != b':'):
		if (ser2.read() == b':'):
			trial_pos = (ser2.read(3)).decode('ascii')


	ser.read()
	tdata = ser.read(81)
	data = [0,0,0,0,0,0,0,0]
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

	print(data);
	print(trial_pos)

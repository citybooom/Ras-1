import serial


ser = serial.Serial('COM14',timeout=5)
ser.baudrate = 115200

ser2 = serial.Serial('COM11', timeout=0)
ser2.baudrate = 115200

f = open("Test_1_S1.txt", "a")

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

	f.write(str(tdata))
	f.write("\n")
	count = count + 1
	print(trial_pos)
	if(trial_pos == '1_33_'):
		f.close()
		break
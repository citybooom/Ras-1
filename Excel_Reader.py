import xlrd
import numpy as np
# Give the location of the file
loc = ("Calibration.xlsx")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

dim1 = 24
dim2 = 10
dim3 = 8

Calibration = np.zeros((dim1, dim2, dim3))
Calibration [0][0][0] = 1

for i in range (0,dim1):
	for j in range (0,dim2):
		for k in range (0,dim3):
			Calibration[i][j][k] = sheet.cell_value( i,j+10*k)

print(Calibration[1,1,:])




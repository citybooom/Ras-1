import sys, math, random, queue, threading, time
import pyautogui
import serial
import numpy	
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread

x = numpy.array([1,2,3,4,5])
y = numpy.array([60,30,10,3,1])

timestart = time.time()
solutions = numpy.polyfit(numpy.log(x), y, 1)

fx = []
for value in x:
	fx.append(solutions[1] + solutions[0]*numpy.log(value))
print(time.time() - timestart)


plt.scatter(x,y)
plt.plot(x,fx)
plt.show()
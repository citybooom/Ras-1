from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
	app = QApplication(sys.argv)
	win = QMainWindow()
	win.setGeometry(0,0,100,100)
	win.setWindowTitle("Test")

	win.show()
	sys.exit(app.exec_())

window()
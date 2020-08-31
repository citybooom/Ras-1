import sys, math, random, queue, threading
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QThread

WIDTH = 10
grid = []
intense = 20
points = [(10,10),(10,15),(12,17)]

class Cell():
    def __init__(self, i, j, intensity):
        self.i = i
        self.j = j
        self.walls = [1, 1, 1, 1]  # top, right, bottom, left
        self.intensity = intensity
        #print(intensity)
    def index(self, i, j, cols, rows):
        if (i < 0) or (j < 0) or (i > (cols - 1)) or (j > (rows - 1)):
            return None
        else:
            return i + j * cols

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 1500
        self.height = 720
        self.color = 0
        self.point = (10,10)
        self.force = 80
        self.up = 0
        self.cols = math.floor(self.width / WIDTH)
        self.rows = math.floor(self.height / WIDTH)
        self.active = False
        self.initui()
        self.init_cells(self.point, intense)

    def keyPressEvent(self, event):
        global intense
        if(event.text() == 'a'):
            intense = intense + 1
        if(event.text() == 'd'):
            intense = intense - 1

    def init_cells(self, point, force):
    	global points
        if not self.active:
            del grid[:]
            for j in range(self.rows):
                for i in range(self.cols):
                	find


                    cell = Cell(i, j, min(255 , 255- (int(math.sqrt(abs(point[0]-i)**2 + abs(point[1]-j)**2)*(100-intense)))))
                    grid.append(cell)
            QTimer.singleShot(1, self.go)

    def go(self):
        self.active = True
        current = grid[0]
        current.visited = 1
        current.currentCell = 1
        while True:
            self.update()
            x, y = (pyautogui.position())
            self.point = [int(x / WIDTH), int(y / WIDTH)]
            QApplication.processEvents()
            QThread.msleep(1)
            if(self.up == 0):
                self.color = self.color + 1
                if self.color == 255:
                     self.up = 1
            else:
                self.color = self.color - 1
                if self.color == 0:
                     self.up = 0
        self.active = False

    def initui(self):
        QShortcut(QKeySequence('F5'), self, self.init_cells)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)
        self.show()

    def paintEvent(self, e):
        for c in grid:
            c.intensity = min(255 , 255- (int(math.sqrt(abs(self.point[0]-c.i)**2 + abs(self.point[1]-c.j)**2)*(100-intense))))
            self.draw_cell_manual(c)


    def draw_cell_manual(self, cell):
        x = cell.i * WIDTH
        y = cell.j * WIDTH
        # LINES
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        if cell.walls[0]:  # top
            qp.drawLine(x    , y    , x + WIDTH, y)
        if cell.walls[1]:  # right
            qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
        if cell.walls[2]:  # bottom
            qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
        if cell.walls[3]:  # left
            qp.drawLine(x    , y + WIDTH, x    , y)
        forcecolor = intense / 100
        qp.setBrush(QColor(max(0,min(255,forcecolor*cell.intensity)), max(0,min(255,((1.0 - forcecolor) * cell.intensity))) , 0, 200))
        qp.drawRect(x, y, WIDTH, WIDTH)


    def draw_cell(self, cell):
        x = cell.i * WIDTH
        y = cell.j * WIDTH
        # LINES
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        if cell.walls[0]:  # top
            qp.drawLine(x    , y    , x + WIDTH, y)
        if cell.walls[1]:  # right
            qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
        if cell.walls[2]:  # bottom
            qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
        if cell.walls[3]:  # left
            qp.drawLine(x    , y + WIDTH, x    , y)
        if cell.visited:
            if cell.currentCell:
                qp.setBrush(QColor(0, 0 , 255, 100))
            else:
                qp.setBrush(QColor(255, 0, 255, 100))
            qp.drawRect(x, y, WIDTH, WIDTH)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



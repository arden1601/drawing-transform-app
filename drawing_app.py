from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QTransform, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QLabel, QWidget, QInputDialog
from PyQt5.QtCore import Qt, QPoint, QRect, QTimer, QPointF
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        
        self.brushSize = 2
        
        self.is_drawing = False
        
        self.beginPoint = QPoint()
        self.lastPoint = QPoint()
        
        self.pen = QPen(Qt.black, 2)
        
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        
        self.mode = 'freedraw'
        
        self.translate_x = 50
        self.translate_y = 50
        
    def initUI(self):
        self.setGeometry(400, 400, 800, 800)
        self.setWindowTitle('TVG APP Arden')
        
        mainMenu = self.menuBar()
        
        modeMenu = mainMenu.addMenu('Mode')
        transformMenu = mainMenu.addMenu('Transform')
        clearMenu = mainMenu.addMenu('Clear')
        
        freedrawAction = QAction('Free Draw', self)
        freedrawAction.setShortcut('Ctrl+F')
        modeMenu.addAction(freedrawAction)
        freedrawAction.triggered.connect(self.freedrawButton)
        
        lineAction = QAction('Line', self)
        lineAction.setShortcut('Ctrl+L')
        modeMenu.addAction(lineAction)
        lineAction.triggered.connect(self.lineButton)
        
        rectAction = QAction('Rectangle', self)
        rectAction.setShortcut('Ctrl+R')
        modeMenu.addAction(rectAction)
        rectAction.triggered.connect(self.rectButton)
        
        circleAction = QAction('Circle', self)
        circleAction.setShortcut('Ctrl+C')
        modeMenu.addAction(circleAction)
        circleAction.triggered.connect(self.circleButton)
        
        translateAction = QAction('Translate', self)
        translateAction.setShortcut('Ctrl+Alt+T')
        transformMenu.addAction(translateAction)
        translateAction.triggered.connect(self.translate)
        
        rotateAction = QAction('Rotate', self)
        rotateAction.setShortcut('Ctrl+Alt+R')
        transformMenu.addAction(rotateAction)
        rotateAction.triggered.connect(self.rotate)
        
        scaleAction = QAction('Scale', self)
        scaleAction.setShortcut('Ctrl+Alt+S')
        transformMenu.addAction(scaleAction)
        scaleAction.triggered.connect(self.scale)
        
        clearAction = QAction('Clear', self)
        clearAction.setShortcut('Ctrl+C')
        clearMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
    def mousePressEvent(self, event):
        match self.mode:
            case 'freedraw':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = True
                    self.lastPoint = event.pos()
                    print(self.lastPoint)
            case 'line':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = True
                    self.beginPoint = event.pos()
                    self.lastPoint = self.beginPoint
                    self.update()
            case 'rectangle':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = True
                    self.beginPoint = event.pos()
                    self.lastPoint = self.beginPoint
                    self.update()
            case 'circle':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = True
                    self.beginPoint = event.pos()
                    self.lastPoint = self.beginPoint
                    self.update()
    def mouseMoveEvent(self, event):
        match self.mode:
            case 'freedraw':
                if (event.buttons() & Qt.LeftButton & self.is_drawing):
                    painter = QPainter(self.image)
                    painter.setPen(self.pen)
                    painter.drawLine(self.lastPoint, event.pos())
                    self.lastPoint = event.pos()
                    self.update()
            case 'line':
                if (event.buttons() & Qt.LeftButton & self.is_drawing):
                    self.lastPoint = event.pos()
                    self.update()
            case 'rectangle':
                if (event.buttons() & Qt.LeftButton & self.is_drawing):
                    self.lastPoint = event.pos()
                    self.update()
            case 'circle':
                if (event.buttons() & Qt.LeftButton & self.is_drawing):
                    self.lastPoint = event.pos()
                    self.update()
    def mouseReleaseEvent(self, event):
        match self.mode:
            case 'freedraw':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = False
            case 'line':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = False
                    canvasPainter = QPainter(self.image)
                    canvasPainter.setPen(self.pen)
                    canvasPainter.drawLine(self.beginPoint, self.lastPoint)
                    self.beginPoint, self.lastPoint = QPoint(), QPoint()
                    self.update()
            case 'rectangle':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = False
                    rect = QRect(self.beginPoint, self.lastPoint)
                    canvasPainter = QPainter(self.image)
                    canvasPainter.setPen(self.pen)
                    canvasPainter.drawRect(rect.normalized())
                    self.beginPoint, self.lastPoint = QPoint(), QPoint()
                    self.update()
            case 'circle':
                if event.button() == Qt.LeftButton:
                    self.is_drawing = False
                    self.lastPoint = event.pos()
                    canvasPainter = QPainter(self.image)
                    canvasPainter.setPen(self.pen)
                    x = round((self.beginPoint.x() - self.lastPoint.x())/2)
                    y = round((self.beginPoint.y() - self.lastPoint.y())/2)
                    center = QPointF(abs(x),abs(y))
                    radius = round(abs((self.beginPoint.x() - self.lastPoint.x())) + abs((self.beginPoint.y() - self.lastPoint.y())))
                    canvasPainter.drawEllipse(x, y, radius, radius)
                    self.beginPoint, self.lastPoint = QPoint(), QPoint()
                    self.update()
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        match self.mode:
            case 'freedraw':
                canvasPainter.setPen(self.pen)
                canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
            case 'line':
                canvasPainter.setPen(self.pen)
                canvasPainter.drawImage(QPoint(), self.image)
                if not self.beginPoint.isNull() and not self.lastPoint.isNull():
                    canvasPainter.drawLine(self.beginPoint, self.lastPoint)
            case 'rectangle':
                canvasPainter.drawImage(QPoint(), self.image)
                canvasPainter.setPen(self.pen)
                if not self.beginPoint.isNull() and not self.lastPoint.isNull():
                    rect = QRect(self.beginPoint, self.lastPoint)
                    canvasPainter.drawRect(rect.normalized())
            case 'circle':
                canvasPainter.setPen(self.pen)
                canvasPainter.drawImage(QPoint(), self.image)
                if not self.beginPoint.isNull() and not self.lastPoint.isNull():
                    x = round((self.beginPoint.x() - self.lastPoint.x())/2)
                    y = round((self.beginPoint.y() - self.lastPoint.y())/2)
                    center = QPointF(x,y)
                    radius = round(abs(self.beginPoint.x() - self.lastPoint.x()) + abs(self.beginPoint.y() - self.lastPoint.y()))
                    canvasPainter.drawEllipse(x, y, radius, radius)
    def freedrawButton(self):
        self.mode = 'freedraw'
    def lineButton(self):
        self.mode = 'line'
    def rectButton(self):
        self.mode = 'rectangle'
    def circleButton(self):
        self.mode = 'circle'
    def translate(self):
        x = QInputDialog.getInt(self,"Translasi X" ,"Berikan Input Translasi X")[0]
        y = QInputDialog.getInt(self,"Translasi Y" ,"Berikan Input Translasi Y")[0]
        self.translate_func(int(x),int(y))
    def translate_func(self, x, y):
        translated = self.image.copy()
        translated.fill(Qt.white)
        painter = QPainter(translated)
        painter.drawImage(QPoint(x,y), self.image)
        self.image = translated
        print("translated")
        self.update()
    
    def rotate(self):
        angle = QInputDialog.getInt(self,"Rotasi" ,"Berikan Input Sudut Rotasi")[0]
        self.rotate_func(angle)
    def rotate_func(self, angle):
        center = self.rect().center()
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(angle)
        transform.translate(center.x(), center.y())
        transform.translate(-center.x(), -center.y())
        rotated = self.image.transformed(transform)
        self.image = rotated
        print("rotated")
        self.update()
        
    def scale(self):
        x = QInputDialog.getDouble(self,"Skala x" ,"Berikan Input Skala x")[0]
        y = QInputDialog.getDouble(self,"Skala y" ,"Berikan Input Skala y")[0]
        self.scale_func(x,y)
    def scale_func(self, x, y):
        center = self.rect().center()
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.scale(x, y)
        transform.translate(center.x(), center.y())
        scaled = self.image.transformed(transform)
        self.image = scaled
        print("scaled")
        self.update()
    def clear(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.update()
    
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
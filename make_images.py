"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)
topWidget = QWidget()
topWidget.setLayout(QVBoxLayout())
label = QLabel()
topWidget.layout().addWidget(label)

def take_screenshot():
    picture = app.primaryScreen().grabWindow(topWidget.winId())
    picture.save(filename, 'jpg')

topWidget.layout().addWidget(QPushButton('take screenshot', clicked=take_screenshot))

topWidget.show()
app.exec_()
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Card: 
	def draw(self, app):
		topWidget = QWidget()
		topWidget.setLayout(QVBoxLayout())
		label = QLabel()
		topWidget.layout().addWidget(label)
		topWidget.show()
		app.exec_()

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)

def take_screenshot():
    picture = app.primaryScreen().grabWindow(topWidget.winId())
    picture.save(filename, 'jpg')

card = Card()
card.draw(app)
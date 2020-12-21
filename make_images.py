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

cardSideMargins = 20



class Card: 
	def draw(self, app):
		wholeCard = QWidget()
		wholeCard.resize(600, 500)
		wholeCard.setLayout(QVBoxLayout())

		topHalf = QWidget()
		topHalf.setLayout(QVBoxLayout())

		topTop = QWidget()
		topTop.setLayout(QHBoxLayout())

		nameLabel = QLabel()
		nameLabel.setText("Brooch")
		topTop.layout().addWidget(nameLabel)

		topRight = QWidget()
		topRight.setLayout(QVBoxLayout())

		rarityLabel = QLabel()
		rarityLabel.setText("Common")
		topRight.layout().addWidget(rarityLabel)

		costLabel = QLabel()
		costLabel.setText("2")
		topRight.layout().addWidget(costLabel)

		topTop.layout().addWidget(topRight)

		topHalf.layout().addWidget(topTop)

		topBottom = QWidget()
		topBottom.setLayout(QHBoxLayout())

		topBottomLeft = QWidget()
		topBottom.layout().addWidget(topBottomLeft)

		topBottomMiddle = QWidget()
		topBottomMiddle.setLayout(QVBoxLayout())

		equipRulesLabel = QLabel()
		equipRulesLabel.setText("Requires completing a special quest")
		topBottomMiddle.layout().addWidget(equipRulesLabel)

		descriptionLabel = QLabel()
		descriptionLabel.setText("Worn at the shoulder or chest, carefully crafted bronze or iron. Often associated with a noble family.")
		topBottomMiddle.layout().addWidget(descriptionLabel)

		topBottom.layout().addWidget(topBottomMiddle)

		topBottomRight = QWidget()
		topBottom.layout().addWidget(topBottomRight)

		topHalf.layout().addWidget(topBottom)

		wholeCard.layout().addWidget(topHalf)

		bottomHalf = QWidget()
		bottomHalf.setLayout(QHBoxLayout())

		bottomLeft = QWidget()
		bottomHalf.layout().addWidget(bottomLeft)

		bottomMiddle = QWidget()
		bottomMiddle.setLayout(QVBoxLayout())

		situationLabel = QLabel()
		situationLabel.setText("Persuade / Command")
		bottomMiddle.layout().addWidget(situationLabel)

		bottomCenter = QWidget()
		bottomCenter.setLayout(QVBoxLayout())

		bonusMain = QLabel()
		bonusMain.setText("+3 Dice")
		bottomCenter.layout().addWidget(bonusMain)

		bonusSecondary = QLabel()
		bonusSecondary.setText("Once check per long rest, double all 4s and halve all 8s")
		bottomCenter.layout().addWidget(bonusSecondary)

		bottomMiddle.layout().addWidget(bottomCenter)

		skillsLabel = QLabel()
		skillsLabel.setText("Charmer, Persuader, Politico, etc")
		bottomMiddle.layout().addWidget(skillsLabel)

		bottomHalf.layout().addWidget(bottomMiddle)

		bottomRight = QWidget()
		bottomHalf.layout().addWidget(bottomRight)

		wholeCard.layout().addWidget(bottomHalf)

		wholeCard.show()
		app.exec_()

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)

"""
def take_screenshot():
    picture = app.primaryScreen().grabWindow(topWidget.winId())
    picture.save(filename, 'jpg')
"""

card = Card()
card.draw(app)
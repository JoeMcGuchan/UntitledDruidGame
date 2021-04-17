import sys
import csv

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

cardSideMargins = 15
standardSpacing = 10
equipRulesIndent = 8
descriptionMargin = 7

topHalfStretchFacor = 13
bottomHalfStretchFactor = 17

mediumFontSize = 24
largeFontSize = 36

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)

celticFontId = QFontDatabase.addApplicationFont("../fonts/MeathFLF.ttf");
celticFontFamily = QFontDatabase.applicationFontFamilies(celticFontId)[0];
basicFontFamily = "arial"

celticTitle = QFont(celticFontFamily, 48)
celticExtraLarge = QFont(celticFontFamily, 64)
basicFont = QFont(basicFontFamily, 14)
basicFontItalic = QFont(basicFontFamily, 14, italic = True)
basicFontMedium = QFont(basicFontFamily, mediumFontSize)
basicFontLarge = QFont(basicFontFamily, largeFontSize)

dataFile = "../cards/items.csv"	

def convertText(string, size):
	return string.replace("<knot>", '<img src="../images/knot_icon.png" height="' + str(size + 5) + '" width="' + str(size + 5) + '">')

class Card: 
	name = "Brooch"
	cost = "2"
	rarity = "Common"
	equipRules = "- Requires completing a special quest."
	uses = 0
	description = "Worn at the shoulder or chest, carefully crafted bronze or iron. Often associated with a noble family."

	situation = "Persuade / Command"
	bonusMain = "+3 Dice"
	bonusSecondary = "Once check per long rest, double all 4s and halve all 8s"
	skills = "Charmer, Persuader, etc"

	secondAbility = True
	situation2 = "Attack - Melee"
	bonusMain2 = "+3 Dice"
	bonusSecondary2 = "Eat all the rice"
	skills2 = "yum yum yum"

	def isNull(self):
		return not bool(self.name.strip())

	def draw(self, app):
		if self.isNull():
			return

		backgroundPixmap = QPixmap()

		if (self.secondAbility):
			backgroundPixmap.load("../images/item_card_double.png")
		else:
			backgroundPixmap.load("../images/item_card_single.png")

		wholeCard = QLabel()
		wholeCard.setPixmap(backgroundPixmap)
		wholeCard.resize(600, 600)
		wholeCard.setLayout(QVBoxLayout())
		wholeCard.layout().setSpacing(standardSpacing)
		wholeCard.layout().setContentsMargins(cardSideMargins,cardSideMargins,cardSideMargins,cardSideMargins)

		topHalf = QFrame()
		topHalf.setLayout(QGridLayout())
		topHalf.layout().setSpacing(1)
		topHalf.layout().setContentsMargins(0,0,0,0)

		nameLabel = QLabel()

		costLabel = QLabel()
		costLabel.setText(self.cost)
		costLabel.setFont(celticExtraLarge)

		rarityLabel = QLabel()
		rarityLabel.setText(self.rarity)
		rarityLabel.setFont(basicFont)

		equipRulesLabel = QLabel()
		equipRulesLabel.setText(self.equipRules)
		equipRulesLabel.setFont(basicFont)

		descriptionLabel = QLabel()
		descriptionLabel.setText(self.description)
		descriptionLabel.setAlignment(Qt.AlignLeft)
		descriptionLabel.setFont(basicFontItalic)
		descriptionLabel.setWordWrap(True)

		topHalf.layout().addWidget(nameLabel, 0,0,1,4, Qt.AlignBottom)
		topHalf.layout().addWidget(costLabel, 0,4,3,2, Qt.AlignLeft)
		topHalf.layout().addWidget(rarityLabel, 1,1,1,1)
		topHalf.layout().addWidget(equipRulesLabel, 1,3,1,1)
		topHalf.layout().addWidget(descriptionLabel, 3,1,1,4)

		topHalf.layout().setColumnMinimumWidth(0,standardSpacing)
		topHalf.layout().setColumnMinimumWidth(5,standardSpacing)
		topHalf.layout().setColumnMinimumWidth(2,equipRulesIndent)
		topHalf.layout().setRowMinimumHeight(2,descriptionMargin)

		topHalf.layout().setColumnStretch(3,1)
		topHalf.layout().setRowStretch(3,1)

		wholeCard.layout().addWidget(topHalf, topHalfStretchFacor)

		bottomHalf = QFrame()
		bottomHalf.setLayout(QGridLayout())
		bottomHalf.layout().setSpacing(0)
		bottomHalf.layout().setContentsMargins(0,0,0,0)

		situationLabel = QLabel()
		situationLabel.setText(self.situation)
		situationLabel.setFont(basicFont)

		bonusWidgetLayout = QVBoxLayout()

		bonusMain = QLabel()
		bonusMain.setVisible(self.bonusMain != "")
		bonusMain.setAlignment(Qt.AlignHCenter)
		if (self.secondAbility):
			bonusMain.setText(convertText(self.bonusMain, mediumFontSize))
			bonusMain.setFont(basicFontMedium)
		else:
			bonusMain.setText(convertText(self.bonusMain, largeFontSize))
			bonusMain.setFont(basicFontLarge)

		bonusSecondary = QLabel()
		bonusSecondary.setText(convertText(self.bonusSecondary, mediumFontSize))
		bonusSecondary.setVisible(self.bonusSecondary != "")
		bonusSecondary.setAlignment(Qt.AlignHCenter)
		bonusSecondary.setWordWrap(True)
		bonusSecondary.setFont(basicFontMedium)

		bonusWidgetLayout.addSpacerItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding))
		bonusWidgetLayout.addWidget(bonusMain, 0)
		bonusWidgetLayout.addWidget(bonusSecondary, 0)
		bonusWidgetLayout.addSpacerItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding))

		skillsLabel = QLabel()
		skillsLabel.setText(self.skills)
		skillsLabel.setFont(basicFont)

		bottomHalf.layout().addWidget(situationLabel, 0,1,1,1, Qt.AlignLeft | Qt.AlignVCenter)
		bottomHalf.layout().addLayout(bonusWidgetLayout, 1,1,1,1)
		bottomHalf.layout().addWidget(skillsLabel, 2,1,1,1, Qt.AlignRight | Qt.AlignVCenter)

		bottomHalf.layout().setRowStretch(1,1)
		bottomHalf.layout().setColumnStretch(1,1)

		bottomHalf.layout().setColumnMinimumWidth(0,standardSpacing)
		bottomHalf.layout().setColumnMinimumWidth(2,standardSpacing)

		if (self.secondAbility):
			situationLabel2 = QLabel()
			situationLabel2.setText(self.situation2)
			situationLabel2.setVisible(self.situation2 != "")
			situationLabel2.setFont(basicFont)

			bonusWidgetLayout2 = QVBoxLayout()

			bonusMain2 = QLabel()
			bonusMain2.setText(convertText(self.bonusMain2,mediumFontSize))
			bonusMain2.setVisible(self.bonusMain2 != "")
			bonusMain2.setAlignment(Qt.AlignHCenter)
			bonusMain2.setFont(basicFontMedium)

			bonusSecondary2 = QLabel()
			bonusSecondary2.setText(convertText(self.bonusSecondary2,mediumFontSize))
			bonusSecondary2.setAlignment(Qt.AlignHCenter)
			bonusSecondary2.setWordWrap(True)
			bonusSecondary2.setFont(basicFontMedium)

			bonusWidgetLayout2.addSpacerItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding))
			bonusWidgetLayout2.addWidget(bonusMain2, 0)
			bonusWidgetLayout2.addWidget(bonusSecondary2, 0)
			bonusWidgetLayout2.addSpacerItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding))

			skillsLabel2 = QLabel()
			skillsLabel2.setText(self.skills2)
			skillsLabel2.setFont(basicFont)

			bottomHalf.layout().addWidget(situationLabel2, 0,3,1,1, Qt.AlignLeft | Qt.AlignVCenter)
			bottomHalf.layout().addLayout(bonusWidgetLayout2, 1,3,1,1)
			bottomHalf.layout().addWidget(skillsLabel2, 2,3,1,1, Qt.AlignRight | Qt.AlignVCenter)

			bottomHalf.layout().setColumnStretch(3,1)
			bottomHalf.layout().setColumnMinimumWidth(4,standardSpacing)

		wholeCard.layout().addWidget(bottomHalf, bottomHalfStretchFactor)

		wholeCard.show()

		#fit name text
		fit = False
		celticTitle.setPointSize(48)

		while (not fit):
			fm = QFontMetrics(celticTitle)
			bound = fm.boundingRect(0,0, nameLabel.width(), 48, Qt.AlignLeft, self.name)

			if (bound.width() <= nameLabel.width()):
				fit = True
			else:
				print("here")
				celticTitle.setPointSize(celticTitle.pointSize() - 1);

		nameLabel.setText(self.name)
		nameLabel.setAlignment(Qt.AlignBottom)
		nameLabel.setFont(celticTitle)

		app.exec_()

def makeCard(cardInfo):
	card = Card()

	card.name = f'{cardInfo["Name"]}'
	card.cost = f'{cardInfo["Value"]}'

	card.rarity = f'{cardInfo["Rarity"]}'
	card.equipRules = f'{cardInfo["Special Equip Rules"]}'
	card.uses = cardInfo["Uses"]

	card.description = f'{cardInfo["Flavour"]}'

	card.secondAbility = (f'{cardInfo["Mode"]}' == "DOUBLE")

	card.situation = f'{cardInfo["Conflict Class"]}'
	card.bonusMain = f'{cardInfo["Bonus Main"]}'
	card.bonusSecondary = f'{cardInfo["Bonus Secondary"]}'
	card.skills = f'{cardInfo["Skills"]}'

	card.situation2 = f'{cardInfo["Conflict Class 2"]}'
	card.bonusMain2 = f'{cardInfo["Bonus 2"]}'
	card.bonusSecondary2 = f'{cardInfo["Bonus 2 Secondary"]}'
	card.skills2 = f'{cardInfo["Skills 2"]}'

	return card

with open(dataFile, newline='') as csvItems:
    itemsReader = csv.DictReader(csvItems, delimiter=',', quotechar='"')
    for card in itemsReader:
        makeCard(card).draw(app)
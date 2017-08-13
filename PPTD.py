'''TODO: 
    need some potential update feature
    populate database and create practice run for presentation
'''
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
import sys
import requests
import random
import string

class DropWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setup()
    
    def setup(self): 
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("GolisoBox - Drop a Pokemon")
        self.namebox = QtWidgets.QLineEdit(self)
        self.namebox.setPlaceholderText("DBID (NOT Optional)")
        self.namebox.move(20, 20)
        self.namebox.resize(280,40)
        self.drop_btn = QtWidgets.QPushButton(self)
        self.drop_btn.setText("Drop")
        self.drop_btn.move(320, 30)
        self.drop_btn.clicked.connect(self.leygo)


    def leygo(self):
        #print("Dropping")
        engine = create_engine("mysql+pymysql://username:password@database:port/name", echo=False)    
        connection = engine.connect()

        if self.namebox.text() != "":
            command = "DELETE FROM POKEMON WHERE PokemonDBID=\"" + (str)(self.namebox.text()) + "\""
            print(command)
            connection.execute(command)
        connection.close()
        self.close()

class AddWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setup()
    
    def setup(self):
        self.label = QtWidgets.QLabel(self)  
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("GolisoBox - Add a Pokemon")
        self.category_bool_list = [0] * 9 
        self.addtheshit = QtWidgets.QPushButton(self)
        self.addtheshit.setText("ADD IT")
        self.addtheshit.move(400, 300)
        self.addtheshit.clicked.connect(self.leygo)
        self.langlist = ['ENG', 'FRE', 'GER', 'JPN', 'SPN', 'CHA', 'KOR', 'ITA']
        self.catlist = ['Breeding', 'Perfect', 'HiddenAbility', 'Sweeper', 'Tank', 'Legendary', 'Mythic', 'EVENT', 'Trained']
        self.lastbutton = None

        self.categories = QtWidgets.QButtonGroup(self)
        #self.eggs = QtWidgets.QButtonGroup(self)
        self.languages = QtWidgets.QButtonGroup(self)

        self.languages.setExclusive(True)
        self.categories.setExclusive(True)

        self.namebox = QtWidgets.QLineEdit(self)
        self.namebox.setPlaceholderText("Pokedex Number (INT)(NOT Optional)")
        self.namebox.move(20, 20)
        self.namebox.resize(280,40)

        self.otidbox = QtWidgets.QLineEdit(self)
        self.otidbox.setPlaceholderText("OTID (INT)(NOT Optional)")
        self.otidbox.move(20, 70)
        self.otidbox.resize(280,40)

        self.levelbox = QtWidgets.QLineEdit(self)
        self.levelbox.setPlaceholderText("Level (INT)(Optional Defaults to 1)")
        self.levelbox.move(20, 120)
        self.levelbox.resize(280,40)

        self.naturebox = QtWidgets.QLineEdit(self)
        self.naturebox.setPlaceholderText("Nature (Optional - Defaults to Bold)")
        self.naturebox.move(20, 170)
        self.naturebox.resize(280,40)

        self.nickbox = QtWidgets.QLineEdit(self)
        self.nickbox.setPlaceholderText("Nickname (Optional - Defaults to NULL)")
        self.nickbox.move(20, 220)
        self.nickbox.resize(280,40)

        self.abilbox = QtWidgets.QLineEdit(self)
        self.abilbox.setPlaceholderText("Ability (Optional - Defaults to NULL)")
        self.abilbox.move(20, 270)
        self.abilbox.resize(280,40)

        self.textlist = []
        self.textlist.append((self.namebox, 'name'))
        self.textlist.append((self.otidbox, 'otid'))
        self.textlist.append((self.levelbox, 'level'))
        self.textlist.append((self.naturebox, 'nature'))
        self.textlist.append((self.nickbox, 'nickname'))


        self.catlabel = QtWidgets.QLabel(self)
        self.catlabel.setText("Category")
        self.catlabel.move(320, 5)

        self.breedingbox = QtWidgets.QCheckBox('Breeding', self)
        self.breedingbox.move(320, 20)
        self.categories.addButton(self.breedingbox, 0)

        self.perfectbox = QtWidgets.QCheckBox('Perfect', self)
        self.perfectbox.move(320, 35)
        self.categories.addButton(self.perfectbox, 1)

        self.abilitybox = QtWidgets.QCheckBox('Hidden Ability', self)
        self.abilitybox.move(320, 50)
        self.categories.addButton(self.abilitybox, 2)

        self.sweepbox = QtWidgets.QCheckBox('Sweeper', self)
        self.sweepbox.move(320, 65)
        self.categories.addButton(self.sweepbox, 3)

        self.tankbox = QtWidgets.QCheckBox('Tank', self)
        self.tankbox.move(320, 80)
        self.categories.addButton(self.tankbox, 4)

        self.legbox = QtWidgets.QCheckBox('Legendary', self)
        self.legbox.move(320, 95)
        self.categories.addButton(self.legbox, 5)

        self.mytbox = QtWidgets.QCheckBox('Mythic', self)
        self.mytbox.move(320, 110)
        self.categories.addButton(self.mytbox, 6)

        self.eventbox = QtWidgets.QCheckBox('Event', self)
        self.eventbox.move(320, 125)
        self.categories.addButton(self.eventbox, 7)

        self.trnbox = QtWidgets.QCheckBox('Trained', self)
        self.trnbox.move(320, 140)
        self.categories.addButton(self.trnbox, 8)

        self.categories.buttonClicked.connect(self.fugginsignal)

        self.langlabel = QtWidgets.QLabel(self)
        self.langlabel.setText("Language")
        self.langlabel.move(450, 5)

        self.engbox = QtWidgets.QCheckBox('ENG', self)
        self.engbox.move(450, 20)
        self.languages.addButton(self.engbox, 0)

        self.frebox = QtWidgets.QCheckBox('FRE', self)
        self.frebox.move(450, 35)
        self.languages.addButton(self.frebox, 1)

        self.gerbox = QtWidgets.QCheckBox('GER', self)
        self.gerbox.move(450, 50)
        self.languages.addButton(self.gerbox, 2)

        self.jpnbox = QtWidgets.QCheckBox('JPN', self)
        self.jpnbox.move(450, 65)
        self.languages.addButton(self.jpnbox, 3)

        self.spnbox = QtWidgets.QCheckBox('SPN', self)
        self.spnbox.move(450, 80)
        self.languages.addButton(self.spnbox, 4)

        self.chabox = QtWidgets.QCheckBox('CHA', self)
        self.chabox.move(450, 95)
        self.languages.addButton(self.chabox, 5)

        self.korbox = QtWidgets.QCheckBox('KOR', self)
        self.korbox.move(450, 110)
        self.languages.addButton(self.korbox, 6)

        self.itabox = QtWidgets.QCheckBox('ITA', self)
        self.itabox.move(450, 125)
        self.languages.addButton(self.itabox, 7)

        self.languages.buttonClicked.connect(self.fugginsignal)

        self.shinybox = QtWidgets.QCheckBox('Shiny', self)
        self.shinybox.move(580, 20)

    def fugginsignal(self, btn):
        #print("uncheck time bois")
        if not self.lastbutton:
            self.lastbutton = btn
        else:
            if self.lastbutton == btn:
                self.sender().setExclusive(False)
                btn.setCheckState(QtCore.Qt.Unchecked)
                self.sender().setExclusive(True)
                self.lastbutton = None
            else:
                self.lastbutton = btn

    def leygo(self):
        engine = create_engine("mysql+pymysql://username:password@database:port/name", echo=False)    
        connection = engine.connect()

        langpressedbutton = self.languages.checkedId()
        categorypressedbutton = self.categories.checkedId()
        uniqueids = []

        '''Being the fucking maddness'''

        command = "SELECT PokemonDBID FROM POKEMON"
        result = connection.execute(command)
        for item in result:
            uniqueids.append((str)(item[0]))

        print(uniqueids)
        command = "INSERT INTO POKEMON(PokemonDBID, PokedexNumber, OTID, Level, Nature, Language, Ability, Shiny, Nickname) VALUES("
        chars=string.ascii_uppercase + string.digits
        newid = ''.join(random.choice(chars) for _ in range(16))
            
        for newid in uniqueids:
            newid = ''.join(random.choice(chars) for _ in range(16))

        print(newid)
        command += "\"" + newid + "\", " + (str)(self.namebox.text()) + ", " + (str)(self.otidbox.text()) + ", "
        if (str)(self.levelbox.text()) == "":
            command += "1, "
        else:
            command += (str)(self.levelbox.text()) + ", "

        if (str)(self.naturebox.text()) == "":
            command += "\"Bold\", "
        else:
            command += "\"" + (str)(self.naturebox.text()) + "\", "

        if langpressedbutton == -1:
            command += "\"ENG\", "
        else:
            command += "\"" + self.langlist[langpressedbutton] + "\", "

        if (str)(self.abilbox.text()) == "":
            command += "NULL, "
        else:
            command += "\"" + (str)(self.abilbox.text()) +"\", "

        if self.shinybox.isChecked():
            command += "1, "
        else:
            command += "0, "

        if (str)(self.nickbox.text()) == "":
            command += "NULL)"
        else:
            command += "\"" + (str)(self.nickbox.text()) + "\")"

        invokecatcall = False
        if categorypressedbutton != -1:
            catcommand = "UPDATE CATEGORY SET "
            catcommand += self.catlist[categorypressedbutton] + "=1 WHERE CATEGORY.Poke=" + "\"" + newid + "\""
            invokecatcall = True

        #print(command, '\n', catcommand)

        connection.execute(command)
        if invokecatcall == True:
            connection.execute(catcommand)

        connection.close()
        print("PENIS")
        self.close()

class ScrollSearch(QtWidgets.QMainWindow):
    def __init__(self, textbs, catbuttons, eggbuttons, langs, shiny):
        QtWidgets.QWidget.__init__(self)
        self.textboxes = textbs
        self.categories = catbuttons
        self.eggs = eggbuttons
        self.languages = langs
        self.shinybox = shiny
        self.setup()

    def setup(self):
        self.setFixedSize(900, 400)
        self.scrolly = QtWidgets.QScrollArea(self)
        self.setWindowTitle("GolisoBox - Search Results")
        self.searchwin = SearchResult(self, self.textboxes, self.categories, self.eggs, self.languages, self.shinybox)
        self.scrolly.setWidget(self.searchwin)
        self.setCentralWidget(self.scrolly)

class ScrollView(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setup()

    def setup(self):
        self.setFixedSize(1200, 400)
        self.scrolly = QtWidgets.QScrollArea(self)
        self.setWindowTitle("GolisoBox - All Pokemon")
        self.allwin = AllWindow(self)
        self.scrolly.setWidget(self.allwin)
        self.setCentralWidget(self.scrolly)

class PPTDWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setup()

    def setup(self):
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("final.py")

        self.dbview = DatabaseView(self)
        self.setCentralWidget(self.dbview)

        self.show()

class TableLabel(QtWidgets.QLabel):
    def __init__(self, parent, text):
        QtWidgets.QWidget.__init__(self)
        self.setup(text)

    def setup(self, text):
        self.setText(text)
        self.resize(self.sizeHint())

class SearchWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setup()
    
    def setup(self):
        self.label = QtWidgets.QLabel(self)
        self.setWindowTitle("GolisoBox - Search for Pokemon")  
        self.setGeometry(200, 200, 800, 600)
        self.category_bool_list = [0] * 9 
        self.lastbutton = None
        
        self.categories = QtWidgets.QButtonGroup(self)
        self.eggs = QtWidgets.QButtonGroup(self)
        self.languages = QtWidgets.QButtonGroup(self)

        self.languages.setExclusive(True)
        self.categories.setExclusive(True)
        self.eggs.setExclusive(True)

        self.namebox = QtWidgets.QLineEdit(self)
        self.namebox.setPlaceholderText("Species Name (Optional)")
        self.namebox.move(20, 20)
        self.namebox.resize(280,40)

        self.levelbox = QtWidgets.QLineEdit(self)
        self.levelbox.setPlaceholderText("Level (Optional - Integer Only)")
        self.levelbox.move(20, 70)
        self.levelbox.resize(280,40)

        self.naturebox = QtWidgets.QLineEdit(self)
        self.naturebox.setPlaceholderText("Nature (Optional)")
        self.naturebox.move(20, 120)
        self.naturebox.resize(280,40)

        self.otidbox = QtWidgets.QLineEdit(self)
        self.otidbox.setPlaceholderText("OTID (INT)(Optional)")
        self.otidbox.move(20, 170)
        self.otidbox.resize(280,40)

        self.textlist = []
        self.textlist.append((self.namebox, 'name'))
        self.textlist.append((self.levelbox, 'level'))
        self.textlist.append((self.naturebox, 'nature'))
        self.textlist.append((self.otidbox, 'otid'))

        self.catlabel = QtWidgets.QLabel(self)
        self.catlabel.setText("Category")
        self.catlabel.move(320, 5)

        self.breedingbox = QtWidgets.QCheckBox('Breeding', self)
        self.breedingbox.move(320, 20)
        self.categories.addButton(self.breedingbox, 0)

        self.perfectbox = QtWidgets.QCheckBox('Perfect', self)
        self.perfectbox.move(320, 35)
        self.categories.addButton(self.perfectbox, 1)

        self.abilitybox = QtWidgets.QCheckBox('Hidden Ability', self)
        self.abilitybox.move(320, 50)
        self.categories.addButton(self.abilitybox, 2)

        self.sweepbox = QtWidgets.QCheckBox('Sweeper', self)
        self.sweepbox.move(320, 65)
        self.categories.addButton(self.sweepbox, 3)

        self.tankbox = QtWidgets.QCheckBox('Tank', self)
        self.tankbox.move(320, 80)
        self.categories.addButton(self.tankbox, 4)

        self.legbox = QtWidgets.QCheckBox('Legendary', self)
        self.legbox.move(320, 95)
        self.categories.addButton(self.legbox, 5)

        self.mytbox = QtWidgets.QCheckBox('Mythic', self)
        self.mytbox.move(320, 110)
        self.categories.addButton(self.mytbox, 6)

        self.eventbox = QtWidgets.QCheckBox('Event', self)
        self.eventbox.move(320, 125)
        self.categories.addButton(self.eventbox, 7)

        self.trnbox = QtWidgets.QCheckBox('Trained', self)
        self.trnbox.move(320, 140)
        self.categories.addButton(self.trnbox, 8)

        self.categories.buttonClicked.connect(self.fugginsignal)

        self.egglabel = QtWidgets.QLabel(self)
        self.egglabel.setText("Egg Group")
        self.egglabel.move(450, 5)

        self.monsterbox = QtWidgets.QCheckBox('Monster', self)
        self.monsterbox.move(450, 20)
        self.eggs.addButton(self.monsterbox, 0)

        self.humanbox = QtWidgets.QCheckBox('Human-Like', self)
        self.humanbox.move(450, 35)
        self.eggs.addButton(self.humanbox, 1)

        self.water1box = QtWidgets.QCheckBox('Water 1', self)
        self.water1box.move(450, 50)
        self.eggs.addButton(self.water1box, 2)

        self.water2box = QtWidgets.QCheckBox('Water 2', self)
        self.water2box.move(450, 65)
        self.eggs.addButton(self.water2box, 3)

        self.water3box = QtWidgets.QCheckBox('Water 3', self)
        self.water3box.move(450, 80)
        self.eggs.addButton(self.water3box, 4)

        self.bugbox = QtWidgets.QCheckBox('Bug', self)
        self.bugbox.move(450, 95)
        self.eggs.addButton(self.bugbox, 5)

        self.mineralbox = QtWidgets.QCheckBox('Mineral', self)
        self.mineralbox.move(450, 110)
        self.eggs.addButton(self.mineralbox, 6)

        self.flyingbox = QtWidgets.QCheckBox('Flying', self)
        self.flyingbox.move(450, 125)
        self.eggs.addButton(self.flyingbox, 7)

        self.amorbox = QtWidgets.QCheckBox('Amorphous', self)
        self.amorbox.move(450, 140)
        self.eggs.addButton(self.amorbox, 8)

        self.fieldbox = QtWidgets.QCheckBox('Field', self)
        self.fieldbox.move(450, 155)
        self.eggs.addButton(self.fieldbox, 9)

        self.fairybox = QtWidgets.QCheckBox('Fairy', self)
        self.fairybox.move(450, 170)
        self.eggs.addButton(self.fairybox, 10)

        self.dittobox = QtWidgets.QCheckBox('Ditto', self)
        self.dittobox.move(450, 185)
        self.eggs.addButton(self.dittobox, 11)

        self.dragbox = QtWidgets.QCheckBox('Dragon', self)
        self.dragbox.move(450, 200)
        self.eggs.addButton(self.dragbox, 12)

        self.undibox = QtWidgets.QCheckBox('Undiscovered', self)
        self.undibox.move(450, 215)
        self.eggs.addButton(self.undibox, 13)

        self.eggs.buttonClicked.connect(self.fugginsignal)

        self.langlabel = QtWidgets.QLabel(self)
        self.langlabel.setText("Language")
        self.langlabel.move(580, 5)

        self.engbox = QtWidgets.QCheckBox('ENG', self)
        self.engbox.move(580, 20)
        self.languages.addButton(self.engbox, 0)

        self.frebox = QtWidgets.QCheckBox('FRE', self)
        self.frebox.move(580, 35)
        self.languages.addButton(self.frebox, 1)

        self.gerbox = QtWidgets.QCheckBox('GER', self)
        self.gerbox.move(580, 50)
        self.languages.addButton(self.gerbox, 2)

        self.jpnbox = QtWidgets.QCheckBox('JPN', self)
        self.jpnbox.move(580, 65)
        self.languages.addButton(self.jpnbox, 3)

        self.spnbox = QtWidgets.QCheckBox('SPN', self)
        self.spnbox.move(580, 80)
        self.languages.addButton(self.spnbox, 4)

        self.chabox = QtWidgets.QCheckBox('CHA', self)
        self.chabox.move(580, 95)
        self.languages.addButton(self.chabox, 5)

        self.korbox = QtWidgets.QCheckBox('KOR', self)
        self.korbox.move(580, 110)
        self.languages.addButton(self.korbox, 6)

        self.itabox = QtWidgets.QCheckBox('ITA', self)
        self.itabox.move(580, 125)
        self.languages.addButton(self.itabox, 7)

        self.languages.buttonClicked.connect(self.fugginsignal)

        self.shinybox = QtWidgets.QCheckBox('Shiny', self)
        self.shinybox.move(710, 20)

        self.go_btn = GoButton(self, self.textlist, self.categories, self.eggs, self.languages, self.shinybox)
        self.go_btn.move(400, 300)

    def fugginsignal(self, btn):
        #print("uncheck time bois")
        if not self.lastbutton:
            self.lastbutton = btn
        else:
            if self.lastbutton == btn:
                self.sender().setExclusive(False)
                btn.setCheckState(QtCore.Qt.Unchecked)
                self.sender().setExclusive(True)
                self.lastbutton = None
            else:
                self.lastbutton = btn


class SearchResult(QtWidgets.QWidget):
    def __init__(self, parent, textbs, catbuttons, eggbuttons, langs, shiny):
        QtWidgets.QWidget.__init__(self)
        self.textboxes = textbs
        self.categories = catbuttons
        self.eggs = eggbuttons
        self.languages = langs
        self.shinybox = shiny
        self.setup()
    
    def setup(self):
        self.grid = QtWidgets.QGridLayout()
        self.setWindowTitle("GolisoBox - Search Results")
        self.gridlist = ['Image', 'Species', 'Pokedex Number', 'DBID', 'OTID', 'Level', 'Nature', 'Language', 'Ability', 'Shiny']
        engine = create_engine("mysql+pymysql://username:password@database:port/name", echo=False)    
        connection = engine.connect()
        self.setLayout(self.grid)
        self.setGeometry(200, 200, 1200, 600)
        self.catlist = [(0, 'Breeding'), (0, 'Perfect'), (0, 'HiddenAbility'), (0, 'Sweeper'), (0, 'Tank'), (0, 'Legendary'), (0, 'Mythic'), (0, 'EVENT'), (0, 'Trained')]
        self.egglist = ['Monster', 'HumanLike', 'Water1', 'Water2', 'Water3', 'Bug', 'Mineral', 'Flying', 'Amorphous', 'Field', 'Fairy', 'Ditto', 'Dragon', 'Undiscovered']
        self.langlist = ['ENG', 'FRE', 'GER', 'JPN', 'SPN', 'CHA', 'KOR', 'ITA']

        command = "SELECT RegImage, Species, PokedexNumber, PokemonDBID, OTID, Level, Nature, Language, Ability, Shiny FROM (((POKEMON LEFT JOIN POKEDEX ON PokedexNumber=DexNumber) LEFT JOIN EGGGROUP ON PokedexNumber=EGGGROUP.DexNumber) LEFT JOIN CATEGORY ON PokemonDBID=CATEGORY.Poke)"
        
        first = True
        for item in self.textboxes:
            #print(item[0].text())
            if item[0].text() != "":
                if first == True:
                    if item[1] == 'name':
                        command += " WHERE Species=\"" + (str)(item[0].text()) + "\""
                    elif item[1] == 'level':
                        command += " WHERE Level=" + (str)(item[0].text())
                    elif item[1] == 'nature':
                        command += " WHERE Nature=\"" + (str)(item[0].text()) + "\""
                    elif item[1] == 'otid':
                        command += " WHERE OTID=" + (str)(item[0].text())
                    first = False
                else:
                    if item[1] == 'name':
                        command += " AND Species=\"" + (str)(item[0].text()) + "\""
                    elif item[1] == 'level':
                        command += " AND Level=" + (str)(item[0].text())
                    elif item[1] == 'nature':
                        command += " AND Nature=\"" + (str)(item[0].text()) + "\""
                    elif item[1] == 'otid':
                        command += " AND OTID=" + (str)(item[0].text())

        
        pressedbutton = self.categories.checkedId()
        if pressedbutton != -1:
            if first == True:
                command += " WHERE " + self.catlist[pressedbutton][1] + "=1"
                first = False
            else:
                command += " AND " + self.catlist[pressedbutton][1] + "=1"

        pressedbutton = self.eggs.checkedId()
        if pressedbutton != -1:
            if first == True:
                command += " WHERE " + self.egglist[pressedbutton] + "=1"
                first = False
            else:
                command += " AND " + self.egglist[pressedbutton] + "=1"

        pressedbutton = self.languages.checkedId()
        if pressedbutton != -1:
            if first == True:
                command += " WHERE Language=\"" + self.langlist[pressedbutton] + "\""
                first = False
            else:
                command += " AND Language=\"" + self.langlist[pressedbutton] + "\""


        if self.shinybox.isChecked(): 
            if first == True:
                command += " WHERE Shiny=1" 
                first = False
            else:
                command += " AND Shiny=1" 

        #print(self.catlist)
        #print(self.isShiny)
        result = connection.execute(command)
        #print(command)
        for i in range(1, 11):
                thing = TableLabel(self, self.gridlist[i - 1])
                self.grid.addWidget(thing, 1, i, 1, 1)
        i, j = 1, 2

        for row in result:
            i = 1
            plabel = QtWidgets.QLabel(self)

            for item in row:    
                if i == 1:
                    qp = QtGui.QPixmap()
                    #print('ITEM ->>>', item)
                    data = requests.get(item)
                    qp.loadFromData(data.content)
                    plabel.setPixmap(qp.scaled(100, 100))
                    self.grid.addWidget(plabel, j, i, 1, 1)
                else:
                    thing = TableLabel(self, (str)(item))
                    self.grid.addWidget(thing, j, i, 1, 1)
                i += 1
            j += 1

            '''for i in range(1, 11):
                thing = TableLabel(self, self.gridlist[i - 1])
                self.grid.addWidget(thing, 1, i, 1, 1)'''

        connection.close()

class AllWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setup()
    
    def setup(self):
        self.gridlist = ['Image', 'Species', 'DBID', 'Pokedex', 'OTID', 'Level', 'Nature', 'Language', 'Ability', 'Shiny', 'Legal', 'Possess', 'Nickname']
        self.label = QtWidgets.QLabel(self)
        #self.scrolly = QtWidgets.QScrollBar(self)
        self.grid = QtWidgets.QGridLayout()
        engine = create_engine("mysql+pymysql://username:password@database:port/name", echo=False)    
        connection = engine.connect()
        self.setLayout(self.grid)
        self.setGeometry(200, 200, 800, 600)

        result = connection.execute("SELECT * FROM POKEMON")
        i, j = 1, 3
        for row in result:
            i = 1
            plabel = QtWidgets.QLabel(self)
            command = "SELECT RegImage, Species FROM POKEDEX WHERE DexNumber=" + (str)(row[1])
            newresult = connection.execute(command)
    
            for thingy in newresult:
                #print(thingy[0])
                data = requests.get(thingy[0])
                name = (str)(thingy[1])
                break

            qp = QtGui.QPixmap()
            qp.loadFromData(data.content)
            plabel.setPixmap(qp.scaled(100, 100))
            self.grid.addWidget(plabel, j, 1, 1, 1)
            nlabel = QtWidgets.QLabel(self)
            nlabel.setText(name)
            nlabel.resize(nlabel.sizeHint())
            self.grid.addWidget(nlabel, j, 2, 1, 1)
            i += 2
            for item in row:
                thing = TableLabel(self, (str)(item))
                self.grid.addWidget(thing, j, i, 1, 1)
                i += 1
            j += 1

            for i in range(1, 14):
                thing = TableLabel(self, self.gridlist[i - 1])
                self.grid.addWidget(thing, 1, i, 1, 1)
        connection.close()
        self.show()

class SpecificButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Search the Database")
        self.resize(self.sizeHint())
        self.clicked.connect(self.showWindow)

    def showWindow(self):
        self.child = SearchWindow(self)
        self.child.show()

class AddButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Add a Pokemon")
        self.resize(self.sizeHint())
        self.clicked.connect(self.goDude)

    def goDude(self):
        self.child = AddWindow(self)
        self.child.show()

class DropButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Drop a Pokemon")
        self.resize(self.sizeHint())
        self.clicked.connect(self.goDude)

    def goDude(self):
        self.child = DropWindow(self)
        self.child.show()
        #print("It's 4 a.m go to bed")

class GoButton(QtWidgets.QPushButton):
    def __init__(self, parent, textbs, catbuttons, eggbuttons, langs, shiny):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("GO")
        self.resize(self.sizeHint())
        self.daddy = parent
        self.clicked.connect(self.goDude)
        self.textboxes = textbs
        self.categories = catbuttons
        self.eggs = eggbuttons
        self.languages = langs
        self.shinybox = shiny

    def goDude(self):
        '''for item in self.textboxes:
            print(item[0].text())'''
        self.child = ScrollSearch(self.textboxes, self.categories, self.eggs, self.languages, self.shinybox)
        self.child.show()
        #self.daddy.close()

class AllButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("See All Pokemon")
        self.resize(self.sizeHint())
        self.clicked.connect(self.showWindow)

    def showWindow(self):
        self.child = ScrollView()
        self.child.show()

class ExitButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Exit")
        self.resize(self.sizeHint())
        self.clicked.connect(QtWidgets.qApp.quit)

class DatabaseView(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()
    
    def setup(self):
        self.query_btn = AllButton(self)
        self.exit_btn = ExitButton(self)
        self.search_btn = SpecificButton(self)
        self.add_btn = AddButton(self)
        self.drop_btn = DropButton(self)
        self.exit_btn.move(730, 550)
        self.drop_btn.move(580, 550)
        self.query_btn.move(400, 550)
        self.search_btn.move(200, 550)
        self.add_btn.move(50, 550)
        self.label = QtWidgets.QLabel(self)
        self.name = QtWidgets.QLabel(self)
        self.url = "https://img.pokemondb.net/sprites/sun-moon/dex/normal/golisopod.png"
        self.data = requests.get(self.url) 

        self.grid = QtWidgets.QGridLayout()
        self.qp = QtGui.QPixmap()
        self.qp.loadFromData(self.data.content)
        self.label.setPixmap(self.qp.scaled(500, 500))
        #self.grid.addWidget(self.exit_btn, 1, 1, 30, 5)
        self.label.move(150, 0)

if __name__ == "__main__":
    print("Starting App...")

    app = QtWidgets.QApplication(sys.argv)
    main_window = PPTDWindow()
    app.exec()

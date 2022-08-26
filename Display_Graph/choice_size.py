#from msilib.schema import CheckBox
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,QCheckBox, QApplication)
import sys

#class Window(QWidget):
class Window(QDialog):

    # constructeur
    def __init__(self):
        super(Window, self).__init__()

        # taille de la fenêtre
        self.setGeometry(100, 100, 300, 400)

        # Creation d'un groupe d'elem
        self.formGroupBox = QGroupBox("Questions")

        # créer une boite combo pour la taille 1
        self.size1ComboBox = QComboBox()

        # adding items to the combo box
        self.size1ComboBox.addItems(["BTech", "MTech", "PhD"])

        #self.size2ComboBox = QComboBox()

        # creating a line edit
        self.nameLineEdit = QLineEdit()

        # calling the method that create the form
        self.createForm()

        # creating a vertical layout
        mainLayout = QVBoxLayout()
  
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
  
        # setting lay out
        self.setLayout(mainLayout)



    def createForm(self):

        # créer un layout (form)
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Name"), self.nameLineEdit)

        # for degree and adding combo box
        layout.addRow(QLabel("Taille 1"), self.size1ComboBox)

        # setting layout
        self.formGroupBox.setLayout(layout)
    '''
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        radiobutton = QRadioButton("Exécuter le programme sur une taille")
        radiobutton.setChecked(True)
        radiobutton.type = "Onesize"
        radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(radiobutton, 0, 0)

        radiobutton = QRadioButton("Comparer deux tailles différentes")
        radiobutton.type = "Twosize"
        radiobutton.toggled.connect(self.onClicked)
        layout.addWidget(radiobutton, 0, 1)

        
    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("button is: %s" % (radioButton.type))
'''
app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
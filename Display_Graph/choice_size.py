#from msilib.schema import CheckBox
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,QCheckBox, QApplication)
import sys

class Window(QWidget):
#class Window(QDialog):

    # constructeur
    ##def __init__(self):
        ##super(Window, self).__init__()

        # taille de la fenêtre
        ##self.setGeometry(100, 100, 300, 400)

        # Creation d'un groupe d'elem
        ##self.formGroupBox = QGroupBox("Questions")




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

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
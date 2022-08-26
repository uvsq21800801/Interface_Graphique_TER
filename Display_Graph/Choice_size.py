
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,QCheckBox, QApplication)
import sys

class MenuWindow(QMainWindow):
    def __init__(self, min_s, max_s):#, size_min, size_max, matrice_chaleur, occur, recouv):
        super(MenuWindow, self).__init__()
        #self.initUI()

        print(min_s)
        print("hello")

        #def initUI(self):
        
        self.setWindowTitle("My App")
        
        # layout unique pour l'instant
        self.one_lay = QGridLayout()

        # Choix exclusif pour le type de comparaison
        self.one_lay = QGridLayout()
        self.radio_1 = QRadioButton('Une taille avec elle-même')
        self.one_lay.addWidget(self.radio_1, 0, 0)
        self.one_lay.addWidget(QRadioButton('Deux tailles'), 0, 1)
        #self.widg_radio = QWidget()
        #self.widg_radio.setLayout(self.one_lay)

        # Choix multiple pour chaquune des tailles
        # créer une boite combo pour la taille n1
        sizeComboB1 = QComboBox()
        list_1 = ["A sélectionner"]
        size_min = 1
        size_max = 5
        for i in range(size_min,size_max+1):
            list_1.append(str(i))
        sizeComboB1.addItems(list_1)  
        # créer une boite combo pour la taille n2
        sizeComboB2 = QComboBox()
        sizeComboB2.addItems(["A sélectionner"])
        # bouton valider
        vbutt = QPushButton()
        vbutt.setText("Valider")
        vbutt.clicked.connect(self.disp_window)
        # Label erreur
        self.label_err = QLabel(self)
        self.label_err.setText("")
        # ajouter les items dans le layout
        #lay_form = QVBoxLayout()
        self.one_lay.addWidget(sizeComboB1, 1, 0)
        self.one_lay.addWidget(sizeComboB2, 1, 1)
        self.one_lay.addWidget(vbutt, 2, 0)
        self.one_lay.addWidget(self.label_err, 2, 1)
        # entrer le layout dans une widget
        self.one_wigd = QWidget()
        self.one_wigd.setLayout(self.one_lay)
        #widg_form.setLayout(lay_form) 

        #no need ### Concatenate the two layout into the displayed window
        #self.layout_final = QVBoxLayout()
        #self.layout_final.addWidget(self.one_wigd)
        #self.layout_final.addWidget(widg_form)
        
        self.setCentralWidget(self.one_wigd)

        
        
    def disp_window(self):
        print('it worked')
        self.label_err.setText("AAAAAA")
        
def window(min_s, max_s):

    app = QApplication(sys.argv)
    
    win = MenuWindow(min_s, max_s)

    win.show()
    app.exec()
    #sys.exit(app.exec_())




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
        
        self.setWindowTitle("Choix de taille")
        
        # layout unique pour l'instant
        self.one_lay = QGridLayout()

        # Choix de l'interface
        ###
        interf_comb = QComboBox()
        list_interf = ["A sélectionner"]
        interf_min_temp = 1
        interf_max_temp = 5
        for i in range(interf_min_temp,interf_max_temp+1):
            list_interf.append(str(i))
        interf_comb.addItems(list_interf) 

        # Choix de la configuration 
        ###
        conf_comb = QComboBox()
        list_conf = ["A sélectionner"]
        conf_min = 1
        conf_max = 5
        for i in range(conf_min,conf_max+1):
            list_conf.append(str(i))
        conf_comb.addItems(list_conf) 

        # Choix exclusif pour le type de comparaison

        ###
        self.one_lay = QGridLayout()
        self.radio_1 = QRadioButton('Une taille avec elle-même')
        self.radio_2 = QRadioButton('Deux tailles')
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
        
        

        # Numéros d'étapes
        label_et1 = QLabel()
        label_et1.setText("1)")
        label_et2 = QLabel()
        label_et2.setText("2)")
        label_et3 = QLabel()
        label_et3.setText("3)")
        label_et4 = QLabel()
        label_et4.setText("4)")
        label_et5 = QLabel()
        label_et5.setText("5)")
        
        # Ajout des numéros d'étapes
        self.one_lay.addWidget(label_et1,1,0)
        self.one_lay.addWidget(label_et2,3,0)
        self.one_lay.addWidget(label_et3,5,0)
        self.one_lay.addWidget(label_et4,7,0)
        self.one_lay.addWidget(label_et5,10,0)

        # labels
        interf_label = QLabel()
        interf_label.setText("Choisissez le nom d'interface:")
        conf_label = QLabel()
        conf_label.setText("Choisissez le numéro de configuration:")
        choix_type_label = QLabel()
        choix_type_label.setText("Choisissez le type de comparaison:")
        choix_tailles_label = QLabel()
        choix_tailles_label.setText("Choisissez la/les tailles:")
        choix_taille_1 = QLabel()
        choix_taille_1.setText("Taille 1")
        choix_taille_2 = QLabel()
        choix_taille_2.setText("Taille 2")

        # ajout des labels
        self.one_lay.addWidget(interf_label, 1,1)
        self.one_lay.addWidget(conf_label, 3,1)
        self.one_lay.addWidget(choix_type_label,5,1)
        self.one_lay.addWidget(choix_tailles_label,7,1)
        self.one_lay.addWidget(choix_taille_1,8,1)
        self.one_lay.addWidget(choix_taille_2,8,2)

        ## ajouter les items dans le layout
        # ajout des labels et item interactifs
        self.one_lay.addWidget(interf_comb, 2, 1)
        self.one_lay.addWidget(conf_comb, 4,1)
        self.one_lay.addWidget(self.radio_1, 6, 1)
        self.one_lay.addWidget(self.radio_2, 6, 2)
        self.one_lay.addWidget(sizeComboB1, 9, 1)
        self.one_lay.addWidget(sizeComboB2, 9, 2)
        self.one_lay.addWidget(vbutt, 10, 1)
        self.one_lay.addWidget(self.label_err, 10, 2)
        #
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



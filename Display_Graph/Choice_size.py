
from traceback import print_tb
from PyQt5.QtWidgets import *
#from PyQt5 import QtCore, QtGui
#from PyQt5.QtGui import * 
#from PyQt5.QtCore import *
#from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout,QCheckBox, QApplication)
import sys
from Inputs import Database_create as DbC
#from Display_Graph import Database_functs as DbC
from bson.objectid import ObjectId

from Display_Graph import Clickable_display

class MenuWindow(QMainWindow):
    def __init__(self):
        super(MenuWindow, self).__init__()
        self.setWindowTitle("Choix de taille")
        
        # init BDD
        ##### CONNECTION A LA BDD
        client = DbC.connect_mongodb()
        if client == None :
            print("Fermeture du programme")
            return 1
        self.db = client.graphetarium2

        # layout unique pour l'instant
        self.one_lay = QGridLayout()

        # Choix de l'interface
        temp = self.db.structures.aggregate([])
        iterable_structures = ["A sélectionner"]
        for t in temp:
            iterable_structures.append(t["name"])
        print(iterable_structures)

        self.combo_interf = QComboBox()
        self.combo_interf.addItems(iterable_structures) 

        # Choix de la configuration 
        iterable_conf = self.db.configurations.aggregate([])
        self.combo_conf = QComboBox()
        list_conf = ["A sélectionner"]
        self.combo_conf.addItems(list_conf) 

        # Choix exclusif pour le type de comparaison

        ###
        self.one_lay = QGridLayout()
        self.radio_1 = QRadioButton('Une taille avec elle-même')
        self.radio_2 = QRadioButton('Deux tailles')
        #self.widg_radio = QWidget()
        #self.widg_radio.setLayout(self.one_lay)

        # Choix multiple pour chaquune des tailles
        # créer une boite combo pour la taille n1
        self.sizeComboB1 = QComboBox()
        list_1 = ["A sélectionner"]
        size_min = 1
        size_max = 5
        for i in range(size_min,size_max+1):
            list_1.append(str(i))
        self.sizeComboB1.addItems(list_1)  
        # créer une boite combo pour la taille n2
        self.sizeComboB2 = QComboBox()
        self.sizeComboB2.addItems(["A sélectionner"])
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
        self.one_lay.addWidget(self.combo_interf, 2, 1)
        self.one_lay.addWidget(self.combo_conf, 4,1)
        self.one_lay.addWidget(self.radio_1, 6, 1)
        self.one_lay.addWidget(self.radio_2, 6, 2)
        self.one_lay.addWidget(self.sizeComboB1, 9, 1)
        self.one_lay.addWidget(self.sizeComboB2, 9, 2)
        self.one_lay.addWidget(vbutt, 10, 1)
        self.one_lay.addWidget(self.label_err, 10, 2)
        #

        # events
        self.combo_interf.activated.connect(self.change_config_choices)
        self.combo_conf.activated.connect(self.update_size_1)
        self.sizeComboB1.activated.connect(self.update_size_2)
        self.radio_1.toggled.connect(self.toggle_type_of_search)
        self.radio_2.toggled.connect(self.toggle_type_of_search)
        self.sizeComboB2.setDisabled(True)
        vbutt.clicked.connect(self.validate)


        #self.sizeComboB1.activated.connect
        #self.sizeComboB2.activated.connect

        # entrer le layout dans une widget
        self.one_wigd = QWidget()
        self.one_wigd.setLayout(self.one_lay)
        #widg_form.setLayout(lay_form) 

        #no need ### Concatenate the two layout into the displayed window
        #self.layout_final = QVBoxLayout()
        #self.layout_final.addWidget(self.one_wigd)
        #self.layout_final.addWidget(widg_form)
        
        self.setCentralWidget(self.one_wigd)

        

    def change_config_choices(self):
        # Interface choisie par l'utilisateur 
        selected = self.combo_interf.currentText()
        # On retrouve l'id de l'interface pour sortir les config associées
        self.structure_id = self.db.structures.find_one({"name":selected})
        self.structure_id = self.structure_id["_id"]
        
        # recherche des configurations qui matchent l'identifiant de la structure choisie
        temp = self.db.configurations.aggregate([
            {"$match": {"struct": ObjectId(self.structure_id)}}
        ])
        # création de la nouvelle liste de num de configurations
        iterable_conf = ["A sélectionner"]
        for t in temp:
            iterable_conf.append(str(t['number']))
        
        # ajout des configurations dans la combo box
        self.combo_conf.clear()
        self.combo_conf.addItems(iterable_conf)
        #self.label_err.setText("")

    def toggle_type_of_search(self):
        r1 = self.radio_1.isChecked()
        r2 = self.radio_2.isChecked()
        
        # verif si on peut lock/unlock t2
        if r1:
            self.sizeComboB2.setDisabled(True)
        if r2:
            self.sizeComboB2.setDisabled(False)            

    def update_size_1(self):
        # configuration choisie par l'utilisateur
        conf = self.combo_conf.currentText()
        selected = self.combo_interf.currentText()

        sizes = self.db.configurations.find_one({"struct":ObjectId(self.structure_id), "number":int(conf)})
        sizes = sizes["sizes"]
        #print(conf_id)

        self.t1 = ["A sélectionner"]
        for s in sizes:
            self.t1.append(str(s))
        self.sizeComboB1.clear()
        self.sizeComboB1.addItems(self.t1)

        #pain = self.db.configurations.aggregate([])
        #for i in pain:
            #print(i) 

    def update_size_2(self):
        t2 = self.t1.copy()
        if (self.sizeComboB1.currentText() != "A sélectionner"):
            t2.remove(self.sizeComboB1.currentText())
        self.sizeComboB2.clear()
        self.sizeComboB2.addItems(t2)

    def validate(self):
        interf = self.combo_interf.currentText()
        conf = self.combo_conf.currentText()
        t1 = self.sizeComboB1.currentText()
        t2 = self.sizeComboB2.currentText()
        r1 = self.radio_1.isChecked()
        r2 = self.radio_2.isChecked()

        cdt = "A sélectionner"
        
        # appel de la nouvelle fenêtre
        self.w = Clickable_display.InteractiveWindow(parent=self)
        self.w.show()

        if t1 != cdt and interf != cdt and conf != cdt: 
            if r2 and t2 != cdt:
                print("call nice windowo 2")
            if r1:
                print("call nice windowo 1")
        


    def update_sizes(self): #trash
        conf = self.combo_conf.currentText()
        t1 = self.sizeComboB1.currentText()
        t2 = self.sizeComboB2.currentText()
        r1 = self.radio_1.isChecked()
        r2 = self.radio_2.isChecked()
        
        # verif si on peut lock/unlock t2
        if r1:
            self.sizeComboB2.setDisabled(True)
        if r2:
            self.sizeComboB2.setDisabled(False)            

        # cas où aucune config n'est choisie
        if conf == "A sélectionner":
            self.label_err.setText("Veuillez choisir une configuration.")
        # cas où aucune taille n'est choisie 
        elif not r1 and not r2:
            self.label_err.setText("Veuillez choisir la/les taille(s).")
        # cas où t2 n'est pas remplie mais r2 est cochée
        if t2 == "A sélectionner" and r2:
            self.label_err.setText("Veuillez choisir une seconde taille.")

        

    def disp_window(self):
        print('it worked')
        self.label_err.setText("AAAAAA")
        
def window():

    app = QApplication(sys.argv)
    
    win = MenuWindow()

    win.show()
    app.exec()
    #sys.exit(app.exec_())



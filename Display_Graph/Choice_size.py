
from ctypes import Structure
from lzma import is_check_supported
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
from Interfaces import Select_process as Sp
#from Interfaces import Study_process as Study

# pas encore utilisé
'''
class db_ids:
    def __init__(self):
        self.structure_id = ""
        self.coloration_id = ""
        self.configuration_dict = {}
        self.motif_spe_id = ""
'''

from Interfaces import Final_process as Fp

class MenuWindow(QMainWindow):
    def __init__(self):
        super(MenuWindow, self).__init__()
        self.setWindowTitle("Choix de taille")
        
        # les options pour certaines fonctions:
        #      0 : Hydrogène conservé?
        #      1 : Tailles traitées
        #      2 : Type de Similarité
        #      3 : Motif spécifique?
        self.options = [False, 0, 0, False]
        # Misc/initialisation de structures de transfert
        # les identifiants de la BDD (format _id)
        #      0 : structure (_id)
        #      1 : coloration (_id)
        #      2 : configuration (dict{_id})
        #      3 : motif spécifique (_id)
        self.db_ids = ["", "", {}, ""]
        # les noms dans la BDD (format str)
        #      0 : structure (name)
        #      1 : coloration (name)
        #      2 : configuration ([number])
        #      3 : motif spécifique (sign)
        self.db_names = ["", "", [], 0]
        
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
        self.dict_struct_name_id = {} 
        for t in temp:
            iterable_structures.append(t["name"])
            ## insert entry to dict here
            self.dict_struct_name_id[str(t["name"])] = str(t["_id"])
        #print(iterable_structures)
        #print(self.dict_struct_name_id)

        self.combo_interf = QComboBox()
        self.combo_interf.addItems(iterable_structures) 

        # Choix de la coloration
        self.combo_color = QComboBox()
        self.list_color = ["A sélectionner"]
        self.combo_color.addItems(self.list_color)

        # Choix de la configuration 
        iterable_conf = self.db.configurations.aggregate([])
        self.dict_conf_name_id = {} 
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
        vbutt.clicked.connect(self.change_err_msg)
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
        label_et6 = QLabel()
        label_et6.setText("6)")
        
        # Ajout des numéros d'étapes
        self.one_lay.addWidget(label_et1,1,0)
        self.one_lay.addWidget(label_et2,3,0)
        self.one_lay.addWidget(label_et3,5,0)
        self.one_lay.addWidget(label_et4,7,0)
        self.one_lay.addWidget(label_et5,9,0)
        self.one_lay.addWidget(label_et6,12,0)

        # labels
        interf_label = QLabel()
        interf_label.setText("Choisissez le nom d'interface:")
        color_label = QLabel()
        color_label.setText("Choisissez la coloration:")
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
        self.one_lay.addWidget(color_label,3, 1)
        self.one_lay.addWidget(conf_label, 5,1)
        self.one_lay.addWidget(choix_type_label,7,1)
        self.one_lay.addWidget(choix_tailles_label,9,1)
        self.one_lay.addWidget(choix_taille_1,10,1)
        self.one_lay.addWidget(choix_taille_2,10,2)

        ## ajouter les items dans le layout
        # ajout des labels et item interactifs
        self.one_lay.addWidget(self.combo_interf, 2, 1)
        self.one_lay.addWidget(self.combo_color, 4, 1)
        self.one_lay.addWidget(self.combo_conf, 6,1)
        self.one_lay.addWidget(self.radio_1, 8, 1)
        self.one_lay.addWidget(self.radio_2, 8, 2)
        self.one_lay.addWidget(self.sizeComboB1, 11, 1)
        self.one_lay.addWidget(self.sizeComboB2, 11, 2)
        self.one_lay.addWidget(vbutt, 12, 1)
        self.one_lay.addWidget(self.label_err, 12, 2)

        # events
        self.combo_interf.activated.connect(self.change_color_choices)
        self.combo_color.activated.connect(self.change_config_choices)
        self.combo_conf.activated.connect(self.update_size_1)
        self.sizeComboB1.activated.connect(self.update_size_2)
        self.radio_1.toggled.connect(self.toggle_type_of_search)
        self.radio_2.toggled.connect(self.toggle_type_of_search)
        self.sizeComboB2.setDisabled(True)
        vbutt.clicked.connect(self.validate)

        # entrer le layout dans une widget
        self.one_wigd = QWidget()
        self.one_wigd.setLayout(self.one_lay)
        
        self.setCentralWidget(self.one_wigd)

        

    def change_color_choices(self):
        # Interface choisie par l'utilisateur 
        selected = self.combo_interf.currentText()
        # On retrouve l'id de l'interface pour sortir les config associées
        self.structure_id = self.db.structures.find_one({"name":selected})
        self.structure_id = self.structure_id["_id"]

        # recherche des coloration qui matchent l'identifiant de la structure
        #temp = self.db.colorations#.aggregate#([
            #{"$match": {"struct": ObjectId(self.structure_id)}}
        #])
        self.list_color = ["A sélectionner"]
        for result in self.db.colorations.find():
            self.list_color.append(result['name'])

        self.combo_color.clear()
        self.combo_color.addItems(self.list_color)


    def change_config_choices(self):
        # couleur choisie par l'utilisateur
        selected = self.combo_color.currentText()
        # On retrouve l'id de la couleur pour sortir les config associées
        self.color_id = self.db.colorations.find_one({"name":selected})
        self.color_id = self.color_id["_id"]

        # recherche des configurations qui matchent l'identifiant de 
        # la structure et de la couleur choisie
        temp = self.db.configurations.aggregate([
            {"$match": {"struct": ObjectId(self.structure_id),"color": ObjectId(self.color_id)}}
        ])
        # création de la nouvelle liste de num de configurations
        self.dict_conf_name_id = {} 
        iterable_conf = ["A sélectionner"]
        for t in temp:
            iterable_conf.append(str(t['number']))
            self.dict_conf_name_id[str(t["number"])] = str(t["_id"])
        
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

        self.t1 = ["A sélectionner"]
        for s in sizes:
            self.t1.append(str(s))
        self.sizeComboB1.clear()
        self.sizeComboB1.addItems(self.t1)

        # temporairement ici
        self.label_err.setText("Regardez le terminal après validation")

    def update_size_2(self):
        t2 = self.t1.copy()
        if (self.sizeComboB1.currentText() != "A sélectionner"):
            t2.remove(self.sizeComboB1.currentText())
        self.sizeComboB2.clear()
        self.sizeComboB2.addItems(t2)

    def validate(self):
        # obselete?
        self.send_interf = self.combo_interf.currentText()
        self.send_conf = self.combo_conf.currentText()
        self.send_r1 = self.radio_1.isChecked()
        self.send_r2 = self.radio_2.isChecked()
        # fin obselete?

        #need error loop
        
        self.db_ids[0] = self.dict_struct_name_id[str(self.combo_interf.currentText())]
        self.db_ids[1] = ObjectId(str(self.color_id))
        self.db_ids[2] = ObjectId(self.dict_conf_name_id[str(self.combo_conf.currentText())])
        self.db_names[0] = str(self.combo_interf.currentText())
        self.db_names[1] = str(self.combo_color.currentText())
        self.db_names[2] = int(self.combo_conf.currentText())
        self.taille1 = self.sizeComboB1.currentText()
        if self.radio_2.isChecked():
            self.taille2 = self.sizeComboB2.currentText()
        else:
            self.taille2 = self.sizeComboB1.currentText()
        
        # cribles à ajouter quand j'aurais le temps

        # pour l'instant, le terminal sera utilisé pour la gestion des cribles
        #lst_color = Di.insert_color(self.db.colorations, self.db_ids, db_names, options)
        #lst_color = self.list_color
        #lst_color.remove("A sélectionner")
        lst_color = self.db.colorations.find_one({"_id":self.db_ids[1]})
        lst_color = lst_color["elements"]

        self.lst_motifs1 = Sp.test_filter(self.db, self.db_ids, int(self.sizeComboB1.currentText()), lst_color)
        if self.radio_1.isChecked():
            self.lst_motifs2 = self.lst_motifs1.copy()
        else:
            self.lst_motifs2 = Sp.test_filter(self.db, self.db_ids, int(self.sizeComboB2.currentText()), lst_color)
            
        # Nombre de comparaison à faire et test des longueurs des listes
        nb_comp = 0
        if self.radio_2.isChecked(): # = plusieurs tailles
        #if Multi_size :
            if len(self.lst_motifs1) == 0 or len(self.lst_motifs2) == 0:
                test = True
                print("Une liste est vide.")
            else :
                nb_comp = len(self.lst_motifs1)*len(self.lst_motifs2)
        else :
            if len(self.lst_motifs1) == 0:
                test = True
                print("La liste est vide.")
            else :
                nb_comp = len(self.lst_motifs1)*(len(self.lst_motifs1)-1)
                nb_comp = nb_comp/2
        print("Il y a jusqu'à "+str(int(nb_comp))+" comparaisons à analyser.")

        # choix du type de simmilarité (à retirer le 0, aucune sim)
        self.options[2] = Sp.select_metric()

        ## Formation des distributions
        self.tab_res = [None, None]
        # Choix du filtre (Une ou plusieurs config)
        pipeline = Fp.unique_config(self.db_ids[0], self.db_ids[1], self.db_ids[2])
        # Construction des distributions
        if self.radio_2.isChecked(): # = plusieurs tailles
            self.tab_res[0], self.tab_res[1] = Fp.construct_2tab(self.db, pipeline, self.lst_motifs1, self.lst_motifs2)
            if len(self.tab_res[0]) == 0 or len(self.tab_res[1]) == 0:
                test = True
                if len(self.tab_res[0])==0:
                    print("Aucun motif de taille "+str(self.taille1)+" sélectionné.")
                if len(self.tab_res[1])==0:
                    print("Aucun motif de taille "+str(self.taille2)+" sélectionné.")
            else :
                print("Il y a "+str(len(self.tab_res[0]))+" et "+str(len(self.tab_res[1]))+ " motifs étudiés.")
        else :
            self.tab_res[0] = Fp.construct_1tab(self.db, pipeline, self.lst_motifs1)
            if len(self.tab_res[0]) == 0:
                test = True
                print("Aucun motif de taille "+str(self.taille1)+" sélectionné.")
            else :
                print("Il y a "+str(len(self.tab_res[0]))+ " motifs étudiés.")

        # appel de la nouvelle fenêtre
        self.w = Clickable_display.InteractiveWindow(parent=self)
        self.w.show()

        # gestion d'erreur (pas encore fait)
        cdt = "A sélectionner"
        #if self.send_t1 != cdt and self.send_interf != cdt and self.send_conf != cdt: 
            


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

        

    def change_err_msg(self):
        
        self.label_err.setText("Regardez le terminal après validation")
        
def window():

    app = QApplication(sys.argv)
    
    win = MenuWindow()

    win.show()
    app.exec()
    #sys.exit(app.exec_())



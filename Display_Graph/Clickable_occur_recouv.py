from curses.ascii import isdigit
from re import X
import telnetlib
from turtle import update
from PyQt5.QtWidgets import *
import sys
from Display_Graph import Smart_Display

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backend_bases import MouseButton
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import numpy as np

import pyximport
pyximport.install()
from Outputs import Graphic_draw as Gd
import matplotlib.colors as clr
import matplotlib.colorbar as colorbar
from Outputs.texture import *

from Interfaces import Final_process as Fp

from PyQt5.QtGui import QPixmap
from Outputs import Graphlet_draw as Gld
from bson.objectid import ObjectId
from bson.binary import Binary
from io import BytesIO
from PIL import Image

import os
import os.path
from os import path

temp_x = 0
x = 'not a float, ce texte vérifie que user a bien choisi une case de la mat de chaleur'
text_x = ' '
t_x = ' '
lst_obj_id_x = []
plot_heatmap = ' '
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent, width=13, height=8, dpi=130):
        
        self.parent = parent
        self.parent.x = 0
        
        # Formation des distributions
        pointer = {'x':None, 'y':None}
        listOfGlobals = globals()
        listOfGlobals['lst_obj_id_x'] = []
        for r in self.parent.parent.tab_res[0]:
            listOfGlobals['lst_obj_id_x'].append(r[3])

        lst_id_x, lst_occ_x, lst_cover_x = split_tab_res_no_file(
                self.parent.parent.tab_res[0], self.parent.parent.options[3], 
                self.parent.parent.db_ids[3], pointer, ['x'])
        
        # positionnement des min et max pour normaliser le gradien de couleurs
        cm = plt.cm.get_cmap(colormap)
        
        # Figures :
        plt.clf()
        fig, axbar = plt.subplots() 
        fig.set_size_inches(13,8)
        super(MplCanvas, self).__init__(fig)
        
        # Dessins
        Gd.xbar(axbar, lst_id_x, lst_occ_x, lst_cover_x, cm, pointer)
        # texte
        listOfGlobals = globals()
        plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event',on_click)

def on_click(event):
    if event.inaxes is None:
        print("is not in ax")

    listOfGlobals = globals()
    listOfGlobals['x'] = temp_x
    
    print('choix du motif d\'indice %d' % (int(x.round())))
    
    if listOfGlobals['plot_heatmap'] == event.inaxes:
        print ("Click is in axes plot_heatmap")

def on_move(event):
# get the x and y pixel coords
    listOfGlobals = globals()
    listOfGlobals['temp_x'] = event.xdata
    if event.inaxes:
        ax = event.inaxes  # the axes instance

class InteractiveWindow(QMainWindow):
    def __init__(self, parent):
        self.parent = parent
        super(InteractiveWindow, self).__init__()
        self.setWindowTitle("Affichage interactif")
        
        # taille de fenetre
        self.setFixedSize(1600,750)
        
        # definition du layout horizontal
        # il englobera en deux parties, l'affichage matplotlib et les motifs
        self.lay_H = QHBoxLayout()
        
        # layout vertical pour matplotlib et le bouton de confirmation
        self.lay_matplot = QVBoxLayout()

        # definition du layout vertical, il englobe l'affichage des 
        # motifs selectionnés
        self.lay_V_motifs = QVBoxLayout()

        ### Affichage matplotlib ###
      
        # copier coller test
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=13, height=9, dpi=130)
        
        # ajout de l'affichage matplotlib
        self.lay_matplot.addWidget(sc)
    
        # bouton valider le choix des indices pour l'affichage des graphlet et 
        # du mcis
        vbutt = QPushButton()
        vbutt.setText("Valider")
        self.lay_matplot.addWidget(vbutt)
        vbutt.clicked.connect(self.validate)
        
        # ajout du layout matplotlib et V au layout horizontal
        self.lay_H.addLayout(self.lay_matplot)
        self.lay_H.addLayout(self.lay_V_motifs)

        # création des labels textes
        # taille 1
        self.label_abs_text = QLabel()
        self.label_abs_text.setText("Motif numéro: ")
        self.label_abs = QLabel()
        self.img_1 = QPixmap('t1.png')
        self.label_abs.setPixmap(self.img_1)
        
        # construction du layout pour motifs
        # abs = première taille selectionnée par l'utilisateur 
        self.lay_V_motifs.addWidget(self.label_abs_text)
        self.lay_V_motifs.addWidget(self.label_abs)
        
        # entrer le layout dans une widget
        self.one_wigd = QWidget()
        self.one_wigd.setLayout(self.lay_H)

        self.setCentralWidget(self.one_wigd)


    def validate(self):
        try:
                    
            print('Afficher le motif d\'indice %d' % (int(x.round())))
            
            # tables
            colors = self.parent.db.colorations
            motifs = self.parent.db.motifs

            listOfGlobals = globals()
            ## récupération de l'id du motif
            id_motif_x = listOfGlobals['lst_obj_id_x'][int(x.round())]
            
            ###### motif X
            # demande l'ObjectId du motif sur la BDD
            while (
                not ObjectId.is_valid(id_motif_x)
                or motifs.count_documents({"_id": ObjectId(id_motif_x)}) == 0
            ):
                id_motif_x = input(str(id_motif_x) + " n'exites pas. Autre id : ")
            motif = motifs.find_one({"_id": ObjectId(id_motif_x)})
            if "img" in motif.keys():
                im = Image.open(BytesIO(motif["img"]))
                im.show()
                
                # Au cas ou le chemin n'existe pas, crée le chemin 
                if (not path.exists("Outputs/Place_Output_here/motifs")):
                    os.makedirs("Outputs/Place_Output_here/motifs")

                im.save("Outputs/Place_Output_here/motifs/draw_"+str(id_motif_x)+".png")
                
            else:
                color_id = motif["color"]
                lst_vertex = list(motif["lst_v"])
                lst_bonds = list(motif["lst_b"])
                
                color = colors.find_one({"_id":ObjectId(color_id)})
                lst_elem = list(color["elements"])
                
                Gld.draw_graphlet(id_motif_x, lst_vertex, lst_bonds, lst_elem)
                data = open("Outputs/Place_Output_here/motifs/draw_" + str(id_motif_x) + ".png", mode='rb').read()
                motifs.find_one_and_update({'_id':ObjectId(id_motif_x)},{"$set":{'img': Binary(data)}})
            
            print("dessin sauvegardé dans Outputs/Place_Output_here/motifs/draw_"+str(id_motif_x)+".png")
            # update l'image du motif 1
            self.label_abs.setPixmap(QPixmap("Outputs/Place_Output_here/motifs/draw_"+str(id_motif_x)+".png")
                    .scaled(600,400))
            self.label_abs_text.setText("Motif numéro: "+str(int(x.round())))
           
            
        except ValueError:
            print('veuillez cliquer une case de la matrice de chaleur')
    

# Sépare les informations dans des listes différentes
def split_tab_res_no_file (tab_res, cible, motif_id, pointer, axis):
    # pour les indices des la liste (trié au préalable)
    plot_index = []
    plot_occur = []
    plot_cover = []
    i = 0
    for tmp in tab_res:
        # récupère les stats
        for a in axis :
            if cible and tmp[3] == motif_id:
                pointer[a] = int(i)
        plot_index.append(int(i))
        plot_occur.append(int(tmp[0]))
        plot_cover.append(float(tmp[1]))
        i += 1
    index = np.array(plot_index, dtype="i")
    occur = np.array(plot_occur, dtype="i")
    cover = np.array(plot_cover, dtype="f")
    return index, occur, cover
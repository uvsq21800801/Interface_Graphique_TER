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
temp_y = 0
x = 'not a float, ce texte vérifie que user a bien choisi une case de la mat de chaleur'
y = 'not a float, ce texte vérifie que user a bien choisi une case de la mat de chaleur'
text_x = ' '
text_y = ' '
t_x = ' '
t_y = ' '
lst_obj_id_x = []
lst_obj_id_y = []
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent, width=5, height=4, dpi=100):
        
        self.parent = parent
        self.parent.x = 0
        self.parent.y = 0
        
        ### def draw_result_2size(dir_O, name, tab_size, tab_res, cible, motif_id, tab_sim, num_type):
        # init values

        ### tentative d'ajouter les listes directement depuis la bdd
        
        print("self.parent.parent.taille1")
        print(self.parent.parent.taille1)
        print("self.parent.parent.taille2")
        print(self.parent.parent.taille2)

        # Formation des distributions
        #tab_res = [None, None]
        #pipeline = Fp.unique_config(self.parent.parent.db_ids[0], 
        #        self.parent.parent.db_ids[1], self.parent.parent.db_ids[2])
        #tab_res[0] = Fp.construct_1tab(self.parent.parent.db, pipeline, lst_motifs)
        pointer = {'x':None, 'y':None}
        listOfGlobals = globals()
        listOfGlobals['lst_obj_id_x'] = []
        for r in self.parent.parent.tab_res[0]:
            listOfGlobals['lst_obj_id_x'].append(r[3])

        lst_id_x, lst_occ_x, lst_cover_x = split_tab_res_no_file(
                self.parent.parent.tab_res[0], self.parent.parent.options[3], 
                self.parent.parent.db_ids[3], pointer, ['x'])
        if self.parent.parent.taille1 != self.parent.parent.taille2:
            listOfGlobals['lst_obj_id_y'] = []
            for r in self.parent.parent.tab_res[1]:
                listOfGlobals['lst_obj_id_y'].append(r[3])
            
            lst_id_y, lst_occ_y, lst_cover_y = split_tab_res_no_file(
                    self.parent.parent.tab_res[1], self.parent.parent.options[3], 
                    self.parent.parent.db_ids[3], pointer, ['y'])
        else:
            lst_id_y, lst_occ_y, lst_cover_y = split_tab_res_no_file(
                self.parent.parent.tab_res[0], self.parent.parent.options[3], 
                self.parent.parent.db_ids[3], pointer, ['x'])
            listOfGlobals['lst_obj_id_y'] = listOfGlobals['lst_obj_id_x'].copy()

        print('self.parent.parent.tab_res[0]')
        print(self.parent.parent.tab_res[0])
        print('self.parent.parent.options[3]')
        print(self.parent.parent.options[3])
        
        
        # Valeurs :
        lenght = max(len(lst_id_y), len(lst_id_x))
        step = int(lenght / 20) + 1
        # positionnement des min et max pour normaliser le gradien de couleurs
        norm = clr.Normalize(vmin=0, vmax=1)
        #norm = clr.Normalize(vmin=min(lst_sim), vmax=max(lst_sim))
        cm = plt.cm.get_cmap(colormap)
        # Répartition des espaces
        ratio_x = max(2, len(lst_id_x)/15)
        ratio_y = max(2, len(lst_id_y)/15)
        ratio_ext = max(1, lenght/40)
        fontsize = max(8, (lenght/5))
        
        if self.parent.parent.taille1 != self.parent.parent.taille2:
            tab_sim = Fp.construct_matrix_2g(self.parent.parent.db, 
                    int(self.parent.parent.options[2]),
                    self.parent.parent.tab_res[0], self.parent.parent.tab_res[1])
        else:
            tab_sim = Fp.construct_matrix_1g(self.parent.parent.db, 
                    int(self.parent.parent.options[2]),
                    self.parent.parent.tab_res[0])

        #print('tab_sim')
        #print(tab_sim)
        lst_sim, tab_sim = Gd.analyse_simil(tab_sim, self.parent.parent.options[2], 2)
        #print('tab_sim')
        
        #print(tab_sim)
        #print('lst_sim')
        
        #print(lst_sim)
        print('lst_id_x')
        print(lst_id_x)
        print('lst_id_y')
        print(lst_id_y)

        # Figures :
        plt.clf()
        fig = plt.figure(figsize = (1.5*(ratio_x+ratio_ext)+10,1.5*(ratio_y+ratio_ext)+10))#, constrained_layout=True)
        super(MplCanvas, self).__init__(fig)
        gs = fig.add_gridspec(2, 4, width_ratios = (ratio_ext,ratio_x,0.1,0.5), height_ratios = (ratio_ext,ratio_y), left=0.05, right=0.95, bottom=0.05, top=0.95)#, hspace=0.25, wspace=0.25) #
        ax_hm = fig.add_subplot(gs[1,1])
        axbar = fig.add_subplot(gs[0,1], sharex=ax_hm)
        aybar = fig.add_subplot(gs[1,0], sharey=ax_hm)
        ax_hist_sim = fig.add_subplot(gs[0,0])
        ax_colorbar = fig.add_subplot(gs[1,2])
        ax_text = fig.add_subplot(gs[0,2]) #### work here
        # Dessins
        Gd.xbar(axbar, lst_id_x, lst_occ_x, lst_cover_x, cm, pointer)
        Gd.ybar(aybar, lst_id_y, lst_occ_y, lst_cover_y, cm, pointer)
        Gd.heatmap(ax_hm, tab_sim, lst_id_x, lst_id_y, lenght, step, norm, cm, pointer)
        cbar = colorbar.Colorbar(ax=ax_colorbar, mappable=None, cmap=cm, norm=norm)
        Gd.sim_hist(ax_hist_sim, lst_sim, cm)
        # texte
        ax_text.axis([0, 10, 0, 10])
        ax_text.text(1, 8, 'Indice des abscices choisi:', fontsize=8)
        listOfGlobals = globals()
        listOfGlobals['t_x'] = ax_text.text(1, 6, 'Lire dans le terminal'+str(text_x), style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        ax_text.text(1, 4, 'Indice des ordonées choisi:', fontsize=8)
        listOfGlobals['t_y'] = ax_text.text(1, 2, 'Lire dans le terminal'+str(text_y), style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        ax_text.axis('off')
        plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event',smarter_on_click)
        #binding_id = plt.connect('button_press_event', on_click)
    
def smarter_on_click(event):
    listOfGlobals = globals()
    listOfGlobals['x'] = temp_x
    listOfGlobals['y'] = temp_y
    listOfGlobals['t_x'].set_text(str(temp_x))
    listOfGlobals['t_y'].set_text(str(temp_y))
    #print('indices selectionnés %f %f' % (x.round(),y.round()))
    print('choix des motifs d\'indices %d et %d' % (int(x.round()),int(y.round())))
            

def on_click(event):
    listOfGlobals = globals()
    listOfGlobals['x'] = temp_x
    listOfGlobals['y'] = temp_y
    #t_x.set_text(str(temp_x))
    #t_y.set_text(str(temp_y))
    print('indices selectionnés %f %f' % (x.round(),y.round()))
def on_move(event):
# get the x and y pixel coords
    listOfGlobals = globals()
    listOfGlobals['temp_x'] = event.xdata
    listOfGlobals['temp_y'] = event.ydata
    if event.inaxes:
        ax = event.inaxes  # the axes instance
        #print('data coords %f %f' % (event.xdata, event.ydata))
        #print('onmove %d %d' % (event.xdata.round(), event.ydata.round()))



class InteractiveWindow(QMainWindow):
    def __init__(self, parent):
        self.parent = parent
        super(InteractiveWindow, self).__init__()
        print(self.parent.combo_interf.currentText())
        self.setWindowTitle("Affichage interactif")
        

        #Smart_Display.One_size()
        
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
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        
        # ajout de l'affichage matplotlib
        self.lay_matplot.addWidget(sc)
        #self.lay_H.addWidget(sc)
        # bouton valider le choix des indices pour l'affichage des graphlet et 
        # du mcis
        vbutt = QPushButton()
        vbutt.setText("Valider")
        self.lay_matplot.addWidget(vbutt)
        vbutt.clicked.connect(self.validate)
        #

        
        # ajout du layout matplotlib et V au layout horizontal
        self.lay_H.addLayout(self.lay_matplot)
        self.lay_H.addLayout(self.lay_V_motifs)

        # création des labels textes
        self.label_abs = QLabel()
        self.label_abs.setText("Motif numéro: ")
        self.img_1 = QPixmap('t1.png')
        self.label_abs.setPixmap(self.img_1)
        self.label_mcis = QLabel()
        self.label_mcis.setText("MCIS obtenu: ")
        self.img_mcis = QPixmap('MCIS.png')
        self.label_mcis.setPixmap(self.img_mcis)
        self.label_ord = QLabel()
        self.label_ord.setText("Motif numéro: ")
        self.img_2 = QPixmap('t2.png')
        self.label_ord.setPixmap(self.img_2)
        # 

        # construction du layout pour motifs
        self.lay_V_motifs.addWidget(self.label_abs)
        # jpeg
        #self.lay_V_motifs.addWidget(self.img_1)
        self.lay_V_motifs.addWidget(self.label_mcis)
        # jpeg
        #self.lay_V_motifs.addWidget(self.img_mcis)
        self.lay_V_motifs.addWidget(self.label_ord)
        # jpeg
        #self.lay_V_motifs.addWidget(self.img_2)


        # entrer le layout dans une widget
        self.one_wigd = QWidget()
        self.one_wigd.setLayout(self.lay_H)

        self.setCentralWidget(self.one_wigd)


    def validate(self):
        try:
                    
            print('Afficher les motifs des indices %d et %d' % (int(x.round()),int(y.round())))
            
            # tables
            colors = self.parent.db.colorations
            motifs = self.parent.db.motifs

            listOfGlobals = globals()
            print('listOfGlobals[\'lst_obj_id_x\'\]\'')
            print(listOfGlobals['lst_obj_id_x'])
            ## récupération de l'id du motif
            id_motif_x = listOfGlobals['lst_obj_id_x'][int(x.round())]
            id_motif_y = listOfGlobals['lst_obj_id_y'][int(y.round())]

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
                    print("detets lacking dirs")
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
            self.label_abs.setPixmap(QPixmap("Outputs/Place_Output_here/motifs/draw_"+str(id_motif_x)+".png"))
            #self.label_abs.scaled(200)
            #self.label_abs.scaledToHeight(100)
            #self.label_abs.setMaximumHeight(100)
            #self.label_abs.setMaximumWidth(200)
            #self.label_abs.setPixmap(p.scaled(200, 100, Qt.KeepAspectRatio))

        except ValueError:
            print('veuillez cliquer une case de la matrice de chaleur')
    
            ###

            #try:
            # code qui génère et affiche les motifs


# Sépare les informations dans des listes différentes
def split_tab_res_no_file (tab_res, cible, motif_id, pointer, axis):
    # pour les indices des la liste (trié au préalable)
    plot_index = []
    plot_occur = []
    plot_cover = []
    # plot_distr = []
    i = 0
    for tmp in tab_res:
        # récupère les stats
        #if cible and tmp[3] == motif_id:
        #    fid.write(">")
        for a in axis :
            if cible and tmp[3] == motif_id:
                pointer[a] = int(i)
        #fid.write(str(tmp[3]) + "\n")
        plot_index.append(int(i))
        plot_occur.append(int(tmp[0]))
        plot_cover.append(float(tmp[1]))
        # plot_distr.append(float(tmp[2]))
        i += 1
    #fid.close()
    index = np.array(plot_index, dtype="i")
    occur = np.array(plot_occur, dtype="i")
    cover = np.array(plot_cover, dtype="f")
    #distr = np.array(plot_distr, dtype="f")
    return index, occur, cover#, distr
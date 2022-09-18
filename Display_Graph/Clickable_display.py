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

temp_x = 0
temp_y = 0
x = 'not a float, ce texte vérifie que user a bien choisi une case de la mat de chaleur'
y = 'not a float, ce texte vérifie que user a bien choisi une case de la mat de chaleur'
text_x = ' '
text_y = ' '
t_x = ' '
t_y = ' '
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent, width=5, height=4, dpi=100):
        
        self.parent = parent
        self.parent.x = 0
        self.parent.y = 0
        print('test')
        print(self.parent.parent.send_t1)

        ### def draw_result_2size(dir_O, name, tab_size, tab_res, cible, motif_id, tab_sim, num_type):
        # init values
        tab_sim = []
        for i in range(5):
            temp = []
            for j in range (5):
                temp.append(1/(j/2+i/2+1))
            tab_sim.append(temp)
        lst_id_y = [0,1,2,3,4]
        lst_id_x = [0,1,2,3,4]
        lst_occ_x = [1,1,3,4,5]
        lst_occ_y = [1,2,3,2,1]
        lst_cover_x = [1,2,3,4,5]
        lst_cover_y = [5,4,3,2,1]
        pointer = {'x':None, 'y':None}
        num_type = {1: 1, 2: 2, 3:3,4:4,5:5}

        ### tentative d'ajouter les listes directement depuis la bdd
        
        print(self.parent.parent.db_ids)

        # Formation des distributions
        tab_res = [None, None]
        #pipeline = Fp.unique_config(db_ids[0], db_ids[1], db_ids[2])
        #tab_res[0] = Fp.construct_1tab(self.parent.parent.db, pipeline, lst_motifs)
        pointer = {'x':None, 'y':None}
        #lst_id, lst_occ, lst_cover = Gd.split_tab_res(tab_res, fid, cible, motif_id, pointer, ['x','y'])

        '''
        pointer = {'x':None, 'y':None}
        pipeline = Fp.complete_struct(db_ids[0], db_ids[1])
        tab_res = [None, None]
        tab_res[0], tab_res[1] = Fp.construct_2tab(self.parent.parent.db,
                                     pipeline, lst_motifs1, lst_motifs2)
        lst_id, lst_occ, lst_cover = Gd.split_tab_res(tab_res, fid, cible, motif_id, pointer, ['x','y'])
        '''
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
        


        lst_sim, tab_sim = Gd.analyse_simil(tab_sim, num_type, 2)
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
        
        self.label_mcis = QLabel()
        self.label_mcis.setText("MCIS obtenu: ")

        self.label_ord = QLabel()
        self.label_ord.setText("Motif numéro: ")

        # 

        # construction du layout pour motifs
        self.lay_V_motifs.addWidget(self.label_abs)
        # jpeg
        self.lay_V_motifs.addWidget(self.label_mcis)
        # jpeg
        self.lay_V_motifs.addWidget(self.label_ord)
        # jpeg


        # entrer le layout dans une widget
        self.one_wigd = QWidget()
        self.one_wigd.setLayout(self.lay_H)

        self.setCentralWidget(self.one_wigd)

    #def mousePressEvent(self, event):
        #print("a")
        #print('data coords %d %d' % (x.round(), y.round()))

    def validate(self):
        try:
            float(x)
            int(x)
            print('Afficher les motifs des indices %d et %d' % (int(x.round()),int(y.round())))
            # code qui génère et affiche les motifs

        except ValueError:
            print('veuillez cliquer une case de la matrice de chaleur')
    

     
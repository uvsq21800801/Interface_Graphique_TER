import sys, os

gitable = os.getcwd()
path = os.path.dirname(gitable)

sys.path.append('Disp/Display_Graph')
sys.path.append('Disp/Input_Output')
#sys.path.append('Disp/Smart_Display')

from Display_Graph import Smart_Display
from Display_Graph import pyqt5_display
from Display_Graph import Choice_size

def main():

    matrice_chaleur = []
    occur = []
    recouv = []
    for i in range(10):
        ligne = []
        for j in range(10):
            ligne.append(j*i)
        matrice_chaleur.append(ligne)
        occur.append(i)
        recouv.append(10-i)

    # pour l'instant seul les deux premiers params 
    # sont totalement utilisés
    Choice_size.window()
    #Smart_Display.One_size(matrice_chaleur, occur, recouv, 5)
    

if __name__=="__main__":
    main()
import sys, os

gitable = os.getcwd()
path = os.path.dirname(gitable)

sys.path.append('Disp/Display_Graph')

from Display_Graph import Choice_size

def main():

    # appel de la fenêtre de choix
    Choice_size.window()
    

if __name__=="__main__":
    main()
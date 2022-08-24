from matplotlib.backend_bases import MouseButton

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import mplcursors


binding_id = 0

def One_size(heatmap, occur, recouv, taille):

    plot_indice = []
    for i in range(len(occur)):
        plot_indice.append(i)

    fig, axes = plt.subplots(2,2, figsize=(8,8))
    
    #en haut à droite (courbes)
    axehd = axes[0][1].twinx()
    
    axes[0][1].bar(plot_indice, occur, 1, color="red")
    axehd.bar(plot_indice, recouv, 0.3, color="black")
    axes[0][1].set_xlabel("Motifs triés par nombre d'occurrence croissant")
    axes[0][1].set_ylabel("Nombre d'occurrence d'un motif", c="red")
    axehd.set_ylabel("Taux de recouvrement du motif", c="black")
    mplcursors.cursor(axes[0][1])
    mplcursors.cursor(axehd)


    #en bas à gauge (courbes)
    axebg = axes[1][0].twinx()
    
    axes[1][0].barh(plot_indice, occur, 1, color="red")
    axebg.barh(plot_indice, recouv, 0.3, color="black")
    axes[1][0].set_xlabel("Motifs triés par nombre d'occurrence croissant")
    axes[1][0].set_ylabel("Nombre d'occurrence d'un motif", c="red")
    axebg.set_ylabel("Taux de recouvrement du motif", c="black")

    #axes[1][0].invert_xaxis()
    axes[1][0].invert_yaxis() 
    axebg.invert_xaxis()
    axebg.invert_yaxis()
    
    #matrice de chaleur

    #fig, ax = plt.subplots()
    
    #fig.set_size_inches(12.8,9.6)
        
    im = axes[1][1].imshow(heatmap, cmap="hot", interpolation='nearest')
    

    '''
    cbarlabels = ["distance d'édition", "similarité Raymond", "similarité Raymond asymétrique"]
    #cbarlabel = cbarlabels[detail[2]-1]
    
    cbar = axes[1][1].figure.colorbar(im, ax=ax, cmap=cmap)
    #cbar.axes[1][1].set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize=16)
    
    step = int(len(plot_indice)/20) + 1
    
    plot_indice[::step]
    np.arange(0,len(plot_indice),step)

    axes[1][1].set_xticks(np.arange(0,len(plot_indice),step), labels=lst_id[::step], fontsize=12)
    axes[1][1].set_yticks(np.arange(0,len(plot_indice),step), labels=lst_id[::step], fontsize=12)
    axes[1][1].tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    axes[1][1].xaxis.set_label_position("top")
    #if detail[2] == 3:
    #    axes[1][1].set_xlabel("MCIS/maxG : Isomorphisme si 1", fontsize=16)
    #    axes[1][1].set_ylabel("MCIS/minG : Inclusion si 1", fontsize=16)
    
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    if len(lst_id) < 20 :
        for i in range(len(lst_id)):
            for j in range(len(lst_id)):
                fontsize = 10
                round_size = 2
                val = round(heatmap[i][j],round_size)
                axes[1][1].text(j,i, val, ha="center", va="center", color='b', fontsize=fontsize)
    
    #titlecompl= str(nb)
    #if detail[0] == False :
    #    titlecompl = "H "+titlecompl
    #axes[1][1].set_title("Similarité entre motifs de "+name+" de taille "+str(detail[1])+" "+titlecompl, fontsize=20)
    axes[1][1].set_title("title", fontsize=20)
    fig.tight_layout()
    '''
    #axes inutilisés
    axes[0, 0].axis('off')
    #ax1, ax2 = ax1.twinx()

    '''
    occur = np.array(plot_occur)
    occur = occur.astype(float)
    recouv = np.array(plot_recouv)
    recouv = recouv.astype(float)
    '''

    # Diagramme baton
    '''
    ax1.bar(plot_indice, occur, 1, color="red")
    ax2.bar(plot_indice, recouv, 0.3, color="black")
    ax1.set_xlabel("Motifs triés par nombre d'occurrence croissant")
    ax1.set_ylabel("Nombre d'occurrence d'un motif", c="red")
    ax2.set_ylabel("Taux de recouvrement du motif", c="black")
    '''
    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)

    plt.show()

    print('success')



def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y
    if event.inaxes:
        ax = event.inaxes  # the axes instance
        #print('data coords %f %f' % (event.xdata, event.ydata))
        print('data coords %d %d' % (event.xdata.round(), event.ydata.round()))


def on_click(event):
    if event.button is MouseButton.LEFT:
        print('disconnecting callback')
        plt.disconnect(binding_id)

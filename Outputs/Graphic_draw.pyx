from os import mkdir
from os.path import isdir, isfile, join
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib.colorbar as colorbar

from Outputs.texture import *

cimport cython
cimport numpy as np
import numpy as np

# Noms des fichiers de sortie
def create_files_names_1dim(fpath, name):
    cdef int nb = 1
    file_id = name + "_" + str(nb) + "_id.txt"
    file_res = name + "_" + str(nb) + "_res.png"
    file_param = name + "_" + str(nb) + "_param.txt"
    while isfile(join(fpath, file_id)) or isfile(join(fpath, file_res)) or isfile(join(fpath, file_param)):
        nb += 1
        file_id = name + "_" + str(nb) + "_id.txt"
        file_res = name + "_" + str(nb) + "_res.png"
        file_param = name + "_" + str(nb) + "_param.txt"
    return file_id, file_res, file_param

def create_files_names_2dim(fpath, name, tab_size):
    cdef int nb = 1
    file_idx = (name + "_" + str(nb) + "_id.txt").replace("-"+str(tab_size[1]), '')
    file_idy = (name + "_" + str(nb) + "_id.txt").replace(str(tab_size[0])+"-", '')
    file_res = name + "_" + str(nb) + "_res.png"
    file_param = name + "_" + str(nb) + "_param.txt"
    while isfile(join(fpath, file_idx)) or isfile(join(fpath, file_idy)) or isfile(join(fpath, file_res)) or isfile(join(fpath, file_param)):
        nb += 1
        file_idx = (name + "_" + str(nb) + "_id.txt").replace("-"+str(tab_size[1]), '')
        file_idy = (name + "_" + str(nb) + "_id.txt").replace(str(tab_size[0])+"-", '')
        file_res = name + "_" + str(nb) + "_res.png"
        file_param = name + "_" + str(nb) + "_param.txt"
    return file_idx, file_idy, file_res, file_param

# Sépare les informations dans des listes différentes
def split_tab_res (tab_res, fid, cible, motif_id, pointer, axis):
    # pour les indices des la liste (trié au préalable)
    plot_index = []
    plot_occur = []
    plot_cover = []
    # plot_distr = []
    cdef int i = 0
    for tmp in tab_res:
        # récupère les stats
        if cible and tmp[3] == motif_id:
            fid.write(">")
        for a in axis :
            if cible and tmp[3] == motif_id:
                pointer[a] = int(i)
        fid.write(str(tmp[3]) + "\n")
        plot_index.append(int(i))
        plot_occur.append(int(tmp[0]))
        plot_cover.append(float(tmp[1]))
        # plot_distr.append(float(tmp[2]))
        i += 1
    fid.close()
    index = np.array(plot_index, dtype="i")
    occur = np.array(plot_occur, dtype="i")
    cover = np.array(plot_cover, dtype="f")
    #distr = np.array(plot_distr, dtype="f")
    return index, occur, cover#, distr

# Liste des similarités et normalisation de la table
def analyse_simil(tab_sim, num_type, nb_size):
    lst_sim = []
    # liste des similarités
    cdef int i, j = 0
    cdef int maximum
    if nb_size == 1:
        for i in range(len(tab_sim)):
            for j in range(i+1, len(tab_sim[0])):
                # récupère les similarités de la table
                lst_sim.append(float(tab_sim[i][j]))
    else :
        for i in range(len(tab_sim)):
            for j in range(len(tab_sim[0])):
                # récupère les similarités de la table
                lst_sim.append(float(tab_sim[i][j]))
    # normalise dans le cas de la distance d'édition
    if num_type == 0:
        # limite maximum
        maximum = max(lst_sim)
        for i in range(len(lst_sim)) :
            lst_sim[i] = 1 - (float(lst_sim[i])/float(maximum))
        for i in range(len(tab_sim)):
            for j in range(len(tab_sim[0])):
                # récupère les similarités de la table
                tab_sim[i][j] = 1 - (float(tab_sim[i][j])/float(maximum))
    return lst_sim, tab_sim

# Dessine la heatmap
def heatmap(ax_hm, tab_sim, lst_id_x, lst_id_y, lenght, step, norm, cm, pointer):
    im = ax_hm.imshow(tab_sim, cmap=cm, interpolation="nearest", norm=norm, aspect='auto')
    ax_hm.set_yticks(
        np.arange(0, len(tab_sim), step),
        #labels=lst_id_y[: len(Tab_sim) : step],
        #fontsize=12,
    )
    ax_hm.set_xticks(
        np.arange(0, len(tab_sim[0]), step),
        #labels=lst_id_x[: len(Tab_sim[0]) : step],
        #fontsize=12,
    )
    #ax_hm.set_aspect(len(lst_id_x)/len(lst_id_y))
    ax_hm.tick_params(top=True, labeltop=False)
    ax_hm.tick_params(bottom=False, labelbottom=False)
    ax_hm.tick_params(left=True, labelleft=False)
    ax_hm.tick_params(right=False, labelright=False)
    ax_hm.xaxis.set_label_position("top")

    
# Dessine l'histogramme des similarités
def sim_hist(ax, lst_sim, cm):
    n, bins, patches = ax.hist(lst_sim, range=(0,1), align="mid",orientation="horizontal")
    bins_centers = 0.5 * (bins[:-1] + bins[1:])

    col = bins_centers - min(bins_centers)
    col /= max(col)

    for c,p in zip(col, patches):
        plt.setp(p,'facecolor', cm(c))
    ax.set_xlabel("Distribution des valeurs de similarité")
    ax.xaxis.set_label_position("top")

# Dessine le graphique des x
def xbar(ax1, lst_id, lst_occ, lst_rec, cm, pointer):
    ## Distrib sur les x
    ax2 = ax1.twinx()
    b1 = ax1.bar(lst_id, lst_occ, width=1, color=cm(color1), label="Occurrences")
    b2 = ax2.bar(lst_id, lst_rec, width=0.3, color=cm(color2), label="Recouvrement")
    if pointer['x'] != None:
        ax2.annotate('x', (pointer['x'], 0.5), color="black", size=10, textcoords="offset points", xytext=(0,0), va="center", ha="center")
    ax1.set_xlabel("Motifs triés par nombre d'occurrence croissant")
    ax2.legend((b1,b2), ("Occurrences","Recouvrement"), loc="upper left")
    ax1.xaxis.set_label_position("top")
    ax1.tick_params(labelbottom=False)
    ax2.tick_params(labelbottom=False)
    ax1.tick_params(axis='y', colors=cm(color1), width=2)
    ax2.tick_params(axis='y', colors=cm(color2), width=2)

# Dessine le graphique des y
def ybar(ay1, lst_id, lst_occ, lst_rec, cm, pointer):
    ## Distrib sur les y
    ay2 = ay1.twiny()
    b1 = ay1.barh(lst_id, lst_occ, height=1, color=cm(0), label="Occurrences")
    b2 = ay2.barh(lst_id, lst_rec, height=0.3, color=cm(0.5), label="Recouvrement")
    ay1.invert_xaxis()
    ay2.invert_xaxis()
    if pointer['y'] != None:
        ay2.annotate('x', (0.5, pointer['y']), color="black", size=10, textcoords="offset points", xytext=(0,0), ha="right", va="center")
    ay1.set_ylabel("Motifs triés par nombre d'occurrence croissant")
    ay2.legend((b1,b2), ("Occ.","Rec."), loc="upper left")
    ay1.yaxis.set_label_position("left")
    ay1.tick_params(left=False, labelleft=False, right=True)
    ay2.tick_params(left=False, labelleft=False, right=True)
    ay1.tick_params(axis='x', colors=cm(0), width=2)#, rotation=90)
    ay2.tick_params(axis='x', colors=cm(0.5), width=2)#, rotation=90)

# Dessine le graphique complet avec 1 taille
def draw_result_1size(dir_O, name, size, tab_res, cible, motif_id, tab_sim, num_type):
    # création du fichier de sortie
    fpath = "Outputs/Place_Output_here/" + str(dir_O) + "/"
    if not isdir(fpath):
        mkdir(fpath)
    # choix des noms des fidhiers de sortie
    file_id, file_res, file_param = create_files_names_1dim(fpath, name)
    fid = open(join(fpath, file_id), "w")
    #fprm = open(join(fpath, file_param), "w")
    pointer = {'x':None, 'y':None}
    lst_id, lst_occ, lst_cover = split_tab_res(tab_res, fid, cible, motif_id, pointer, ['x','y'])

    # Valeurs :
    cdef float lenght = len(lst_id)
    cdef int step = int(lenght / 20) + 1
    # positionnement des min et max pour normaliser le gradien de couleurs
    norm = clr.Normalize(vmin=0, vmax=1)
    #norm = clr.Normalize(vmin=min(lst_sim), vmax=max(lst_sim))
    cm = plt.cm.get_cmap(colormap)
    # Répartition des espaces
    cdef float ratio_axe = max(2, lenght/15)
    cdef float ratio_ext = max(1, lenght/40)
    if tab_sim != None :
        lst_sim, tab_sim = analyse_simil(tab_sim, num_type, 1)
        # Figures :
        plt.clf()
        fig = plt.figure(figsize = (1.5*(ratio_axe+ratio_ext),1.5*(ratio_axe+ratio_ext)))#, constrained_layout=True)
        gs = fig.add_gridspec(2, 3, width_ratios = (ratio_ext,ratio_axe,0.1), height_ratios = (ratio_ext,ratio_axe), left=0.05, right=0.95, bottom=0.05, top=0.95)#, hspace=0.25, wspace=0.25) #
        #fig = plt.figure(figsize = (8,8))#, constrained_layout=True)
        #gs = fig.add_gridspec(2, 3, width_ratios = (1,2,0.1), height_ratios = (1,2), hspace=0.25, wspace=0.25) #, left=0.1, right=0.9, bottom=0.1, top=0.9)#
        ax_hm = fig.add_subplot(gs[1,1])
        axbar = fig.add_subplot(gs[0,1], sharex=ax_hm)
        aybar = fig.add_subplot(gs[1,0], sharey=ax_hm)
        ax_hist_sim = fig.add_subplot(gs[0,0])
        ax_colorbar = fig.add_subplot(gs[1,2])
        # Dessins
        xbar(axbar, lst_id, lst_occ, lst_cover, cm, pointer)
        ybar(aybar, lst_id, lst_occ, lst_cover, cm, pointer)
        heatmap(ax_hm, tab_sim, lst_id, lst_id, lenght, step, norm, cm, pointer)
        cbar = colorbar.Colorbar(ax=ax_colorbar, mappable=None, cmap=cm, norm=norm)
        sim_hist(ax_hist_sim, lst_sim, cm)
        plt.savefig(join(fpath, file_res))
        plt.clf()
    else :
        fig = plt.figure(figsize = (ratio_axe,ratio_ext), constrained_layout=True)
        axbar = fig.add_subplot()
        xbar(axbar, lst_id, lst_occ, lst_cover, cm, pointer)
        plt.savefig(join(fpath, file_res))
        plt.clf()


# Dessine le graphique complet avec 2 taille
def draw_result_2size(dir_O, name, tab_size, tab_res, cible, motif_id, tab_sim, num_type):
    # création du fichier de sortie
    fpath = "Outputs/Place_Output_here/" + str(dir_O) + "/"
    if not isdir(fpath):
        mkdir(fpath)
    # choix des noms des fidhiers de sortie
    file_idx, file_idy, file_res, file_param = create_files_names_2dim(fpath, name, tab_size)
    fidx = open(join(fpath, file_idx), "w")
    fidy = open(join(fpath, file_idy), "w")
    #fprm = open(join(fpath, file_param), "w")
    pointer = {'x':None, 'y':None}
    lst_id_x, lst_occ_x, lst_cover_x = split_tab_res(tab_res[0], fidx, cible, motif_id, pointer, ['x'])
    lst_id_y, lst_occ_y, lst_cover_y = split_tab_res(tab_res[1], fidy, cible, motif_id, pointer, ['y'])

    # Valeurs :
    cdef float lenght = max(len(lst_id_y), len(lst_id_x))
    cdef int step = int(lenght / 20) + 1
    # positionnement des min et max pour normaliser le gradien de couleurs
    norm = clr.Normalize(vmin=0, vmax=1)
    #norm = clr.Normalize(vmin=min(lst_sim), vmax=max(lst_sim))
    cm = plt.cm.get_cmap(colormap)
    # Répartition des espaces
    cdef float ratio_x = max(2, len(lst_id_x)/15)
    cdef float ratio_y = max(2, len(lst_id_y)/15)
    cdef float ratio_ext = max(1, lenght/40)
    cdef float fontsize = max(8, (lenght/5))
    if tab_sim != None :
        lst_sim, tab_sim = analyse_simil(tab_sim, num_type, 2)
        # Figures :
        plt.clf()
        fig = plt.figure(figsize = (1.5*(ratio_x+ratio_ext),1.5*(ratio_y+ratio_ext)))#, constrained_layout=True)
        gs = fig.add_gridspec(2, 3, width_ratios = (ratio_ext,ratio_x,0.1), height_ratios = (ratio_ext,ratio_y), left=0.05, right=0.95, bottom=0.05, top=0.95)#, hspace=0.25, wspace=0.25) #
        ax_hm = fig.add_subplot(gs[1,1])
        axbar = fig.add_subplot(gs[0,1], sharex=ax_hm)
        aybar = fig.add_subplot(gs[1,0], sharey=ax_hm)
        ax_hist_sim = fig.add_subplot(gs[0,0])
        ax_colorbar = fig.add_subplot(gs[1,2])
        # Dessins
        xbar(axbar, lst_id_x, lst_occ_x, lst_cover_x, cm, pointer)
        ybar(aybar, lst_id_y, lst_occ_y, lst_cover_y, cm, pointer)
        heatmap(ax_hm, tab_sim, lst_id_x, lst_id_y, lenght, step, norm, cm, pointer)
        cbar = colorbar.Colorbar(ax=ax_colorbar, mappable=None, cmap=cm, norm=norm)
        sim_hist(ax_hist_sim, lst_sim, cm)
        plt.savefig(join(fpath, file_res))
        plt.clf()
    else :
        # Figures :
        plt.clf()
        fig = plt.figure(figsize = ((max(ratio_x, ratio_y)),2*(ratio_ext)), constrained_layout=True)
        gs = fig.add_gridspec(2, 1, height_ratios = (1,1), left=0.05, right=0.95, bottom=0.05, top=0.95)#, hspace=0.25, wspace=0.25) #
        axbar1 = fig.add_subplot(gs[0,0])
        axbar2 = fig.add_subplot(gs[1,0])
        xbar(axbar1, lst_id_x, lst_occ_x, lst_cover_x, cm, pointer)
        xbar(axbar2, lst_id_y, lst_occ_y, lst_cover_y, cm, pointer)
        plt.savefig(join(fpath, file_res))
        plt.clf()

# Dessine le graphique d'occurrence et recouvrement
def draw_graphic(dir_O, name, lst_res, cible, motif_id):
    # création du fichier de sortie
    fpath = "Outputs/Place_Output_here/" + str(dir_O) + "/"
    if not isdir(fpath):
        mkdir(fpath)

    cdef int nb = 1
    filename = name + "_" + str(nb) + "_id.txt"
    while isfile(join(fpath, filename)):
        nb += 1
        filename = name + "_" + str(nb) + "_id.txt"
    f = open(fpath + filename, "w")

    # pour les indices des la liste (trié au préalable)
    plot_index = []
    plot_occur = []
    plot_cover = []
    pointer = None
    # plot_distr = []
    cdef int i = 0
    for tmp in lst_res:
        # récupère les stats
        if cible and tmp[3] == motif_id :
            f.write(">")
            pointer = int(i)
        f.write(str(tmp[3]) + "\n")
        plot_index.append(int(i))
        plot_occur.append(float(tmp[0]))
        plot_cover.append(float(tmp[1]))
        # plot_distr.append(float(tmp[2]))
        i += 1
    f.close()

    plt.clf()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    fig.set_size_inches(12.8, 9.6)

    occur = np.array(plot_occur)
    occur = occur.astype(float)
    cover = np.array(plot_cover)
    cover = cover.astype(float)

    # Diagramme baton
    ax1.bar(plot_index, occur, 1, color=color1)
    ax2.bar(plot_index, cover, 0.3, color=color2)
    if pointer != None :
        ax2.axvline(x = pointer, color=color3, lw=3)
    ax1.set_xlabel("Motifs triés par nombre d'occurrence croissant")
    ax1.set_ylabel("Nombre d'occurrence d'un motif", c=color1)
    ax2.set_ylabel("Taux de recouvrement du motif", c=color2)

    plt.savefig(fpath + name + "_" + str(nb) + "_graph.png")

    plt.clf()


# Dessine la matrice de chaleur
def draw_heatmap(dir_O, name, Tab_sim, num_type):
    cdef int nb = 1
    # création du fichier de sortie
    fpath = "Outputs/Place_Output_here/" + dir_O + "/"
    if not isdir(fpath):
        mkdir(fpath)

    filename = name + "_" + str(nb) + "_sim_" + str(num_type) + ".txt"
    while isfile(join(fpath, filename)):
        nb += 1
        filename = name + "_" + str(nb) + "_sim_" + str(num_type) + ".txt"
    f = open(fpath + filename, "w")

    for i in range(len(Tab_sim)):
        s = ""
        for j in range(len(Tab_sim[i])):
            s += str(Tab_sim[i][j]) + " "
        f.write(s + "\n")
    f.close()

    if num_type == 0:
        cmap = colormap + "_r"
    else:
        cmap = colormap

    plt.clf()

    fig, ax = plt.subplots()

    fig.set_size_inches(14.8, 12.8)

    im = ax.imshow(Tab_sim, cmap=cmap, interpolation="nearest")

    cbarlabels = [
        "distance d'édition",
        "similarité Raymond",
        "similarité Raymond asymétrique",
    ]
    cbarlabel = cbarlabels[num_type]

    cbar = ax.figure.colorbar(im, ax=ax, cmap=cmap)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize=16)

    lenght = max(len(Tab_sim), len(Tab_sim[0]))
    step = int(lenght / 20) + 1

    lst_id = list(range(0, lenght))

    ax.set_yticks(
        np.arange(0, len(Tab_sim), step),
        labels=lst_id[: len(Tab_sim) : step],
        fontsize=12,
    )
    ax.set_xticks(
        np.arange(0, len(Tab_sim[0]), step),
        labels=lst_id[: len(Tab_sim[0]) : step],
        fontsize=12,
    )
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    ax.xaxis.set_label_position("top")
    if num_type == 2:
        ax.set_xlabel("MCIS/minG : Inclusion si 1", fontsize=16)
        ax.set_ylabel("MCIS/maxG : Isomorphisme si 1", fontsize=16)

    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    if lenght < 20:
        for i in range(len(Tab_sim)):
            for j in range(len(Tab_sim[i])):
                fontsize = 10
                round_size = 2
                val = round(Tab_sim[i][j], round_size)
                ax.text(
                    j, i, val, ha="center", va="center", color="b", fontsize=fontsize
                )

    ax.set_title("Similarité entre motifs de " + name + " " + str(nb), fontsize=20)
    fig.tight_layout()

    plt.savefig(fpath + name + "_" + str(nb) + "_sim_" + str(num_type) + "_hm.png")
    plt.clf()

    ### Distribution des similarités
    # liste des similarités
    lst_sim = []
    for line in Tab_sim:
        for tmp in line:
            # récupère les similarités de la table
            lst_sim.append(float(tmp))
    # normalise dans le cas de la distance d'édition
    if num_type == 0:
        maximum = max(lst_sim)
        for i in range(len(lst_sim)) :
            lst_sim[i] = 1 - (lst_sim[i]/maximum)

    fig, ax = plt.subplots()
    fig.set_size_inches(9.6, 9.6)

    sim = np.array(lst_sim)
    sim = sim.astype(float)

    # histogramme
    ax.hist(sim, range=(0,1))

    ax.set_xlabel("Facteur de similarité")
    ax.set_ylabel("Distribution")

    plt.savefig(fpath + name + "_" + str(nb) + "_sim_" + str(num_type) + "_g.png")

    plt.clf()

# Dessine la distribution du motif à travers les configurations
def draw_occurrence_motif(dir_O, motif_id, lst_occ, lst_label):
    # Distribution des occurrences
    fig = plt.figure(constrained_layout=True)

    ax = fig.add_subplot()

    occ = np.array(lst_occ)
    occ = occ.astype(int)

    # histogramme
    ax.bar(np.arange(len(lst_label)), occ, align="center")
    ax.set_xticks(np.arange(len(lst_label)), labels= lst_label, rotation=45, ha='right')

    ax.set_ylabel("Nombre d'apparition")

    plt.savefig(join(dir_O, "motif_" + str(motif_id) + "_graph.png"))
    plt.clf()

from pynauty import *
import numpy as np

# Traduit une combinaison de booléen par une combinaison de 0 et 1
def interize(combi_bool):
    combi_int = np.zeros(len(combi_bool), dtype=int)
    cdef int i
    for i in range(len(combi_int)):
        if combi_bool[i] == True:
            combi_int[i] += 1
    return combi_int


####
## 1. Algo principal de regroupement des sous-graphes par certificat canonique
####


def combi_iso(
    matrix_bonds,  # matrice d'adjacence de la structure étudiée
    tab_atom,  # carctéristiques des sommets (atomes)
    lst_elmt,  # ordre des éléments de la coloration
    lst_combi,  # liste des combinaisons de sommets
):
    ## Structures de stockage :
    # Listes:
    lst_certif = []  # = identifiant : certificat
    lst_id = []  # = [identifiant*]
    # Dictionnaires:
    # dictionnaires des occurrences d'un motif
    dict_occurs = {}  # = {identifiant: [combi*]}

    # dictionnaire des motifs apportant sur celui-ci:
    #   le nombre d'occurrence du motif
    #   un tableau qui décompte le nombre de fois où un sommet est utilisé dans une occurrence du motif
    dict_motif = {}  # = {identifiant: [nb_occurrence, occurrence_sommet]}

    ###### Boucle sur la liste de combinaison ######
    cdef int i
    for combi_bool in lst_combi:
        # calcule du certificat de la combinaison
        certif = combi_to_certif(combi_bool, matrix_bonds, tab_atom, lst_elmt)

        # trie les certificats connus ou non
        if certif not in lst_certif:
            # ajoute à la liste des certificats
            lst_certif.append(certif)
            # identifit son indice dans la liste
            indice = lst_certif.index(certif)
            # ajoute la première occurrence aux dictionnaires
            dict_occurs[indice] = [interize(combi_bool)]
            dict_motif[indice] = [1, interize(combi_bool)]
            # ajoute l'indice à la liste
            lst_id.append(indice)
        else:
            # identifit son indice dans la liste
            indice = lst_certif.index(certif)
            # ajoute la nouvelle occurrence au dictionnaire des occurrences
            dict_occurs[indice].append(interize(combi_bool))
            # met à jour les données du motif
            tmp = dict_motif.get(indice)
            for i in range(len(combi_bool)):
                if combi_bool[i] == True:
                    tmp[1][i] += 1
            dict_motif[indice] = [tmp[0] + 1, tmp[1].copy()]

    return (
        dict_occurs,  # = {identifiant: [combi*]}
        dict_motif,  # = {identifiant: [nb_occurrence, occurrence_sommet]}
        lst_id,  # = [identifiant*] ##MODIF?##
        lst_certif,  # = [certificat*]
    )


# Fonction constrisant le graphe PyNauty
def construct_pynauty_graph(matrix_bonds, tab_atom, lst_elmt, ref):
    dict_connex = {}
    cdef int nb_vertex = len(ref)
    cdef int i
    cdef int j
    cdef int num_col
    # pour tous sommets de la combinaison
    for i in range(len(ref)):
        list_connex = []
        # pour tous les sommets différents de la combinaison
        for j in range(len(ref)):
            # si ils sont connexes, alors ajoute un lien à la liste des connexions
            if i != j and matrix_bonds[ref[i]][ref[j]] != 0:
                list_connex.append(j)

        # détermine le nombre de voisins fantômes à ajouter
        elmt_name = tab_atom[ref[i]].split()
        num_col = (
            lst_elmt.index(elmt_name[0]) + 1
        )  # +1 car on doit mettre au moins 1 voisin

        # ajoute les liens vers les nouveaux sommets fantômes et incrémente le nombre de sommets
        for j in range(num_col):
            list_connex.append(nb_vertex)
            nb_vertex += 1

        # ajout de la liste d'arcs dont ref(index) i est la queue dans le dictionnaire
        dict_connex.setdefault(i, list_connex)
    # génération du graph PyNauty
    return Graph(nb_vertex, directed=True, adjacency_dict=dict_connex)


# Fonction qui génère une signature canonique à partir d'un graphe "coloré"
#
# La coloration se fera en ajoutant n voisins fantômes à un sommet étant le nième dans la liste des éléments
def combi_to_certif(combi_bool, matrix_bonds, tab_atom, lst_elmt):
    ###### Initialisations ######
    # liste des indices des sommets de la combinaison dans la matrice d'adjacence
    ref = []
    combi_bool = np.array(combi_bool, dtype=bool)
    cdef int i
    # si la combi est de type np.ndarray
    for i in range(combi_bool.size):
        if combi_bool[i]:
            ref.append(i)
    ref = np.array(ref, dtype=int)
    # construit le graphe PyNauty
    g = construct_pynauty_graph(matrix_bonds, tab_atom, lst_elmt, ref)

    # calcule le certificat depuis ce graphe grâce à l'algorithme de McKay
    certif = certificate(g)

    # retourn le certificat avec les valeurs tests
    return certif

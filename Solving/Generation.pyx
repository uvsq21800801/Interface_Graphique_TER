import numpy as np

"""
# Explication de l'algorithme
On sélectionne un sommet
De façon récursive, on génère tous les sous-graphes connexes qui le contiennent
On stocke ces nouvelles combinaisons de sommets
On passe aux sommets suivants et on n'inclue plus les sommets déjà sélectionnés
"""

# Test d'inclusion d'une table (myarr) dans une liste de table (lst_arrays)
def arreq_in_list(myarr, lst_arrays):
    # test pour chaque élément de la liste jusqu'à un "True" ou la fin de l'itération
    return next((True for elem in lst_arrays if np.array_equal(elem, myarr)), False)


# Génération de toutes les combinaisons connexes possibles
# avec chaque sommet en générateur successif
# et pour chaque taille jusqu'à la limite
#
# Paramètres : matrice d'adjencence [[bool]], bornes des tailles
def subgen(matrix_bonds, size_min, size_max):
    cdef int i

    # cette variable est la structure qui contient les graphlets de chaque taille
    lst_combi_ord = []

    for i in range(size_max):
        lst_combi_ord.append([])

    # création des combis de taille 1
    for i in range(len(matrix_bonds)):
        combi_tmp = np.zeros(len(matrix_bonds), dtype=bool)
        combi_tmp[i] = True
        lst_combi_ord[0].append(combi_tmp.copy())

    cdef int size = 1  # taille étudiée à chaque tour récursif

    # chaque sommet du graphe est générateur successivement
    for i in range(len(matrix_bonds)):
        # appel de la fonction récursive pour le sommet générateur i
        lst_combi_ord = subgen_rec(
            matrix_bonds, size_max, lst_combi_ord[0][i], size + 1, lst_combi_ord, i
        )

    ## Résultat de la fonction
    # Y-a-t'il une seule taille visée
    if size_max == size_min:
        # retourne la liste des combinaisons
        return lst_combi_ord[size_min - 1].copy()
    else:
        # reconstruit la table qui ne contient que les tailles d'intérêt
        combi_return = []
        for i in range(size_min, size_max + 1):
            combi_return.append(lst_combi_ord[i - 1].copy())
        return combi_return


# Fonction recursive qui va chercher toutes les sous-graphes contenant le sous-graphe précédent
def subgen_rec(
    matrix_bonds,  # matrice d'adjacence [[bool]]
    size_max,  # taille maximale de sous-graphes
    combi_prec,  # la combinaison de sommet du sous-graphe à agrandir
    size,  # taille des sous-graphes à obtenir à ce tour
    lst_combi_ord,  # liste des combinaisons par taille
    sommets_elim,  # sommet générateur actuel (ceux avant déjà traités)
):
    # si taille max atteinte
    if size > size_max:
        return lst_combi_ord

    # définition des variables
    cdef int len_matrix = len(matrix_bonds)
    cdef int i
    cdef int j
    # pour chaque sommet sélectionnable dans la matrice
    for i in range(sommets_elim, len_matrix):
        # si le sommet i est dans le sous-graphe précédent
        if combi_prec[i] == True:
            # pour tout autres sommets sélectionnables (pas de boucle sur soit donc i==j éliminé)
            for j in range(sommets_elim, len_matrix):
                # s'il est lié au sous-graphe précédent et n'y est pas déjà
                if (matrix_bonds[j][i] == True or matrix_bonds[i][j] == True) and (
                    combi_prec[j] == False
                ):
                    # créé la combinaison qui associe le sous-graphe et lui
                    combi_temp = combi_prec.copy()
                    combi_temp[j] = True
                    # si il n'est pas déjà dans les sous-graphes de cette taille
                    if not arreq_in_list(combi_temp, lst_combi_ord[size - 1]):
                        # ajoute la combinaison à la liste pour sa taille
                        lst_combi_ord[size - 1].append(combi_temp.copy())
                        # lance la recherche récursive pour la taille supérieur avec ce nouveau graphe
                        subgen_rec(
                            matrix_bonds,
                            size_max,
                            combi_temp,
                            size + 1,
                            lst_combi_ord,
                            sommets_elim,
                        )
    return lst_combi_ord

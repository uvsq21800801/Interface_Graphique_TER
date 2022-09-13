###
# 1. Recouvrement des sommets occurrences d'un motif entre eux
###

# Calcul les taux de recouvrement et d'occupation pour un groupe d'isomorphes
# ajoute les valeurs de taux à la suite des tableaux dans le dictionnaire
def calculate_rates(dict_stat):
    cdef float addup
    cdef float nb_in
    cdef float nb_tot
    cdef int i
    # pour chaque indice dans le dictionnaire des stats
    for indice in dict_stat.keys():
        stat = dict_stat.get(indice)
        addup = 0.0  # cumule des occurrences de sommets
        nb_in = 0.0  # nombre de sommets apparus
        nb_tot = len(stat[1])  # nombre de sommets dans la structure
        for i in range(len(stat[1])):
            addup += stat[1][i]
            if stat[1][i] > 0:
                nb_in += 1.0
        # taux de recouvrement
        if nb_in > 0:
            dict_stat[indice].append(addup / nb_in)
        else:
            dict_stat[indice].append(0.0)

        # taux d'occupation
        dict_stat[indice].append(nb_in / nb_tot)


###
# 2. Fonctions utiles
###

# Calcul le nombre de sous-graphes sans équivalent isomorphe (unique)
def get_unique_number(lst_id, dict_stat):
    nb_in = 0
    for indice in lst_id:
        tmp = dict_stat.get(indice)
        if tmp[0] == 1:
            nb_in += 1
    return nb_in


# Tri par occurrence et recouvrement croissant
def occurr_sorting(lst_id, dict_stat):
    lst_sorted = []
    # liste des couples de donnée { occurrence : [[indice, taux]] }
    d = {}
    # pour chaque indice (de certificat/ de motif)
    for i in lst_id:
        tmp = dict_stat.get(i)
        if tmp[0] not in d.keys():
            d[tmp[0]] = [[i, tmp[2]]]
        else:
            d[tmp[0]].append([i, tmp[2]])

    # pour tous les nombres d'occurrence triés
    for k in sorted(d.keys()):
        # récupère la liste des couples [indice, taux]
        tmp = d.get(k)
        # pour tous les couples triés selon le taux
        for l in sorted(tmp, key=second):
            lst_sorted.append(l[0])

    return lst_sorted


# retourne le second terme d'un tableau
def second(tab):
    return tab[1]

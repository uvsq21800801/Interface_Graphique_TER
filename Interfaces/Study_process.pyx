from bson.objectid import ObjectId
from datetime import datetime
import time

from Inputs import Files_read as Fr
from Outputs import Data_insert as Di
from Interfaces import Terminal_ask as Ta
from Solving import Generation as SSG
from Solving import Isomorphism as Iso
from Solving import Analysis as An

# cimport cython
# cimport numpy as np
import numpy as np

# Traiter les fichiers de données pour la structure
def Complete_process(db, db_ids, db_names, options, lst_color, path_I):
    ##### Dossier d'informations à traiter
    # récupère le nom du dossier
    dir_I = Fr.Get_dir_name(path_I)
    # recherche des fichiers trad-atom et bonds dans le dossier
    files_T, files_B, db_names[2] = Fr.Search_files_conf(path_I, dir_I)

    # Recherche des configurations sur la BDD
    for i in sorted(db_names[2]):
        if (
            db.configurations.count_documents(
                {
                    "struct": ObjectId(db_ids[0]),
                    "color": ObjectId(db_ids[1]),
                    "number": i,
                }
            )
            > 0
        ):
            result = db.configurations.find_one(
                {
                    "struct": ObjectId(db_ids[0]),
                    "color": ObjectId(db_ids[1]),
                    "number": i,
                }
            )
            db_ids[2][i] = result["_id"]
        else:  # si innexitante, création de la configuration
            result = db.configurations.insert_one(
                {
                    "struct": ObjectId(db_ids[0]),
                    "color": ObjectId(db_ids[1]),
                    "number": i,
                    "sizes": list(),
                }
            )
            db_ids[2][i] = result.inserted_id

    # Choix de la taille maximale à analyser
    question = "Quelle la plus grande taille de motifs visée?"
    max_size = Ta.terminal_input_num_borne(question, 3, 100)
    min_size = 3
    options[1] = list(range(min_size, max_size + 1))

    # Exécute par configuration
    for i in db_names[2]:
        exec_combi_1conf(
            options,
            path_I,
            dir_I,
            files_T[i],
            files_B[i],
            i,
            db,
            db_ids,
            lst_color,
        )

    return 0


# Recherche les occurrences connues et calcul celle cumulée sur une interface


# Exécute le processus de génération de combis sur une configuration
def exec_combi_1conf(
    options,
    path_I,
    dir_I,
    filename_T,
    filename_B,
    conf_num,
    db,
    db_ids,
    lst_color,
):
    # Tailles des motifs
    sizes = search_sizes(db.configurations, db_ids, conf_num, options[1])
    if len(sizes) == 0:
        print("Tailles déjà traitées pour la configuration " + str(conf_num))
        print("conf" + str(conf_num) + " fini " + str(datetime.now().time()) + "\n")
        return 0

    # Lecture des fichiers et construction de la structure
    _, tab_atom, matrix_bonds = Fr.Files_read(
        options[0], path_I, dir_I, filename_T, filename_B
    )

    # Met à jour les tailles
    while max(sizes) > len(tab_atom):
        sizes.remove(max(sizes))
    max_size = max(sizes)
    min_size = min(sizes)

    # Met la liste de couleurs à jour
    for element in tab_atom:
        splitted = element.split(" ")
        element = splitted[0]
        if element not in lst_color:
            # ajoute l'élément à la coloration
            lst_color.append(element)
            db.colorations.find_one_and_update(
                {"_id": ObjectId(db_ids[1])}, {"$push": {"elements": element}}
            )

    # Génération des sous-graphes
    print("conf" + str(conf_num) + " commence " + str(datetime.now().time()))
    lst_combi = SSG.subgen(matrix_bonds, min_size, max_size)
    print("conf" + str(conf_num) + " combinaisons finis " + str(datetime.now().time()))

    # Pour toutes tailles non enregistrées : tri des motifs et décompte des occurrences
    for i in sizes:
        (dict_isomorph, dict_stat, lst_id, lst_certif) = sort_motifs(
            matrix_bonds,
            tab_atom,
            lst_combi[i - min_size],
            lst_color,
        )
        # ajoute dans la Base de Données
        Di.insert_occurs_motifs(
            db_ids,
            db.occurrences,
            db.motifs,
            conf_num,
            tab_atom,
            matrix_bonds,
            lst_certif,
            lst_id,
            dict_isomorph,
            dict_stat,
        )
        # ajoute la taille sur celles traitées sur la config
        db.configurations.find_one_and_update(
            {
                "struct": ObjectId(db_ids[0]),
                "color": ObjectId(db_ids[1]),
                "number": conf_num,
            },
            {"$push": {"sizes": i}},
        )
        print(
            str(conf_num)
            + " taille "
            + str(i)
            + " fini "
            + str(datetime.now().time())
            + "\n"
        )
    print("conf" + str(conf_num) + " fini " + str(datetime.now().time()) + "\n")
    return 0


# Tri les motifs isomorphes
def sort_motifs(matrix_bonds, tab_atom, lst_combi, lst_color):
    time_temp = time.time()  ## test
    # Programme de regroupement des isomorphes
    (dict_isomorph, dict_stat, lst_id, lst_certif) = Iso.combi_iso(
        matrix_bonds, tab_atom, lst_color, lst_combi
    )

    print("Tri des isomorphes fini en " + str(time.time() - time_temp) + " seconds")

    # Calcul le taux de recouvrement et celui d'occupation pour chaque groupe
    An.calculate_rates(dict_stat)
    return (dict_isomorph, dict_stat, lst_id, lst_certif)


# Recherche les tailles non traitées dans la Base de Données
def search_sizes(config, db_ids, conf_num, sizes_tot):
    sizes = sizes_tot.copy()
    if (
        config.count_documents(
            {
                "struct": ObjectId(db_ids[0]),
                "color": ObjectId(db_ids[1]),
                "number": conf_num,
            }
        )
        > 0
    ):
        result = config.find_one(
            {
                "struct": ObjectId(db_ids[0]),
                "color": ObjectId(db_ids[1]),
                "number": conf_num,
            }
        )
        for i in list(result["sizes"]):
            if i in sizes:
                sizes.remove(i)
    return sizes

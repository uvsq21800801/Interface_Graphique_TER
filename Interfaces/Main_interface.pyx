import sys

sys.path.append("Graphetarium/Inputs")
sys.path.append("Graphetarium/Outputs")
sys.path.append("Graphetarium/Solving")
sys.path.append("Graphetarium/Interfaces")

from Inputs import Database_create as DbC
from Outputs import Graphic_draw as Gd
from Outputs import Files_write as Fw
from Interfaces.Study_process import Complete_process
from Interfaces import Final_process as Fp
from Interfaces import Select_process as Sp
from Interfaces import Terminal_ask as Ta

cimport cython
cimport numpy as np

import numpy as np

#############################################
############ PROGRAMME PRINCIPAL ############
#############################################


def interface():
    ##### VARIABLES PRINCIPALES
    # le chemin des entrées
    path_I = "Inputs/Place_Folder_here/"
    # les types de protocole
    cdef bint Multi_conf = False    # Une ou toutes celle de la structure
    cdef bint Multi_size = False    # Une taille ou comparer 2 tailles
    # les options pour certaines fonctions:
    #      0 : Hydrogène conservé?
    #      1 : Tailles traitées
    #      2 : Type de Similarité
    #      3 : Motif spécifique?
    options = [False, 0, 0, False]
    # les identifiants de la BDD (format _id)
    #      0 : structure (_id)
    #      1 : coloration (_id)
    #      2 : configuration (dict{_id})
    #      3 : motif spécifique (_id)
    db_ids = ["", "", {}, ""]
    # les noms dans la BDD (format str)
    #      0 : structure (name)
    #      1 : coloration (name)
    #      2 : configuration ([number])
    #      3 : motif spécifique (sign)
    db_names = ["", "", [], 0]
    # la(les) taille(s) comparée(s)
    tab_size = []
    # la liste de choix pour le crible :
    #       0 : nombre de liaisons (None, modificateur par rapport à n)
    #       1 : degré minimum [0 ; n-1]
    #       2 : degré maximum [1 ; n]
    #       3 : présence de OW
    #       3 : présence de liaison H
    tab_filter = [None, None, None, None, None]

    ##### CONNECTION A LA BDD
    client = DbC.connect_mongodb()
    if client == None :
        print("Fermeture du programme")
        return 1
    # Base de données
    db = client.graphetarium2
    # Tables
    _ = DbC.create_collections(db)

    ##### Questions de contexte
    # Choix de structure
    # -1 fermer le programme ; 0 créer ; 1 trouver
    res = Sp.select_struct(db.structures, db_ids, db_names)
    if res == -1:  # Fermeture
        print("Tentatives épuisées - Fermeture du programme")
        return 0
    else:
        # Choix de la coloration
        lst_color = Sp.select_color(db, db_ids, db_names, options)
        # Affiche les num de configuration et les tailles
        nb_config, _ = Sp.view_config(db, db_ids, db_names)
        # Choix de procéder sur les données actuelles ou d'en créer
        res = Sp.select_process(nb_config)
        if res == -1:  # Fermeture
            print("Fermeture du programme")
            return 0
        if res == 0:  # Génération de données
            Complete_process(db, db_ids, db_names, options, lst_color, path_I)
    test = True
    ############ Partie Traitement de Données ##################
    while test :
        test = False
        ## Questions d'Analyse
        # Interrogation sur la(les) configuration(s)
        Multi_conf, max_size = Sp.select_config(db, db_ids, db_names)

        # Interrogation sur la(les) taille(s)
        Multi_size, tab_size = Sp.select_size(max_size)

        # Crible sur les motifs
        # lst_motifs regroupe les motifs correspondant aux critères - {_id : sign}
        if Multi_size :
            # 1ere taille
            lst_motifs1 = Sp.test_filter(db, db_ids, tab_size[0])
            # 2eme taille
            lst_motifs2 = Sp.test_filter(db, db_ids, tab_size[1])
        else :
            # taille unique
            lst_motifs = Sp.test_filter(db, db_ids, tab_size[0])

        # Nombre de comparaison à faire et test des longueurs des listes
        nb_comp = 0
        if Multi_size :
            if len(lst_motifs1) == 0 or len(lst_motifs2) == 0:
                test = True
                print("Une liste est vide.")
            else :
                nb_comp = len(lst_motifs1)*len(lst_motifs2)
        else :
            if len(lst_motifs) == 0:
                test = True
                print("La liste est vide.")
            else :
                nb_comp = len(lst_motifs)*(len(lst_motifs)-1)
                nb_comp = nb_comp/2
        
        if not test:
            # Choix du type de similarité
            print("Il y a jusqu'à "+str(int(nb_comp))+" comparaisons à analyser.")
            options[2] = Sp.select_metric()

            # Choix d'un motif à suivre
            question = "Pointer un motif sur les figures ?"
            message = "Cible"
            options[3] = Ta.terminal_question_On(question, message, "Non", False)
            while options[3] and db_ids[3] == "" :
                options[3] = Sp.select_the_motif(db, db_ids, db_names, lst_color, options)
                if options[3] and Multi_size:
                    if db_ids[3] not in lst_motifs1 and db_ids[3] not in lst_motifs2 :
                        print("Le motif ciblé ne correspond pas aux filtres.")
                        options[3] = Ta.terminal_question_On("Sélectionner un nouveau motif?", message, "Oui", True)
                        db_ids[3] = ""
                elif options[3] and not Multi_size :
                    if db_ids[3] not in lst_motifs :
                        print("Le motif ciblé ne correspond pas au filtre.")
                        options[3] = Ta.terminal_question_On("Sélectionner un nouveau motif?", message, "Oui", True)
                        db_ids[3] = ""

            ## Formation des distributions
            tab_res = [None, None]
            # Choix du filtre (Une ou plusieurs config)
            if Multi_conf:
                # Correction si choix asymétrique
                if options[2] == 2:
                    options[2] = 1
                pipeline = Fp.complete_struct(db_ids[0], db_ids[1])
            else :
                pipeline = Fp.unique_config(db_ids[0], db_ids[1], db_ids[2])
            # Construction des distributions
            if Multi_size:
                tab_res[0], tab_res[1] = Fp.construct_2tab(db, pipeline, lst_motifs1, lst_motifs2)
                if len(tab_res[0]) == 0 or len(tab_res[1]) == 0:
                    test = True
                    if len(tab_res[0])==0:
                        print("Aucun motif de taille "+str(tab_size[0])+" sélectionné.")
                    if len(tab_res[1])==0:
                        print("Aucun motif de taille "+str(tab_size[1])+" sélectionné.")
                else :
                    print("Il y a "+str(len(tab_res[0]))+" et "+str(len(tab_res[1]))+ " motifs étudiés.")
            else :
                tab_res[0] = Fp.construct_1tab(db, pipeline, lst_motifs)
                if len(tab_res[0]) == 0:
                    test = True
                    print("Aucun motif de taille "+str(tab_size[0])+" sélectionné.")
                else :
                    print("Il y a "+str(len(tab_res[0]))+ " motifs étudiés.")
        #print(test, options[2])
        if not test :
            ## Formation de la matrice de chaleur
            if Multi_size :
                tab_sim = Fp.construct_matrix_2g(db, options[2], tab_res[0], tab_res[1])
            else :
                tab_sim = Fp.construct_matrix_1g(db, options[2], tab_res[0])
            name = Fw.filename_heatmap(Multi_size, Multi_conf, db_names, tab_size)
            if Multi_size:
                Gd.draw_result_2size(db_names[0], name, tab_size, tab_res, options[3], db_ids[3], tab_sim, options[2])
            else :
                Gd.draw_result_1size(db_names[0], name, tab_size[0], tab_res[0], options[3], db_ids[3], tab_sim, options[2])

        if test :
            question = "Fermer le programme ?"
            test = not Ta.terminal_question_On(question, "Fermer?", "Non", False)
    # Fin de programme
    print("Fermeture du programme")
    return 0

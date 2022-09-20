from os import mkdir
from os.path import isdir, isfile, join
from bson.objectid import ObjectId

from Inputs import Files_read as Fr
from Interfaces import Terminal_ask as Ta
from Interfaces import Final_process as Fp
from Outputs import Data_insert as Di


# Choix de la structure
def select_struct(struct, db_ids, db_names):
    test = 0
    while test < 5:  # 5 tentatives avant fermeture du programme
        struct_name = input("Quel est le nom de la structure traitée? ")
        if struct.count_documents({"name": struct_name}) > 0:
            # structure trouvée
            res = struct.find_one({"name": struct_name})
            db_ids[0] = str(res["_id"])
            db_names[0] = struct_name
            return 1
        else:
            # structure non trouvée donc à créer?
            if Ta.terminal_question_On(
                "Créé " + struct_name + "?", "Structure", "Oui", True
            ):
                # crée la structure
                db_ids[0] = str(
                    struct.insert_one(
                        {"name": struct_name, "colors": list()}
                    ).inserted_id
                )
                db_names[0] = struct_name
                return 0
        test += 1
    return -1


# Choix de la coloration (existant ou non)
def select_color(db, db_ids, db_names, options):
    choices = []
    colors_ids = []
    for result in db.colorations.find():
        colors_ids.append(result["_id"])
        choices.append(str(result["name"]) + " : " + str_list(result["elements"], ", "))
    choices.append("Nouvelle coloration")
    if len(colors_ids) > 0:
        question = "Quelle coloration utilisée?"
        index = Ta.terminal_question_choice(question, choices)
        if index < len(colors_ids):
            result = db.colorations.find_one({"_id": ObjectId(colors_ids[index])})
            db_ids[1] = result["_id"]
            db_names[1] = result["name"]
            options[0] = result["haveH"]
            Di.insert_struct_color(db.structures, db_ids)
            return result["elements"]
    # Par défaut ou par choix, créé une coloration
    list_color = Di.insert_color(db.colorations, db_ids, db_names, options)
    # Ajouter cette coloration à la liste de la structure
    if db_ids[0] != "":
        Di.insert_struct_color(db.structures, db_ids)
    return list_color


# Question pour le processus
def select_process(nb_config):
    if nb_config == 0:
        return 0  # créé des données
    question = "Créer des données ou Utiliser celles présentes"
    choices = ["Fermer le programme", "Créer des données", "Utiliser celles présentes"]
    return Ta.terminal_question_choice(question, choices) - 1


# Affichage des configurations
# pour la coloration et la structure séléctionnée
# Calcul de la taille maximale traitée sur toute
def view_config(db, db_ids, db_names):
    view = []
    max_size = -1
    db_names[2] = []
    db_ids[2] = {}
    for result in db.configurations.find(
        {"struct": ObjectId(db_ids[0]), "color": ObjectId(db_ids[1])}
    ):
        db_names[2].append(str(result["number"]))
        db_ids[2][int(result["number"])] = result["_id"]
        view.append(str(result["number"]) + " : " + str_list(result["sizes"], ", "))
        if len(result["sizes"]) > 0:
            if max(result["sizes"]) < max_size or max_size == -1:
                max_size = max(result["sizes"])
    if len(view) == 0:
        view.append("Aucune donnée")
        return 0, 0
    else:
        print(view)
        return len(view), max_size


# Choisi la(les) configuration(s)
def select_config(db, db_ids, db_names):
    # choix de la ou des config
    config_nums = []
    config_ids = {}
    max_sizes = []
    choices = []
    for result in db.configurations.find(
        {"struct": ObjectId(db_ids[0]), "color": ObjectId(db_ids[1])}
    ):
        if len(result["sizes"]) > 0:
            choices.append(
                "number "
                + str(result["number"])
                + " : "
                + str_list(result["sizes"], ", ")
            )
            config_nums.append(int(result["number"]))
            config_ids[int(result["number"])] = result["_id"]
            max_sizes.append(max(result["sizes"]))
    if len(choices) == 0:
        return False, 0
    else:
        choices.append("Toutes les configurations")
        res = Ta.terminal_question_choice("Quelle configuration?", choices)
        if res == len(choices) - 1:
            db_ids[2] = config_ids
            db_names[2] = config_nums
            return True, min(max_sizes)
        else:
            db_ids[2] = config_ids[config_nums[res]]
            db_names[2] = config_nums[res]
            return False, max_sizes[res]


# Interrogation sur les cribles
# la liste de choix pour le crible :
#       0 : nombre de liaisons (None, modificateur par rapport à n)
#       1 : degré minimum [0 ; n-1] 0 étant le cas nul
#       2 : degré maximum [1 ; n] n étant le cas nul
#       3 : présence d'atome OW
#       3 : présence de liaison H
def select_filter(nb_v, lst_color): 
    # Définition du filtre
    question = "Nombre de lien dans le motif?"
    if nb_v == 3 :
        nb_b = Ta.terminal_question_choice(question, ["Aucun", "= 2", "= 3"])
    nb_b = (
        Ta.terminal_question_choice(
            question, ["Aucun", "= "+str(nb_v-1), "= "+str(nb_v), "> "+str(nb_v)]
        )
        - 2
    )
    if nb_b == -2:
        nb_b = None
    degre_min = Ta.terminal_input_num_borne(
        "Degre minimum (= 0 aucune filtre):", 0, nb_v - 1
    )
    if degre_min < 2:
        if degre_min == 0:
            degre_min = None
        degre_max = Ta.terminal_input_num_borne(
            "Degre maximum (= " + str(nb_v) + " aucune filtre):", 2, nb_v
        )
    else:
        degre_max = Ta.terminal_input_num_borne(
            "Degre maximum (= " + str(nb_v) + " aucune filtre):", degre_min, nb_v
        )
    if degre_max == nb_v:
        degre_max = None
    question = "Motif contenant au moins une fois le(s) élément(s)?"
    lst_in = Ta.terminal_question_text_choice(question,lst_color)
    question = "Motif contenant aucune fois le(s) élément(s)?"
    lst_out = Ta.terminal_question_text_choice(question,lst_color)
    lst_elem = []
    if lst_out != None:
        for elem in lst_color :
            if elem not in lst_out:
                lst_elem.append(elem)
    if len(lst_elem) == 0:
        lst_elem = None
    res = [None, True, False]
    question = "Motif contenant une liaison hydrogène?"
    h_bool = Ta.terminal_question_choice(question,["Pas de filtre", "Au moins 1", "Aucune"])
    h_bool = res[h_bool]
    return [nb_b, degre_min, degre_max, lst_in, lst_elem, h_bool]

# Sélectionne les motifs selon leur coloration, taille et un filtre
def select_motifs(coll, db_ids, size, filter):
    lst_res = []
    test = {"color": ObjectId(db_ids[1]), "nb_v": size}
    if filter[0] != None:
        if filter[0] == 1:
            test["nb_b"] = {"$gt": size}
        else:
            test["nb_b"] = size + filter[0]
    if filter[1] != None:
        test["degre_min"] = filter[1]
    if filter[2] != None:
        test["degre_max"] = filter[2]
    if filter[3] != None or filter[4] != None:
        test["$and"] = []
        if filter[4] != None:
            test["$and"].append({'lst_v': {'$not': {'$elemMatch': {'$nin': filter[4]}}}})
        if filter[3] != None:
            for elem in filter[3]:
                test["$and"].append({'lst_v':elem})
    if filter[5] != None:
        test["haveHbond"] = filter[5]
    print(test)
    for data in coll.aggregate(Fp.pipeline_motif_filter_struct(db_ids, test)):
        lst_res.append(data["_id"])
    return lst_res

# Cherche un filtre pour une taille et une coloration données
def test_filter(db, db_ids, size, lst_color):
    question = "Appliquer un filtre sur les motifs de taille "+str(size)+"?"
    message = "Filtre"
    if Ta.terminal_question_On(question, message, "Oui", True):
        tab_filter = select_filter(size, lst_color)
    else :
        tab_filter = [None, None, None, None, None, None]
    lst_motifs = select_motifs(db.motifs, db_ids, size, tab_filter)
    print(str(len(lst_motifs))+" motifs correspondant parmi les informations sur cette structure.")
    while Ta.terminal_question_On("Changer le filtre?", "", "Non", False):
        tab_filter = select_filter(size, lst_color)
        lst_motifs = select_motifs(db.motifs, db_ids, size, tab_filter)
        print(str(len(lst_motifs))+" motifs correspondant parmi les informations sur cette structure.")
    return lst_motifs

# Selection d'un motif à suivre
def select_the_motif(db, db_ids, db_names, lst_elmt, options):
    test = True
    number = None
    file_path = "Inputs/Place_Folder_here/"
    name_dir = "motif_solo"
    if not isdir(join(file_path, name_dir)):
        mkdir(join(file_path, name_dir))
    while number == None and test : # tant qu'il n'y a pas de motif reconnu et si l'on souhaite en rechercher un
        number = Ta.terminal_input_num("Quel est le numéro du motif dans /motif_solo?", "Numéro motif")
        file_T = "trad-atom_motif"+str(number)+".txt"
        file_B = "bonds_motif"+str(number)+".txt"
        if isfile(join(file_path, name_dir, file_T)) and isfile(join(file_path, name_dir, file_B)):
            db_names[3] = Fr.extract_motif(db, options[0], lst_elmt, file_path, name_dir, file_T, file_B)
            # récupération de l'id du motif
            if db.motifs.count_documents({"sign": db_names[3], "color": ObjectId(db_ids[1])})>0 :
                print("Le motif est présent sur la BDD")
                motif = db.motifs.find_one({"sign": db_names[3], "color": ObjectId(db_ids[1])})
                db_ids[3] = motif["_id"]
            else :
                print("Le motif est absent de la BDD")
                test = False
                number = None
        else : # l'un des fichiers est absent
            print("Fichiers motif_solo/*_motif"+str(number)+".txt non trouvés")
            test = False
            number = None
        if not test :
            test = Ta.terminal_question_On("Voulez vous recommencer ?", "", "Oui", True)
    return test

# Questions des tailles
def select_size(max_size):
    # interrogation comparaison entre 2 tailles ou juste étude d'une taille
    question = "Comparer entre combien de tailles?"
    Multi_size = Ta.terminal_input_num_borne(question, 1, 2) == 2
    # choix de(s) taille(s)
    tab_size = []
    minimum = 3
    maximum = max_size
    if Multi_size:
        # Si il n'y a pas de choix
        if max_size == 3:
            tab_size.append(3)
            Multi_size = False
        elif max_size == 4:
            tab_size.append(3)
            tab_size.append(4)
        else:
            # Choisir les deux tailles différentes
            tab_size.append(
                Ta.terminal_input_num_borne("1ère taille :", minimum, maximum)
            )
            if tab_size[0] == maximum:
                maximum -= 1
            if tab_size[0] == minimum:
                minimum += 1
            tab_size.append(
                Ta.terminal_input_num_borne("2eme taille :", minimum, maximum)
            )
            while tab_size[0] == tab_size[1]:
                tab_size[1] = Ta.terminal_input_num_borne(
                    " Attend deux tailles différentes :",
                    minimum,
                    maximum,
                )
    else:
        # Si il n'y a pas de choix
        if minimum == maximum:
            tab_size.append(minimum)
        else:
            # Choisir la taille
            tab_size.append(Ta.terminal_input_num_borne("Taille :", minimum, maximum))
    return Multi_size, tab_size

# Choix du type de comparaison de similarite
def select_metric():
    question = "Par quel type de similarité sont comparés les motif du(des) groupe(s)? "
    choices = [
        "Ne pas analyser la similarité des motifs",
        "Similarité par cout d'édition",
        "Similarité par calcul de Raymond sur MCIS",
        "Similarité par calcul asymétrique sur MCIS",
    ]
    res = Ta.terminal_question_choice(question, choices)
    return res - 1

# Conversion d'une liste en chaine de caractères
def str_list(l, sep):
    s = ""
    for i in range(len(l)):
        if i > 0:
            s += sep
        s += str(l[i])
    return s

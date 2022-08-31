from bson.objectid import ObjectId

from Interfaces import Terminal_ask as Ta
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
def select_filter(nb_v):
    # interrogation si application de crible
    question = "Appliquer un filtre sur les motifs de taille "+str(nb_v)+"?"
    message = "Filtre"
    if Ta.terminal_question_On(question, message, "Oui", True):
        question = "Nombre de lien par rapport au nombre de sommet N?"
        nb_b = (
            Ta.terminal_question_choice(
                question, ["Aucun", "=N-1", "=N", ">N"]
            )
            - 2
        )
        if nb_b == -2:
            nb_b = None
        degre_min = Ta.terminal_input_num_borne(
            "Degre minimum (=0 aucune filtre):", 0, nb_v - 1
        )
        if degre_min < 2:
            if degre_min == 0:
                degre_min = None
            degre_max = Ta.terminal_input_num_borne(
                "Degre maximum (=" + str(nb_v) + " aucune filtre):", 2, nb_v
            )
        else:
            degre_max = Ta.terminal_input_num_borne(
                "Degre maximum (=" + str(nb_v) + " aucune filtre):", degre_min, nb_v
            )
        if degre_max == nb_v:
            degre_max = None
        res = [None, True, False]
        question = "Motif contenant un oxygène appartenant à une molécule d'eau?"
        ow_bool = Ta.terminal_question_choice(question,["Pas de filtre", "Au moins 1", "Aucun"])
        ow_bool = res[ow_bool]
        question = "Motif contenant une liaison hydrogène?"
        h_bool = Ta.terminal_question_choice(question,["Pas de filtre", "Au moins 1", "Aucune"])
        h_bool = res[h_bool]
        return [nb_b, degre_min, degre_max, ow_bool, h_bool]
    return [None, None, None, None, None]

# Sélectionne les motifs selon leur coloration, taille et un filtre
def select_motifs(coll, color, size, filter):
    lst_res = []
    test = {"color": ObjectId(color), "nb_v": size}
    if filter[0] != None:
        if filter[0] == 1:
            test["nb_b"] = {"$gt": size}
        else:
            test["nb_b"] = size + filter[0]
    if filter[1] != None:
        test["degre_min"] = filter[1]
    if filter[2] != None:
        test["degre_max"] = filter[2]
    if filter[3] != None:
        test["haveOW"] = filter[3]
    if filter[4] != None:
        test["haveHbond"] = filter[4]
    if coll.count_documents(test) > 0:
        for motif in coll.find(test):
            lst_res.append(motif["_id"])
    return lst_res

# Cherche un filtre pour une taille et une coloration données
def test_filter(db, db_ids, size):
    tab_filter = select_filter(size)
    lst_motifs = select_motifs(db.motifs, db_ids[1], size, tab_filter)
    print(str(len(lst_motifs))+" motifs sélectionnables.")
    while not Ta.terminal_question_On("Conserver ce filtre?", "Filtre", "Oui", True):
        tab_filter = select_filter(size)
        lst_motifs = select_motifs(db.motifs, db_ids[1], size, tab_filter)
        print(str(len(lst_motifs))+" motifs sélectionnables.")
    return lst_motifs

# Questions des tailles
def select_size(max_size):
    # interrogation comparaison entre 2 tailles ou juste étude d'une taille
    question = "Analyser une seule taille ou comparer 2 tailles?"
    choices = ["Une taille", "Deux tailles"]
    Multi_size = Ta.terminal_question_choice(question, choices) == 1
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
    question = "Quel type de similarité étudier? "
    choices = [
        "Aucune comparaison",
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

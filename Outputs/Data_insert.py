from bson.objectid import ObjectId
from bson.binary import Binary

from Interfaces import Terminal_ask as Ta
from Outputs import Graphlet_draw as Gld

# converti le certificat en un str de signature plus court
def convert_sign(certif):
    # reconnait la chaine comme un hexadécimal
    sign = certif.hex()
    # retire les 0 en trop devant
    while sign[0] == "0":
        sign = sign[1:]
    return sign


# récupère les indices des sommets d'une combinaison de sommets
def get_combi_vertex_ref(combi):
    ref = []
    # pour tous les sommets du graphe sur la combinaison
    for i in range(0, len(combi)):
        # ajouter s'il appartienne au sous-graphe
        if combi[i]:
            ref.append(i)
    return ref


# restitue les informations du sous-graphe sous le format pour la base de donnée
def convert_graph(ref, tab_atom, matrix_bonds):
    # liste des éléments et liaisons
    lst_vertex = []
    lst_bonds = []
    # autres valeurs
    nb_bond = 0
    degre_min = -1
    degre_max = -1
    # pour chaque sommet reconstitue ses caractéristiques et ses adjacences
    for i in ref:
        degre = 0
        # copie des caractéristiques
        splitted = tab_atom[i].split()
        lst_vertex.append(splitted[0])
        # copie des liaisons avec d'autres sommets du sous-graphe
        for j in ref:
            if j != i:
                if matrix_bonds[i][j]:
                    degre += 1
                    if i < j and matrix_bonds[j][i]:
                        lst_bonds.append([1, ref.index(i), ref.index(j)])
                        nb_bond += 1
                    elif not matrix_bonds[j][i]:
                        lst_bonds.append([2, ref.index(i), ref.index(j)])
                        nb_bond += 1
                elif matrix_bonds[j][i]:
                    degre += 1
        if degre < degre_min or degre_min == -1:
            degre_min = degre
        if degre > degre_max or degre_max == -1:
            degre_max = degre
    return lst_vertex, lst_bonds, nb_bond, degre_min, degre_max


## Extrait le document d'une recherche par _id
##ATTENTION## erreur possible si introuvé
def extract_byId(collection, id):
    result = collection.find_one({"_id": ObjectId(id)})
    return dict(result)

# Insert un motif seul
def insert_motif(motifs, sign, color_id, tab_atom, matrix_bonds, combi):
    ### Reconstruit le document du motif
    # récupre les indices dans le graphe original
    ref = get_combi_vertex_ref(combi)
    nb_vertex = len(ref)

    # reconstitue les paramètres du graphe
    lst_vertex, lst_bonds, nb_bond, degre_min, degre_max = convert_graph(
        ref, tab_atom, matrix_bonds
    )

    # test si il y a un élément OW
    bool_OW = "OW" in lst_vertex
    # test si il y a une liaison H
    bool_H = False
    for bond in lst_bonds:
        if bond[0]==2:
            bool_H = True

    # le document d'un motif
    motif = {
        "sign": sign,
        "color": ObjectId(color_id),
        "nb_v": nb_vertex,
        "nb_b": nb_bond,
        "lst_v": lst_vertex,
        "lst_b": lst_bonds,
        "degre_min": degre_min,
        "degre_max": degre_max,
        "haveOW": bool_OW,
        "haveHbond": bool_H,
    }
    # insert le motif à la base de données
    result = motifs.insert_one(motif)
    if nb_vertex < 5 :
        Gld.draw_graphlet(result.inserted_id, lst_vertex, lst_bonds, lst_vertex)
        data = open("Outputs/Place_Output_here/motifs/draw_" + str(result.inserted_id) + ".png", mode='rb').read()
        motifs.find_one_and_update({'_id':result.inserted_id},{"$set":{'img': Binary(data)}})
    return result.inserted_id


# Insert l'ensemble des occurrences de motifs dans la configuration étudiée
def insert_occurs_motifs(
    db_ids,  # identifiants de la base de données [structure, coloration]
    occurs,  # collection des occurrences
    motifs,  # collection des motifs
    conf_num,  # numéro de la configuration où occure le motif
    tab_atom,  # traduction des atomes de la configuration
    matrix_bonds,  # matrice d'adjacence de la configuration
    lst_certif,  # liste des certificats rangé avec leur indice
    lst_index,  # liste des indices des certificats d'une taille (groupe par taille)
    dict_isomorph,  # dictionnaire des occurrences de motifs (isomorphes)
    dict_stat,  # dictionnaire des statistiques sur les motifs
):
    for index in lst_index:
        ## Signature
        sign = convert_sign(lst_certif[index])

        ## Motif de la config
        # Si motif déjà présent?
        if motifs.count_documents({"sign": sign, "color": ObjectId(db_ids[1])}) > 0:
            result = motifs.find_one({"sign": sign, "color": ObjectId(db_ids[1])})
            motif_id = result["_id"]
        else:
            # dict_isomorph = {id : [combi*]}
            combis = dict_isomorph.get(index)
            motif_id = insert_motif(
                motifs, sign, db_ids[1], tab_atom, matrix_bonds, combis[0]
            )
        ## Occurrence du motif dans cette config
        # Si déjà présent?
        if (
            occurs.count_documents(
                {
                    "motif": ObjectId(motif_id),
                    "struct": ObjectId(db_ids[0]),
                    "config": ObjectId(db_ids[2][conf_num]),
                }
            )
            > 0
        ):
            result = occurs.find_one(
                {
                    "motif": ObjectId(motif_id),
                    "struct": ObjectId(db_ids[0]),
                    "config": ObjectId(db_ids[2][conf_num]),
                }
            )
            # Comparer les résultats
        else:
            stats = dict_stat.get(index)

            occur = {
                "motif": ObjectId(motif_id),
                "struct": ObjectId(db_ids[0]),
                "color": ObjectId(db_ids[1]),
                "config": ObjectId(db_ids[2][conf_num]),
                "repetition": stats[0],  # multiplier par le nombre d'apparition de la conf
                "cover_rate": stats[2],
                "distr_rate": stats[3],
            }
            # créé l'occurrence
            result = occurs.insert_one(occur)

    return True


# Ajout d'une nouvelle coloration dans la BDD
def insert_color(colors, db_ids, db_names, options):
    name = input("Nom de la coloration : ")
    while colors.count_documents({"name":name}) > 0 :
        name = input(name+" exites déjà. Autre nom : ")
    # la liste des elements (index +1 pour les numéros réels)
    list_color = []
    element = "temp"
    while element != "":
        element = input("Quel est le nom de l'élément (ne rien rentrer pour finir)? ")
        list_color.append(str(element))
    # Hydrogène ou non ?
    if "H" in list_color:
        print("Les Hydrogènes sont présents.")
        options[0] = True
    else:
        question = "Doit-on retirer les Hydrogène et déplacer les liaisons H ?"
        options[0] = not Ta.terminal_question_On(question, "", "Oui", True)
    color = {"name": name,
            "elements": list_color,
            "haveH": options[0]}
    # insertion dans la bdd
    result = colors.insert_one(color)
    db_ids[1] = result.inserted_id
    db_names[1] = name
    return list_color

# Ajoute une coloration à partir d'une ligne de fichier
def insert_color_direct(colors, text):
    splitted = text.split(' ')
    name = splitted[0]
    if colors.count_documents({"name":name}) > 0 :
        print("Error : color already charged (name)")
        return -1
    if splitted[1][0] == '[' and splitted[1][-1] == ']' :
        #print(splitted[1], splitted[1][1:-1])
        splitted[1] = splitted[1][1:-1]
        listed = splitted[1].split(',')
    else :
        print("Error : file incorrect (list coloration)")
        return -1
    splitted[2] = splitted[2].lower()
    if splitted[2] == "true" :
        test = True
    elif splitted[2] == "false" :
        test = False
    else :
        print("Error : file incorrect (boolean)")
        return -1
    color = {"name": name,
            "elements": listed,
            "haveH": test}
    # insertion dans la bdd
    result = colors.insert_one(color)
    #print(name, listed, test)
    return result.inserted_id, listed, test


# Ajoute la coloration à celles utilisées pour la structure
def insert_struct_color(struct, db_ids):
    ## ajouter la coloration sur l'interface
    result = struct.find_one({"_id":ObjectId(db_ids[0])})
    if ObjectId(db_ids[1]) not in result["colors"]:
        struct.find_one_and_update({"_id":ObjectId(db_ids[0])}, {'$push':{"colors":ObjectId(db_ids[1])}})


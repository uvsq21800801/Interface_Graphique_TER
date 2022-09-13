from bson.objectid import ObjectId

from Interfaces import Compare_process as Cp

# Pipeline pour filtre les motif selon la structure en plus du filtre
def pipeline_motif_filter_struct(db_ids, dict_filter):
    return [{
            '$match': dict_filter
        }, {
            '$lookup': {
                'from': 'occurrences', 
                'localField': '_id', 
                'foreignField': 'motif', 
                'as': 'occurs'
            }
        }, {
            '$unwind': {
                'path': '$occurs', 
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$addFields': {
                'test': {
                    '$eq': [
                        '$occurs.struct', ObjectId(db_ids[0])
                    ]
                }
            }
        }, {
            '$match': {
                'test': True
            }
        }, {
            '$group': {
                '_id': '$_id'
            }
        }
    ]

# Pipeline pour distribution sur structure complète
def complete_struct(struct_id, color_id):
    return [
        {"$match": {"struct": ObjectId(struct_id), "color": ObjectId(color_id)}},
        {
            "$project": {
                "motif": 1,
                "repetition": 1,
                "cover_rate": {"$multiply": ["$cover_rate", "$repetition"]},
                "distr_rate": {"$multiply": ["$distr_rate", "$repetition"]},
            }
        },
        {
            "$group": {
                "_id": "$motif",
                "repetition": {"$sum": "$repetition"},
                "cover": {"$sum": "$cover_rate"},
                "distr": {"$sum": "$distr_rate"},
            }
        },
        {
            "$project": {
                "_id": 1,
                "repetition": 1,
                "cover_rate": {"$divide": ["$cover", "$repetition"]},
                "distr_rate": {"$divide": ["$distr", "$repetition"]},
            }
        },
        {"$sort": {"repetition": 1, "cover_rate": 1, "distr_rate": 1}},
    ]

# Pipeline pour distribution sur structure complète (prise en compte des répétitions de conf)
def complete_struct_join(struct_id, color_id):
    return[
        {"$match": {"struct": ObjectId(struct_id), "color": ObjectId(color_id)}},
        {
            '$lookup': {
                'from': 'configurations', 
                'localField': 'config', 
                'foreignField': '_id', 
                'as': 'confOb'
            }
        }, { '$unwind': '$confOb'},
        {
            '$project': {
                'motif': 1, 
                'cumul': {
                    '$multiply': [
                        '$repetition', '$confOb.number' # remplacer number par repetition une fois ajouter aux conf
                    ]
                }, 
                'cover_rate': 1, 
                'distr_rate': 1
            }
        }, {
            '$project': {
                'motif': 1, 
                'cumul': 1, 
                'cover_rate': {
                    '$multiply': [
                        '$cover_rate', '$cumul'
                    ]
                }, 
                'distr_rate': {
                    '$multiply': [
                        '$distr_rate', '$cumul'
                    ]
                }
            }
        }, {
            '$group': {
                '_id': '$motif', 
                'cumul': {
                    '$sum': '$cumul'
                }, 
                'cover': {
                    '$sum': '$cover_rate'
                }, 
                'distr': {
                    '$sum': '$distr_rate'
                }
            }
        }, {
            '$project': {
                '_id': 1, 
                'repetition': '$cumul', 
                'cover_rate': {
                    '$divide': [
                        '$cover', '$cumul'
                    ]
                }, 
                'distr_rate': {
                    '$divide': [
                        '$distr', '$cumul'
                    ]
                }
            }
        }, {
            '$sort': {
                'repetition': 1, 
                'cover_rate': 1, 
                'distr_rate': 1
            }
        }
    ]

# Pipeline pour distribution sur une configuration de la structure
def unique_config(struct_id, color_id, config_id):
    return [
        {
            "$match": {
                "struct": ObjectId(struct_id),
                "color": ObjectId(color_id),
                "config": ObjectId(config_id),
            }
        },
        {
            "$project": {
                "_id": "$motif",
                "repetition": 1,
                "cover_rate": 1,
                "distr_rate": 1,
            }
        },
        {"$sort": {"repetition": 1, "cover_rate": 1, "distr_rate": 1}},
    ]

# Construction d'une table de résultats sur la liste de motifs
def construct_1tab(db, pipeline, lst_motifs):
    tab_res = [] # liste des résultats [rep, cover, distr, _id]
    for data in db.occurrences.aggregate(pipeline):
        # Applique les filtres sur les motifs (par la table motifs)
        if data["_id"] in lst_motifs:
            tab_res.append(
                [
                    data["repetition"],
                    data["cover_rate"],
                    data["distr_rate"],
                    data["_id"],
                ]
            )
    return tab_res

# Construction des deux tables de résultats sur 2 liste de motifs
def construct_2tab(db, pipeline, lst_motifs1, lst_motifs2):
    tab_res1 = []  # 1ere liste des résultats [rep, cover, distr, _id]
    tab_res2 = []  # 2eme liste des résultats [rep, cover, distr, _id]
    for data in db.occurrences.aggregate(pipeline):
        # Applique les filtres sur les motifs (par la table motifs)
        if data["_id"] in lst_motifs1:
            tab_res1.append(
                [
                    data["repetition"],
                    data["cover_rate"],
                    data["distr_rate"],
                    data["_id"],
                ]
            )
        if data["_id"] in lst_motifs2:
            tab_res2.append(
                [
                    data["repetition"],
                    data["cover_rate"],
                    data["distr_rate"],
                    data["_id"],
                ]
            )
    return tab_res1, tab_res2

# Construction de la matrice de chaleur sur 1 groupe
def construct_matrix_1g(db, type, tab_res):
    if type >= 0:
        # Valeurs des similarités
        tab_sim = [
            [0.0 for _ in range(len(tab_res))] for _ in range(len(tab_res))
        ]  # tableau de similarité des 2 listes
        for i in range(len(tab_sim)):
            if type == 0:
                tab_sim[i][i] = 0.0
            else:
                tab_sim[i][i] = 1.0
            for j in range(i + 1, len(tab_sim)):
                if type < 2:
                    idi = tab_res[i][3]
                    idj = tab_res[j][3]
                    tab_sim[i][j] = float(Cp.search_simil(db, idi, idj, type))
                    tab_sim[j][i] = tab_sim[i][j]
                else:
                    idi = tab_res[i][3]
                    idj = tab_res[j][3]
                    tab_sim[i][j] = float(Cp.search_simil(db, idi, idj, type))  # min
                    tab_sim[j][i] = float(
                        Cp.search_simil(db, idi, idj, type + 1)
                    )  # max
    else:
        tab_sim = None
    return tab_sim

# Construction de la matrice de chaleur sur 2 groupe
def construct_matrix_2g(db, type, tab_res1, tab_res2):
    if type >= 0 and type < 2:
        # Valeurs des similarités
        tab_sim = [
            [[m1[3], m2[3]] for m1 in tab_res1] for m2 in tab_res2
        ]  # tableau de similarité des 2 listes
        for i in range(len(tab_res2)):
            for j in range(len(tab_res1)):
                idi = tab_res2[i][3]
                idj = tab_res1[j][3]
                tab_sim[i][j] = float(Cp.search_simil(db, idi, idj, type))
    else:
        tab_sim = None
    return tab_sim

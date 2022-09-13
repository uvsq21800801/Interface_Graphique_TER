import networkx as nx
from Solving import nx_convert as nxC

from bson.objectid import ObjectId
from Outputs import Data_insert as Di

from Solving import Similarity as Sim

# Lance la recherche des similarités connues
# Envoie en comparaison les motifs sans similaritée connue
def compare_motifs(db, id1, id2):
    # recherche les 2 motifs
    motif1 = Di.extract_byId(db.motifs, id1)
    G1 = nxC.construct_graph_bdd(motif1["lst_v"], motif1["lst_v"])
    motif2 = Di.extract_byId(db.motifs, id2)
    G2 = nxC.construct_graph_bdd(motif2["lst_v"], motif2["lst_v"])
    # construit le Mcis
    Mcis = nxC.construct_mcis(G1, G2)
    # calcul les 3 similarités
    cdef float de = Sim.distance_edition(G1, G2)
    cdef float sr = Sim.sim_raymond(Mcis, G1, G2)
    cdef float sbm = Sim.sim_raymond_asym(Mcis, G1, G2, True)
    cdef float sbp = Sim.sim_raymond_asym(Mcis, G1, G2, False)
    # ajoute les 3 similarités à la BDD
    db.similarities.insert_one(
        {"motif1": ObjectId(id1), "motif2": ObjectId(id2), "values": [de, sr, sbm, sbp]}
    )
    return [de, sr, sbm, sbp]


# Recherche la valeur de similarité du numéro indiqué (indice dans values)
def search_simil(db, id1, id2, num):
    # Cas de comparer un motif avec lui-même
    if id1 == id2:
        if num == 0:
            return 0.0
        else:
            return 1.0
    # Sinon recherche dans la DBB
    elif (
        db.similarities.count_documents(
            {"motif1": ObjectId(id1), "motif2": ObjectId(id2)}
        )
        == 0
    ):
        if (
            db.similarities.count_documents(
                {"motif1": ObjectId(id2), "motif2": ObjectId(id1)}
            )
            == 0
        ):
            # Si introuvable, alors on la construit
            res = compare_motifs(db, id1, id2)
            return res[num]
        else:
            res = db.similarities.find_one(
                {"motif1": ObjectId(id2), "motif2": ObjectId(id1)}
            )
            return res["values"][num]
    else:
        res = db.similarities.find_one(
            {"motif1": ObjectId(id1), "motif2": ObjectId(id2)}
        )
        return res["values"][num]

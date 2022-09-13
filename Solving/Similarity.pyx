import networkx as nx
from Solving import nx_convert as nxg

'''
######## Etude de la similarité de motifs
'''

# Distance d'édition
def distance_edition(sgA, sgB):
    cdef float res = nx.graph_edit_distance(sgA,sgB,node_match=nxg.colors_match,edge_match=nxg.edge_col_match)
    return res

# Metrique de Raymond symétrique
def sim_raymond(g_mcis, g_a, g_b):
    cdef float res 
    cdef float val_a 
    cdef float val_b
    if g_mcis == -1 :
        return 0.0
    else:
        # calcul similarité de raymond
        res = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
        res *= res
        val_a = g_a.number_of_edges()+g_a.number_of_nodes()
        val_b = g_b.number_of_edges()+g_b.number_of_nodes()
        res /= (val_a*val_b)
        return res

# Metrique de Raymond asymétrique
def sim_raymond_asym(g_mcis, g_a, g_b, minimum):
    cdef float res 
    cdef float val_a 
    cdef float val_b
    
    # cas où il n'y a pas de mcis
    if g_mcis == -1 :
        return 0.0
    else :
        # calcul similarité de raymond
        res = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
        val_a = g_a.number_of_edges()+g_a.number_of_nodes()
        val_b = g_b.number_of_edges()+g_b.number_of_nodes()
        if minimum:
            res /= min(val_a,val_b)
        else:
            res /= max(val_a,val_b)
        return res
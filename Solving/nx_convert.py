import networkx as nx

# Converti une combinaison de sommets en sa matrice d'ajacence et liste d'atomes
#
# Entrées : matrice d'adjacence (transfert des valeurs des cases aveuglément)
#           caractéristique des atomes (transfert du contenu aveuglément)
#           et combinaisons de sommet du motif (compatible str, bool et [0|1])
#
# Sorties : matrice d'adjacence et caractéristique des atomes du motif
def convert_combi(matrix_bonds, tab_atom, combi):
    # initialise les sorties
    new_matrix_bonds = []
    new_tab_atom = []
    # pour tous les sommets du graphe original
    for i in range(0, len(combi)):
        # s'il appartienne au sous-graphe
        if int(combi[i])==1:
            # copie des caractéristiques
            new_tab_atom.append(tab_atom[i])
            line_bonds = []
            # copie des liaisons avec d'autres sommets du sous-graphe
            for j in range(0, len(combi)):
                if int(combi[j])==1:
                    line_bonds.append(matrix_bonds[i][j])
            new_matrix_bonds.append(line_bonds)
    return new_matrix_bonds, new_tab_atom
#

# Construit un graphe Networkx avec une liste de lien et une liste d'atome
#
# Entrées : liste des atomes et liste des liens
#
# Sortie : graphe "coloré" sur les sommets et arêtes
def construct_graph_bdd (lst_vertex, lst_edge):
    # Déclare les structures
    G = nx.Graph()
    
    # Ajoute les sommets et gère les couleurs
    for i in range(len(lst_vertex)):
        G.add_node(i, color = lst_vertex[i])
    
    # Ajoute les arcs et arêtes selon les liens du motif
    for x in lst_edge:
        if x[0]==1:
            G.add_edge(x[1] , x[2] , color="black")
        if x[0]==2:
            G.add_edge(x[1] , x[2] , color="red")
    return G
#

# Construit un digraphe Networkx avec une liste de lien et une liste d'atome
#
# Entrées : liste des atomes et liste des liens
#
# Sortie : digraphe "coloré" sur les sommets et arêtes
def construct_digraph_bdd (lst_vertex, lst_edge):
    # Déclare les structures
    G = nx.DiGraph()
    
    # Ajoute les sommets et gère les couleurs
    for i in range(len(lst_vertex)):
        G.add_node(i, color = lst_vertex[i])
    
    # Ajoute les arcs et arêtes selon les liens du motif
    for x in lst_edge:
        if x[0]==1:
            G.add_edge(x[1] , x[2] , color="black")
            G.add_edge(x[2] , x[1] , color="black")
        if x[0]==2:
            G.add_edge(x[1] , x[2] , color="red")
    return G
#

# Fonction de comparaison des colorations de noeuds
#
# Entrées : attributs des 2 noeuds
#
# Sorties : Booleen
def colors_match(n1_attrib,n2_attrib):
    '''returns False if either does not have a color or if the colors do not match'''
    try:
        return n1_attrib['color']==n2_attrib['color']
    except KeyError:
        print('Error in colors_match')
        return False
#

# Fonction de comparaison des colorations d'arêtes
#
# Entrées : attributs des 2 arêtes
#
# Sorties : Booleen
def edge_col_match(a1_attrib,a2_attrib):
    '''returns False if either does not have a color or if the colors do not match'''
    try:
        return a1_attrib['color']==a2_attrib['color']
    except KeyError:
        print('Error in edge_col_match')
        return False
#

# Fonction pour construire le MCIS de deux graphes
#
# Entrées : les 2 graphes à comparer
#
# Sorties : le MCIS ou -1
def construct_mcis(g_a, g_b):
    # Utilise l'algorithme d'isomorphisme ISMAGS
    ismags = nx.isomorphism.ISMAGS(g_a,g_b,node_match=colors_match, edge_match=edge_col_match)
    # sur les résultats d'ISMAGS resort le MCIS
    largest_common_sub = list(ismags.largest_common_subgraph())
    
    if(largest_common_sub != []):
        # Prend les sommets du MCIS et le construit
        ls_nodes_mcis = largest_common_sub[0].keys()
        g_mcis = g_a.subgraph(ls_nodes_mcis)
        return g_mcis
    # cas où il n'y a pas de MCIS
    return -1
#
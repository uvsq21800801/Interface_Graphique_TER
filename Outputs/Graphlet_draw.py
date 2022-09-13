import networkx as nx
import matplotlib.pyplot as plt
from Outputs import element_color as elmc
import os

# Construit le DiGraph networkX avec les informations format BDD
def construct_graplet_forDraw(atom_colors, lst_vertex, lst_bonds):
    # Déclare les structures
    node_colors = []
    edges_black = []
    edges_red = []
    G = nx.DiGraph()

    # Ajoute les sommets et gère les couleurs
    for i in range(len(lst_vertex)):
        node_color = atom_colors.get(lst_vertex[i])
        G.add_node(i, label=lst_vertex[i])
        node_colors.append(node_color)

    # Ajoute les arcs et arêtes selon les liens du motif
    for x in lst_bonds:
        if x[0] == 1:
            G.add_edge(x[1], x[2], color="black")
            edges_black.append((x[1], x[2]))
        if x[0] == 2:
            G.add_edge(x[1], x[2], color="red")
            edges_red.append((x[1], x[2]))

    return G, node_colors, edges_black, edges_red


# Créé le dessin du graph avec le DiGraph networkx et les informations de couleur
def create_graphlet_picture(G, node_colors, edges_black, edges_red, motif_id):
    plt.clf()
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, edgecolors=None)
    node_labels = nx.get_node_attributes(G, "label")
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    nx.draw_networkx_edges(
        G, pos, edgelist=edges_black, edge_color="black", arrows=False
    )
    nx.draw_networkx_edges(
        G, pos, edgelist=edges_red, edge_color="red", arrows=True, arrowstyle="->"
    )

    # le chemin des sorties
    out_path = "Outputs/Place_Output_here/motifs"
    out_path_exist = os.path.exists(out_path)
    if (not out_path_exist):
        os.makedirs(out_path)
    plt.savefig("Outputs/Place_Output_here/motifs/draw_" + str(motif_id) + ".png")
    # print("dessin sauvegardé dans Outputs/Place_Output_here/motifs/draw_" + str(motif_id) + ".png")


# Dessine un graph à partir d'un identifiant, des caractéristiques sous le format BDD
# et la liste d'élément considéré dans la coloration
def draw_graphlet(motif_id, lst_vertex, lst_bonds, lst_elem):
    # Définit les couleurs sur la liste de la coloration de référence
    atom_colors = {}
    for e in lst_elem:
        if e in elmc.element.keys():
            atom_colors[e] = elmc.element.get(e)
        else:
            atom_colors[e] = "#ff1493"

    # Construit les structures
    G, node_colors, edges_black, edges_red = construct_graplet_forDraw(
        atom_colors, lst_vertex, lst_bonds
    )

    # Créé l'image du graphlet
    create_graphlet_picture(G, node_colors, edges_black, edges_red, motif_id)

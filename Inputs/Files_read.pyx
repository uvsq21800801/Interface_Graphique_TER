from os import listdir, remove
from os.path import isfile, isdir, join
import re
import numpy as np
cimport numpy as np
from bson.objectid import ObjectId
from operator import itemgetter
from pynauty import certificate

from Interfaces import Terminal_ask as Term
from Solving import Isomorphism as Iso
from Outputs import Data_insert as Di


###
### name_file_T ou file_T : trad-atom_conf[number].txt
### name_file_B ou file_B : bonds_conf[number].txt
### option : True = tout ; False = pas les hydrogènes
###

# Récupère le nom du dossier de travail
def Get_dir_name(path_I):
    namefolder_check = False
    while namefolder_check == False:
        dir_I = input("Quel est le nom du dossier? ")
        if isdir(join(path_I, dir_I)):
            return dir_I
        else: 
            print("Erreur : ce dossier n'existe pas")

# Récupération des données des fichiers d'une même configuration
#
# Entrées : option haveH, chemin vers le dossier,
#           dossier de l'interface, noms des 2 fichiers
#
# Sorties : liste des anciens indices, tableau des atomes et matrice des liens
def Files_read(option, path, name_dir, name_file_T, name_file_B):
    
    path_dir = join(path, name_dir)
    cdef int nb_sommet = Get_nb_vertex(option, join(path_dir,name_file_T))
    tab_atom = np.empty((nb_sommet,), dtype='<U32')
    cdef np.ndarray[np.int32_t, ndim=1] lst_index = np.empty(nb_sommet, dtype=np.int32)
    nb_test = File_read_atom_trad(option, path_dir, name_file_T, lst_index, tab_atom)
    matrix_bonds = np.zeros((nb_sommet,nb_sommet),dtype=bool)
    read_test = File_read_bonds(option, path_dir, name_file_B, lst_index, matrix_bonds)

    return lst_index, tab_atom, matrix_bonds
#

# Recherche les fichiers des configurations
#
# Entrées : chemin vers le dossier et dossier de l'interface
#
# Sorties : listes des fichiers (trad-atom et bonds) et les numéros des configurations
def Search_files_conf(path, name_dir):
    files_T = {}
    files_B = {}
    conf_num = []
    # demande quelles configurations (toutes ou ensemble de numéros)
    question = "Quels sont les configurations étudiées?"
    while len(files_T)==0:
        res = Term.terminal_ensemble_num(question)
        if -1 in res:
            #tous les duos trouvés
            for f in Extract_files(join(path, name_dir), "bonds"):
                part = f.split("conf")
                part = part[1].split('.')
                if part[0].isnumeric():
                    i = int(part[0])
                    t_name = "trad-atom_conf"+part[0]+".txt"
                    b_name = "bonds_conf"+part[0]+".txt"
                    # si le deuxième existe alors on ajoute la conf à la liste
                    if isfile(join(path,name_dir,t_name)):
                        conf_num.append(i)
                        files_T[i] = t_name
                        files_B[i] = b_name
        else :
            conf_num = list(res)
            # les duos désignés
            # recherche chaque numéro et les ajoute aux sorties un à un
            for i in conf_num:
                t_name = "trad-atom_conf"+str(i)+".txt"
                b_name = "bonds_conf"+str(i)+".txt"
                # si les deux fichiers existent alors on les ajoute aux listes
                if isfile(join(path,name_dir,t_name)) and isfile(join(path,name_dir,b_name)):
                    files_T[i] = t_name
                    files_B[i] = b_name
                else :
                    conf_num.remove(i)
        conf_num.sort()
    return files_T, files_B, conf_num
#

# Extrait la liste des noms de fichiers contenant une partie donnée
# 
# Entrées : chemin dans le dossier, partie du nom devant apparraître
#
# Sortie : liste des fichiers
def Extract_files(path_dir, part_name):
    files = []
    for f in listdir(path_dir):
        if isfile(join(path_dir,f)) and part_name in f:
            files.append(f)
    return files
#

# Retourne le nombre de sommets dans le fichier de traduction
# 
# Entrées : option haveH et chemin vers le fichier à tester
# 
# Sortie : nombre de sommets décompté (moins les Hydrogène si haveH faux)
def Get_nb_vertex(option, path_file):
    # récum du fichier
    f = open(path_file, 'r').readlines()
    
    # ajoute 1 pour chaque sommet qui nous intéresse
    cdef int count_verticles = 0
    for line in f:
        splitted = line.split()
        # test needed to exclude the first like
        if len(splitted) == 3:
            if (option == False and splitted[1] != 'H') or (option == True):
                count_verticles += 1
    return count_verticles
#

# Lis le fichier trad-atom.txt pour remplir les structures
# 
# Entrées : option(haveH), chemin, nom fichier, liste d'anciens indices (lst_index)
#            et tableau de caractéristiques des atomes (tab_atom)
# 
# Sortie : nombre d'atomes traités ou None
def File_read_atom_trad(option, path_dir, name_file_T, li, ta):
    # si le nom est bien représenté, on récupère les données
    cdef int i = 0
    if isfile(join(path_dir, name_file_T)):
        # lecture du fichier des "traductions" des atomes
        f = open(join(path_dir,name_file_T), 'r').readlines()
        for line in f:
            splitted = line.split()
            # si la ligne correspond au format et est informative
            if len(splitted) == 3:
                # si l'option est fausse et le sommet est un H, alors le sommet est ignoré
                if (option == False and splitted[1] != 'H') or (option == True):
                    # l'ancien numéro de l'atome est stocké
                    li[i] = splitted[0]
                    # le nom de l'atome est stocké 
                    # avec le numéro associé sur l'image de la configuration
                    tmp = splitted[2]
                    txt_car = splitted[1]+' '+tmp[len(splitted[1]):]
                    ta[i] = txt_car
                    i += 1
        return i
    else :
        return None
#

# Lis le fichier trad-atom.txt pour remplir les structures
# 
# Entrées : option(haveH), chemin, nom fichier, liste d'anciens indices (lst_index)
#            et matrice des liaisons entre atomes (matrix_bond)
# 
# Sortie : booléen si le fichier est reconnu ou non
def File_read_bonds(option, path_dir, name_file_B, li, ma ):    
    # si le nom est bien représenté, on récupère les données

    if isfile(join(path_dir,name_file_B)):
        # lecture du fichier bonds et transcription dans la matrice d'adjacence
        f = open(join(path_dir,name_file_B), 'r').readlines()
        for line in f:
            splitted = line.split()
            # liaison covalente
            if splitted[0] == '1' and len(splitted) == 3:
                if int(splitted[1]) in li and int(splitted[2]) in li:
                    #ajoute un lien symétrique pour différencier les liaisons covalentes
                    ma[np.where(li == int(splitted[1]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True
                    ma[np.where(li == int(splitted[2]))[0][0]][np.where(li == int(splitted[1]))[0][0]] = True
            # liaison hydrogene
            if splitted[0] == '4' and len(splitted) == 4:
                if int(splitted[1]) in li and int(splitted[2]) in li:
                    if option == False : # hydrogènes non présents dans le graphe
                        #ajoute un lien de l'atomes donneur vers l'accepteur
                        ma[np.where(li == int(splitted[1]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True
                    elif option == True and int(splitted[3]) in li:
                        #ajoute un lien de l'hydrogène vers l'accepteur
                        ma[np.where(li == int(splitted[3]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True
        return True
    else :
        return False
#

# Recupère un fichier de motif
def extract_motif(db, option, lst_elmt, path, name_dir, name_file_T, name_file_B):
    lst_index, tab_atom, matrix_bonds = Files_read(option, path, name_dir, name_file_T, name_file_B)
    ref = [i for i in range(len(lst_index))]
    # identification du motif (signature)
    g = Iso.construct_pynauty_graph(matrix_bonds, tab_atom, lst_elmt, ref)
    certif = certificate(g)
    sign = Di.convert_sign(certif)
    return sign

def read_parameters_file(path, filename):
    if isfile(join(path, filename)):
        # lecture du fichier bonds et transcription dans la matrice d'adjacence
        f = open(join(path,filename), 'r').readlines()
        if 'C' in f[0] and len(f) >= 2:
            return 1, f[1], None, None, None
        elif 'S' in f[0] and len(f) >= 5:
            return 2, f[1], f[2], f[3], f[4]
    return 0, None, None, None, None
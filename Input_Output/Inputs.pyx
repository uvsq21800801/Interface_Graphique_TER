from os import listdir, remove
from os.path import isfile, join
import re
import numpy as np
cimport numpy as np

from User_interface import commande_terminal as ct

###
### option : True = tout ; False = pas les hydrogènes
###

###
# 1. Fonctions de lecture et écriture sur fichiers
###

# recuperation des donnees d'un type de fichier
def data_input(option, dir, filename_T, filename_B):
    
    complete_path = 'Inputs_Outputs/Place_Folder_here/'+str(dir)#+'/'+str(filename_T)
    cdef int nb_sommet = Get_nb_vertex(option, complete_path+'/'+filename_T)
    atom_caract = np.empty((nb_sommet,), dtype='<U32')
    cdef np.ndarray[np.int32_t, ndim=1] lst_index = np.empty(nb_sommet, dtype=np.int32)
    filename1 = Input_trad(complete_path, option, filename_T, lst_index, atom_caract)
    matrice_adja = np.zeros((nb_sommet,nb_sommet),dtype=bool)
    filename2 = Input_bonds(complete_path, option, filename_B, lst_index, matrice_adja)

    ''' 
    lst_index = []
    atom_caract = []
    filename1 = Input_trad(option, name, lst_index, atom_caract)
    matrice_adja = []
    filename2 = Input_bonds(option, name, lst_index, matrice_adja)
    '''
    return filename1, filename2, lst_index, atom_caract, matrice_adja

# Recherche des fichiers des configurations
#
# Entrées : path d'entré et dossier de l'interface
#
# Sorties : liste des fichier de trad-atom, de bonds et des numéros de configurations

def recherche_files_conf (path_I, dir_I):
    files_T = {}
    files_B = {}
    conf_num = []
    # demande si toutes les conf ou désigné(s)
    question = "Quels sont les configurations étudiées?"
    res = ct.terminal_ensemble_num(question)
    if -1 in res:
        #tous les duos trouvés
        for f in extrait_files(path_I, dir_I, "bonds"):
            part = f.split("conf")
            part = part[1].split('.')
            if part[0].isnumeric():
                i = int(part[0])
                t_name = "trad-atom_conf"+str(i)+".txt"
                b_name = "bonds_conf"+str(i)+".txt"
                # si le deuxième existe alors on ajoute la conf à la liste
                if isfile(join(path_I,dir_I,t_name)):
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
            if isfile(join(path_I,dir_I,t_name)) and isfile(join(path_I,dir_I,b_name)):
                files_T[i] = t_name
                files_B[i] = b_name
            else :
                conf_num.remove(i)
    conf_num.sort()
    print(conf_num)
    print("files_T"+str(files_T))
    print("files_B"+str(files_B))
    return files_T, files_B, conf_num

# Fonction qui extrait la liste des noms de fichier
# contenant la partie en paramètre

def extrait_files(path, dir, part_name):
    files = []
    for f in listdir(join(path,dir)):
        if isfile(join(path,dir,f)) and part_name in f:
            files.append(f)
    return files

###
# 2. Fonctions de récupération de données d'atomes
###

# retourne le nombre de sommets qui nous intéresse
def Get_nb_vertex(option, compl_path):
    # récum du fichier
    f1 = open(compl_path, 'r').readlines()
    
    # ajoute +1 pour chaque sommet qui nous intéresse
    cdef int count_verticles = 0
    for line in f1:
        splitted = line.split()
        # test needed to exclude the first like
        if len(splitted) == 3:
            if (option == False and splitted[1] != 'H') or (option == True):
                count_verticles += 1    

    return count_verticles

# Retourne le contenu d'un fichier texte pour un nom donné
def Input_trad(cfpath, option, filename_T, li, atom_caract):
    # si le nom est bien représenté, on récupère les données
    cdef int i = 0
    if isfile(join(cfpath, filename_T)):
        # lecture du fichier bonds et transcription dans la matrice de traduction
        f1 = open(join(cfpath,filename_T), 'r').readlines()
        for line in f1:
            splitted = line.split()
            if len(splitted) == 3:
                
                if (option == False and splitted[1] != 'H') or (option == True):
                    #li.append(splitted[0])
                    li[i] = splitted[0]

                    # Liste de traduction suivant le modele '[type atome] [numero]'
                    temp = splitted[2]
                    caracteristiques = splitted[1]+' '+temp[len(splitted[1]):]
                    atom_caract[i] = caracteristiques
                    #print(splitted[0]+' '+splitted[1]+' '+splitted[2])
                    i += 1
        return "name"
    else :
        return ""

###
# 3. Fonctions de récupération de données de liaisons
###

def Input_bonds(cfpath, option, filename_B, li, ma ):    
    # si le nom est bien représenté, on récupère les données

    if isfile(join(cfpath,filename_B)):
        #initie la matrice d'adjacence
        #init_matrice(ma,len(li))

        # lecture du fichier bonds et transcription dans la matrice d'adjacence
        f1 = open(join(cfpath,filename_B), 'r').readlines()
        
        #print(li)
        
        for line in f1:
            splitted = line.split()
            # liaison covalente

            if splitted[0] == '1' and len(splitted) == 3:
                if int(splitted[1]) in li and int(splitted[2]) in li:
                    ma[np.where(li == int(splitted[1]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True
                    ma[np.where(li == int(splitted[2]))[0][0]][np.where(li == int(splitted[1]))[0][0]] = True
            # liaison hydrogene
            if splitted[0] == '4' and len(splitted) == 4:
                if int(splitted[1]) in li and int(splitted[2]) in li:
                    if option == False : # hydrogènes non présents dans le graphe
                        #ajoute un 2 de l'atomes donneur vers l'accepteur
                        ma[np.where(li == int(splitted[1]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True # 2 changé en 1 pour optimiser la matrice en bool
                    elif option == True and int(splitted[3]) in li:
                        #ajoute un 2 de l'hydrogène vers l'accepteur
                        ma[np.where(li == int(splitted[3]))[0][0]][np.where(li == int(splitted[2]))[0][0]] = True # 2 changé en 1 pour optimiser la matrice en bool
        #print(ma)
        return "name"
    else :
        #print(ma)
        return ""

###
# 5. Fonctions utile à la lecture ou l'écriture de données
###

# Récupère le nom dans les formats type_name.txt
def get_name(filename):
    name1 = filename.split('_',1)
    name2 = name1[1].split('.')
    return name2[0]

# Fichiers déjà existant et donc calcul probablement non utile
def done(name, detail):
    if detail[0] == 1 :
        compl = "_H"
    else :
        compl = ""
    fpath = "Inputs_Outputs/Place_Output_here/"
    filename1 = name+compl+"_data.txt"
    filename2 = name+compl+"_res.txt"
    # tests si les 2 fichiers existes déjà
    if isfile(join(fpath, filename1)) and isfile(join(fpath, filename2)):
        return True
    else:
        return False

# Fichiers déjà existant dans le dossier donné et donc calcul probablement inutile
def done_here(fpath, name, detail):
    if detail[0] == 1 :
        compl = "_H"
    else :
        compl = ""
    filename1 = name+compl+"_data.txt"
    filename2 = name+compl+"_res.txt"
    # tests si les 2 fichiers existes déjà
    if isfile(join(fpath, filename1)) and isfile(join(fpath, filename2)):
        return True
    else:
        return False

# Initie la matrice d'adjacence pour stocker les données
def init_matrice(matrice, taille):
    for i in range(taille):
        matrice.append([])
        for j in range(taille):
            matrice[i].append(0)


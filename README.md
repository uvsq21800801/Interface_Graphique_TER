# Interface_Graphique_TER

# fichiers utilisés

**Main.py**: Permet d'appeler la fonctione de fenêtre de choix des tailles pour l'interface (Display_Graph/Choice_size.py).
**Choice_size.py**: Affiche une fenêtre de séléction des tailles. Les options sont fournies par les informations de la base
de donnée (fonction d'appel de la bdd dans Inputs/Database_create.py).
**Database_create.py**:
**Clickable_display.py**: Affiche matrice de chaleur, courbes d'occurence et de recouvrement... L'interface est également cliquable. Lorsque une case de la matrice de chaleur, ou un axe vertical d'une courbe est cliqué, l'image des ensembles d'atomes concernés seront affichés sur la même fenêtre.

## Lancer le programme:
Lancement du programme principal:
```bash
  python3 Main.py
```

Commande à utiliser pour chercher les choses à optimiser en cython
```
cython -a chemin/nom_fichier.pyx
```
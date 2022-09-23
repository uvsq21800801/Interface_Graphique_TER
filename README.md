# Interface_Graphique_TER
> Affichage interactif de Graphétarium

## Dépendences:
Avant de lancer l'application, entrez cela dans le terminal depuis le dossier contenant ce Readme:
``` bash
  pip install -r requirement.txt
```

Après avoir ajouté de nouvelles dépendences au projet, il ne faut pas oublier de mettre à jour la liste.

Pour la visualisation des motifs avec Draw.py, il faut avoir installer eog sur Unix.

## Avant de lancer le programme:
Il faut ajouter un .env dans Inputs/ avec CLIENT_URI associé au cluster de MongoDb souhaité ou alors les données seront déposés dans localhost.

## Lancer le programme:
Lancement du programme principal:
```bash
  python3 Main.py
```

Commande à utiliser pour chercher les choses à optimiser en cython
```
cython -a chemin/nom_fichier.pyx
```

## fichiers utilisés
* Les dossiers **Interfaces**, **Solving**, **Inputs** et **Outputs** sont les dossiers originaux de Graphétarium. Certaines fonctions de ceux-ci sont réutilisées dans ce programme. 

**Main.py**: Permet d'appeler la fonctione de fenêtre de choix des tailles pour l'interface (Display_Graph/Choice_size.py).

* Dossier **Display_Graph** : 
  * *Choice_size.py*: Affiche une fenêtre de séléction des tailles. Les options sont fournies par les informations de la base de donnée (fonction d'appel de la bdd dans Inputs/Database_create.py). Après avoir rempli les choix et validé, Display_Graph/Clickable_display.py ou Display_Graph/Clickable_occur_recouv.py sera appelé, selon le choix de l'utilisateur.
  * *Clickable_display.py*: Affiche matrice de chaleur, diagramme à barre d'occurence et de recouvrement... L'interface est également cliquable. Lorsque une case de la matrice de chaleur, ou un axe vertical d'une courbe est cliqué, l'image des ensembles d'atomes concernés seront affichés sur la même fenêtre. (note: seul la matrice de chaleur est cliquable, les dragrammes ne le sont pas)
  * *Clickable_occur_recouv.py*: Affiche le diagramme à barre et d'occurence cliquable d'une taille séléctionnée.

Dessins des motifs dans Outputs/Place_Output_here/motifs :
**draw_[id_ du motif].png**
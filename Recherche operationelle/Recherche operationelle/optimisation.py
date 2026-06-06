## Harry MBENGMO

"""
Algorithme de Bin Packing 1D (Rangement unidimensionnel).
Cette version simplifiée ne prend en compte que la longueur des objets (les autres dimensions sont ignorées).
Elle utilise l'heuristique First-Fit (Premier arrivé, premier casé) dans un contexte Online 
(les objets sont traités dans leur ordre d'arrivée, sans tri préalable).
"""

import time
import csv

# Constantes
LONGUEUR_WAGON = 11.583
LARGEUR_WAGON = 2.294
HAUTEUR_WAGON = 2.569
NB_MARCHANDISES = 100

class Marchandise:
    """
    Modélisation basique d'une marchandise pour le problème 1D.
    Seule la propriété 'longueur' sera réellement exploitée par l'algorithme.
    """
    def __init__(self, id_marchandise, nom, longueur, largeur, hauteur):
        self.id = int(id_marchandise)
        self.nom = nom
        # Remplacement des éventuelles virgules par des points pour la conversion en float
        self.longueur = float(str(longueur).replace(',', '.'))
        self.largeur = float(str(largeur).replace(',', '.'))
        self.hauteur = float(str(hauteur).replace(',', '.'))

def online_1d(table):
    """
    Algorithme First-Fit pour le problème de rangement 1D (Online).
    Pour chaque objet, on essaie de le placer dans le premier wagon ayant assez de place.
    S'il ne rentre dans aucun wagon existant, on ouvre un nouveau wagon.
    Retourne la liste complète des wagons utilisés.
    """
    wagons = [] # Format: [{"espace_restant": X, "items": []}, ...]
    
    for marchandise in table:
        place = False
        
        # ÉTAPE 1 : Chercher de la place dans les wagons déjà ouverts (Stratégie First-Fit)
        for j in range(len(wagons)):
            if marchandise.longueur <= wagons[j]["espace_restant"]:
                wagons[j]["espace_restant"] -= marchandise.longueur
                wagons[j]["items"].append(marchandise)
                place = True
                break
        
        # ÉTAPE 2 : Si l'objet n'a pu être placé nulle part, on est obligé d'ouvrir un nouveau wagon
        if not place:
            nouveau_wagon = {
                "espace_restant": LONGUEUR_WAGON - marchandise.longueur,
                "items": [marchandise]
            }
            wagons.append(nouveau_wagon)
            
    return wagons

def charger_donnees(fichier_path, n):
    """Importation des données depuis le fichier CSV"""
    objets = []
    try:
        with open(fichier_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                # Vérifie qu'il y a bien 5 colonnes (id;nom;longueur;largeur;hauteur)
                if len(row) >= 5:
                    objets.append(Marchandise(row[0], row[1], row[2], row[3], row[4]))
                # On arrête la lecture si on a atteint le nombre max
                if len(objets) == n:
                    break
    except FileNotFoundError:
        print(f"Erreur : Impossible de trouver le fichier '{fichier_path}'")
        exit(1)
        
    return objets

if __name__ == "__main__":
    """
    Point d'entrée du script. 
    Exécute l'algorithme 1D très basique pour évaluer ses performances par rapport aux versions 2D/3D.
    """
    time1 = time.time() # Début du chronomètre

    # Chargement des données
    tab = charger_donnees("Données_marchandises.csv", NB_MARCHANDISES)

    # Exécution de l'algorithme
    wagons = online_1d(tab)
    print(f"Nombre de wagons utilisés : {len(wagons)}")

    time2 = time.time() # Fin du chronomètre
    print(f"Temps d'exécution : {time2 - time1:.6f} secondes")
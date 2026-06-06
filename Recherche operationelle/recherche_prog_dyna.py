### Programmation dynamique ###

import csv
import math
import time


# Modélisation d'un objet pouvant être placé dans le sac
class Objet: 
    def __init__(self, nom, masse, utilite):
        self.nom = nom
        self.masse = float(masse)
        self.utilite = float(utilite)


def data(fichier_path):
    """
    Importation des données des objets depuis un fichier CSV.
    Retourne une liste d'instances de la classe Objet.
    """
    objets = []
    with open(fichier_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if len(row) >= 3:
                objets.append(Objet(row[0], row[1], row[2]))
    return objets


def sac_a_dos_dynamique(objets, poids_max_float):
    """
    Résout le problème du sac à dos en utilisant la Programmation Dynamique.
    Cette méthode garantit la solution optimale en explorant systématiquement les sous-problèmes.
    """
    n = len(objets)
    # La programmation dynamique nécessite des indices de tableau entiers pour le poids.
    # On multiplie par un facteur (ici 100) pour transformer un poids décimal (ex: 0.60) en entier (60).
    facteur = 100 
    W = round(poids_max_float * facteur) # Capacité maximale du sac transformée en entier

    poids = [round(obj.masse * facteur) for obj in objets]

    # Création de la matrice de programmation dynamique (DP) initialisée à 0
    # dp[i][w] représentera l'utilité maximale possible en utilisant les 'i' premiers objets pour une capacité de 'w'
    dp = [[0.0] * (W + 1) for _ in range(n + 1)]

    # ÉTAPE 1 : Remplissage de la matrice de bas en haut (Bottom-up)
    for i in range(1, n + 1):
        w_i = poids[i - 1]
        v_i = objets[i - 1].utilite
        for w in range(W + 1):
            if w_i <= w: # Si l'objet courant a un poids inférieur ou égal à la capacité courante 'w'
                # On compare deux choix : inclure l'objet (val_avec) ou ne pas l'inclure (val_sans)
                val_avec = dp[i - 1][w - w_i] + v_i
                val_sans = dp[i - 1][w]
                dp[i][w] = val_avec if val_avec > val_sans else val_sans
            else:
                # L'objet est trop lourd pour la capacité 'w', on ne l'inclut pas
                dp[i][w] = dp[i - 1][w]

    # ÉTAPE 2 : Retracer le chemin dans la matrice pour identifier les objets exacts à emporter (Backtracking)
    utilite_max = dp[n][W]
    res = utilite_max
    w = W
    index_choisis = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if abs(dp[i][w] - dp[i - 1][w]) > 1e-6:
            index_choisis.append(i - 1)
            res -= objets[i - 1].utilite
            w -= poids[i - 1]

    index_choisis.reverse()

    return utilite_max, index_choisis

def run_dyna():
    """
    Fonction conçue pour être appelée depuis une interface web (webapp).
    Exécute l'algorithme et retourne un dictionnaire contenant les résultats et les métriques de temps.
    """
    import time
    start = time.time()
    objets = data("datas.csv")
    poids_max = 0.60
    
    utilite_max, index_choisis = sac_a_dos_dynamique(objets, poids_max)
    
    choisis = [objets[i] for i in index_choisis]
    masse_totale = sum(o.masse for o in choisis)
    
    end = time.time()
    
    return {
        "time_ms": (end - start) * 1000,
        "items": [{"nom": o.nom, "masse": o.masse, "utilite": o.utilite} for o in choisis],
        "poids_total": masse_totale,
        "utilite_totale": utilite_max,
        "poids_max": 0.60
    }

if __name__ == "__main__":
    """
    Point d'entrée pour l'exécution directe du script dans la console.
    Permet de tester l'algorithme et d'afficher les résultats.
    """
    time1 = time.time()

    objets = data("datas.csv")
    poids_max = 0.60

    utilite_max, index_choisis = sac_a_dos_dynamique(objets, poids_max)

    print(f"Utilité maximale trouvée : {utilite_max:.2f}\n")
    print("Objets ajoutés au sac :")

    masse_totale = 0.0
    for i in index_choisis: # Affichage des détails de chaque objet retenu par l'algorithme
        obj = objets[i]
        print(f" - {obj.nom} (Masse: {obj.masse:.2f}, Utilité: {obj.utilite:.2f})")
        masse_totale += obj.masse

    time2 = time.time()
    print(f"\nTemps d'exécution : {time2 - time1:.6f} secondes")

    
## Harry MBENGMO
## Hector JODON DE VILLEROCHE

### Algorithme glouton ###

import time ## importation de la librairie time
time1 = time.time()

import csv ## importation de la librairie csv

class Objet:
    def __init__(self, nom, masse, utilite): ## initialisation des variables
        self.nom = nom ## nom de l'objet
        self.masse = float(masse) ## masse de l'objet
        self.utilite = float(utilite) ## utilite de l'objet
        self.ratio = 0.0 ## ratio utilite/masse

    def __repr__(self): ## representation des objets
        return f"{self.nom} {self.masse:.2f} {self.utilite:.2f} {self.ratio:.2f}"


def calcul_ratio(objets): ## calcul du ratio utilite/masse des objets
    for obj in objets:
        obj.ratio = obj.utilite / obj.masse ## calcul du ratio utilite/masse


def trirapide(B, debut, fin): ## tri rapide des objets par ratio
    if debut < fin:
        pivot = B[debut].ratio
        i = debut + 1
        j = fin

        while i <= j:
            while i <= j and B[i].ratio <= pivot:
                i += 1
            while i <= j and B[j].ratio > pivot:
                j -= 1
            if i < j:
                B[i], B[j] = B[j], B[i]

        B[debut], B[j] = B[j], B[debut]
        trirapide(B, debut, j - 1)
        trirapide(B, j + 1, fin)


def additionner_objets(objets): ## additionner les objets par ratio
    poids_max = 0.60
    masse_courante = 0.0
    utilite_courante = 0.0
    choisis = []

    for obj in reversed(objets):
        if masse_courante == poids_max:
            break
        if masse_courante + obj.masse <= poids_max:
            masse_courante += obj.masse
            utilite_courante += obj.utilite
            choisis.append(obj)
            
    return choisis, masse_courante, utilite_courante

def run_glouton():
    start = time.time()
    objets = data("datas.csv")
    n = len(objets)
    calcul_ratio(objets)
    trirapide(objets, 0, n - 1)
    choisis, masse_totale, utilite_totale = additionner_objets(objets)
    end = time.time()
    
    return {
        "time_ms": (end - start) * 1000,
        "items": [{"nom": o.nom, "masse": o.masse, "utilite": o.utilite} for o in choisis],
        "poids_total": masse_totale,
        "utilite_totale": utilite_totale,
        "poids_max": 0.60
    }


def data(fichier_path): ## data des objets
    objets = [] ## liste des objets
    with open(fichier_path, "r", encoding="utf-8") as f: ## ouverture du fichier
        reader = csv.reader(f, delimiter=";") ## lecture du fichier
        for row in reader:
            if len(row) >= 3:
                nom, masse, utilite = row[0], row[1], row[2]
                objets.append(Objet(nom, masse, utilite))
    return objets


if __name__ == "__main__":
    time1 = time.time()
    objets = data("datas.csv")
    n = len(objets)

    calcul_ratio(objets)

    for obj in objets:
        print(obj)

    trirapide(objets, 0, n - 1)
    choisis, masse, util = additionner_objets(objets)
    for c in choisis:
        print(c.nom, end=" ")
    print()

    time2 = time.time()
    print("Temps d'exécution :", time2 - time1)

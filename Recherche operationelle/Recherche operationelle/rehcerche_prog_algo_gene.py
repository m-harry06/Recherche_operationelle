## Harry MBENGMO

### Algorithme génétique ###

import time
import random
import csv

# Constantes du problème et de l'algorithme génétique
TAILLE = 23 # Nombre total d'objets disponibles
POIDS_MAX = 0.6 # Capacité maximale du sac à dos
TAILLE_POPULATION = 100 # Nombre d'individus dans chaque génération

# Modélisation d'un objet pouvant être placé dans le sac
class Objet:
    def __init__(self, nom, masse, utilite):
        self.nom = nom
        # Remplacement d'une éventuelle virgule par un point pour la conversion (gestion des formats français/anglais)
        self.masse = float(str(masse).replace(',', '.'))
        self.utilite = float(str(utilite).replace(',', '.'))

# Modélisation d'un individu (représente une solution potentielle = un sac à dos spécifique)
class Individu:
    def __init__(self):
        # Le génome: une liste de 0 et de 1. (1 = l'objet est dans le sac, 0 = l'objet n'y est pas)
        self.gennes = [0] * TAILLE
        self.score = 0.0 # Utilité totale des objets dans le sac (Fitness)
        self.masse_totale = 0.0 # Poids total des objets dans le sac

# ---------------------------------------------------------
# FONCTIONS DE L'ALGORITHME GÉNÉTIQUE
# ---------------------------------------------------------

def charger_donnees(fichier_path, n):
    """
    Importation des données des objets depuis un fichier CSV.
    Retourne une liste d'instances de la classe Objet.
    """
    objets = []
    try:
        with open(fichier_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if len(row) >= 3:
                    nom, masse, utilite = row[0], row[1], row[2]
                    objets.append(Objet(nom, masse, utilite))
                if len(objets) == n:
                    break
    except FileNotFoundError:
        print(f"Erreur : Impossible de trouver le fichier '{fichier_path}'")
        exit(1)
    return objets

def initialisation_population():
    """
    Crée la première génération d'individus aléatoirement.
    Chaque gène a 5% de chance d'être à 1 (objet sélectionné).
    """
    population = []
    for _ in range(TAILLE_POPULATION):
        ind = Individu()
        for j in range(TAILLE):
            ind.gennes[j] = 1 if random.randint(0, 99) < 5 else 0
        population.append(ind)
    return population

def evaluation(population, objets):
    """
    Évalue chaque individu de la population.
    Calcule le poids total et l'utilité (score) de chaque sac à dos.
    Applique une pénalité sévère si le poids maximal est dépassé.
    """
    for ind in population:
        ind.masse_totale = 0.0
        ind.score = 0.0
        
        for j in range(TAILLE):
            if ind.gennes[j] == 1:
                ind.masse_totale += objets[j].masse
                ind.score += objets[j].utilite
                
        # Arrondi pour éviter les problèmes de précision des flottants (ex: 0.600000001)
        ind.masse_totale = round(ind.masse_totale, 2)
        ind.score = round(ind.score, 2)
                
        # LA PUNITION PROGRESSIVE 
        if ind.masse_totale > POIDS_MAX:
            ind.score = ind.score - (ind.masse_totale - POIDS_MAX) * 1000.0

def selection(population):
    """
    Sélectionne un parent pour la reproduction par la méthode du tournoi :
    On prend deux individus au hasard et on garde le meilleur.
    """
    a = random.randint(0, TAILLE_POPULATION - 1)
    b = random.randint(0, TAILLE_POPULATION - 1)
    
    if population[a].score > population[b].score:
        return a
    return b

def croisement(pere, mere):
    """
    Croisement uniforme : crée deux enfants à partir de deux parents.
    Pour chaque gène, l'enfant 1 prend soit le gène du père, soit de la mère (50% de chance).
    L'enfant 2 prend le gène de l'autre parent.
    """
    enfant1 = Individu()
    enfant2 = Individu()
    
    for i in range(TAILLE):
        if random.choice([0, 1]) == 0:
            enfant1.gennes[i] = pere.gennes[i]
            enfant2.gennes[i] = mere.gennes[i]
        else:
            enfant1.gennes[i] = mere.gennes[i]
            enfant2.gennes[i] = pere.gennes[i]
            
    return enfant1, enfant2

def mutation(elu):
    """
    Mutation génétique : introduit de la diversité.
    Chaque gène de l'individu a 5% de chance de s'inverser (0 devient 1, 1 devient 0).
    """
    for i in range(TAILLE):
        if random.randint(1, 100) <= 5:
            elu.gennes[i] = 1 - elu.gennes[i]

def main():
    """
    Fonction principale exécutant l'algorithme génétique pour résoudre le problème du sac à dos.
    """
    time1 = time.time() # Début du chronomètre
    
    # ÉTAPE 1 : Chargement des données et création de la population initiale
    objets = charger_donnees("datas.csv", TAILLE)
    population = initialisation_population()
    evaluation(population, objets)
    
    # ÉTAPE 2 : Boucle principale de l'évolution (1000 générations)
    for gen in range(1000):
        # ÉLITISME : On garde une copie stricte du meilleur pour ne jamais perdre l'optimum
        meilleur_actuel = max(population, key=lambda ind: ind.score)
        elite = Individu()
        elite.gennes = meilleur_actuel.gennes[:]
        elite.masse_totale = meilleur_actuel.masse_totale
        elite.score = meilleur_actuel.score
        
        population_suivante = [elite]
        
        # Remplir la nouvelle génération deux par deux
        while len(population_suivante) < TAILLE_POPULATION:
            idx_pere = selection(population)
            idx_mere = selection(population)
            
            enfant1, enfant2 = croisement(population[idx_pere], population[idx_mere])
            
            mutation(enfant1)
            mutation(enfant2)
            
            population_suivante.extend([enfant1, enfant2])
            
        if len(population_suivante) > TAILLE_POPULATION:
            population_suivante.pop()
            
        # Évaluer la nouvelle population
        evaluation(population_suivante, objets)
        
        # Remplacer l'ancienne population
        population = population_suivante

    # ÉTAPE 3 : Fin de l'algorithme - Recherche de la meilleure solution trouvée
    # Extraction de l'individu ayant le meilleur score (utilité) dans la dernière population
    meilleur_individu = max(population, key=lambda ind: ind.score)

    print(f"Meilleur score (Utilité) : {meilleur_individu.score:.2f}")
    print(f"Masse totale : {meilleur_individu.masse_totale:.1f} sur {POIDS_MAX:.1f}")
    print("Contenu du sac :")
    
    for j in range(TAILLE):
        if meilleur_individu.gennes[j] == 1:
            print(f" - {objets[j].nom}")

    time2 = time.time() # Fin du chronomètre
    print(f"\nTemps d'exécution : {time2 - time1:.6f} secondes")

def run_gene():
    """
    Version de l'algorithme conçue pour être appelée depuis une interface web (webapp).
    Retourne les résultats au format dictionnaire (JSON) au lieu de les afficher dans la console.
    """
    time1 = time.time()
    
    objets = charger_donnees("datas.csv", TAILLE)
    population = initialisation_population()
    evaluation(population, objets)
    
    for gen in range(1000):
        # ÉLITISME
        meilleur_actuel = max(population, key=lambda ind: ind.score)
        elite = Individu()
        elite.gennes = meilleur_actuel.gennes[:]
        elite.masse_totale = meilleur_actuel.masse_totale
        elite.score = meilleur_actuel.score
        
        population_suivante = [elite]
        
        while len(population_suivante) < TAILLE_POPULATION:
            idx_pere = selection(population)
            idx_mere = selection(population)
            enfant1, enfant2 = croisement(population[idx_pere], population[idx_mere])
            mutation(enfant1)
            mutation(enfant2)
            population_suivante.extend([enfant1, enfant2])
            
        if len(population_suivante) > TAILLE_POPULATION:
            population_suivante.pop()
            
        evaluation(population_suivante, objets)
        population = population_suivante

    meilleur_individu = max(population, key=lambda ind: ind.score)
    time2 = time.time()
    
    choisis = []
    for j in range(TAILLE):
        if meilleur_individu.gennes[j] == 1:
            choisis.append(objets[j])

    #        
    return {
        "time_ms": (time2 - time1) * 1000,
        "items": [{"nom": o.nom, "masse": o.masse, "utilite": o.utilite} for o in choisis],
        "poids_total": meilleur_individu.masse_totale,
        "utilite_totale": meilleur_individu.score,
        "poids_max": POIDS_MAX
    }

if __name__ == "__main__":
    main()
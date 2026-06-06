import random
import math
import time
import dico

def run_offline_rs():
    import time
    temps_debut = time.perf_counter()
    donnees = dico.objets
    liste_objets = list(donnees.keys())

    temperature = 100.0
    taux_refroidissement = 0.995

    sac = {obj: 0 for obj in liste_objets}
    meilleure_utilite = 0
    meilleur_sac = sac.copy()
    meilleur_poids = 0

    while temperature > 0.01:
        obj = random.choice(liste_objets)
        sac[obj] = 1 - sac[obj]
        
        poids = round(sum(donnees[o]["poids"] for o in sac if sac[o] == 1), 2)
        utilite = round(sum(donnees[o]["utilite"] for o in sac if sac[o] == 1), 2)
        
        if poids <= 0.6:
            if utilite > meilleure_utilite:
                meilleure_utilite = utilite
                meilleur_sac = sac.copy()
                meilleur_poids = poids
            elif random.random() < math.exp((utilite - meilleure_utilite) / temperature):
                meilleure_utilite = utilite
                meilleur_poids = poids
            else:
                sac[obj] = 1 - sac[obj]
        else:
            sac[obj] = 1 - sac[obj]
            
        temperature *= taux_refroidissement

    temps_execution = (time.perf_counter() - temps_debut) * 1000
    objets_choisis = [o for o in meilleur_sac if meilleur_sac[o] == 1]

    return {
        "time_ms": temps_execution,
        "items": [{"nom": obj} for obj in objets_choisis],
        "poids_total": meilleur_poids,
        "utilite_totale": meilleure_utilite,
        "poids_max": 0.6
    }

if __name__ == "__main__":
    res = run_offline_rs()
    print("Objets à prendre :", [i["nom"] for i in res["items"]])
    print("Utilité totale maximale obtenue :", res["utilite_totale"])
    print(f"Temps d'exécution : {round(res['time_ms'], 4)} ms")
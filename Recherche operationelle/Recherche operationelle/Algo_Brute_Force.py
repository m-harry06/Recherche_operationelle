import itertools
import time  
import dico

def run_offline_bf():
    import time
    temps_debut = time.perf_counter()
    donnees = dico.objets
    meilleure_utilite = 0
    meilleur_sac = []
    meilleur_poids = 0

    for r in range(1, len(donnees) + 1):
        for combinaison in itertools.combinations(donnees.keys(), r):
            poids_total = sum(donnees[obj]["poids"] for obj in combinaison)
            espace_restant = 0.6 - poids_total
            
            if round(espace_restant, 2) == 0:
                utilite_total = sum(donnees[obj]["utilite"] for obj in combinaison)
                
                if utilite_total > meilleure_utilite:
                    meilleure_utilite = utilite_total
                    meilleur_sac = combinaison
                    meilleur_poids = poids_total

    temps_fin = time.perf_counter()
    temps_execution = (temps_fin - temps_debut) * 1000

    return {
        "time_ms": temps_execution,
        "items": [{"nom": obj} for obj in meilleur_sac],
        "poids_total": meilleur_poids,
        "utilite_totale": meilleure_utilite,
        "poids_max": 0.6
    }

if __name__ == "__main__":
    res = run_offline_bf()
    print("Objets à prendre :", [i["nom"] for i in res["items"]])
    print("Poids total :", round(res["poids_total"], 2), "kg")
    print("Utilité totale maximale obtenue :", round(res["utilite_totale"], 2))
    print(f"Temps d'exécution : {round(res['time_ms'], 2)} ms")
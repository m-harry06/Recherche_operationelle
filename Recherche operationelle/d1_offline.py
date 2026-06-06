# Hector Jodon de Villeroché
import dico_train
import time

temps_debut = time.time()
def trier_longueurs(dictionnaire_complet):
    #on prend le nom et la longueur
    liste_objets = [(nom, dimensions["Longueur"]) for nom, dimensions in dictionnaire_complet.items()]

    #on trie selon la longueur de manière décroissante 
    liste_objets.sort(key=lambda x: x[1], reverse=True)

    # Reconversion en dictionnaire
    return dict(liste_objets)


def charger_train_d1_offline(dico_simplifie_trie): #NFD
    LONGUEUR_MAX_WAGON = 11.583
    wagons_restants = []
    composition_wagons = []

    for nom, longueur in dico_simplifie_trie.items():
        place_trouvee = False

        for i in range(len(wagons_restants)):
            if wagons_restants[i] >= longueur:
                wagons_restants[i] -= longueur
                composition_wagons[i].append(nom)
                place_trouvee = True
                break

        if not place_trouvee:
            wagons_restants.append(LONGUEUR_MAX_WAGON - longueur)
            composition_wagons.append([nom])

    return composition_wagons, wagons_restants


def run_offline_1d():
    temps_debut = time.perf_counter()
    dico_trie = trier_longueurs(dico_train.objets)
    wagons, wagons_restants = charger_train_d1_offline(dico_trie)
    temps_fin = time.perf_counter()
    temps_execution = (temps_fin - temps_debut) * 1000

    wagons_data = []
    for i in range(len(wagons)):
        items_data = []
        for nom in wagons[i]:
            items_data.append({
                "nom": nom,
                "longueur": dico_train.objets[nom]["Longueur"]
            })
        wagons_data.append({
            "id": i,
            "espace_restant": wagons_restants[i],
            "items": items_data
        })

    return {
        "mode": "1D",
        "time_ms": temps_execution,
        "wagons_count": len(wagons),
        "wagons": wagons_data,
        "wagon_length": 11.583
    }

if __name__ == "__main__":
    res = run_offline_1d()
    print(f"Nombre de wagons complets : {res['wagons_count']}")

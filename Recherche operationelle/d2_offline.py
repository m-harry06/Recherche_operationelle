# Hector Jodon de Villeroché
import time
import dico_train

def trier_objets_2d(dictionnaire_complet):
    # Création d'une liste de tuples (nom, dimensions)
    liste_objets = list(dictionnaire_complet.items())
    
    #tri décroissant par rappart à la longueur, puis par la largeur
    liste_trie = sorted(
        liste_objets, 
        key=lambda item: (item[1]["Longueur"], item[1]["Largeur"]), #met la priorité sur la longueur, puis la largeur
        reverse=True #pour le tri decroissant
    )
    
    #remise des données dans un dico
    return dict(liste_trie)

def charger_train_2d_shelf(dico_trie):
    LONGUEUR_MAX_WAGON = 11.583
    LARGEUR_MAX_WAGON = 2.294
        
    wagons = [] 

    for nom, dimensions in dico_trie.items():
        obj_longueur = dimensions["Longueur"]
        obj_largeur = dimensions["Largeur"]
        place_trouvee = False

        #on parcours tous les wagons
        for wagon in wagons:
            for etagere in wagon["etageres"]:#si l'objet rentre en largeur sur l'etagere
                if obj_largeur <= etagere["largeur_restante"]:
                    etagere["objets"].append(nom)
                    etagere["largeur_restante"] -= obj_largeur
                    place_trouvee = True
                    break
            
            if place_trouvee:
                break
            
            #si il n'y a plus de place sur les etagères dans le wagon, on en créé une autre si on peut
            longueur_totale_etageres = 0
            for e in wagon["etageres"]:
                longueur_totale_etageres += e["longueur_max"]
            if longueur_totale_etageres + obj_longueur <= LONGUEUR_MAX_WAGON:
                nouvelle_etagere = {
                    "longueur_max": obj_longueur, # Défini par le premier objet de la ligne
                    "largeur_restante": LARGEUR_MAX_WAGON - obj_largeur,
                    "objets": [nom]
                }
                wagon["etageres"].append(nouvelle_etagere)
                place_trouvee = True
                break

        #si l'objet n'as pas de place on ouvre un nouveau wagon
        if not place_trouvee:
            nouveau_wagon = {
                "etageres": [{
                        "longueur_max": obj_longueur,
                        "largeur_restante": LARGEUR_MAX_WAGON - obj_largeur,
                        "objets": [nom]
                    }
                ]
            }
            wagons.append(nouveau_wagon)
    return wagons

def run_offline_2d():
    temps_debut = time.perf_counter()
    dico_trie = trier_objets_2d(dico_train.objets)
    wagons_brut = charger_train_2d_shelf(dico_trie)
    temps_fin = time.perf_counter()
    temps_calcul = (temps_fin - temps_debut) * 1000

    wagons_data = []
    for i, wagon in enumerate(wagons_brut):
        items_data = []
        x_offset = 0
        for etagere in wagon["etageres"]:
            y_offset = 0
            for nom in etagere["objets"]:
                w = dico_train.objets[nom]["Longueur"]
                h = dico_train.objets[nom]["Largeur"]
                
                # Extraire l'ID (le numéro à la fin du nom)
                mots = nom.split()
                id_court = mots[-1] if mots else nom
                
                items_data.append({
                    "id": id_court,
                    "nom": nom,
                    "x": x_offset,
                    "y": y_offset,
                    "w": w,
                    "h": h
                })
                y_offset += h
            x_offset += etagere["longueur_max"]
        
        wagons_data.append({
            "id": i,
            "items": items_data
        })

    return {
        "mode": "2D",
        "time_ms": temps_calcul,
        "wagons_count": len(wagons_brut),
        "wagons": wagons_data,
        "wagon_width": 11.583,
        "wagon_height": 2.294
    }

if __name__ == "__main__":
    res = run_offline_2d()
    print(f"Nombre de wagons complets: {res['wagons_count']}")
    print(f"Temps de calcul : {res['time_ms']:.6f} ms")
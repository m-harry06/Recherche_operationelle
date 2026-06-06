# Hector Jodon de Villeroché
import dico_train
import time 

temps_debut = time.time()

def charger_train_d1_online(dictionnaire_complet): #first fit
    LONGUEUR_MAX_WAGON = 11.583
    dico_simple = {} #on recupere que le nom et la longueur dans le dico
    for nom, dimensions in dictionnaire_complet.items():
        dico_simple[nom] = dimensions["Longueur"]
        
    #listes de l'espace restant et la composition de chaque wagon
    wagons_restants = []
    composition_wagons = []

    for nom, longueur in dico_simple.items():
        place_trouvee = False

        #On cherche le premier wagon qui a assez de place
        for i in range(len(wagons_restants)):
            if wagons_restants[i] >= longueur:
                wagons_restants[i] -= longueur
                composition_wagons[i].append(nom)
                place_trouvee = True
                break  #si l'objet est placé, on s'arrête pour cet objet

        #si aucun wagon existant n'a de place, on en crée un nouveau
        if not place_trouvee:
            wagons_restants.append(LONGUEUR_MAX_WAGON - longueur)
            composition_wagons.append([nom])

    return composition_wagons


wagons = charger_train_d1_online(dico_train.objets)

temps_fin = time.time()

temps_calcul = temps_fin - temps_debut


print(f"Nombre de wagons complets : {len(wagons)}")

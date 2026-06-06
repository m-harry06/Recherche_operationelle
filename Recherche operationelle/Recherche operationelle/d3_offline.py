# Hector Jodon de Villeroché

 

import time

from dico_train import objets

 

LONGUEUR_CONTENEUR, LARGEUR_CONTENEUR, HAUTEUR_CONTENEUR = 11.583, 2.294, 2.569

 

ROTATIONS_INTERDITES = ["Acide chlorhydrique", "Verre","Verre blanc vrac","Verre brun vrac","Vitraux","Carrelage","Tuiles","Briques","Briques","Ciment","Quicailleries","Treuil","Ardoises","Semi conducteurs","Lithium","Batterie","Moteur electrique","Pompe à chaleur"]

 

 

class EspaceVide:

    # création d'un repère pour utiliser la guillotine

    def __init__(self, x, y, z, longueur, largeur, hauteur):

        self.x, self.y, self.z = x, y, z

        self.longueur, self.largeur, self.hauteur = longueur, largeur, hauteur

       

class Wagon:

    # definition d'un conteneur

    def __init__(self):

        self.espaces_vides = [EspaceVide(0, 0, 0, LONGUEUR_CONTENEUR, LARGEUR_CONTENEUR, HAUTEUR_CONTENEUR)]

        self.objets_charges = []

 

    def inserer_objet(self, nom, lon_obj, larg_obj, haut_obj):

        # insertion d'un objet dans un conteneur + rotation pour qu'il prenne le moins de place

        self.espaces_vides.sort(key=lambda e: e.longueur * e.largeur * e.hauteur)

 

        for index, esp in enumerate(self.espaces_vides):

            for lon, larg, haut in obtenir_orientations(nom, lon_obj, larg_obj, haut_obj):

               

                # permet de verifier que l'objet ne depasse pas avant et apres rotation

                if lon <= esp.longueur and larg <= esp.largeur and haut <= esp.hauteur:

                    self.objets_charges.append({"nom": nom, "x": esp.x, "y": esp.y, "z": esp.z, "longueur": lon, "largeur": larg, "hauteur": haut})

                   

                    # mise à jour des espaces vides apres guillotine

                    self.espaces_vides.extend(self._decouper_espace(esp, lon, larg, haut))

                    self.espaces_vides.pop(index)

                    return True

        return False

 

    def _decouper_espace(self, esp, lon, larg, haut):

        # permet de créer avec guillotine de nouveau espaces vides

        nouveaux = []

        if esp.longueur - lon > 0: # À droite (Axe X)

            nouveaux.append(EspaceVide(esp.x + lon, esp.y, esp.z, esp.longueur - lon, esp.largeur, esp.hauteur))

        if esp.largeur - larg > 0: # Devant (Axe Y)

            nouveaux.append(EspaceVide(esp.x, esp.y + larg, esp.z, lon, esp.largeur - larg, esp.hauteur))

        if esp.hauteur - haut > 0: # Au-dessus (Axe Z)

            nouveaux.append(EspaceVide(esp.x, esp.y, esp.z + haut, lon, larg, esp.hauteur - haut))

        return nouveaux

 

 

def obtenir_orientations(nom, lon, larg, haut):

    # Si le nom de l'objet est dans la liste des interdits, on bloque la rotation

    if nom in ROTATIONS_INTERDITES:

        return [(lon, larg, haut)] # Renvoie uniquement l'orientation d'origine

       

    # Sinon, l'objet a le droit de tester toutes les rotations possibles

    return list({(lon, larg, haut), (lon, haut, larg), (larg, lon, haut),

                 (larg, haut, lon), (haut, lon, larg), (haut, larg, lon)})

 

 

def lancer_chargement_offline(dictionnaire_objets):

    # extraction des données et calcul du volume en une ligne

    liste_objets = [{"nom": k, "longueur": v["Longueur"], "largeur": v["Largeur"], "hauteur": v["Hauteur"], "volume": v["Longueur"] * v["Largeur"] * v["Hauteur"]} for k, v in dictionnaire_objets.items()]

   

    # Tri stratégique pour le Challenge Précision

    liste_objets.sort(key=lambda o: (max(o["longueur"], o["largeur"], o["hauteur"]), o["volume"]), reverse=True)

 

    # on regarde si l'objet rentre dans un wagon existant

    flotte_wagons = []

    for obj in liste_objets:

        place = False

        for wagon in flotte_wagons:

            if wagon.inserer_objet(obj["nom"], obj["longueur"], obj["largeur"], obj["hauteur"]):

                place = True

                break

       

        # sinon creation d'un nouveau wagon

        if not place:

            nouveau = Wagon()

            if nouveau.inserer_objet(obj["nom"], obj["longueur"], obj["largeur"], obj["hauteur"]):

                flotte_wagons.append(nouveau)

            else:

                print(f"Erreur : L'objet {obj['nom']} surpasse un wagon vide.")

               

    return flotte_wagons

def run_offline_3d():
    debut = time.perf_counter()
    train_final = lancer_chargement_offline(objets)
    temps_execution = (time.perf_counter() - debut) * 1000
    
    wagons_data = []
    for i, wagon in enumerate(train_final):
        items_data = []
        for obj in wagon.objets_charges:
            items_data.append({
                "id": obj["nom"],
                "nom": obj["nom"],
                "x": obj["x"],
                "y": obj["y"],
                "z": obj["z"],
                "w": obj["longueur"],
                "h": obj["largeur"],
                "d": obj["hauteur"]
            })
        wagons_data.append({
            "id": i,
            "items": items_data
        })
    
    return {
        "mode": "3D",
        "time_ms": temps_execution,
        "wagons_count": len(train_final),
        "wagons": wagons_data,
        "wagon_length": LONGUEUR_CONTENEUR,
        "wagon_width": LARGEUR_CONTENEUR,
        "wagon_height": HAUTEUR_CONTENEUR
    }

if __name__ == "__main__":
   
    debut = time.perf_counter()
    train_final = lancer_chargement_offline(objets)
    temps_execution = time.perf_counter() - debut
   
    print(f"RÉSULTATS : {len(train_final)} wagons | {temps_execution:.6f} secondes")
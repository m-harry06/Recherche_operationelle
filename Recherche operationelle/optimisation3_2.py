## Harry MBENGMO

"""
Algorithme de Bin Packing 3D (Rangement de conteneurs).
Utilise une heuristique Bottom-Left-Fill avec découpe Guillotine pour ranger des objets dans des wagons.
Optimisé pour la vitesse d'exécution extrême (utilisation de tuples, désactivation du Garbage Collector).
"""

import csv
import time
import math

L_WAGON = 11.583
LARG_WAGON = 2.294
H_WAGON = 2.569

# Liste des mots-cles pour les objets qui ne doivent pas etre retournes (mis sur le cote)
FRAGILES = ["acide", "verre", "vitraux", "carrelage", "tuile", "brique", "ciment", 
            "quincaillerie", "treuil", "ardoise", "semi conducteur", "littium", 
            "batterie", "moteur elect", "pompe a chaleur"]

class Item:
    """
    Modélisation d'une marchandise à ranger dans un wagon.
    Conserve les dimensions de l'objet et enregistre ses futures coordonnées de rangement.
    """
    # On garde juste l'objet Item pour l'affichage final, son impact est nul car on ne l'instancie qu'une fois
    def __init__(self, id_item, nom, L, l, h):
        self.id = id_item
        self.nom = nom
        self.L, self.l, self.h = L, l, h
        self.wagon_id = -1
        self.pos_x = -1
        self.pos_y = -1
        self.pos_z = -1
        self.rot_L = -1
        self.rot_l = -1
        self.rot_h = -1
        
        # Verification si c'est un objet qui doit rester droit (Haut/Bas strict)
        nom_min = nom.lower().replace("_", " ")
        self.ne_pas_retourner = any(mot in nom_min for mot in FRAGILES)

    def get_rotations(self):
        """
        Renvoie la liste de toutes les orientations 3D (rotations) permises pour cet objet.
        Les objets fragiles ne peuvent pivoter que sur la base (X, Y) sans être renversés (axe Z fixe).
        """
        if self.ne_pas_retourner:
            # Ne pas retourner : La hauteur (h) DOIT rester sur l'axe Z (vers le haut)
            # On autorise juste a le faire pivoter sur le sol (echanger Longueur et Largeur)
            rots = [
                (self.L, self.l, self.h),
                (self.l, self.L, self.h)
            ]
        else:
            # Objet normal : On peut le basculer dans tous les sens (6 rotations 3D)
            rots = [
                (self.L, self.l, self.h),
                (self.L, self.h, self.l),
                (self.l, self.L, self.h),
                (self.l, self.h, self.L),
                (self.h, self.L, self.l),
                (self.h, self.l, self.L)
            ]
        return list(set(rots)) # set() elimine les doublons (cubes) pour gagner du temps

def pack_items_online(items):
    """
    Rangement ultra-rapide Online OPTIMISÉ EXTREME. 
    Algorithme Heuristique de type "Guillotine 3D" couplé à un "Bottom-Left-Fill".
    
    Pour des raisons de performance, l'algorithme n'utilise que des Tuples primitifs 
    pour modéliser les espaces vides (pas d'overhead d'instanciation de classes).
    
    Retourne : (score_fitness, liste_des_wagons)
    """
    # wagons sera une liste de listes de tuples. Chaque tuple = (x, y, z, w, l, h) représentant un espace vide 3D.
    wagons = []
    
    for item in items:
        rotations = item.get_rotations()
        placed = False
        
        for w_idx, spaces in enumerate(wagons):
            best_s_idx = -1
            best_rot = None
            best_z = float('inf')
            best_vol = float('inf')
            
            # Recherche lineaire du meilleur trou (Bottom-Left-Fill) sans appeler sort()
            for s_idx, (sx, sy, sz, sw, sl, sh) in enumerate(spaces):
                # Si le trou est deja plus haut que notre meilleur trouvé, on n'a pas besoin de verifier ses dimensions
                # Sauf si on veut absolument le plus petit volume... mais Bottom prioritaire.
                if sz > best_z:
                    continue
                    
                for r0, r1, r2 in rotations:
                    # Check geometrique rapide
                    if r0 <= sw and r1 <= sl and r2 <= sh:
                        vol = sw * sl * sh
                        # Priorité 1: Le plus bas possible (Z). Priorité 2: Le plus petit trou possible (Volume)
                        if sz < best_z or (sz == best_z and vol < best_vol):
                            best_z = sz
                            best_vol = vol
                            best_s_idx = s_idx
                            best_rot = (r0, r1, r2)
                            
            if best_s_idx != -1:
                # On a trouve un trou ! On l'enleve de la liste
                sx, sy, sz, sw, sl, sh = spaces.pop(best_s_idx)
                r0, r1, r2 = best_rot
                
                # Découpe Guillotine 3D ultra-rapide : 
                # L'espace vide initial est subdivisé en 3 nouveaux sous-espaces (droite, devant, au-dessus)
                if sw - r0 > 0:
                    spaces.append((sx + r0, sy, sz, sw - r0, sl, sh))
                if sl - r1 > 0:
                    spaces.append((sx, sy + r1, sz, r0, sl - r1, sh))
                if sh - r2 > 0:
                    spaces.append((sx, sy, sz + r2, r0, r1, sh - r2))
                    
                item.wagon_id = w_idx
                item.pos_x, item.pos_y, item.pos_z = sx, sy, sz
                item.rot_L, item.rot_l, item.rot_h = r0, r1, r2
                placed = True
                break
                
        if not placed:
            # Nouveau wagon (Tuple primordial)
            spaces = [(0.0, 0.0, 0.0, L_WAGON, LARG_WAGON, H_WAGON)]
            wagons.append(spaces)
            sx, sy, sz, sw, sl, sh = spaces.pop(0)
            
            for r0, r1, r2 in rotations:
                if r0 <= L_WAGON and r1 <= LARG_WAGON and r2 <= H_WAGON:
                    if sw - r0 > 0:
                        spaces.append((sx + r0, sy, sz, sw - r0, sl, sh))
                    if sl - r1 > 0:
                        spaces.append((sx, sy + r1, sz, r0, sl - r1, sh))
                    if sh - r2 > 0:
                        spaces.append((sx, sy, sz + r2, r0, r1, sh - r2))
                        
                    item.wagon_id = len(wagons) - 1
                    item.pos_x, item.pos_y, item.pos_z = 0.0, 0.0, 0.0
                    item.rot_L, item.rot_l, item.rot_h = r0, r1, r2
                    placed = True
                    break
                    
            if not placed:
                print(f"ERREUR: Impossible de ranger l'objet {item.id}")
                return float('inf'), wagons

    if len(wagons) == 0: return float('inf'), wagons
    
    # Calcul de la precision exacte
    vol_vide = sum((sw * sl * sh) for (_, _, _, sw, sl, sh) in wagons[-1])
    fraction = vol_vide / (L_WAGON * LARG_WAGON * H_WAGON)
    return float(len(wagons)) - fraction, wagons

def read_data():
    """
    Charge les marchandises depuis le fichier CSV.
    Gère la conversion des virgules en points pour éviter les bugs de décimales avec Python.
    """
    items = []
    with open('Données_marchandises.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if not row or len(row) < 5: continue
            items.append(Item(row[0], row[1], float(row[2].replace(',', '.')), float(row[3].replace(',', '.')), float(row[4].replace(',', '.'))))
    return items

def main():
    """
    Point d'entrée principal du programme. Teste le rangement des objets et affiche un rapport avec chronométrage.
    """
    print("--------------------------------------------------")
    print("SPEEDRUN : MOTEUR GUILLOTINE 3D ONLINE (TUPLES)")
    print("--------------------------------------------------")
    items = read_data()
    
    # Le Garbage Collector (ramasse-miette) peut ralentir Python.
    # Dans un contexte de speedrun, on peut desactiver la collecte automatique.
    import gc
    gc.disable()
    
    # Lancement du chronometre (haute precision, exclut le temps de lecture du CSV)
    start_time = time.perf_counter()
    
    fitness, wagons = pack_items_online(items)
    nb_wagons_reel = math.ceil(fitness)
    
    end_time = time.perf_counter()
    gc.enable()
    
    execution_time_ms = (end_time - start_time) * 1000  # Conversion en millisecondes
    
    print("\n--- DETAILS DU RANGEMENT FINAL ---")
    current_wagon = -1
    for item in items:
        if item.wagon_id != current_wagon:
            current_wagon = item.wagon_id
            print(f"\n[ WAGON {current_wagon + 1} ]")
        print(f" - {item.nom[:15]:15s} (ID: {item.id:3s}) : Pos(x={item.pos_x:5.2f}, y={item.pos_y:5.2f}, z={item.pos_z:5.2f})")

    print("\n--------------------------------------------------")
    print(f"PRECISION      : {nb_wagons_reel} WAGONS")
    print(f"TEMPS D'EXEC.  : {execution_time_ms:.4f} millisecondes !")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
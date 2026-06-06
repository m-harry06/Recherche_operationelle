## Harry MBENGMO

"""
Algorithme de Bin Packing 2.5D (Rangement de conteneurs au sol avec gestion de la hauteur).
Utilise une heuristique géométrique (Découpe Guillotine 2D) couplée à une Hyper-Heuristique (poids W).
L'algorithme tente d'optimiser l'espace au sol (2D) tout en s'assurant que la hauteur passe (0.5D).
Génère également un rendu graphique 2D des wagons à l'aide de Matplotlib.
"""

import time
import csv
import sys
import math
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONSTANTES ---
# Dimensions physiques d'un wagon standard (en mètres)
LONGUEUR_WAGON = 11.583
LARGEUR_WAGON = 2.294
HAUTEUR_WAGON = 2.569
NB_MARCHANDISES = 100 # Nombre d'objets à lire dans le fichier

FRAGILES = ["acide", "verre", "vitraux", "carrelage", "tuile", "brique", "ciment", 
            "quincaillerie", "treuil", "ardoise", "semi conducteur", "littium", 
            "batterie", "moteur elect", "pompe a chaleur"]

class Marchandise:
    """
    Représente un objet (colis) à ranger dans le wagon.
    """
    def __init__(self, id_marchandise, nom, longueur, largeur, hauteur):
        self.id = int(id_marchandise)
        self.nom = nom
        # On remplace la virgule par un point pour pouvoir convertir en flottant (float)
        self.longueur = float(str(longueur).replace(',', '.'))
        self.largeur = float(str(largeur).replace(',', '.'))
        self.hauteur = float(str(hauteur).replace(',', '.'))
        
        # Variables utilisées pour sauvegarder l'emplacement final de l'objet pour l'affichage
        self.id_wagon = -1  # Le wagon dans lequel l'objet a été placé
        self.pos_x = -1     # Sa position X au sol
        self.pos_y = -1     # Sa position Y au sol
        self.rot_L = -1     # La longueur qu'il prend au sol selon la rotation choisie
        self.rot_l = -1     # La largeur qu'il prend au sol selon la rotation choisie
        
        # Objet fragile ? (pour empecher le basculement en hauteur)
        nom_min = nom.lower().replace("_", " ")
        self.ne_pas_retourner = any(mot in nom_min for mot in FRAGILES)

    def get_rotations_2d(self):
        """
        Génère les 2 orientations possibles au sol pour l'empreinte optimisée (Astuce 2.5D).
        """
        if self.ne_pas_retourner:
            # Fragile : la hauteur d'origine reste en l'air (Axe Z)
            rots = [(self.longueur, self.largeur), (self.largeur, self.longueur)]
        else:
            # Astuce : On cherche la face qui prend le MOINS de surface au sol, 
            # à condition que la 3ème dimension (la nouvelle hauteur) rentre dans le wagon.
            faces_valides = []
            
            # 1. Posé normalement (L, l au sol -> h en l'air)
            if self.hauteur <= HAUTEUR_WAGON:
                faces_valides.append((self.longueur, self.largeur))
            # 2. Basculé sur la longueur (L, h au sol -> l en l'air)
            if self.largeur <= HAUTEUR_WAGON:
                faces_valides.append((self.longueur, self.hauteur))
            # 3. Basculé sur la largeur (l, h au sol -> L en l'air)
            if self.longueur <= HAUTEUR_WAGON:
                faces_valides.append((self.largeur, self.hauteur))
                
            if not faces_valides:
                # Securite si rien ne rentre en hauteur (ex: objet geant)
                faces_valides.append((self.longueur, self.largeur))
                
            # On selectionne la face avec la surface (L*l) la plus petite !
            best_face = min(faces_valides, key=lambda f: f[0]*f[1])
            
            # On retourne les 2 rotations (90 degres) possibles sur le sol pour cette face ideale
            rots = [(best_face[0], best_face[1]), (best_face[1], best_face[0])]
            
        # set() permet d'éliminer les doublons si l'empreinte au sol est un carré
        return list(set(rots))

class Space2D:
    """
    Représente un espace vide (un "trou") disponible sur le sol d'un wagon.
    """
    def __init__(self, x, y, L, l):
        self.x = x          # Coordonnée X de départ du trou
        self.y = y          # Coordonnée Y de départ du trou
        self.L = L          # Longueur disponible dans ce trou
        self.l = l          # Largeur disponible dans ce trou
        self.surface = L * l # Surface totale du trou

class Wagon2D:
    """
    Représente un wagon qui contient une liste de trous (espaces vides).
    """
    def __init__(self):
        # À sa création, le wagon ne contient qu'un seul immense espace vide (tout son sol)
        self.spaces = [Space2D(0, 0, LONGUEUR_WAGON, LARGEUR_WAGON)]

def evaluer_online_guillotine2d(W, table, verbose=False):
    """
    Cœur de l'algorithme géométrique (Guillotine 2D) couplé à une Hyper-Heuristique (Poids W).
    Place les objets dans l'ordre de leur arrivée (Online).
    
    Paramètres W (appris par l'IA) :
    W[0] : Poids pour la surface du trou restant après placement
    W[1] : Poids pour la coordonnée Y (tasser au fond)
    W[2] : Poids pour la coordonnée X (tasser à gauche)
    W[3] : Poids pour la longueur restante dans le trou
    W[4] : Poids pour la largeur restante dans le trou
    W[5] : Biais (bonus ou malus) pour le fait d'ouvrir un tout nouveau wagon
    """
    wagons = [] # Liste de nos conteneurs
    
    # On traite les objets un par un (contrainte du problème Online)
    for item in table:
        rotations = item.get_rotations_2d()
        
        best_score = float('-inf') # Initialisé à -infini
        best_action = None         # Sauvegardera (id_wagon, index_du_trou, (rotation_L, rotation_l), est_un_nouveau_wagon)
        
        # --- ETAPE 1 : Trouver le meilleur trou existant parmi tous les wagons ---
        for w_idx, wagon in enumerate(wagons):
            for s_idx, space in enumerate(wagon.spaces):
                for rot_L, rot_l in rotations:
                    # Vérifier si l'objet rentre géométriquement dans ce trou
                    if rot_L <= space.L and rot_l <= space.l:
                        # Calculer les caractéristiques du vide qui restera si on le place ici
                        surface_restante = space.surface - (rot_L * rot_l)
                        L_rest = space.L - rot_L
                        l_rest = space.l - rot_l
                        
                        # L'Hyper-Heuristique calcule un score basé sur les poids mathématiques
                        score = (W[0] * surface_restante +
                                 W[1] * space.y +
                                 W[2] * space.x +
                                 W[3] * L_rest +
                                 W[4] * l_rest)
                                 
                        # Si ce trou obtient un meilleur score, il devient le candidat numéro 1
                        if score > best_score:
                            best_score = score
                            best_action = (w_idx, s_idx, (rot_L, rot_l), False) # False = On utilise un wagon existant
                            
        # --- ETAPE 2 : Évaluer si ouvrir un nouveau wagon serait encore meilleur ---
        for rot_L, rot_l in rotations:
            # Vérifier que l'objet n'est pas plus grand qu'un wagon entier
            if rot_L <= LONGUEUR_WAGON and rot_l <= LARGEUR_WAGON:
                surface_restante = (LONGUEUR_WAGON * LARGEUR_WAGON) - (rot_L * rot_l)
                L_rest = LONGUEUR_WAGON - rot_L
                l_rest = LARGEUR_WAGON - rot_l
                
                # Le score d'un nouveau wagon utilise le poids W[5]
                score = (W[0] * surface_restante +
                         W[1] * 0 + # Posé au fond (y=0)
                         W[2] * 0 + # Posé à gauche (x=0)
                         W[3] * L_rest +
                         W[4] * l_rest +
                         W[5])      # Le Biais W5
                         
                if score > best_score:
                    best_score = score
                    best_action = (len(wagons), 0, (rot_L, rot_l), True) # True = C'est un nouveau wagon
                    
        # --- ETAPE 3 : Action ! On place l'objet dans le meilleur emplacement trouvé ---
        if not best_action:
            print(f"ERREUR GEOMETRIQUE: Impossible de ranger l'objet ID {item.id} (Trop grand ?)")
            sys.exit(1)
            
        w_idx, s_idx, (rot_L, rot_l), is_new_wagon = best_action
        
        # Si la meilleure action est d'ouvrir un nouveau wagon
        if is_new_wagon:
            nv_wagon = Wagon2D()
            wagons.append(nv_wagon)
            used_space = nv_wagon.spaces.pop(0) # On consomme la grande surface vide
        else:
            # Sinon, on consomme le trou sélectionné dans le wagon existant
            used_space = wagons[w_idx].spaces.pop(s_idx)
            
        # --- ETAPE 4 : DECOUPE GUILLOTINE 2D ---
        # L'objet a été posé. Il faut diviser le vide restant en 2 nouveaux rectangles (trous parfaits)
        
        # Rectangle n°1 : Le vide qui reste à droite de l'objet
        if used_space.L - rot_L > 0:
            wagons[w_idx].spaces.append(Space2D(
                used_space.x + rot_L, used_space.y, 
                used_space.L - rot_L, used_space.l
            ))
            
        # Rectangle n°2 : Le vide qui reste devant l'objet
        if used_space.l - rot_l > 0:
            wagons[w_idx].spaces.append(Space2D(
                used_space.x, used_space.y + rot_l, 
                rot_L, used_space.l - rot_l
            ))
            
        # Si verbose=True (Rangement final), on sauvegarde les coordonnées pour pouvoir les dessiner plus tard
        if verbose:
            item.id_wagon = w_idx
            item.pos_x = used_space.x
            item.pos_y = used_space.y
            item.rot_L = rot_L
            item.rot_l = rot_l

    # --- ÉVALUATION FINALE (Fitness) ---
    # On cherche à minimiser le nombre de wagons.
    # Pour aider l'IA à différencier "3 wagons presque pleins" de "3 wagons presque vides", 
    # on soustrait la fraction de volume vide du tout dernier wagon.
    if not wagons: return float('inf')
    vol_vide_dernier = sum(s.surface for s in wagons[-1].spaces)
    fraction = vol_vide_dernier / (LONGUEUR_WAGON * LARGEUR_WAGON)
    return float(len(wagons)) - fraction

def charger_donnees(fichier_path, n):
    """ Importation des données depuis le fichier CSV """
    objets = []
    try:
        with open(fichier_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if len(row) >= 5:
                    objets.append(Marchandise(row[0], row[1], row[2], row[3], row[4]))
                if len(objets) == n:
                    break
    except FileNotFoundError:
        print(f"Erreur : Impossible de trouver le fichier '{fichier_path}'")
        sys.exit(1)
    return objets

def dessiner_wagons(table):
    """ Utilise Matplotlib pour dessiner le plan d'architecte des wagons (Vue de haut 2D) """
    # Grouper les objets par wagon
    wagons_dict = {}
    for item in table:
        if item.id_wagon not in wagons_dict:
            wagons_dict[item.id_wagon] = []
        wagons_dict[item.id_wagon].append(item)
        
    nb_wagons = len(wagons_dict)
    if nb_wagons == 0: return
    
    # Calcul de la grille (max 3 colonnes de wagons affichés sur l'écran)
    cols = min(3, nb_wagons)
    rows = math.ceil(nb_wagons / cols)
    
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 9*rows))
    # Securité si subplot renvoie un seul axe ou un tableau 1D
    if nb_wagons == 1: axes = [axes]
    elif rows > 1: axes = axes.flatten()
    
    # Dessiner chaque wagon
    for i, w_idx in enumerate(sorted(wagons_dict.keys())):
        ax = axes[i]
        ax.set_title(f"Wagon {w_idx + 1}")
        ax.set_xlim(0, LONGUEUR_WAGON)
        ax.set_ylim(0, LARGEUR_WAGON)
        ax.set_xlabel("Longueur (m)")
        ax.set_ylabel("Largeur (m)")
        
        # Dessiner le bord du wagon
        ax.add_patch(patches.Rectangle((0, 0), LONGUEUR_WAGON, LARGEUR_WAGON, linewidth=2, edgecolor='black', facecolor='none'))
        
        # Dessiner les objets
        for item in wagons_dict[w_idx]:
            # Générer une couleur aléatoire douce (pastelle) pour l'objet
            color = (random.random()*0.5+0.5, random.random()*0.5+0.5, random.random()*0.5+0.5)
            rect = patches.Rectangle((item.pos_x, item.pos_y), item.rot_L, item.rot_l, linewidth=1, edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            # Ajouter l'ID au centre de l'objet
            ax.text(item.pos_x + item.rot_L/2, item.pos_y + item.rot_l/2, str(item.id), 
                    color='black', fontsize=8, ha='center', va='center', weight='bold')
                    
    # Cacher les cases inutilisées de la grille Matplotlib
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
        
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    random.seed(time.time())
    time1 = time.time()

    # 1. Chargement du fichier
    tab = charger_donnees("Données_marchandises.csv", NB_MARCHANDISES)
    
    # Poids fixes parfaits pour l'heuristique (trouvés précédemment)
    meilleur_W = [-1.0, -10.0, -5.0, -1.0, -1.0, -100.0]
    
    print("=== Lancement SPEEDRUN Guillotine 2D ===")
    
    # Désactiver le ramasse-miettes pour avoir un chronomètre pur
    import gc
    gc.disable()
    
    # Démarrage du chrono ultra-précis
    start_time = time.perf_counter()
    
    # Lancement du rangement Online avec les Poids parfaits
    final_fitness = evaluer_online_guillotine2d(meilleur_W, tab, verbose=True)
    final_wagons = math.ceil(final_fitness)
    
    # Arrêt du chrono
    end_time = time.perf_counter()
    gc.enable()
    
    execution_time_ms = (end_time - start_time) * 1000
    
    print("\n--------------------------------------------------")
    print(f"RESULTAT FINAL : {final_wagons} WAGONS !")
    print(f"TEMPS D'EXEC.  : {execution_time_ms:.4f} millisecondes !")
    print("--------------------------------------------------")
    
    print("\n[ Generation du rendu graphique 2D en cours (le temps est deja arrete) ... ]")
    dessiner_wagons(tab)
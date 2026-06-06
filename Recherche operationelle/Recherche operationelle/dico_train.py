objets: dict[str, dict[str, float]] = {
        "Tubes acier 1": {
            "Longueur": 10,
            "Largeur": 1,
            "Hauteur": 0.5
        },
        "Tubes acier 2": {
            "Longueur": 9,
            "Largeur": 2,
            "Hauteur": 0.7
        },
        "Tubes acier 3": {
            "Longueur": 7.5,
            "Largeur": 1.2,
            "Hauteur": 0.4
        },
        "Acide chlorhydrique 4": {
            "Longueur": 1,
            "Largeur": 1,
            "Hauteur": 1
        },
        "Godet pelleteuse 5": {
            "Longueur": 2,
            "Largeur": 2,
            "Hauteur": 1
        },
        "Rails 6": {
            "Longueur": 11,
            "Largeur": 1,
            "Hauteur": 0.2
        },
        "Tubes PVC 7": {
            "Longueur": 3,
            "Largeur": 2,
            "Hauteur": 0.6
        },
        "Echaffaudage 8": {
            "Longueur": 3,
            "Largeur": 1.3,
            "Hauteur": 1.8
        },
        "Verre 9": {
            "Longueur": 3,
            "Largeur": 2.1,
            "Hauteur": 0.6
        },
        "Ciment 10": {
            "Longueur": 4,
            "Largeur": 1,
            "Hauteur": 0.5
        },
        "Bois vrac 11": {
            "Longueur": 5,
            "Largeur": 0.8,
            "Hauteur": 1
        },
        "Troncs chênes 12": {
            "Longueur": 6,
            "Largeur": 1.9,
            "Hauteur": 1
        },
        "Troncs hêtres 13": {
            "Longueur": 7,
            "Largeur": 1.6,
            "Hauteur": 1.5
        },
        "Pompe à chaleur 14": {
            "Longueur": 5,
            "Largeur": 1.1,
            "Hauteur": 2.3
        },
        "Cuivre 15": {
            "Longueur": 6,
            "Largeur": 2,
            "Hauteur": 1.4
        },
        "Zinc 16": {
            "Longueur": 5,
            "Largeur": 0.8,
            "Hauteur": 0.8
        },
        "Papier 17": {
            "Longueur": 4,
            "Largeur": 1.6,
            "Hauteur": 0.6
        },
        "Carton 18": {
            "Longueur": 7,
            "Largeur": 1,
            "Hauteur": 1.3
        },
        "Verre blanc vrac 19": {
            "Longueur": 9,
            "Largeur": 0.9,
            "Hauteur": 2.2
        },
        "Verre brun vrac 20": {
            "Longueur": 3,
            "Largeur": 1.6,
            "Hauteur": 0.9
        },
        "Briques rouges 21": {
            "Longueur": 5,
            "Largeur": 1.1,
            "Hauteur": 2.4
        },
        "Pièces métalliques 22": {
            "Longueur": 6,
            "Largeur": 1.6,
            "Hauteur": 1.4
        },
        "Pièces métalliques 23": {
            "Longueur": 7,
            "Largeur": 0.9,
            "Hauteur": 1.2
        },
        "Pièces métalliques 24": {
            "Longueur": 3,
            "Largeur": 1.6,
            "Hauteur": 1.9
        },
        "Ardoises 25": {
            "Longueur": 1,
            "Largeur": 1.8,
            "Hauteur": 1
        },
        "Tuiles 26": {
            "Longueur": 2,
            "Largeur": 1.2,
            "Hauteur": 2.3
        },
        "Vitraux 27": {
            "Longueur": 4,
            "Largeur": 0.7,
            "Hauteur": 1.2
        },
        "Carrelage 28": {
            "Longueur": 6,
            "Largeur": 1.2,
            "Hauteur": 2.5
        },
        "Tôles 29": {
            "Longueur": 7,
            "Largeur": 0.6,
            "Hauteur": 1.5
        },
        "Tôles 30": {
            "Longueur": 9,
            "Largeur": 1.7,
            "Hauteur": 1
        },
        "Tôles 31": {
            "Longueur": 6,
            "Largeur": 1.9,
            "Hauteur": 1.6
        },
        "Tôles 32": {
            "Longueur": 3,
            "Largeur": 2.2,
            "Hauteur": 2.2
        },
        "Tôles 33": {
            "Longueur": 3,
            "Largeur": 0.5,
            "Hauteur": 2.2
        },
        "Mobilier urbain 34": {
            "Longueur": 4,
            "Largeur": 0.7,
            "Hauteur": 1.9
        },
        "Lin 35": {
            "Longueur": 5,
            "Largeur": 2.2,
            "Hauteur": 0.7
        },
        "Textiles à recycler 36": {
            "Longueur": 6,
            "Largeur": 1.3,
            "Hauteur": 2.5
        },
        "Aluminium 37": {
            "Longueur": 6,
            "Largeur": 1.3,
            "Hauteur": 1.2
        },
        "Batteries automobile 38": {
            "Longueur": 7,
            "Largeur": 1.4,
            "Hauteur": 2.5
        },
        "Quincaillerie 39": {
            "Longueur": 6,
            "Largeur": 1.1,
            "Hauteur": 1
        },
        "Treuil 40": {
            "Longueur": 7,
            "Largeur": 0.9,
            "Hauteur": 1.3
        },
        "Treuil 41": {
            "Longueur": 8,
            "Largeur": 0.5,
            "Hauteur": 0.5
        },
        "Acier 42": {
            "Longueur": 8,
            "Largeur": 0.9,
            "Hauteur": 1.7
        },
        "Laine de bois 43": {
            "Longueur": 8,
            "Largeur": 0.9,
            "Hauteur": 1.8
        },
        "Ouate de cellulose 44": {
            "Longueur": 5,
            "Largeur": 1.7,
            "Hauteur": 1.2
        },
        "Chanvre isolation 45": {
            "Longueur": 2.2,
            "Largeur": 1.6,
            "Hauteur": 1.1
        },
        "Moteur électrique 46": {
            "Longueur": 4.2,
            "Largeur": 1.5,
            "Hauteur": 0.8
        },
        "Semi conducteurs 47": {
            "Longueur": 3.7,
            "Largeur": 0.9,
            "Hauteur": 1.4
        },
        "Semi conducteurs 48": {
            "Longueur": 5.6,
            "Largeur": 0.5,
            "Hauteur": 1.4
        },
        "Semi conducteurs 49": {
            "Longueur": 4.9,
            "Largeur": 0.9,
            "Hauteur": 2.5
        },
        "Semi conducteurs 50": {
            "Longueur": 8.7,
            "Largeur": 1.3,
            "Hauteur": 1.3
        },
        "Semi conducteurs 51": {
            "Longueur": 6.1,
            "Largeur": 2.2,
            "Hauteur": 2.3
        },
        "Semi conducteurs 52": {
            "Longueur": 3.3,
            "Largeur": 1.8,
            "Hauteur": 2.3
        },
        "Semi conducteurs 53": {
            "Longueur": 2.6,
            "Largeur": 1.6,
            "Hauteur": 2.3
        },
        "Semi conducteurs 54": {
            "Longueur": 2.9,
            "Largeur": 1.6,
            "Hauteur": 2
        },
        "Aluminium 55": {
            "Longueur": 2,
            "Largeur": 1.1,
            "Hauteur": 0.6
        },
        "Aluminium 56": {
            "Longueur": 3,
            "Largeur": 0.6,
            "Hauteur": 1.2
        },
        "Aluminium 57": {
            "Longueur": 6,
            "Largeur": 1,
            "Hauteur": 0.8
        },
        "Aluminium 58": {
            "Longueur": 5,
            "Largeur": 1.3,
            "Hauteur": 0.6
        },
        "Aluminium 59": {
            "Longueur": 4,
            "Largeur": 2.1,
            "Hauteur": 2.1
        },
        "Aluminium 60": {
            "Longueur": 6,
            "Largeur": 1.5,
            "Hauteur": 1.9
        },
        "Aluminium 61": {
            "Longueur": 4,
            "Largeur": 0.8,
            "Hauteur": 2.1
        },
        "Aluminium 62": {
            "Longueur": 2,
            "Largeur": 2,
            "Hauteur": 2.3
        },
        "Aluminium 63": {
            "Longueur": 4,
            "Largeur": 1,
            "Hauteur": 1.1
        },
        "Aluminium 64": {
            "Longueur": 6,
            "Largeur": 1.8,
            "Hauteur": 1.1
        },
        "Lithium 65": {
            "Longueur": 6,
            "Largeur": 1.9,
            "Hauteur": 0.9
        },
        "Lithium 66": {
            "Longueur": 3,
            "Largeur": 2,
            "Hauteur": 2.2
        },
        "Lithium 67": {
            "Longueur": 4,
            "Largeur": 1.5,
            "Hauteur": 0.9
        },
        "Lithium 68": {
            "Longueur": 4,
            "Largeur": 2.1,
            "Hauteur": 2.5
        },
        "Lithium 69": {
            "Longueur": 2,
            "Largeur": 1.2,
            "Hauteur": 1.5
        },
        "Lithium 70": {
            "Longueur": 6,
            "Largeur": 1.3,
            "Hauteur": 2
        },
        "Lithium 71": {
            "Longueur": 2,
            "Largeur": 0.8,
            "Hauteur": 1.1
        },
        "Contreplaqué 72": {
            "Longueur": 4,
            "Largeur": 1.4,
            "Hauteur": 2
        },
        "Contreplaqué 73": {
            "Longueur": 5,
            "Largeur": 0.6,
            "Hauteur": 0.5
        },
        "Contreplaqué 74": {
            "Longueur": 5,
            "Largeur": 0.6,
            "Hauteur": 1.8
        },
        "Contreplaqué 75": {
            "Longueur": 4,
            "Largeur": 0.7,
            "Hauteur": 1.4
        },
        "Contreplaqué 76": {
            "Longueur": 6,
            "Largeur": 0.5,
            "Hauteur": 0.7
        },
        "Contreplaqué 77": {
            "Longueur": 3,
            "Largeur": 1.5,
            "Hauteur": 1.8
        },
        "Contreplaqué 78": {
            "Longueur": 3,
            "Largeur": 1.4,
            "Hauteur": 2
        },
        "Contreplaqué 79": {
            "Longueur": 3,
            "Largeur": 2,
            "Hauteur": 2.3
        },
        "Contreplaqué 80": {
            "Longueur": 5,
            "Largeur": 1.5,
            "Hauteur": 0.7
        },
        "Contreplaqué 81": {
            "Longueur": 5,
            "Largeur": 2.2,
            "Hauteur": 0.5
        },
        "Contreplaqué 82": {
            "Longueur": 6,
            "Largeur": 1.2,
            "Hauteur": 1.2
        },
        "Poutre 83": {
            "Longueur": 5,
            "Largeur": 0.8,
            "Hauteur": 0.7
        },
        "Poutre 84": {
            "Longueur": 3,
            "Largeur": 0.5,
            "Hauteur": 1.9
        },
        "Poutre 85": {
            "Longueur": 5,
            "Largeur": 1.4,
            "Hauteur": 0.7
        },
        "Poutre 86": {
            "Longueur": 6,
            "Largeur": 0.7,
            "Hauteur": 0.7
        },
        "Poutre 87": {
            "Longueur": 6,
            "Largeur": 1.2,
            "Hauteur": 2
        },
        "Poutre 88": {
            "Longueur": 3,
            "Largeur": 1.7,
            "Hauteur": 1.1
        },
        "Poutre 89": {
            "Longueur": 5,
            "Largeur": 1.6,
            "Hauteur": 2.1
        },
        "Pneus 90": {
            "Longueur": 3,
            "Largeur": 1.3,
            "Hauteur": 1.7
        },
        "Pneus 91": {
            "Longueur": 4,
            "Largeur": 1.5,
            "Hauteur": 1.7
        },
        "Pneus 92": {
            "Longueur": 3,
            "Largeur": 1.5,
            "Hauteur": 1.9
        },
        "Pneus 93": {
            "Longueur": 3,
            "Largeur": 0.6,
            "Hauteur": 1.9
        },
        "Pneus 94": {
            "Longueur": 5,
            "Largeur": 1.8,
            "Hauteur": 0.5
        },
        "Pneus 95": {
            "Longueur": 3,
            "Largeur": 1.8,
            "Hauteur": 0.7
        },
        "Pneus 96": {
            "Longueur": 4,
            "Largeur": 1.7,
            "Hauteur": 1.4
        },
        "Pneus 97": {
            "Longueur": 4,
            "Largeur": 1.5,
            "Hauteur": 0.5
        },
        "Pneus 98": {
            "Longueur": 2,
            "Largeur": 2.1,
            "Hauteur": 1.8
        },
        "Pneus 99": {
            "Longueur": 2,
            "Largeur": 0.7,
            "Hauteur": 1.1
        },
        "Pneus 100": {
            "Longueur": 6,
            "Largeur": 1.2,
            "Hauteur": 1.3
        }
}
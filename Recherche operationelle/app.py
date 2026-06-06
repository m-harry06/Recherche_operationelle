from flask import Flask, jsonify
from flask_cors import CORS

# Imports Knapsack (Partie 1)
from recherche_glouton import run_glouton
from recherche_prog_dyna import run_dyna
from rehcerche_prog_algo_gene import run_gene

# Imports Bin Packing (Partie 2 - Online)
# Imports Bin Packing (Partie 2 - Online)
import optimisation
import optimisation2
import optimisation3_2

import time
import math

# Imports Bin Packing (Partie 2 - Offline)
from d1_offline import run_offline_1d
from d2_offline import run_offline_2d
from d3_offline import run_offline_3d

# Imports Knapsack (Offline)
from Algo_Brute_Force import run_offline_bf
from Algo_Recuit_Simule import run_offline_rs

app = Flask(__name__)
CORS(app)

# ==========================================
# PARTIE 1 : SAC À DOS (KNAPSACK)
# ==========================================

@app.route('/api/knapsack/glouton', methods=['GET'])
def api_knapsack_glouton():
    try:
        data = run_glouton()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/knapsack/dyna', methods=['GET'])
def api_knapsack_dyna():
    try:
        data = run_dyna()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/knapsack/gene', methods=['GET'])
def api_knapsack_gene():
    try:
        data = run_gene()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================
# PARTIE 2 : BIN PACKING (ONLINE)
# ==========================================

@app.route('/api/run/1d', methods=['GET'])
def api_run_1d():
    try:
        import time
        start_time = time.perf_counter()
        tab = optimisation.charger_donnees("Données_marchandises.csv", optimisation.NB_MARCHANDISES)
        wagons = optimisation.online_1d(tab)
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        
        wagons_data = []
        for i, w in enumerate(wagons):
            items_data = []
            for item in w["items"]:
                items_data.append({
                    "nom": item.nom,
                    "longueur": item.longueur
                })
            wagons_data.append({
                "id": i,
                "espace_restant": w["espace_restant"],
                "items": items_data
            })
        
        return jsonify({
            "mode": "1D",
            "time_ms": execution_time_ms,
            "wagons_count": len(wagons),
            "wagons": wagons_data,
            "wagon_length": optimisation.LONGUEUR_WAGON
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/run/2d', methods=['GET'])
def run_2d():
    # Rangement 2D (Guillotine Online 2.5D)
    tab = optimisation2.charger_donnees("Données_marchandises.csv", optimisation2.NB_MARCHANDISES)
    meilleur_W = [-1.0, -10.0, -5.0, -1.0, -1.0, -100.0]
    
    import gc
    gc.disable()
    start_time = time.perf_counter()
    
    final_fitness = optimisation2.evaluer_online_guillotine2d(meilleur_W, tab, verbose=True)
    final_wagons = math.ceil(final_fitness)
    
    end_time = time.perf_counter()
    gc.enable()
    execution_time_ms = (end_time - start_time) * 1000
    
    # Formatage des donnees pour l'UI
    wagons_data = {}
    for item in tab:
        if item.id_wagon not in wagons_data:
            wagons_data[item.id_wagon] = []
        wagons_data[item.id_wagon].append({
            "id": item.id,
            "nom": item.nom,
            "x": item.pos_x,
            "y": item.pos_y,
            "w": item.rot_L,
            "h": item.rot_l
        })
        
    wagons_list = [{"id": k, "items": v} for k, v in wagons_data.items()]
    
    return jsonify({
        "mode": "2D",
        "time_ms": execution_time_ms,
        "wagons_count": final_wagons,
        "wagons": wagons_list,
        "wagon_width": optimisation2.LONGUEUR_WAGON,
        "wagon_height": optimisation2.LARGEUR_WAGON
    })

@app.route('/api/run/3d', methods=['GET'])
def run_3d():
    # Rangement 3D (Guillotine Online 3D)
    items = optimisation3_2.read_data()
    
    import gc
    gc.disable()
    start_time = time.perf_counter()
    
    fitness, wagons = optimisation3_2.pack_items_online(items)
    nb_wagons_reel = math.ceil(fitness)
    
    end_time = time.perf_counter()
    gc.enable()
    execution_time_ms = (end_time - start_time) * 1000
    
    wagons_data = {}
    for item in items:
        if item.wagon_id != -1:
            if item.wagon_id not in wagons_data:
                wagons_data[item.wagon_id] = []
            wagons_data[item.wagon_id].append({
                "id": item.id,
                "nom": item.nom,
                "x": item.pos_x,
                "y": item.pos_y,
                "z": item.pos_z,
                "w": item.rot_L,
                "h": item.rot_l,
                "d": item.rot_h
            })
            
    wagons_list = [{"id": k, "items": v} for k, v in wagons_data.items()]
    
    return jsonify({
        "mode": "3D",
        "time_ms": execution_time_ms,
        "wagons_count": nb_wagons_reel,
        "wagons": wagons_list,
        "wagon_length": optimisation3_2.L_WAGON,
        "wagon_width": optimisation3_2.LARG_WAGON,
        "wagon_height": optimisation3_2.H_WAGON
    })

# ==========================================
# PARTIE 1 : SAC À DOS (OFFLINE)
# ==========================================

@app.route('/api/offline/knapsack/bf', methods=['GET'])
def api_offline_knapsack_bf():
    try:
        data = run_offline_bf()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/knapsack/rs', methods=['GET'])
def api_offline_knapsack_rs():
    try:
        data = run_offline_rs()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================
# PARTIE 2 : BIN PACKING (OFFLINE) - Placeholders
# ==========================================

@app.route('/api/offline/1d', methods=['GET'])
def api_offline_1d():
    try:
        data = run_offline_1d()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/2d', methods=['GET'])
def api_offline_2d():
    try:
        data = run_offline_2d()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/3d', methods=['GET'])
def api_offline_3d():
    try:
        data = run_offline_3d()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

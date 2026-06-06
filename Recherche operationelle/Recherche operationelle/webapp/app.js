// Configuration
const API_BASE = 'http://127.0.0.1:5000/api';

// Couleurs aleatoires
function getRandomColor(alpha = 1) {
    const r = Math.floor(Math.random() * 127 + 128); // Couleurs claires (pastelles)
    const g = Math.floor(Math.random() * 127 + 128);
    const b = Math.floor(Math.random() * 127 + 128);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// ==========================================
// PARTIE 1 : SAC À DOS (KNAPSACK)
// ==========================================

async function runKnapsack(endpoint, btnId, resId) {
    const btn = document.getElementById(btnId);
    const res = document.getElementById(resId);
    const oldText = btn.textContent;
    btn.textContent = 'Calcul en cours...';
    res.innerHTML = '<div style="color: #94a3b8;">Recherche en cours...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/${endpoint}`);
        const data = await response.json();
        
        if (data.error) {
            res.innerHTML = `<div style="color: #ef4444;">Erreur: ${data.error}</div>`;
            return;
        }

        res.innerHTML = `
            <div><strong>Temps :</strong> <span style="color: #10b981;">${data.time_ms.toFixed(3)} ms</span></div>
            <div><strong>Utilité max :</strong> <span style="color: #3b82f6;">${data.utilite_totale.toFixed(2)}</span></div>
            <div><strong>Poids :</strong> ${data.poids_total.toFixed(2)} / ${data.poids_max.toFixed(2)} kg</div>
            <div style="margin-top: 10px; color: #94a3b8; font-size: 0.8rem;">
                <strong>Objets choisis :</strong> ${data.items.map(i => i.nom).join(', ')}
            </div>
        `;
    } catch (e) {
        res.innerHTML = '<div style="color: #ef4444;">Erreur de connexion au Serveur Python.</div>';
    } finally {
        btn.textContent = oldText;
    }
}

document.getElementById('btn-glouton').addEventListener('click', () => runKnapsack('knapsack/glouton', 'btn-glouton', 'res-glouton'));
document.getElementById('btn-dyna').addEventListener('click', () => runKnapsack('knapsack/dyna', 'btn-dyna', 'res-dyna'));
document.getElementById('btn-gene').addEventListener('click', () => runKnapsack('knapsack/gene', 'btn-gene', 'res-gene'));
document.getElementById('btn-bf').addEventListener('click', () => runKnapsack('offline/knapsack/bf', 'btn-bf', 'res-bf'));
document.getElementById('btn-rs').addEventListener('click', () => runKnapsack('offline/knapsack/rs', 'btn-rs', 'res-rs'));


// ==========================================
// FONCTIONS DE RENDU (1D, 2D, 3D)
// ==========================================

function render1D(data, visId, containerId) {
    document.querySelector(`#${visId} .placeholder`).style.display = 'none';
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    data.wagons.forEach(wagon => {
        const wagonWrap = document.createElement('div');
        wagonWrap.style.marginBottom = '10px';
        
        const title = document.createElement('div');
        const espace = wagon.espace_restant !== undefined ? wagon.espace_restant.toFixed(2) : '0.00';
        title.textContent = `Wagon ${wagon.id + 1} (Espace restant: ${espace}m)`;
        title.style.fontSize = '0.9rem';
        title.style.color = '#94a3b8';
        title.style.marginBottom = '5px';
        wagonWrap.appendChild(title);
        
        const bar = document.createElement('div');
        bar.className = 'bar-container';
        bar.style.width = '100%';
        bar.style.height = '40px';
        bar.style.background = '#1e293b';
        bar.style.borderRadius = '20px';
        bar.style.overflow = 'hidden';
        bar.style.display = 'flex';
        
        wagon.items.forEach(item => {
            const pct = (item.longueur / data.wagon_length) * 100;
            const div = document.createElement('div');
            div.className = 'item-1d';
            div.style.width = pct + '%';
            div.style.backgroundColor = getRandomColor();
            div.textContent = item.nom.substring(0, 3);
            div.title = `${item.nom} (${item.longueur}m)`;
            div.style.height = '100%';
            div.style.display = 'flex';
            div.style.justifyContent = 'center';
            div.style.alignItems = 'center';
            div.style.color = 'white';
            div.style.fontSize = '0.7rem';
            div.style.borderRight = '1px solid rgba(0,0,0,0.2)';
            bar.appendChild(div);
        });
        
        wagonWrap.appendChild(bar);
        container.appendChild(wagonWrap);
    });
}

function render2D(data, visId, containerId) {
    document.querySelector(`#${visId} .placeholder`).style.display = 'none';
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (data.wagons.length === 0) return;
    
    data.wagons.forEach(wagon => {
        const wrapper = document.createElement('div');
        wrapper.style.display = 'flex';
        wrapper.style.flexDirection = 'column';
        wrapper.style.alignItems = 'center';
        
        const title = document.createElement('div');
        title.textContent = `Wagon ${wagon.id + 1}`;
        title.style.color = '#94a3b8';
        title.style.marginBottom = '5px';
        wrapper.appendChild(title);
        
        const canvas = document.createElement('canvas');
        canvas.width = 300; 
        canvas.height = 300 * (data.wagon_height / data.wagon_width);
        wrapper.appendChild(canvas);
        container.appendChild(wrapper);
        
        const ctx = canvas.getContext('2d');
        const scale = Math.min(
            (canvas.width - 20) / data.wagon_width,
            (canvas.height - 20) / data.wagon_height
        );
        
        const offsetX = 10;
        const offsetY = 10;
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 2;
        ctx.fillRect(offsetX, offsetY, data.wagon_width * scale, data.wagon_height * scale);
        ctx.strokeRect(offsetX, offsetY, data.wagon_width * scale, data.wagon_height * scale);
        
        wagon.items.forEach(item => {
            const x = offsetX + item.x * scale;
            const y = offsetY + item.y * scale;
            const w = item.w * scale;
            const h = item.h * scale;
            
            ctx.fillStyle = getRandomColor(0.8);
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 1;
            ctx.fillRect(x, y, w, h);
            ctx.strokeRect(x, y, w, h);
            
            ctx.fillStyle = '#000';
            ctx.font = 'bold 10px Inter';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            if (w > 12 && h > 12) {
                ctx.fillText(item.id !== undefined ? item.id : item.nom, x + w/2, y + h/2);
            }
        });
    });
}

let scene, camera, renderer, controls;
function initThree(containerId) {
    const container = document.getElementById(containerId);
    container.style.display = 'block';
    const rect = container.parentElement.getBoundingClientRect();
    
    if (!scene) {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(45, rect.width / rect.height, 0.1, 1000);
        camera.position.set(10, 8, 15);
        
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        
        const light = new THREE.HemisphereLight(0xffffff, 0x444444);
        light.position.set(0, 20, 0);
        scene.add(light);
        
        const dirLight = new THREE.DirectionalLight(0xffffff);
        dirLight.position.set(5, 10, 5);
        scene.add(dirLight);
        
        const animate = function () {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };
        animate();
    }
    
    renderer.setSize(rect.width, rect.height);
    container.appendChild(renderer.domElement);
}

function render3D(data, visId, controlsId, containerId) {
    document.querySelector(`#${visId} .placeholder`).style.display = 'none';
    document.getElementById(controlsId).style.display = 'flex';
    initThree(containerId);
    
    while(scene.children.length > 2){ 
        scene.remove(scene.children[2]); 
    }
    
    if (data.wagons.length === 0) return;
    
    data.wagons.forEach((wagon, wIndex) => {
        const offsetX = wIndex * (data.wagon_length + 2);
        
        const geoWagon = new THREE.BoxGeometry(data.wagon_length, 0.1, data.wagon_width);
        const matWagon = new THREE.MeshPhongMaterial({ color: 0x3b82f6, transparent: true, opacity: 0.2 });
        const meshWagon = new THREE.Mesh(geoWagon, matWagon);
        meshWagon.position.set(offsetX + data.wagon_length/2, -0.05, data.wagon_width/2);
        scene.add(meshWagon);
        
        const edges = new THREE.EdgesGeometry( geoWagon );
        const line = new THREE.LineSegments( edges, new THREE.LineBasicMaterial( { color: 0x3b82f6 } ) );
        line.position.copy(meshWagon.position);
        scene.add(line);
        
        wagon.items.forEach(item => {
            const geo = new THREE.BoxGeometry(item.w, item.d, item.h); 
            const color = new THREE.Color(getRandomColor());
            const mat = new THREE.MeshPhongMaterial({ color: color, transparent: true, opacity: 0.85 });
            const mesh = new THREE.Mesh(geo, mat);
            
            mesh.position.set(
                offsetX + item.x + item.w/2, 
                item.z + item.d/2, 
                item.y + item.h/2
            );
            
            scene.add(mesh);
            
            const edgesBox = new THREE.EdgesGeometry(geo);
            const lineBox = new THREE.LineSegments(edgesBox, new THREE.LineBasicMaterial({color: 0x000000}));
            lineBox.position.copy(mesh.position);
            scene.add(lineBox);
        });
    });
    
    const controlsDiv = document.getElementById(controlsId);
    controlsDiv.innerHTML = '';
    
    const btnAll = document.createElement('button');
    btnAll.className = 'tab-btn active';
    btnAll.style.padding = '0.5rem 1rem';
    btnAll.style.fontSize = '0.9rem';
    btnAll.textContent = 'Vue Globale';
    btnAll.onclick = () => {
        Array.from(controlsDiv.children).forEach(c => c.classList.remove('active'));
        btnAll.classList.add('active');
        const totalLength = data.wagons.length * (data.wagon_length + 2);
        controls.target.set(totalLength/2, data.wagon_height/2, data.wagon_width/2);
        camera.position.set(totalLength/2, data.wagon_height*5, data.wagon_width*5);
    };
    controlsDiv.appendChild(btnAll);
    
    data.wagons.forEach((wagon, idx) => {
        const wBtn = document.createElement('button');
        wBtn.className = 'tab-btn';
        wBtn.style.padding = '0.5rem 1rem';
        wBtn.style.fontSize = '0.9rem';
        wBtn.textContent = `Wagon ${idx + 1}`;
        wBtn.onclick = () => {
            Array.from(controlsDiv.children).forEach(c => c.classList.remove('active'));
            wBtn.classList.add('active');
            const offsetX = idx * (data.wagon_length + 2);
            controls.target.set(offsetX + data.wagon_length/2, data.wagon_height/2, data.wagon_width/2);
            camera.position.set(offsetX + data.wagon_length/2, data.wagon_height*2.5, data.wagon_width*2.5);
        };
        controlsDiv.appendChild(wBtn);
    });
    
    btnAll.click();
}


// ==========================================
// EXÉCUTION ALGORITHMES BIN PACKING
// ==========================================

async function runBinPacking(endpoint, btnId, timeId, wagonsId, rendererFn, renderArgs) {
    const btn = document.getElementById(btnId);
    const oldText = btn.textContent;
    btn.textContent = 'Calcul en cours...';
    
    try {
        const response = await fetch(`${API_BASE}/${endpoint}`);
        const data = await response.json();
        
        if (data.error) {
            alert(`Erreur: ${data.error}`);
            return;
        }

        document.getElementById(timeId).textContent = data.time_ms.toFixed(3) + ' ms';
        document.getElementById(wagonsId).textContent = data.wagons_count;
        
        // Appel de la fonction de rendu (render1D, render2D, render3D)
        rendererFn(data, ...renderArgs);
        
    } catch (e) {
        alert("Erreur de connexion au Serveur Python.");
    } finally {
        btn.textContent = oldText;
    }
}

// Boutons Online
document.getElementById('btn-run-1d').addEventListener('click', () => 
    runBinPacking('run/1d', 'btn-run-1d', 'time-1d', 'wagons-1d', render1D, ['vis-1d', 'wagons-container-1d']));

document.getElementById('btn-run-2d').addEventListener('click', () => 
    runBinPacking('run/2d', 'btn-run-2d', 'time-2d', 'wagons-2d', render2D, ['vis-2d', 'wagons-container-2d']));

document.getElementById('btn-run-3d').addEventListener('click', () => 
    runBinPacking('run/3d', 'btn-run-3d', 'time-3d', 'wagons-3d', render3D, ['vis-3d', 'wagon-controls-3d', 'container-3d']));

// Boutons Offline
document.getElementById('btn-off-1d').addEventListener('click', () => 
    runBinPacking('offline/1d', 'btn-off-1d', 'time-off-1d', 'wagons-off-1d', render1D, ['vis-off-1d', 'wagons-container-off-1d']));

document.getElementById('btn-off-2d').addEventListener('click', () => 
    runBinPacking('offline/2d', 'btn-off-2d', 'time-off-2d', 'wagons-off-2d', render2D, ['vis-off-2d', 'wagons-container-off-2d']));

document.getElementById('btn-off-3d').addEventListener('click', () => 
    runBinPacking('offline/3d', 'btn-off-3d', 'time-off-3d', 'wagons-off-3d', render3D, ['vis-off-3d', 'wagon-controls-off-3d', 'container-off-3d']));

// ==========================================
// THÈME CLAIR / SOMBRE
// ==========================================
const darkModeToggle = document.getElementById('darkmode-toggle');
if (darkModeToggle) {
    darkModeToggle.addEventListener('change', () => {
        if (!darkModeToggle.checked) {
            document.body.classList.add('light-mode');
        } else {
            document.body.classList.remove('light-mode');
        }
    });
}

// Interactive Impact Simulation - Meteorite Madness
// ================================================

// Initialize Leaflet map
const map = L.map('impact-map').setView([20.0, -40.0], 3);
const impactLayer = L.layerGroup();
const populationHeatmap = L.layerGroup().addTo(map);

// Base map layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap | Meteorite Madness'
}).addTo(map);

// UI References
const diameterSlider = document.getElementById('diameter');
const diameterValue = document.getElementById('diameter-value');
const velocitySlider = document.getElementById('velocity');
const velocityValue = document.getElementById('velocity-value');
const angleSlider = document.getElementById('angle');
const angleValue = document.getElementById('angle-value');
const densitySlider = document.getElementById('density');
const densityValue = document.getElementById('density-value');
const meteoroidType = document.getElementById('meteoroid-type');

const systemStatus = document.getElementById('system-status');
const runButton = document.getElementById('run-simulation');
const resetButton = document.getElementById('reset-simulation');
const loadNasaButton = document.getElementById('load-nasa-data');
const simulationOverlay = document.getElementById('simulation-overlay');

let simulationInterval = null;

// Major world cities data
const cities = [
    { lat: 19.4326, lng: -99.1332, name: "Mexico City", population: 9000000 },
    { lat: 40.7128, lng: -74.0060, name: "New York", population: 8400000 },
    { lat: 51.5074, lng: -0.1278, name: "London", population: 9000000 },
    { lat: 35.6762, lng: 139.6503, name: "Tokyo", population: 14000000 },
    { lat: 28.6139, lng: 77.2090, name: "Delhi", population: 11000000 },
    { lat: -23.5505, lng: -46.6333, name: "São Paulo", population: 12000000 },
    { lat: 30.0444, lng: 31.2357, name: "Cairo", population: 10000000 },
    { lat: -33.8688, lng: 151.2093, name: "Sydney", population: 5300000 }
];

// Add city markers to population layer
cities.forEach(city => {
    L.circleMarker([city.lat, city.lng], {
        radius: Math.log(city.population / 100000) * 3,
        fillColor: '#e74c3c',
        color: '#c0392b',
        weight: 1,
        opacity: 0.8,
        fillOpacity: 0.6
    }).addTo(populationHeatmap).bindPopup(`
        <strong>${city.name}</strong><br>
        Population: ${city.population.toLocaleString()}
    `);
});

// Update density based on meteoroid type
meteoroidType.addEventListener('change', () => {
    let newDensity = 3000;
    switch(meteoroidType.value) {
        case 'metallic':
            newDensity = 7800;
            break;
        case 'carbonaceous':
            newDensity = 1500;
            break;
        case 'porous':
            newDensity = 1000;
            break;
        case 'conglomerate':
            newDensity = 4000;
            break;
        case 'rocky':
        default:
            newDensity = 3000;
            break;
    }
    densitySlider.value = newDensity;
    document.getElementById('density-value').textContent = newDensity;
    updateImpactMetrics();
});

// Update slider values
[diameterSlider, velocitySlider, angleSlider, densitySlider].forEach(slider => {
    slider.addEventListener('input', () => {
        document.getElementById(slider.id + '-value').textContent = slider.value;
        updateImpactMetrics();
    });
});

// Calculate impact metrics
function updateImpactMetrics() {
    const diameter = parseFloat(diameterSlider.value); // m
    const velocity = parseFloat(velocitySlider.value) * 1000; // km/s to m/s
    const density = parseFloat(densitySlider.value); // kg/m³
    
    // Calculate mass
    const volume = (4/3) * Math.PI * Math.pow(diameter/2, 3);
    const mass = volume * density; // kg
    
    // Calculate kinetic energy (Joules)
    const energyJoules = 0.5 * mass * Math.pow(velocity, 2);
    // Convert to Megatons of TNT (1 MT TNT = 4.184e15 J)
    const energyMT = energyJoules / (4.184e15); 
    
    // Crater diameter (simplified scaling)
    const craterDiameter = Math.pow(energyJoules * 1e-12, 1/3.4) * 0.05; // km
    
    // Overpressure (approximate maximum)
    const overpressure = Math.min(energyMT * 100, 50000); // kPa
    
    // Population affected (rough estimate)
    const populationAffected = Math.round(energyMT * 500000); 

    document.getElementById('energy-value').textContent = energyMT.toFixed(2);
    document.getElementById('crater-value').textContent = craterDiameter.toFixed(2);
    document.getElementById('overpressure-value').textContent = Math.round(overpressure);
    document.getElementById('population-value').textContent = populationAffected.toLocaleString();
}

// Layer control
document.querySelectorAll('.layer-item').forEach(item => {
    item.addEventListener('click', function() {
        const checkbox = this.querySelector('.layer-checkbox');
        checkbox.classList.toggle('checked');
        
        const layerName = this.id.replace('layer-', '');
        toggleLayer(layerName, checkbox.classList.contains('checked'));
    });
});

function toggleLayer(layerName, visible) {
    switch(layerName) {
        case 'population':
            if (visible) {
                map.addLayer(populationHeatmap);
            } else {
                map.removeLayer(populationHeatmap);
            }
            break;
        case 'blast':
            if (visible && impactLayer.getLayers().length > 0) {
                map.addLayer(impactLayer);
            } else if (!visible) {
                map.removeLayer(impactLayer);
            }
            break;
    }
}

// Run simulation
runButton.addEventListener('click', function() {
    if (systemStatus.textContent !== 'SIMULATING') {
        resetSimulation(false);
        simulationOverlay.style.display = 'block';
        systemStatus.textContent = 'SIMULATING';
        systemStatus.style.color = 'var(--color-warning)';
        runButton.disabled = true;
        simulateEntry();
    }
});

// Reset simulation
resetButton.addEventListener('click', function() {
    resetSimulation(true);
});

function resetSimulation(resetStatus) {
    if (simulationInterval) {
        clearInterval(simulationInterval);
        simulationInterval = null;
    }

    impactLayer.clearLayers();
    if (map.hasLayer(impactLayer)) {
        map.removeLayer(impactLayer);
    }
    
    simulationOverlay.style.display = 'none';
    runButton.disabled = false;

    if (resetStatus) {
        systemStatus.textContent = 'READY';
        systemStatus.style.color = 'var(--color-success)';
        document.getElementById('sim-time').textContent = 'T+0s';
    }
}

function simulateEntry() {
    let altitude = 120; // km
    let velocity = parseFloat(velocitySlider.value); // km/s
    const initialDiameter = parseFloat(diameterSlider.value);
    const density = parseFloat(densitySlider.value);
    const initialVolume = (4/3) * Math.PI * Math.pow(initialDiameter/2, 3);
    let mass = initialVolume * density;
    const initialMass = mass;
    let time = 0;
    
    const steps = 24;
    const altitudeStep = 120 / steps;
    
    simulationInterval = setInterval(() => {
        time += 0.5;
        altitude -= altitudeStep;
        
        const densityFactor = 1 - Math.exp(-altitude / 10);
        const drag = 0.05 * densityFactor;
        const ablationRate = 0.02 * densityFactor * (velocity / 20);

        velocity = velocity * (1 - drag);
        mass = Math.max(mass * (1 - ablationRate), initialMass * 0.05);
        
        const massPercentage = (mass / initialMass * 100);
        const energyLiberated = (initialMass - mass) * Math.pow(velocity * 1000, 2) / (4.184e12);

        document.getElementById('sim-altitude').textContent = Math.max(0, altitude).toFixed(1);
        document.getElementById('sim-velocity').textContent = velocity.toFixed(1);
        document.getElementById('sim-mass').textContent = massPercentage.toFixed(1) + '%';
        document.getElementById('sim-energy').textContent = energyLiberated.toFixed(1);
        document.getElementById('sim-time').textContent = `T+${time.toFixed(1)}s`;
        
        if (altitude <= 0) {
            clearInterval(simulationInterval);
            simulationInterval = null;
            simulateImpact();
        }
    }, 500);
}

function simulateImpact() {
    const locationInput = document.getElementById('impact-location').value;
    let [latStr, lngStr] = locationInput.split(',').map(s => s.trim());
    
    const impactLat = parseFloat(latStr) || 40.7128;
    const impactLng = parseFloat(lngStr) || -74.0060;
    const craterDiameter = parseFloat(document.getElementById('crater-value').textContent);

    const impactMarker = L.circleMarker([impactLat, impactLng], {
        radius: 20,
        color: 'transparent',
        fillColor: 'var(--color-danger)',
        fillOpacity: 1,
        className: 'pulse'
    }).addTo(impactLayer);
    
    impactLayer.addTo(map);
    map.flyTo([impactLat, impactLng], Math.max(9, 6));

    impactMarker.bindPopup(`
        <strong>Impact Point</strong><br>
        ID: ${document.getElementById('meteoroid-id').value}<br>
        Energy: ${document.getElementById('energy-value').textContent} MT<br>
        Crater: ${craterDiameter.toFixed(2)} km<br>
        Location: ${impactLat.toFixed(4)}, ${impactLng.toFixed(4)}
    `).openPopup();
    
    createShockwaveRings(impactLat, impactLng, craterDiameter);
    
    systemStatus.textContent = 'IMPACT COMPLETE';
    systemStatus.style.color = 'var(--color-danger)';
    simulationOverlay.style.display = 'none';

    setTimeout(() => {
        const element = impactMarker.getElement();
        if (element) {
            element.classList.remove('pulse');
        }
    }, 5000);
}

function createShockwaveRings(lat, lng, baseCraterKm) {
    const ringsData = [
        { radiusFactor: 1.5, pressure: "50 kPa (Severe Structural Damage)", color: '#e74c3c', weight: 4 },
        { radiusFactor: 3, pressure: "20 kPa (Moderate Structural Damage)", color: '#e67e22', weight: 3 },
        { radiusFactor: 6, pressure: "5 kPa (Glass Breakage)", color: '#f1c40f', weight: 2 },
    ];

    ringsData.forEach((ring, index) => {
        const radius = baseCraterKm * ring.radiusFactor;
        setTimeout(() => {
            if (document.getElementById('layer-blast').querySelector('.layer-checkbox').classList.contains('checked')) {
                L.circle([lat, lng], {
                    radius: radius * 1000,
                    color: ring.color,
                    fillColor: 'transparent',
                    weight: ring.weight,
                    opacity: 0.8
                }).addTo(impactLayer).bindPopup(`Effect Radius: ${radius.toFixed(0)} km<br>Pressure: ${ring.pressure}`);
            }
        }, index * 1000);
    });
}

// Load NASA data
loadNasaButton.addEventListener('click', async function() {
    try {
        const response = await fetch('/api/neo/recent');
        const data = await response.json();
        
        if (data.success && data.asteroids.length > 0) {
            // Use first asteroid as example
            const asteroid = data.asteroids[0];
            document.getElementById('meteoroid-id').value = asteroid.name;
            
            // Convert diameter to meters
            diameterSlider.value = Math.round(asteroid.diameter_km * 1000);
            diameterValue.textContent = Math.round(asteroid.diameter_km * 1000);
            
            // Convert velocity
            velocitySlider.value = Math.round(asteroid.velocity_kmh / 3600);
            velocityValue.textContent = Math.round(asteroid.velocity_kmh / 3600);
            
            updateImpactMetrics();
            
            alert(`Loaded data for ${asteroid.name}!\nDiameter: ${(asteroid.diameter_km * 1000).toFixed(0)}m\nVelocity: ${(asteroid.velocity_kmh / 3600).toFixed(1)} km/s`);
        } else {
            alert('No asteroid data available. Please check NASA API connection.');
        }
    } catch (error) {
        console.error('Error loading NASA data:', error);
        alert('Failed to load NASA data. Please try again.');
    }
});

// Export report
document.getElementById('export-report').addEventListener('click', function() {
    const report = `
METEORITE IMPACT SIMULATION REPORT
===========================================
Generated: ${new Date().toUTCString()}

METEOROID PARAMETERS:
- ID: ${document.getElementById('meteoroid-id').value}
- Type: ${meteoroidType.options[meteoroidType.selectedIndex].text}
- Diameter: ${diameterSlider.value} m
- Velocity: ${velocitySlider.value} km/s
- Entry Angle: ${angleSlider.value}°
- Density: ${densitySlider.value} kg/m³

IMPACT LOCATION:
${document.getElementById('impact-location').value}

CALCULATED METRICS:
- Impact Energy: ${document.getElementById('energy-value').textContent} MT
- Crater Diameter: ${document.getElementById('crater-value').textContent} km
- Overpressure: ${document.getElementById('overpressure-value').textContent} kPa
- Population Affected: ${document.getElementById('population-value').textContent}

SIMULATION STATUS: ${systemStatus.textContent}

===========================================
Meteorite Madness - Planetary Defense Platform
    `;
    
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `impact_simulation_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
});

// Update UTC time
function updateUTCTime() {
    const now = new Date();
    const utcTime = now.toUTCString().split(' ')[4];
    document.getElementById('utc-time').textContent = utcTime;
}
setInterval(updateUTCTime, 1000);
updateUTCTime();

// Initialize
updateImpactMetrics();

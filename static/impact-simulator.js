// Impact Simulator JavaScript
// Gemini AI Configuration
const GEMINI_API_KEY = 'AIzaSyDM36G2Dgw4J6RfQJvkFja1MPPd4VJHhx4';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent';

// Global variables
let map;
let impactMarker;
let blastCircle;
let trajectoryLine;
let simulationRunning = false;

// Initialize map
function initMap() {
    map = L.map('impact-map').setView([23.6345, -102.5528], 5);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);

    // Click to set impact location
    map.on('click', function(e) {
        const lat = e.latlng.lat.toFixed(4);
        const lng = e.latlng.lng.toFixed(4);
        document.getElementById('impact-location').value = `${lat}, ${lng}`;
        updateImpactMarker(e.latlng);
    });
}

// Update impact marker
function updateImpactMarker(latlng) {
    if (impactMarker) {
        map.removeLayer(impactMarker);
    }
    
    impactMarker = L.marker(latlng, {
        icon: L.divIcon({
            className: 'impact-marker',
            html: '<i class="fas fa-crosshairs" style="color: red; font-size: 24px;"></i>',
            iconSize: [24, 24]
        })
    }).addTo(map);
}

// Calculate impact physics
function calculateImpact() {
    const diameter = parseFloat(document.getElementById('diameter').value);
    const velocity = parseFloat(document.getElementById('velocity').value);
    const angle = parseFloat(document.getElementById('angle').value);
    const density = parseFloat(document.getElementById('density').value);
    
    // Calculate volume and mass
    const radius = diameter / 2;
    const volume = (4/3) * Math.PI * Math.pow(radius, 3);
    const mass = volume * density;
    
    // Calculate kinetic energy (in Joules)
    const velocityMs = velocity * 1000; // Convert to m/s
    const energy = 0.5 * mass * Math.pow(velocityMs, 2);
    const energyMT = energy / 4.184e15; // Convert to megatons TNT
    
    // Crater diameter (Holsapple & Schmidt scaling)
    const craterDiameter = 0.07 * Math.pow(energy / 1e15, 0.33) * Math.pow(Math.sin(angle * Math.PI / 180), 0.33);
    
    // Overpressure at 10km (rough estimate)
    const distance = 10000; // 10 km in meters
    const overpressure = (energyMT * 1e6) / Math.pow(distance, 2) * 100; // kPa
    
    // Population affected (very rough estimate based on 500 people/km²)
    const affectedArea = Math.PI * Math.pow(craterDiameter * 10, 2); // 10x crater radius
    const populationAffected = Math.floor(affectedArea * 500);
    
    return {
        energy: energyMT,
        crater: craterDiameter,
        overpressure: overpressure,
        population: populationAffected,
        mass: mass
    };
}

// Update simulation metrics display
function updateMetrics(results) {
    document.getElementById('energy-value').textContent = results.energy.toFixed(2);
    document.getElementById('crater-value').textContent = results.crater.toFixed(2);
    document.getElementById('overpressure-value').textContent = Math.floor(results.overpressure);
    document.getElementById('population-value').textContent = results.population.toLocaleString();
    
    // Update severity
    let severity = 'Minor';
    let severityClass = 'severity-minor';
    
    if (results.energy > 100) {
        severity = 'Catastrophic';
        severityClass = 'severity-catastrophic';
    } else if (results.energy > 10) {
        severity = 'Severe';
        severityClass = 'severity-severe';
    } else if (results.energy > 1) {
        severity = 'Moderate';
        severityClass = 'severity-moderate';
    }
    
    const severityElement = document.getElementById('severity-level');
    severityElement.textContent = severity;
    severityElement.className = `status-value ${severityClass}`;
}

// Run simulation
async function runSimulation() {
    if (simulationRunning) return;
    
    simulationRunning = true;
    document.getElementById('system-status').textContent = 'SIMULATING';
    document.getElementById('system-status').className = 'status-value severity-warning';
    
    // Get impact location
    const locationStr = document.getElementById('impact-location').value;
    const [lat, lng] = locationStr.split(',').map(s => parseFloat(s.trim()));
    
    if (isNaN(lat) || isNaN(lng)) {
        alert('Invalid location coordinates');
        simulationRunning = false;
        return;
    }
    
    const latlng = L.latLng(lat, lng);
    updateImpactMarker(latlng);
    map.setView(latlng, 8);
    
    // Calculate impact
    const results = calculateImpact();
    updateMetrics(results);
    
    // Show simulation overlay
    document.getElementById('simulation-overlay').style.display = 'block';
    
    // Simulate atmospheric entry
    await simulateEntry(latlng, results);
    
    // Show blast wave
    showBlastWave(latlng, results.crater);
    
    // Hide overlay after simulation
    setTimeout(() => {
        document.getElementById('simulation-overlay').style.display = 'none';
        document.getElementById('system-status').textContent = 'COMPLETE';
        document.getElementById('system-status').className = 'status-value severity-success';
        simulationRunning = false;
    }, 3000);
}

// Simulate atmospheric entry
function simulateEntry(latlng, results) {
    return new Promise((resolve) => {
        let altitude = 100; // Start at 100 km
        const velocity = parseFloat(document.getElementById('velocity').value);
        let mass = results.mass;
        
        const interval = setInterval(() => {
            altitude -= 5;
            mass *= 0.95; // Ablation
            
            document.getElementById('sim-altitude').textContent = altitude.toFixed(1);
            document.getElementById('sim-velocity').textContent = velocity.toFixed(1);
            document.getElementById('sim-mass').textContent = `${((mass / results.mass) * 100).toFixed(0)}%`;
            document.getElementById('sim-energy').textContent = `${(results.energy * (mass / results.mass)).toFixed(2)} MT`;
            
            if (altitude <= 0) {
                clearInterval(interval);
                resolve();
            }
        }, 100);
    });
}

// Show blast wave
function showBlastWave(latlng, craterDiameter) {
    if (blastCircle) {
        map.removeLayer(blastCircle);
    }
    
    const blastRadius = craterDiameter * 1000 * 10; // 10x crater diameter in meters
    
    blastCircle = L.circle(latlng, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.3,
        radius: blastRadius
    }).addTo(map);
    
    // Add shockwave rings
    for (let i = 1; i <= 3; i++) {
        setTimeout(() => {
            const ring = L.circle(latlng, {
                color: 'orange',
                fillColor: 'transparent',
                weight: 2,
                opacity: 0.8,
                radius: blastRadius * i * 0.5
            }).addTo(map);
            
            setTimeout(() => map.removeLayer(ring), 2000);
        }, i * 500);
    }
}

// Generate defense strategy using Gemini AI
async function generateDefenseStrategy() {
    const btn = document.getElementById('generate-defense');
    const content = document.getElementById('defense-strategy-content');
    const spinner = document.querySelector('#generate-defense .loading-spinner');
    
    if (!btn || !content) return;
    
    btn.disabled = true;
    if (spinner) spinner.style.display = 'inline-block';
    content.textContent = 'Analyzing threat and generating defense strategy...';
    
    const diameter = document.getElementById('diameter').value;
    const velocity = document.getElementById('velocity').value;
    const results = calculateImpact();
    
    const prompt = `You are a planetary defense expert. An asteroid is approaching Earth with the following characteristics:
- Diameter: ${diameter} meters
- Velocity: ${velocity} km/s
- Estimated impact energy: ${results.energy.toFixed(2)} megatons
- Potential crater size: ${results.crater.toFixed(2)} km
- Population at risk: ${results.population.toLocaleString()}

Generate a comprehensive defense strategy including:
1. Threat assessment
2. Recommended deflection method (kinetic impactor, nuclear, gravity tractor)
3. Timeline and mission requirements
4. Success probability
5. Backup contingency plans

Keep the response concise but actionable.`;

    try {
        const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.candidates && data.candidates[0]) {
            const text = data.candidates[0].content.parts[0].text;
            content.textContent = text;
        } else {
            content.textContent = 'Error: Unable to generate defense strategy. Please check your API key.';
        }
    } catch (error) {
        content.textContent = `Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        if (spinner) spinner.style.display = 'none';
    }
}

// Generate impact narrative using Gemini AI
async function generateImpactNarrative() {
    const btn = document.getElementById('generate-narrative');
    const content = document.getElementById('narrative-content');
    const spinner = document.querySelector('#generate-narrative .loading-spinner');
    
    if (!btn || !content) return;
    
    btn.disabled = true;
    if (spinner) spinner.style.display = 'inline-block';
    content.textContent = 'Generating impact scenario narrative...';
    
    const diameter = document.getElementById('diameter').value;
    const velocity = document.getElementById('velocity').value;
    const location = document.getElementById('impact-location').value;
    const results = calculateImpact();
    
    const prompt = `Write a dramatic but scientifically accurate narrative describing an asteroid impact with these parameters:
- Location: ${location}
- Diameter: ${diameter} meters
- Velocity: ${velocity} km/s
- Impact energy: ${results.energy.toFixed(2)} megatons
- Crater size: ${results.crater.toFixed(2)} km
- Population affected: ${results.population.toLocaleString()}

Describe:
1. The final moments before impact
2. The immediate aftermath
3. Regional and global consequences
4. Long-term effects

Keep it engaging but realistic. Limit to 250 words.`;

    try {
        const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.candidates && data.candidates[0]) {
            const text = data.candidates[0].content.parts[0].text;
            content.textContent = text;
        } else {
            content.textContent = 'Error: Unable to generate narrative. Please check your API key.';
        }
    } catch (error) {
        content.textContent = `Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        if (spinner) spinner.style.display = 'none';
    }
}

// Reset simulation
function resetSimulation() {
    if (impactMarker) map.removeLayer(impactMarker);
    if (blastCircle) map.removeLayer(blastCircle);
    if (trajectoryLine) map.removeLayer(trajectoryLine);
    
    document.getElementById('energy-value').textContent = '0.00';
    document.getElementById('crater-value').textContent = '0.0';
    document.getElementById('overpressure-value').textContent = '0';
    document.getElementById('population-value').textContent = '0';
    document.getElementById('severity-level').textContent = 'Minor';
    document.getElementById('severity-level').className = 'status-value severity-minor';
    document.getElementById('system-status').textContent = 'READY';
    document.getElementById('system-status').className = 'status-value severity-minor';
    
    map.setView([23.6345, -102.5528], 5);
}

// Load historical scenarios
function loadScenario(scenario) {
    const scenarios = {
        chelyabinsk: {
            diameter: 20,
            velocity: 19,
            angle: 20,
            density: 3300,
            location: '54.8150, 61.3700',
            type: 'rocky'
        },
        tunguska: {
            diameter: 60,
            velocity: 27,
            angle: 30,
            density: 1000,
            location: '60.8858, 101.8939',
            type: 'porous'
        }
    };
    
    const data = scenarios[scenario];
    if (!data) return;
    
    document.getElementById('diameter').value = data.diameter;
    document.getElementById('velocity').value = data.velocity;
    document.getElementById('angle').value = data.angle;
    document.getElementById('density').value = data.density;
    document.getElementById('impact-location').value = data.location;
    document.getElementById('meteoroid-type').value = data.type;
    
    updateSliderValues();
}

// Update slider value displays
function updateSliderValues() {
    document.getElementById('diameter-value').textContent = document.getElementById('diameter').value;
    document.getElementById('velocity-value').textContent = document.getElementById('velocity').value;
    document.getElementById('angle-value').textContent = document.getElementById('angle').value;
    document.getElementById('density-value').textContent = document.getElementById('density').value;
}

// Update UTC time
function updateTime() {
    const now = new Date();
    document.getElementById('utc-time').textContent = now.toUTCString().slice(17, 25);
}

// Layer toggle functionality
function toggleLayer(layerId) {
    const checkbox = document.querySelector(`#${layerId} .layer-checkbox`);
    checkbox.classList.toggle('checked');
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    updateTime();
    setInterval(updateTime, 1000);
    
    // Slider updates
    document.getElementById('diameter').addEventListener('input', updateSliderValues);
    document.getElementById('velocity').addEventListener('input', updateSliderValues);
    document.getElementById('angle').addEventListener('input', updateSliderValues);
    document.getElementById('density').addEventListener('input', updateSliderValues);
    
    // Meteoroid type selector
    document.getElementById('meteoroid-type').addEventListener('change', function() {
        const densities = {
            'rocky': 3000,
            'metallic': 7800,
            'carbonaceous': 1500,
            'porous': 1000
        };
        const density = densities[this.value];
        document.getElementById('density').value = density;
        updateSliderValues();
    });
    
    // Buttons
    document.getElementById('run-simulation').addEventListener('click', runSimulation);
    document.getElementById('reset-simulation').addEventListener('click', resetSimulation);
    
    // Historical scenarios
    document.querySelectorAll('.btn-scenario').forEach(btn => {
        btn.addEventListener('click', function() {
            loadScenario(this.dataset.scenario);
        });
    });
    
    // Layer controls
    document.getElementById('layer-population').addEventListener('click', () => toggleLayer('layer-population'));
    document.getElementById('layer-blast').addEventListener('click', () => toggleLayer('layer-blast'));
    
    // AI features (if buttons exist)
    const defenseBtn = document.getElementById('generate-defense');
    const narrativeBtn = document.getElementById('generate-narrative');
    
    if (defenseBtn) {
        defenseBtn.addEventListener('click', generateDefenseStrategy);
    }
    
    if (narrativeBtn) {
        narrativeBtn.addEventListener('click', generateImpactNarrative);
    }
});

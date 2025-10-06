"""
🌌 Meteorite Madness - Interactive Web Application
=====================================================
Flask-based web application for planetary defense analysis
"""

from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime, timedelta
import sys
sys.path.append('.')
from main import NASAAPIClient
from impact_consequence_simulator import (
    ImpactConsequenceSimulator, 
    ImpactEvent,
    USGSDataIntegrator,
    PopulationImpactAssessor,
    EconomicImpactCalculator
)
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meteorite-madness-2025'

# Global instances
nasa_client = None
impact_simulator = None

def initialize_clients():
    """Initialize NASA and impact analysis clients"""
    global nasa_client, impact_simulator
    if nasa_client is None:
        # Use NASA DEMO_KEY or environment variable
        import os
        api_key = os.environ.get('NASA_API_KEY', 'DEMO_KEY')
        nasa_client = NASAAPIClient(api_key)
    if impact_simulator is None:
        import os
        api_key = os.environ.get('NASA_API_KEY', 'DEMO_KEY')
        impact_simulator = ImpactConsequenceSimulator(api_key)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/impact-simulator')
def impact_simulator():
    """Advanced interactive impact simulation page with Leaflet map"""
    return render_template('impact_simulation.html')

@app.route('/api/impact/advanced-simulate', methods=['POST'])
def advanced_impact_simulation():
    """Advanced impact simulation with detailed atmospheric entry modeling"""
    try:
        data = request.json
        
        # Extract parameters
        diameter_m = float(data.get('diameter', 100))
        velocity_kms = float(data.get('velocity', 20))
        density = float(data.get('density', 3000))
        angle = float(data.get('angle', 45))
        location = data.get('location', '19.4326, -99.1332')
        
        # Parse location
        lat, lon = map(float, location.split(','))
        
        # Calculate impact metrics
        diameter_km = diameter_m / 1000
        velocity_ms = velocity_kms * 1000
        
        # Mass calculation
        volume = (4/3) * np.pi * (diameter_m/2)**3
        mass_kg = volume * density
        
        # Energy calculation
        energy_joules = 0.5 * mass_kg * velocity_ms**2
        energy_megatons = energy_joules / 4.184e15
        
        # Crater diameter (empirical scaling)
        crater_diameter_km = (energy_joules * 1e-12)**(1/3.4) * 0.05
        
        # Blast radius
        blast_radius_km = 0.28 * (energy_megatons ** 0.33)
        
        # Overpressure (simplified)
        overpressure_kpa = min(energy_megatons * 100, 50000)
        
        # Population estimate (very rough)
        population_affected = int(energy_megatons * 500000)
        
        # Atmospheric entry simulation data
        atmospheric_data = simulate_atmospheric_entry(
            diameter_m, velocity_kms, density, angle
        )
        
        return jsonify({
            'success': True,
            'metrics': {
                'energy_megatons': round(energy_megatons, 2),
                'crater_diameter_km': round(crater_diameter_km, 2),
                'blast_radius_km': round(blast_radius_km, 2),
                'overpressure_kpa': round(overpressure_kpa, 0),
                'population_affected': population_affected,
                'impact_location': [lat, lon]
            },
            'atmospheric_entry': atmospheric_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def simulate_atmospheric_entry(diameter_m, velocity_kms, density, angle):
    """Simulate atmospheric entry with ablation and drag effects"""
    altitude = 120  # km
    velocity = velocity_kms
    
    volume = (4/3) * np.pi * (diameter_m/2)**3
    mass = volume * density
    initial_mass = mass
    
    steps = 24
    altitude_step = 120 / steps
    
    trajectory = []
    
    for step in range(steps):
        altitude -= altitude_step
        
        # Atmospheric effects
        density_factor = 1 - np.exp(-altitude / 10)
        drag = 0.05 * density_factor
        ablation_rate = 0.02 * density_factor * (velocity / 20)
        
        velocity = velocity * (1 - drag)
        mass = max(mass * (1 - ablation_rate), initial_mass * 0.05)
        
        mass_percentage = (mass / initial_mass) * 100
        energy_liberated = (initial_mass - mass) * (velocity * 1000)**2 / 4.184e12
        
        trajectory.append({
            'altitude': round(max(0, altitude), 1),
            'velocity': round(velocity, 1),
            'mass_percentage': round(mass_percentage, 1),
            'energy_liberated': round(energy_liberated, 1)
        })
        
        if altitude <= 0:
            break
    
    return trajectory

@app.route('/api/neo/recent')
def get_recent_neos():
    """Get recent Near Earth Objects data"""
    initialize_clients()
    
    try:
        # Get data for the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        neo_data = nasa_client.get_neo_feed(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Process and structure the data
        asteroids = []
        if neo_data and 'near_earth_objects' in neo_data:
            for date, objects in neo_data['near_earth_objects'].items():
                for obj in objects:
                    asteroids.append({
                        'id': obj.get('id', 'Unknown'),
                        'name': obj.get('name', 'Unknown'),
                        'diameter_km': obj['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        'velocity_kmh': float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                        'miss_distance_km': float(obj['close_approach_data'][0]['miss_distance']['kilometers']),
                        'is_hazardous': obj.get('is_potentially_hazardous_asteroid', False),
                        'approach_date': obj['close_approach_data'][0]['close_approach_date']
                    })
        
        return jsonify({
            'success': True,
            'count': len(asteroids),
            'asteroids': sorted(asteroids, key=lambda x: x['diameter_km'], reverse=True)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/impact/simulate', methods=['POST'])
def simulate_impact():
    """Simulate asteroid impact on specified location"""
    initialize_clients()
    
    try:
        data = request.json
        asteroid_id = data.get('asteroid_id')
        latitude = float(data.get('latitude', 40.7128))
        longitude = float(data.get('longitude', -74.0060))
        
        # Fetch NEO data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        neo_data = nasa_client.get_neo_feed(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Find the specific asteroid
        target_asteroid = None
        if neo_data and 'near_earth_objects' in neo_data:
            for date, objects in neo_data['near_earth_objects'].items():
                for obj in objects:
                    if obj.get('id') == asteroid_id or obj.get('name') == asteroid_id:
                        target_asteroid = obj
                        break
                if target_asteroid:
                    break
        
        if not target_asteroid:
            return jsonify({
                'success': False,
                'error': 'Asteroid not found'
            }), 404
        
        # Create impact event
        impact_event = ImpactEvent(
            asteroid_name=target_asteroid.get('name', 'Unknown'),
            diameter_km=target_asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
            velocity_kmh=float(target_asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
            impact_location=(latitude, longitude)
        )
        
        # Run simulation
        result = impact_simulator.simulate_impact(impact_event)
        
        return jsonify({
            'success': True,
            'impact_data': {
                'asteroid_name': result.asteroid_name,
                'diameter_km': result.diameter_km,
                'velocity_kmh': result.velocity_kmh,
                'impact_energy_megatons': result.impact_energy_megatons,
                'crater_diameter_km': result.crater_diameter_km,
                'blast_radius_km': result.blast_radius_km,
                'seismic_magnitude': result.seismic_magnitude,
                'population_affected': result.population_affected,
                'economic_damage_usd': result.economic_damage_usd,
                'impact_location': result.impact_location,
                'usgs_earthquakes': len(result.usgs_data.get('earthquakes', [])) if result.usgs_data else 0
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visualizations/threat-map')
def threat_map():
    """Generate interactive threat map visualization"""
    initialize_clients()
    
    try:
        # Get recent NEO data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        neo_data = nasa_client.get_neo_feed(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Major world cities for impact simulation
        cities = [
            {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},
            {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
            {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
            {'name': 'Mexico City', 'lat': 19.4326, 'lon': -99.1332},
            {'name': 'Delhi', 'lat': 28.6139, 'lon': 77.2090},
            {'name': 'São Paulo', 'lat': -23.5505, 'lon': -46.6333},
            {'name': 'Cairo', 'lat': 30.0444, 'lon': 31.2357},
            {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093},
        ]
        
        # Extract top asteroids
        asteroids = []
        if neo_data and 'near_earth_objects' in neo_data:
            for date, objects in neo_data['near_earth_objects'].items():
                for obj in objects[:10]:  # Top 10
                    asteroids.append({
                        'name': obj.get('name', 'Unknown'),
                        'diameter': obj['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        'velocity': float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                        'hazardous': obj.get('is_potentially_hazardous_asteroid', False)
                    })
        
        asteroids = sorted(asteroids, key=lambda x: x['diameter'], reverse=True)[:5]
        
        # Create map data
        map_data = []
        for city in cities:
            for asteroid in asteroids[:3]:  # Top 3 threats
                # Quick impact calculation
                mass_kg = (4/3) * np.pi * (asteroid['diameter']/2 * 1000)**3 * 3000  # Density ~3000 kg/m³
                velocity_ms = asteroid['velocity'] * 1000 / 3600
                energy_joules = 0.5 * mass_kg * velocity_ms**2
                energy_megatons = energy_joules / 4.184e15
                blast_radius = 0.28 * (energy_megatons ** 0.33)
                
                map_data.append({
                    'city': city['name'],
                    'lat': city['lat'],
                    'lon': city['lon'],
                    'asteroid': asteroid['name'],
                    'energy': energy_megatons,
                    'blast_radius': blast_radius,
                    'hazardous': asteroid['hazardous']
                })
        
        # Create interactive map
        fig = go.Figure()
        
        # Add city markers with threat circles
        for item in map_data:
            # Threat circle
            circle_lats = []
            circle_lons = []
            for angle in np.linspace(0, 2*np.pi, 50):
                # Approximate circle in lat/lon
                dlat = item['blast_radius'] / 111  # 111 km per degree lat
                dlon = item['blast_radius'] / (111 * np.cos(np.radians(item['lat'])))
                circle_lats.append(item['lat'] + dlat * np.sin(angle))
                circle_lons.append(item['lon'] + dlon * np.cos(angle))
            
            fig.add_trace(go.Scattergeo(
                lon=circle_lons,
                lat=circle_lats,
                mode='lines',
                line=dict(width=1, color='red' if item['hazardous'] else 'orange'),
                fill='toself',
                fillcolor='rgba(255,0,0,0.1)' if item['hazardous'] else 'rgba(255,165,0,0.1)',
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Add city markers
        cities_unique = {item['city']: (item['lat'], item['lon']) for item in map_data}
        fig.add_trace(go.Scattergeo(
            lon=[coords[1] for coords in cities_unique.values()],
            lat=[coords[0] for coords in cities_unique.values()],
            mode='markers+text',
            marker=dict(size=10, color='darkblue', symbol='circle'),
            text=list(cities_unique.keys()),
            textposition='top center',
            hoverinfo='text',
            name='Major Cities'
        ))
        
        fig.update_layout(
            title='Global Asteroid Impact Threat Assessment',
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(230, 245, 255)'
            ),
            height=600,
            showlegend=True
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualizations/threat-analysis')
def threat_analysis():
    """Generate comprehensive threat analysis charts"""
    initialize_clients()
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        neo_data = nasa_client.get_neo_feed(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        # Process data
        asteroids = []
        if neo_data and 'near_earth_objects' in neo_data:
            for date, objects in neo_data['near_earth_objects'].items():
                for obj in objects:
                    diameter = obj['estimated_diameter']['kilometers']['estimated_diameter_max']
                    velocity = float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
                    
                    # Calculate impact energy
                    mass_kg = (4/3) * np.pi * (diameter/2 * 1000)**3 * 3000
                    velocity_ms = velocity * 1000 / 3600
                    energy_joules = 0.5 * mass_kg * velocity_ms**2
                    energy_megatons = energy_joules / 4.184e15
                    
                    asteroids.append({
                        'name': obj.get('name', 'Unknown'),
                        'diameter': diameter,
                        'velocity': velocity,
                        'energy': energy_megatons,
                        'hazardous': obj.get('is_potentially_hazardous_asteroid', False),
                        'miss_distance': float(obj['close_approach_data'][0]['miss_distance']['kilometers'])
                    })
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Size vs Impact Energy',
                'Velocity Distribution',
                'Hazardous vs Non-Hazardous',
                'Miss Distance Analysis'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "histogram"}],
                [{"type": "pie"}, {"type": "scatter"}]
            ]
        )
        
        # 1. Size vs Energy scatter
        hazardous = [a for a in asteroids if a['hazardous']]
        non_hazardous = [a for a in asteroids if not a['hazardous']]
        
        fig.add_trace(
            go.Scatter(
                x=[a['diameter'] for a in hazardous],
                y=[a['energy'] for a in hazardous],
                mode='markers',
                marker=dict(size=10, color='red'),
                name='Hazardous',
                text=[a['name'] for a in hazardous],
                hovertemplate='<b>%{text}</b><br>Diameter: %{x:.3f} km<br>Energy: %{y:.2f} MT'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[a['diameter'] for a in non_hazardous],
                y=[a['energy'] for a in non_hazardous],
                mode='markers',
                marker=dict(size=8, color='blue'),
                name='Non-Hazardous',
                text=[a['name'] for a in non_hazardous],
                hovertemplate='<b>%{text}</b><br>Diameter: %{x:.3f} km<br>Energy: %{y:.2f} MT'
            ),
            row=1, col=1
        )
        
        # 2. Velocity histogram
        fig.add_trace(
            go.Histogram(
                x=[a['velocity'] for a in asteroids],
                nbinsx=20,
                marker_color='purple',
                name='Velocity',
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 3. Hazardous pie chart
        hazard_counts = {
            'Hazardous': len(hazardous),
            'Non-Hazardous': len(non_hazardous)
        }
        
        fig.add_trace(
            go.Pie(
                labels=list(hazard_counts.keys()),
                values=list(hazard_counts.values()),
                marker=dict(colors=['red', 'blue']),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # 4. Miss distance vs size
        fig.add_trace(
            go.Scatter(
                x=[a['diameter'] for a in asteroids],
                y=[a['miss_distance'] for a in asteroids],
                mode='markers',
                marker=dict(
                    size=[a['energy']*2 for a in asteroids],
                    color=[a['velocity'] for a in asteroids],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Velocity<br>(km/h)", x=1.15)
                ),
                text=[a['name'] for a in asteroids],
                hovertemplate='<b>%{text}</b><br>Diameter: %{x:.3f} km<br>Miss: %{y:.0f} km',
                showlegend=False
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_xaxes(title_text="Diameter (km)", row=1, col=1)
        fig.update_yaxes(title_text="Impact Energy (MT)", type="log", row=1, col=1)
        fig.update_xaxes(title_text="Velocity (km/h)", row=1, col=2)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_xaxes(title_text="Diameter (km)", row=2, col=2)
        fig.update_yaxes(title_text="Miss Distance (km)", type="log", row=2, col=2)
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Comprehensive Asteroid Threat Analysis"
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get overall statistics about NEO data"""
    initialize_clients()
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        neo_data = nasa_client.get_neo_feed(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        total_count = 0
        hazardous_count = 0
        total_energy = 0
        largest_asteroid = None
        fastest_asteroid = None
        
        if neo_data and 'near_earth_objects' in neo_data:
            for date, objects in neo_data['near_earth_objects'].items():
                total_count += len(objects)
                for obj in objects:
                    if obj.get('is_potentially_hazardous_asteroid', False):
                        hazardous_count += 1
                    
                    diameter = obj['estimated_diameter']['kilometers']['estimated_diameter_max']
                    velocity = float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
                    
                    # Calculate energy
                    mass_kg = (4/3) * np.pi * (diameter/2 * 1000)**3 * 3000
                    velocity_ms = velocity * 1000 / 3600
                    energy_megatons = (0.5 * mass_kg * velocity_ms**2) / 4.184e15
                    total_energy += energy_megatons
                    
                    if largest_asteroid is None or diameter > largest_asteroid['diameter']:
                        largest_asteroid = {
                            'name': obj.get('name'),
                            'diameter': diameter,
                            'velocity': velocity
                        }
                    
                    if fastest_asteroid is None or velocity > fastest_asteroid['velocity']:
                        fastest_asteroid = {
                            'name': obj.get('name'),
                            'diameter': diameter,
                            'velocity': velocity
                        }
        
        return jsonify({
            'total_asteroids': total_count,
            'hazardous_asteroids': hazardous_count,
            'hazard_percentage': round((hazardous_count / total_count * 100) if total_count > 0 else 0, 1),
            'total_energy_megatons': round(total_energy, 2),
            'largest_asteroid': largest_asteroid,
            'fastest_asteroid': fastest_asteroid,
            'average_energy': round(total_energy / total_count, 2) if total_count > 0 else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Meteorite Madness Web Application...")
    print("📡 Initializing NASA API client...")
    initialize_clients()
    print("✅ Ready! Access the app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

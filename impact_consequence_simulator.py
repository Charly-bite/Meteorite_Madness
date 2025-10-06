#!/usr/bin/env python3
"""
Meteor Impact Consequence Simulator
Combines NEO data with USGS, population, and economic data to model real-world impact consequences
"""

import numpy as np
import pandas as pd
import requests
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime

@dataclass
class ImpactEvent:
    """Data class for meteor impact events"""
    asteroid_name: str
    diameter_km: float
    velocity_kmh: float
    impact_location: Tuple[float, float]  # lat, lon
    impact_energy_megatons: float
    crater_diameter_km: float
    blast_radius_km: float
    population_affected: int
    economic_damage_usd: float
    seismic_magnitude: float

class USGSDataIntegrator:
    """Integration with USGS APIs for geological and seismic data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.earthquake_api = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.elevation_api = "https://nationalmap.gov/epqs/pqs.php"
        
    def get_earthquake_data(self, lat: float, lon: float, radius_km: float = 100) -> Optional[Dict]:
        """Get historical earthquake data for impact location"""
        try:
            params = {
                'format': 'geojson',
                'latitude': lat,
                'longitude': lon,
                'maxradiuskm': radius_km,
                'minmagnitude': 4.0,
                'limit': 100
            }
            
            print(f"🌍 Fetching earthquake data for ({lat:.2f}, {lon:.2f})...")
            response = self.session.get(self.earthquake_api, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Retrieved {len(data.get('features', []))} earthquake records")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching earthquake data: {e}")
            return None
    
    def get_elevation_data(self, lat: float, lon: float) -> Optional[float]:
        """Get elevation data for impact location"""
        try:
            params = {
                'x': lon,
                'y': lat,
                'units': 'Meters',
                'output': 'json'
            }
            
            response = self.session.get(self.elevation_api, params=params, timeout=8)
            response.raise_for_status()
            
            data = response.json()
            elevation = data.get('USGS_Elevation_Point_Query_Service', {}).get('Elevation_Query', {}).get('Elevation')
            
            if elevation:
                print(f"🏔️  Elevation at impact site: {elevation} meters")
                return float(elevation)
            
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"⚠️  Could not fetch elevation data: {e}")
            return None

class ImpactPhysicsCalculator:
    """Calculate physical consequences of meteor impacts"""
    
    def __init__(self):
        # Physical constants and empirical formulas
        self.earth_density = 5515  # kg/m³
        self.rock_density = 2600   # kg/m³
        self.gravity = 9.81        # m/s²
        
    def calculate_impact_energy(self, diameter_km: float, velocity_kmh: float, density_kg_m3: float = 2600) -> float:
        """Calculate kinetic energy of impact in megatons TNT equivalent"""
        # Convert units
        diameter_m = diameter_km * 1000
        velocity_ms = velocity_kmh / 3.6
        
        # Calculate mass (sphere volume * density)
        volume_m3 = (4/3) * math.pi * (diameter_m/2)**3
        mass_kg = volume_m3 * density_kg_m3
        
        # Kinetic energy in joules
        energy_joules = 0.5 * mass_kg * velocity_ms**2
        
        # Convert to megatons TNT (1 megaton = 4.184 × 10^15 joules)
        energy_megatons = energy_joules / (4.184e15)
        
        return energy_megatons
    
    def calculate_crater_diameter(self, energy_megatons: float) -> float:
        """Calculate crater diameter using empirical scaling laws"""
        # Empirical formula: D = 1.8 * (E^0.28) where D is in km, E in megatons
        crater_diameter_km = 1.8 * (energy_megatons ** 0.28)
        return crater_diameter_km
    
    def calculate_blast_radius(self, energy_megatons: float) -> float:
        """Calculate blast radius for significant damage"""
        # Empirical formula for blast radius (severe damage threshold)
        # R = 0.28 * (E^0.33) where R is in km, E in megatons
        blast_radius_km = 0.28 * (energy_megatons ** 0.33)
        return blast_radius_km
    
    def calculate_seismic_magnitude(self, energy_megatons: float) -> float:
        """Estimate seismic magnitude from impact energy"""
        # Empirical relationship between energy and magnitude
        # M = (2/3) * log10(E) + 3.2 where E is in megatons
        if energy_megatons > 0:
            magnitude = (2/3) * math.log10(energy_megatons) + 3.2
            return max(magnitude, 0)  # Ensure non-negative
        return 0

class PopulationImpactAssessor:
    """Assess population impact based on blast radius and population density"""
    
    def __init__(self):
        self.population_data = {}
        
    def load_population_data(self, world_bank_data: pd.DataFrame):
        """Load population data from World Bank API"""
        if not world_bank_data.empty:
            self.population_data = world_bank_data.to_dict('records')
    
    def estimate_population_in_radius(self, lat: float, lon: float, radius_km: float) -> int:
        """Estimate population within blast radius"""
        # Simplified calculation using global population density
        # Average global population density: ~15 people per km²
        area_km2 = math.pi * radius_km**2
        
        # Adjust for geographic location (rough estimates)
        population_density = self._get_population_density_estimate(lat, lon)
        estimated_population = int(area_km2 * population_density)
        
        return estimated_population
    
    def _get_population_density_estimate(self, lat: float, lon: float) -> float:
        """Estimate population density based on coordinates"""
        # Very simplified model - in reality would use detailed census data
        
        # Urban areas (major cities) - higher density
        urban_centers = [
            (40.7128, -74.0060),   # New York
            (51.5074, -0.1278),    # London  
            (35.6762, 139.6503),   # Tokyo
            (19.4326, -99.1332),   # Mexico City
            (28.6139, 77.2090),    # Delhi
        ]
        
        # Check if near major urban center
        for city_lat, city_lon in urban_centers:
            distance = self._calculate_distance(lat, lon, city_lat, city_lon)
            if distance < 100:  # Within 100km of major city
                return 1000  # High density
        
        # Check latitude bands for general density
        abs_lat = abs(lat)
        
        if abs_lat < 30:  # Tropical regions
            return 50
        elif abs_lat < 60:  # Temperate regions  
            return 20
        else:  # Polar regions
            return 1
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

class EconomicImpactCalculator:
    """Calculate economic consequences of meteor impacts"""
    
    def __init__(self):
        # Economic constants (in USD)
        self.gdp_per_capita_global = 12000  # Average global GDP per capita
        self.infrastructure_cost_per_km2 = 50000000  # $50M per km² (rough estimate)
        
    def calculate_economic_damage(self, population_affected: int, blast_radius_km: float, 
                                 crater_diameter_km: float) -> float:
        """Calculate total economic damage from impact"""
        
        # Direct infrastructure damage
        affected_area_km2 = math.pi * blast_radius_km**2
        infrastructure_damage = affected_area_km2 * self.infrastructure_cost_per_km2
        
        # Human capital loss (economic value)
        human_capital_loss = population_affected * self.gdp_per_capita_global * 10  # 10 years of GDP
        
        # Agricultural/land loss
        crater_area_km2 = math.pi * (crater_diameter_km/2)**2
        land_value_loss = crater_area_km2 * 1000000  # $1M per km² land value
        
        # Emergency response and recovery costs
        response_costs = (infrastructure_damage + human_capital_loss) * 0.3  # 30% additional
        
        total_damage = infrastructure_damage + human_capital_loss + land_value_loss + response_costs
        
        return total_damage

class ImpactConsequenceSimulator:
    """Main simulator combining all impact assessment components"""
    
    def __init__(self, nasa_api_key: str):
        self.nasa_api_key = nasa_api_key
        self.usgs_integrator = USGSDataIntegrator()
        self.physics_calculator = ImpactPhysicsCalculator()
        self.population_assessor = PopulationImpactAssessor()
        self.economic_calculator = EconomicImpactCalculator()
        
    def simulate_impact(self, asteroid_data: Dict, impact_lat: float, impact_lon: float) -> ImpactEvent:
        """Simulate complete impact consequences for an asteroid"""
        
        print(f"\n🔥 SIMULATING IMPACT: {asteroid_data.get('name', 'Unknown Asteroid')}")
        print(f"📍 Impact Location: ({impact_lat:.2f}°, {impact_lon:.2f}°)")
        print("="*60)
        
        # Extract asteroid parameters
        diameter_km = asteroid_data.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max', 0.1)
        velocity_kmh = float(asteroid_data.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_hour', 50000))
        name = asteroid_data.get('name', 'Unknown Asteroid')
        
        # Calculate physical consequences
        print("⚡ Calculating impact physics...")
        energy_megatons = self.physics_calculator.calculate_impact_energy(diameter_km, velocity_kmh)
        crater_diameter = self.physics_calculator.calculate_crater_diameter(energy_megatons)
        blast_radius = self.physics_calculator.calculate_blast_radius(energy_megatons)
        seismic_magnitude = self.physics_calculator.calculate_seismic_magnitude(energy_megatons)
        
        # Assess population impact
        print("👥 Assessing population impact...")
        population_affected = self.population_assessor.estimate_population_in_radius(
            impact_lat, impact_lon, blast_radius
        )
        
        # Calculate economic damage
        print("💰 Calculating economic consequences...")
        economic_damage = self.economic_calculator.calculate_economic_damage(
            population_affected, blast_radius, crater_diameter
        )
        
        # Get geological context
        print("🌍 Gathering geological data...")
        earthquake_data = self.usgs_integrator.get_earthquake_data(impact_lat, impact_lon)
        elevation = self.usgs_integrator.get_elevation_data(impact_lat, impact_lon)
        
        # Create impact event
        impact_event = ImpactEvent(
            asteroid_name=name,
            diameter_km=diameter_km,
            velocity_kmh=velocity_kmh,
            impact_location=(impact_lat, impact_lon),
            impact_energy_megatons=energy_megatons,
            crater_diameter_km=crater_diameter,
            blast_radius_km=blast_radius,
            population_affected=population_affected,
            economic_damage_usd=economic_damage,
            seismic_magnitude=seismic_magnitude
        )
        
        # Print summary
        self._print_impact_summary(impact_event)
        
        return impact_event
    
    def _print_impact_summary(self, impact: ImpactEvent):
        """Print detailed impact summary"""
        print(f"\n🎯 IMPACT ASSESSMENT COMPLETE")
        print(f"{'='*60}")
        print(f"🌌 Asteroid: {impact.asteroid_name}")
        print(f"📏 Diameter: {impact.diameter_km:.3f} km")
        print(f"🚀 Velocity: {impact.velocity_kmh:,.0f} km/h")
        print(f"⚡ Impact Energy: {impact.impact_energy_megatons:.2f} megatons")
        print(f"🕳️  Crater Diameter: {impact.crater_diameter_km:.2f} km")
        print(f"💥 Blast Radius: {impact.blast_radius_km:.2f} km")
        print(f"📊 Seismic Magnitude: {impact.seismic_magnitude:.1f}")
        print(f"👥 Population Affected: {impact.population_affected:,}")
        print(f"💰 Economic Damage: ${impact.economic_damage_usd:,.0f}")
        print(f"{'='*60}")

    def create_impact_visualization(self, impact_events: List[ImpactEvent]) -> go.Figure:
        """Create comprehensive impact visualization"""
        
        if not impact_events:
            print("No impact events to visualize")
            return go.Figure()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Global Impact Map', 'Energy vs Damage', 'Population Risk', 'Economic Impact'),
            specs=[[{"type": "scattergeo"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Extract data for plotting
        names = [event.asteroid_name for event in impact_events]
        lats = [event.impact_location[0] for event in impact_events]
        lons = [event.impact_location[1] for event in impact_events]
        energies = [event.impact_energy_megatons for event in impact_events]
        damages = [event.economic_damage_usd for event in impact_events]
        populations = [event.population_affected for event in impact_events]
        blast_radii = [event.blast_radius_km for event in impact_events]
        
        # 1. Global impact map
        fig.add_trace(
            go.Scattergeo(
                lon=lons,
                lat=lats,
                text=names,
                mode='markers',
                marker=dict(
                    size=[max(5, min(50, energy/10)) for energy in energies],
                    color=energies,
                    colorscale='Reds',
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<b>%{text}</b><br>' +
                             'Location: (%{lat:.2f}, %{lon:.2f})<br>' +
                             'Energy: %{marker.color:.2f} MT<br>' +
                             '<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Energy vs Economic Damage
        fig.add_trace(
            go.Scatter(
                x=energies,
                y=damages,
                mode='markers+text',
                text=[name.split()[0] for name in names],
                textposition="top center",
                marker=dict(size=10, color='red', opacity=0.7),
                hovertemplate='<b>%{text}</b><br>' +
                             'Energy: %{x:.2f} MT<br>' +
                             'Damage: $%{y:,.0f}<br>' +
                             '<extra></extra>'
            ),
            row=1, col=2
        )
        
        # 3. Population at Risk
        fig.add_trace(
            go.Bar(
                x=[name.split()[0] for name in names],
                y=populations,
                marker_color='orange',
                hovertemplate='<b>%{x}</b><br>' +
                             'Population: %{y:,}<br>' +
                             '<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Blast Radius vs Economic Impact
        fig.add_trace(
            go.Scatter(
                x=blast_radii,
                y=damages,
                mode='markers+text',
                text=[name.split()[0] for name in names],
                textposition="top center",
                marker=dict(
                    size=[max(5, pop/50000) for pop in populations],
                    color='darkred',
                    opacity=0.7
                ),
                hovertemplate='<b>%{text}</b><br>' +
                             'Blast Radius: %{x:.2f} km<br>' +
                             'Economic Damage: $%{y:,.0f}<br>' +
                             '<extra></extra>'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_geos(
            projection_type="natural earth",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            coastlinecolor="rgb(204, 204, 204)",
        )
        
        fig.update_layout(
            title_text="🔥 Meteor Impact Consequence Analysis",
            title_x=0.5,
            showlegend=False,
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white')
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Impact Energy (Megatons)", row=1, col=2, gridcolor='gray')
        fig.update_yaxes(title_text="Economic Damage (USD)", row=1, col=2, gridcolor='gray')
        fig.update_xaxes(title_text="Asteroid", row=2, col=1, gridcolor='gray')
        fig.update_yaxes(title_text="Population Affected", row=2, col=1, gridcolor='gray')
        fig.update_xaxes(title_text="Blast Radius (km)", row=2, col=2, gridcolor='gray')
        fig.update_yaxes(title_text="Economic Damage (USD)", row=2, col=2, gridcolor='gray')
        
        return fig

def main():
    """Main function to demonstrate impact consequence simulation"""
    
    print("🔥 METEOR IMPACT CONSEQUENCE SIMULATOR")
    print("="*50)
    print("Combining NEO data with USGS geological data for comprehensive impact assessment")
    
    # Initialize simulator
    nasa_api_key = "Ch4TrNR37h2gfN5g1vyRcLsgtHeKv9SPw5aDHplE"
    simulator = ImpactConsequenceSimulator(nasa_api_key)
    
    # Sample asteroid data (would come from real NEO API)
    sample_asteroids = [
        {
            "name": "2024 TM3",
            "estimated_diameter": {"kilometers": {"estimated_diameter_max": 0.030}},
            "close_approach_data": [{"relative_velocity": {"kilometers_per_hour": "45000"}}]
        },
        {
            "name": "186822 (2004 FE31)", 
            "estimated_diameter": {"kilometers": {"estimated_diameter_max": 1.637}},
            "close_approach_data": [{"relative_velocity": {"kilometers_per_hour": "25000"}}]
        },
        {
            "name": "2019 FT",
            "estimated_diameter": {"kilometers": {"estimated_diameter_max": 0.025}},
            "close_approach_data": [{"relative_velocity": {"kilometers_per_hour": "108673"}}]
        }
    ]
    
    # Simulate impacts at different locations
    impact_locations = [
        (40.7128, -74.0060),  # New York City
        (51.5074, -0.1278),   # London
        (35.6762, 139.6503),  # Tokyo
    ]
    
    impact_events = []
    
    for i, asteroid in enumerate(sample_asteroids):
        if i < len(impact_locations):
            lat, lon = impact_locations[i]
            impact_event = simulator.simulate_impact(asteroid, lat, lon)
            impact_events.append(impact_event)
    
    # Create comprehensive visualization
    print("\n🎨 Creating impact consequence visualization...")
    fig = simulator.create_impact_visualization(impact_events)
    
    # Save visualization
    fig.write_html("meteor_impact_consequences.html")
    print("✅ Impact consequence visualization saved to 'meteor_impact_consequences.html'")
    
    # Generate impact report
    print("\n📋 Generating comprehensive impact assessment report...")
    
    report = f"""
🔥 METEOR IMPACT CONSEQUENCE ASSESSMENT REPORT
{'='*70}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 SCENARIO ANALYSIS:
Total Scenarios Analyzed: {len(impact_events)}
Combined Population at Risk: {sum(event.population_affected for event in impact_events):,}
Total Economic Damage: ${sum(event.economic_damage_usd for event in impact_events):,.0f}

🎯 INDIVIDUAL IMPACT SCENARIOS:
"""
    
    for i, event in enumerate(impact_events, 1):
        report += f"""
Scenario {i}: {event.asteroid_name}
{'─'*40}
📍 Location: {event.impact_location[0]:.2f}°N, {event.impact_location[1]:.2f}°E
⚡ Energy: {event.impact_energy_megatons:.2f} megatons TNT equivalent
🕳️  Crater: {event.crater_diameter_km:.2f} km diameter
💥 Blast: {event.blast_radius_km:.2f} km radius
📊 Seismic: Magnitude {event.seismic_magnitude:.1f} earthquake
👥 Casualties: {event.population_affected:,} people affected
💰 Economic: ${event.economic_damage_usd:,.0f} in damages
"""
    
    report += f"""
🌍 GLOBAL IMPACT ASSESSMENT:
• Immediate Response Required: International emergency coordination
• Long-term Effects: Climate impact from debris, agricultural disruption
• Recovery Timeline: 5-50 years depending on impact magnitude
• Planetary Defense: Enhanced detection and deflection systems needed

🚨 RISK MITIGATION RECOMMENDATIONS:
1. Strengthen NEO detection networks globally
2. Develop rapid response asteroid deflection technology  
3. Create international impact response protocols
4. Establish emergency evacuation procedures for high-risk areas
5. Build resilient infrastructure in populated regions

💡 SCIENTIFIC INSIGHTS:
• Size matters: Even small asteroids can cause significant regional damage
• Location is critical: Impacts near populated areas have exponential consequences  
• Early warning essential: Detection time allows for evacuation and preparation
• Economic impact far exceeds direct physical damage

{'='*70}
This analysis demonstrates the critical importance of planetary defense systems
and the need for continued investment in asteroid detection and deflection technology.
"""
    
    # Save report
    with open("impact_consequence_report.txt", "w") as f:
        f.write(report)
    
    print("✅ Comprehensive impact assessment report saved to 'impact_consequence_report.txt'")
    print(f"\n🌍 Impact consequence simulation complete!")
    print(f"📁 Files generated:")
    print(f"   • meteor_impact_consequences.html - Interactive visualization")
    print(f"   • impact_consequence_report.txt - Detailed assessment report")

if __name__ == "__main__":
    main()

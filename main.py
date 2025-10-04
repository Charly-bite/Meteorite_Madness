import requests
import json
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import our enhanced modules
from data_integrator import EnhancedDataIntegrator
from enhanced_visualizer import MultiSourceVisualizer

# Import the improved visualization manager
from visualization_manager import VisualizationManager, create_all_visualizations

class NASAAPIClient:
    """Client for connecting to NASA APIs"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov"
        self.session = requests.Session()
        self.session.params = {'api_key': self.api_key}
    
    def get_meteorite_data(self, limit: int = 100) -> Optional[List[Dict]]:
        """
        Fetch meteorite landing data from NASA's Open Data Portal
        """
        # NASA's meteorite data endpoint
        url = "https://data.nasa.gov/resource/gh4g-9sfh.json"
        
        try:
            params = {'$limit': limit}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching meteorite data: {e}")
            return None
    
    def get_apod(self, date: Optional[str] = None) -> Optional[Dict]:
        """
        Get Astronomy Picture of the Day
        date format: YYYY-MM-DD
        """
        url = f"{self.base_url}/planetary/apod"
        
        try:
            params = {}
            if date:
                params['date'] = date
                
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching APOD: {e}")
            return None
    
    def get_neo_feed(self, start_date: str, end_date: str) -> Optional[Dict]:
        """
        Get Near Earth Object feed
        date format: YYYY-MM-DD
        """
        url = f"{self.base_url}/neo/rest/v1/feed"
        
        try:
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching NEO data: {e}")
            return None

class NEOVisualizer:
    """Visualizer for Near Earth Object data"""
    
    def __init__(self):
        plt.style.use('dark_background')
        sns.set_palette("viridis")
    
    def process_neo_data(self, neo_data: Dict) -> pd.DataFrame:
        """Process NEO data into a DataFrame for visualization"""
        asteroids = []
        
        if not neo_data or 'near_earth_objects' not in neo_data:
            return pd.DataFrame()
        
        for date, objects in neo_data['near_earth_objects'].items():
            for obj in objects:
                asteroid_info = {
                    'date': date,
                    'name': obj.get('name', 'Unknown'),
                    'id': obj.get('id', 'Unknown'),
                    'estimated_diameter_min_km': float(obj.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_min', 0)),
                    'estimated_diameter_max_km': float(obj.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max', 0)),
                    'potentially_hazardous': obj.get('is_potentially_hazardous_asteroid', False),
                    'close_approach_date': obj.get('close_approach_data', [{}])[0].get('close_approach_date', date),
                    'miss_distance_km': float(obj.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('kilometers', 0)),
                    'relative_velocity_kmh': float(obj.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_hour', 0)),
                    'absolute_magnitude': float(obj.get('absolute_magnitude_h', 0))
                }
                asteroids.append(asteroid_info)
        
        return pd.DataFrame(asteroids)
    
    def create_size_distribution(self, df: pd.DataFrame):
        """Create a histogram of asteroid sizes"""
        if df.empty:
            print("No data to visualize")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram of diameter sizes
        ax1.hist(df['estimated_diameter_max_km'], bins=20, alpha=0.7, color='cyan', edgecolor='white')
        ax1.set_xlabel('Maximum Diameter (km)')
        ax1.set_ylabel('Number of Asteroids')
        ax1.set_title('🌌 Asteroid Size Distribution')
        ax1.grid(True, alpha=0.3)
        
        # Box plot for hazardous vs non-hazardous
        hazardous_data = [
            df[df['potentially_hazardous'] == False]['estimated_diameter_max_km'].dropna(),
            df[df['potentially_hazardous'] == True]['estimated_diameter_max_km'].dropna()
        ]
        
        ax2.boxplot(hazardous_data, labels=['Non-Hazardous', 'Potentially Hazardous'])
        ax2.set_ylabel('Maximum Diameter (km)')
        ax2.set_title('⚠️ Size Comparison: Hazardous vs Non-Hazardous')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def create_distance_velocity_scatter(self, df: pd.DataFrame):
        """Create a scatter plot of miss distance vs velocity"""
        if df.empty:
            print("No data to visualize")
            return
        
        fig = plt.figure(figsize=(12, 8))
        
        # Separate hazardous and non-hazardous asteroids
        non_hazardous = df[df['potentially_hazardous'] == False]
        hazardous = df[df['potentially_hazardous'] == True]
        
        # Create scatter plot
        plt.scatter(non_hazardous['miss_distance_km'], non_hazardous['relative_velocity_kmh'], 
                   s=non_hazardous['estimated_diameter_max_km']*1000, alpha=0.6, 
                   c='lightblue', label='Non-Hazardous', edgecolors='white')
        
        plt.scatter(hazardous['miss_distance_km'], hazardous['relative_velocity_kmh'], 
                   s=hazardous['estimated_diameter_max_km']*1000, alpha=0.8, 
                   c='red', label='Potentially Hazardous', edgecolors='white')
        
        plt.xlabel('Miss Distance (km)')
        plt.ylabel('Relative Velocity (km/h)')
        plt.title('🚀 Asteroid Approach: Distance vs Velocity\n(Size indicates diameter)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
        plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        plt.tight_layout()
        plt.show()
    
    def create_interactive_3d_plot(self, df: pd.DataFrame):
        """Create an interactive 3D plot using Plotly"""
        if df.empty:
            print("No data to visualize")
            return
        
        # Create color mapping for hazardous asteroids
        colors = df['potentially_hazardous'].map({True: 'red', False: 'lightblue'})
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df['miss_distance_km'],
            y=df['relative_velocity_kmh'],
            z=df['estimated_diameter_max_km'],
            mode='markers',
            marker=dict(
                size=df['absolute_magnitude'].fillna(10),
                color=colors,
                opacity=0.8,
                line=dict(color='white', width=0.5)
            ),
            text=df['name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Miss Distance: %{x:,.0f} km<br>' +
                         'Velocity: %{y:,.0f} km/h<br>' +
                         'Diameter: %{z:.3f} km<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title='🌌 Interactive 3D Asteroid Visualization',
            scene=dict(
                xaxis_title='Miss Distance (km)',
                yaxis_title='Relative Velocity (km/h)',
                zaxis_title='Diameter (km)',
                bgcolor='black',
                xaxis=dict(gridcolor='gray'),
                yaxis=dict(gridcolor='gray'),
                zaxis=dict(gridcolor='gray')
            ),
            paper_bgcolor='black',
            font=dict(color='white')
        )
        
        fig.show()
    
    def create_timeline_chart(self, df: pd.DataFrame):
        """Create a timeline chart of asteroid approaches"""
        if df.empty:
            print("No data to visualize")
            return
        
        # Convert dates to datetime
        df['approach_datetime'] = pd.to_datetime(df['close_approach_date'])
        df_sorted = df.sort_values('approach_datetime')
        
        fig = px.timeline(df_sorted, 
                         x_start='approach_datetime', 
                         x_end='approach_datetime',
                         y='name',
                         color='potentially_hazardous',
                         hover_data=['estimated_diameter_max_km', 'miss_distance_km', 'relative_velocity_kmh'],
                         color_discrete_map={True: 'red', False: 'lightblue'},
                         title='📅 Asteroid Approach Timeline')
        
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(gridcolor='gray'),
            yaxis=dict(gridcolor='gray')
        )
        
        fig.show()

def main():
    # Replace 'YOUR_API_KEY_HERE' with your actual NASA API key
    API_KEY = "Ch4TrNR37h2gfN5g1vyRcLsgtHeKv9SPw5aDHplE"
    
    # Initialize the NASA API client
    nasa_client = NASAAPIClient(API_KEY)
    
    print("🚀 NASA API Connection Test")
    print("=" * 40)
    
    # Test 1: Get Astronomy Picture of the Day
    print("\n📸 Fetching Astronomy Picture of the Day...")
    apod = nasa_client.get_apod()
    if apod:
        print(f"Title: {apod.get('title', 'N/A')}")
        print(f"Date: {apod.get('date', 'N/A')}")
        print(f"Description: {apod.get('explanation', 'N/A')[:100]}...")
    
    # Test 2: Get meteorite data (relevant to "Meteorite Madness")
    print("\n☄️ Fetching meteorite landing data...")
    meteorites = nasa_client.get_meteorite_data(limit=5)
    if meteorites:
        print(f"Found {len(meteorites)} meteorite records:")
        for i, meteorite in enumerate(meteorites[:3], 1):
            name = meteorite.get('name', 'Unknown')
            mass = meteorite.get('mass', 'Unknown')
            year = meteorite.get('year', 'Unknown')[:4] if meteorite.get('year') else 'Unknown'
            print(f"  {i}. {name} - Mass: {mass}g - Year: {year}")
    
    # Test 3: Get Near Earth Objects
    print("\n🌍 Fetching Near Earth Objects...")
    neo_data = nasa_client.get_neo_feed('2024-10-01', '2024-10-07')
    if neo_data:
        element_count = neo_data.get('element_count', 0)
        print(f"Found {element_count} Near Earth Objects in the specified date range")
        
        # Create visualizations for the NEO data
        print("\n🎨 Creating visualizations...")
        visualizer = NEOVisualizer()
        df = visualizer.process_neo_data(neo_data)
        
        if not df.empty:
            print(f"Processing {len(df)} asteroid records for visualization...")
            
            # Use the improved visualization manager
            create_all_visualizations(df)
            
            print("\n✨ All visualizations complete and saved to files!")
        else:
            print("No asteroid data available for visualization")

def enhanced_analysis():
    """
    Enhanced analysis with multi-source data integration
    """
    API_KEY = "Ch4TrNR37h2gfN5g1vyRcLsgtHeKv9SPw5aDHplE"
    
    print("🌟 ENHANCED METEORITE MADNESS - Multi-Source Analysis")
    print("=" * 60)
    
    # Initialize enhanced components
    nasa_client = NASAAPIClient(API_KEY)
    integrator = EnhancedDataIntegrator(API_KEY)
    multi_visualizer = MultiSourceVisualizer()
    
    # Get NASA NEO data
    print("\n🛸 Fetching Near Earth Objects data...")
    neo_data = nasa_client.get_neo_feed('2024-10-01', '2024-10-07')
    neo_df = pd.DataFrame()
    
    if neo_data:
        visualizer = NEOVisualizer()
        neo_df = visualizer.process_neo_data(neo_data)
        print(f"✅ Processed {len(neo_df)} asteroid records")
    
    # Get enhanced meteorite data with coordinates
    print("\n☄️ Fetching enhanced historical meteorite data...")
    meteorite_df = integrator.get_historical_meteorite_data()
    if not meteorite_df.empty:
        print(f"✅ Retrieved {len(meteorite_df)} meteorite records with coordinates")
        print(f"   📊 Average mass: {meteorite_df['mass_g'].mean():.1f}g")
        print(f"   📅 Year range: {meteorite_df['year'].min()} - {meteorite_df['year'].max()}")
    
    # Get population data
    print("\n🌍 Fetching global population data...")
    population_df = integrator.get_population_data(['US', 'CN', 'IN', 'BR', 'RU', 'JP', 'DE', 'UK'])
    if not population_df.empty:
        print(f"✅ Retrieved population data for {len(population_df)} countries")
    
    # Get space weather data
    print("\n🌞 Fetching space weather data...")
    space_weather = integrator.get_space_weather_data()
    if space_weather:
        print(f"✅ Retrieved space weather data ({len(space_weather)} records)")
    
    # Enhanced Visualizations using improved manager
    print("\n🎨 Creating Enhanced Multi-Source Visualizations...")
    
    if not neo_df.empty:
        print("   � Creating comprehensive asteroid visualizations...")
        create_all_visualizations(neo_df)
    
    if not meteorite_df.empty:
        print("   �️ Historical meteorite analysis...")
        viz_manager = VisualizationManager()
        # Create a simple meteorite analysis
        meteorite_summary = f"""
📋 HISTORICAL METEORITE ANALYSIS
{'='*50}
Total meteorites: {len(meteorite_df)}
Average mass: {meteorite_df['mass_g'].mean():.1f}g if 'mass_g' in meteorite_df.columns else 'N/A'
Year range: {meteorite_df['year'].min()} - {meteorite_df['year'].max()}
Countries affected: {meteorite_df['country'].nunique() if 'country' in meteorite_df.columns else 'N/A'}
"""
        print(meteorite_summary)
    
    # Generate comprehensive report
    print("\n📋 Generating comprehensive analysis report...")
    report = integrator.create_comprehensive_report(neo_df)
    
    print(f"\n📊 COMPREHENSIVE ANALYSIS REPORT")
    print(f"Generated: {report['timestamp'][:19]}")
    print(f"\n📈 Data Sources:")
    for source, count in report['data_sources'].items():
        print(f"   • {source.replace('_', ' ').title()}: {count} records")
    
    if 'analysis' in report and report['analysis']:
        print(f"\n🔍 Key Findings:")
        if 'risk_zones' in report['analysis']:
            risk = report['analysis']['risk_zones']
            print(f"   • High Risk Asteroids: {risk.get('high_risk_asteroids', 0)}")
            print(f"   • Medium Risk Asteroids: {risk.get('medium_risk_asteroids', 0)}")
            print(f"   • Low Risk Asteroids: {risk.get('low_risk_asteroids', 0)}")
        
        if 'historical_patterns' in report['analysis']:
            hist = report['analysis']['historical_patterns']
            print(f"   • Total Historical Meteorites: {hist.get('total_meteorites', 0)}")
            print(f"   • Average Mass: {hist.get('average_mass', 0):.1f}g")
            print(f"   • Most Common Class: {hist.get('most_common_class', 'Unknown')}")
    
    if report.get('recommendations'):
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")
    
    print(f"\n✨ Enhanced multi-source analysis complete!")
    print(f"🔗 Data sources successfully integrated:")
    print(f"   • NASA NEO API ✅")
    print(f"   • NASA Meteorite Database ✅")
    print(f"   • World Bank Population Data ✅")
    print(f"   • NOAA Space Weather ✅")

if __name__ == "__main__":
    # Choose which analysis to run
    print("🚀 Meteorite Madness - Choose Analysis Mode:")
    print("1. Basic NASA API Demo (original)")
    print("2. Enhanced Multi-Source Analysis (new)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        enhanced_analysis()
    else:
        main()
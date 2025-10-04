"""
Enhanced Data Integration Module for Meteorite Madness
Connects NASA asteroid data with external data sources
"""

import requests
import pandas as pd
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
import numpy as np

class EnhancedDataIntegrator:
    """Integrates NASA data with external sources for richer analysis"""
    
    def __init__(self, nasa_api_key: str, weather_api_key: Optional[str] = None):
        self.nasa_api_key = nasa_api_key
        self.weather_api_key = weather_api_key
        self.session = requests.Session()
    
    def get_population_data(self, country_codes: List[str] = None) -> pd.DataFrame:
        """
        Fetch world population data from World Bank API
        """
        if not country_codes:
            country_codes = ['all']  # Get all countries
        
        url = "http://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL"
        
        try:
            countries_str = ';'.join(country_codes) if country_codes != ['all'] else 'all'
            response = self.session.get(
                url.format(countries_str),
                params={
                    'format': 'json',
                    'date': '2023',
                    'per_page': 300
                },
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1:
                population_data = []
                for item in data[1]:  # Skip metadata
                    if item['value'] is not None:
                        population_data.append({
                            'country_code': item['country']['id'],
                            'country_name': item['country']['value'],
                            'population': item['value'],
                            'year': item['date']
                        })
                
                return pd.DataFrame(population_data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching population data: {e}")
        
        return pd.DataFrame()
    
    def get_space_weather_data(self) -> Optional[Dict]:
        """
        Fetch current space weather data from NOAA
        """
        url = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
        
        try:
            response = self.session.get(url, timeout=8)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching space weather data: {e}")
            return None
    
    def get_historical_meteorite_data(self) -> pd.DataFrame:
        """
        Enhanced meteorite data with additional filtering and processing
        """
        url = "https://data.nasa.gov/resource/gh4g-9sfh.json"
        
        try:
            # Fetch more comprehensive data
            params = {
                '$limit': 1000,
                '$order': 'year DESC',
                '$where': 'mass IS NOT NULL AND reclat IS NOT NULL AND reclong IS NOT NULL'
            }
            
            print(f"🔄 Fetching enhanced meteorite data (timeout: 12s)...")
            response = self.session.get(url, params=params, timeout=12)
            response.raise_for_status()
            
            meteorites = response.json()
            print(f"✅ Successfully fetched {len(meteorites)} enhanced meteorite records")
            
            # Process and enhance the data
            enhanced_data = []
            for meteorite in meteorites:
                if meteorite.get('mass') and meteorite.get('reclat') and meteorite.get('reclong'):
                    enhanced_data.append({
                        'name': meteorite.get('name', 'Unknown'),
                        'mass_g': float(meteorite.get('mass', 0)),
                        'year': meteorite.get('year', '1900-01-01T00:00:00.000')[:4],
                        'latitude': float(meteorite.get('reclat', 0)),
                        'longitude': float(meteorite.get('reclong', 0)),
                        'recclass': meteorite.get('recclass', 'Unknown'),
                        'fall': meteorite.get('fall', 'Unknown')
                    })
            
            return pd.DataFrame(enhanced_data)
        
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout fetching enhanced meteorite data - using fallback data")
            return self._get_fallback_meteorite_df()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching enhanced meteorite data: {e}")
            print(f"🔄 Using fallback meteorite data...")
            return self._get_fallback_meteorite_df()
    
    def _get_fallback_meteorite_df(self) -> pd.DataFrame:
        """Provide fallback meteorite DataFrame when API is unavailable"""
        fallback_data = [
            {
                'name': 'Allende',
                'mass_g': 2000000.0,
                'year': '1969',
                'latitude': 26.96667,
                'longitude': -105.31667,
                'recclass': 'CV3',
                'fall': 'Fell'
            },
            {
                'name': 'Murchison',
                'mass_g': 100000.0,
                'year': '1969',
                'latitude': -36.61667,
                'longitude': 145.2,
                'recclass': 'CM2', 
                'fall': 'Fell'
            },
            {
                'name': 'Canyon Diablo',
                'mass_g': 30000.0,
                'year': '1891',
                'latitude': 35.05,
                'longitude': -111.03333,
                'recclass': 'IAB-MG',
                'fall': 'Found'
            },
            {
                'name': 'Chelyabinsk',
                'mass_g': 500000.0,
                'year': '2013',
                'latitude': 54.83333,
                'longitude': 61.13333,
                'recclass': 'LL5',
                'fall': 'Fell'
            },
            {
                'name': 'Tunguska',
                'mass_g': 10000000.0,
                'year': '1908',
                'latitude': 60.886,
                'longitude': 101.886,
                'recclass': 'Unknown',
                'fall': 'Fell'
            }
        ]
        print(f"📊 Using {len(fallback_data)} fallback meteorite records")
        return pd.DataFrame(fallback_data)
    
    def calculate_impact_risk_zones(self, neo_df: pd.DataFrame, population_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate potential impact risk based on asteroid trajectories and population density
        """
        if neo_df.empty or population_df.empty:
            return pd.DataFrame()
        
        risk_analysis = []
        
        for _, asteroid in neo_df.iterrows():
            # Simple risk calculation based on size, velocity, and miss distance
            risk_score = (
                (asteroid['estimated_diameter_max_km'] * 1000) +  # Size factor
                (asteroid['relative_velocity_kmh'] / 1000) +      # Speed factor
                (1 / max(asteroid['miss_distance_km'] / 1000000, 0.1))  # Distance factor
            )
            
            # Determine risk level
            if risk_score > 100:
                risk_level = 'High'
            elif risk_score > 50:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            risk_analysis.append({
                'asteroid_name': asteroid['name'],
                'risk_score': risk_score,
                'risk_level': risk_level,
                'approach_date': asteroid['close_approach_date'],
                'potentially_hazardous': asteroid['potentially_hazardous']
            })
        
        return pd.DataFrame(risk_analysis)
    
    def get_correlations_with_solar_activity(self, neo_df: pd.DataFrame) -> Dict:
        """
        Analyze correlations between solar activity and asteroid detections
        """
        space_weather = self.get_space_weather_data()
        
        if not space_weather or neo_df.empty:
            return {}
        
        # Convert space weather data to DataFrame
        sw_df = pd.DataFrame(space_weather)
        
        # Simple correlation analysis (placeholder)
        correlations = {
            'data_available': len(space_weather) > 0,
            'neo_count': len(neo_df),
            'space_weather_records': len(space_weather),
            'analysis': 'Solar activity correlation analysis would require historical alignment of dates'
        }
        
        return correlations
    
    def create_comprehensive_report(self, neo_df: pd.DataFrame) -> Dict:
        """
        Generate a comprehensive report integrating all data sources
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_sources': {
                'nasa_neo': len(neo_df),
                'population_data': 0,
                'space_weather': 0,
                'meteorite_historical': 0
            },
            'analysis': {},
            'recommendations': []
        }
        
        # Get additional data
        population_df = self.get_population_data()
        meteorite_df = self.get_historical_meteorite_data()
        space_weather = self.get_space_weather_data()
        
        # Update counts
        report['data_sources']['population_data'] = len(population_df)
        report['data_sources']['meteorite_historical'] = len(meteorite_df)
        report['data_sources']['space_weather'] = 1 if space_weather else 0
        
        # Risk analysis
        if not neo_df.empty and not population_df.empty:
            risk_df = self.calculate_impact_risk_zones(neo_df, population_df)
            report['analysis']['risk_zones'] = {
                'high_risk_asteroids': len(risk_df[risk_df['risk_level'] == 'High']),
                'medium_risk_asteroids': len(risk_df[risk_df['risk_level'] == 'Medium']),
                'low_risk_asteroids': len(risk_df[risk_df['risk_level'] == 'Low'])
            }
        
        # Historical analysis
        if not meteorite_df.empty:
            report['analysis']['historical_patterns'] = {
                'total_meteorites': len(meteorite_df),
                'average_mass': meteorite_df['mass_g'].mean(),
                'most_common_class': meteorite_df['recclass'].mode().iloc[0] if not meteorite_df['recclass'].mode().empty else 'Unknown'
            }
        
        # Recommendations
        hazardous_count = len(neo_df[neo_df['potentially_hazardous'] == True]) if not neo_df.empty else 0
        if hazardous_count > 0:
            report['recommendations'].append(f"Monitor {hazardous_count} potentially hazardous asteroids closely")
        
        if not meteorite_df.empty:
            recent_falls = len(meteorite_df[meteorite_df['year'].astype(int) > 2020])
            report['recommendations'].append(f"Analyze patterns from {recent_falls} recent meteorite falls")
        
        return report

def main():
    """Demo of enhanced data integration"""
    # This would use your NASA API key
    integrator = EnhancedDataIntegrator("DEMO_KEY")
    
    print("🌍 Enhanced Meteorite Madness - Data Integration Demo")
    print("=" * 50)
    
    # Demo population data
    print("\n📊 Fetching global population data...")
    pop_df = integrator.get_population_data(['US', 'CN', 'IN', 'BR', 'RU'])
    if not pop_df.empty:
        print(f"Retrieved population data for {len(pop_df)} countries")
        print(pop_df.head())
    
    # Demo meteorite data
    print("\n☄️ Fetching enhanced meteorite data...")
    meteorite_df = integrator.get_historical_meteorite_data()
    if not meteorite_df.empty:
        print(f"Retrieved {len(meteorite_df)} meteorite records with coordinates")
        print(f"Average mass: {meteorite_df['mass_g'].mean():.2f}g")
    
    # Demo space weather
    print("\n🌞 Fetching space weather data...")
    space_weather = integrator.get_space_weather_data()
    if space_weather:
        print(f"Retrieved {len(space_weather)} space weather records")
    
    print("\n✨ Data integration demo complete!")

if __name__ == "__main__":
    main()

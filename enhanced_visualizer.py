"""
Enhanced Visualization Module
Creates integrated visualizations combining multiple data sources
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import seaborn as sns
from typing import Dict, List, Optional

class MultiSourceVisualizer:
    """Creates visualizations combining NASA data with external sources"""
    
    def __init__(self):
        plt.style.use('dark_background')
        sns.set_palette("viridis")
    
    def create_global_impact_map(self, meteorite_df: pd.DataFrame, population_df: pd.DataFrame = None):
        """
        Create an interactive world map showing meteorite impacts
        """
        if meteorite_df.empty:
            print("No meteorite data available for mapping")
            return
        
        # Filter out invalid coordinates
        valid_coords = meteorite_df[
            (meteorite_df['latitude'].between(-90, 90)) & 
            (meteorite_df['longitude'].between(-180, 180))
        ].copy()
        
        if valid_coords.empty:
            print("No valid coordinates found")
            return
        
        # Create size categories for better visualization
        valid_coords['size_category'] = pd.cut(
            valid_coords['mass_g'], 
            bins=[0, 100, 1000, 10000, float('inf')], 
            labels=['Small (<100g)', 'Medium (100g-1kg)', 'Large (1-10kg)', 'Massive (>10kg)']
        )
        
        # Create color mapping for fall vs find
        color_map = {'Fell': 'red', 'Found': 'lightblue'}
        valid_coords['color'] = valid_coords['fall'].map(color_map).fillna('gray')
        
        fig = go.Figure()
        
        # Add meteorite points
        for category in valid_coords['size_category'].unique():
            if pd.notna(category):
                subset = valid_coords[valid_coords['size_category'] == category]
                
                fig.add_trace(go.Scattergeo(
                    lon=subset['longitude'],
                    lat=subset['latitude'],
                    text=subset['name'],
                    mode='markers',
                    marker=dict(
                        size=np.log10(subset['mass_g'] + 1) * 3,  # Log scale for size
                        color=subset['color'],
                        opacity=0.7,
                        line=dict(width=1, color='white')
                    ),
                    name=category,
                    hovertemplate='<b>%{text}</b><br>' +
                                 'Mass: %{customdata[0]:.1f}g<br>' +
                                 'Year: %{customdata[1]}<br>' +
                                 'Type: %{customdata[2]}<br>' +
                                 'Coordinates: (%{lat:.2f}, %{lon:.2f})<br>' +
                                 '<extra></extra>',
                    customdata=subset[['mass_g', 'year', 'fall']].values
                ))
        
        fig.update_layout(
            title='🌍 Global Meteorite Impact Map<br><sub>Size indicates mass, color indicates fall vs found</sub>',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth',
                bgcolor='black'
            ),
            paper_bgcolor='black',
            font=dict(color='white'),
            height=600
        )
        
        fig.show()
    
    def create_temporal_analysis(self, meteorite_df: pd.DataFrame, neo_df: pd.DataFrame = None):
        """
        Create temporal analysis combining historical meteorites and current NEO data
        """
        if meteorite_df.empty:
            print("No meteorite data for temporal analysis")
            return
        
        # Convert year to numeric and filter reasonable years
        meteorite_df = meteorite_df.copy()
        meteorite_df['year_num'] = pd.to_numeric(meteorite_df['year'], errors='coerce')
        meteorite_df = meteorite_df[
            (meteorite_df['year_num'] >= 1800) & 
            (meteorite_df['year_num'] <= 2024)
        ].dropna(subset=['year_num'])
        
        if meteorite_df.empty:
            print("No valid years found for analysis")
            return
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Meteorite Falls by Decade',
                'Mass Distribution Over Time',
                'Geographic Distribution (Latitude)',
                'Fall vs Found Over Time'
            ],
            specs=[
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "bar"}]
            ]
        )
        
        # 1. Meteorite falls by decade
        meteorite_df['decade'] = (meteorite_df['year_num'] // 10) * 10
        decade_counts = meteorite_df.groupby('decade').size().reset_index(name='count')
        
        fig.add_trace(
            go.Bar(x=decade_counts['decade'], y=decade_counts['count'], 
                   name='Falls per Decade', marker_color='cyan'),
            row=1, col=1
        )
        
        # 2. Mass vs Year scatter
        fig.add_trace(
            go.Scatter(
                x=meteorite_df['year_num'], 
                y=np.log10(meteorite_df['mass_g'] + 1),
                mode='markers',
                marker=dict(
                    color=meteorite_df['mass_g'],
                    colorscale='Viridis',
                    size=6,
                    opacity=0.6
                ),
                name='Log(Mass) vs Year',
                text=meteorite_df['name']
            ),
            row=1, col=2
        )
        
        # 3. Latitude distribution over time
        fig.add_trace(
            go.Scatter(
                x=meteorite_df['year_num'],
                y=meteorite_df['latitude'],
                mode='markers',
                marker=dict(color='orange', size=4, opacity=0.6),
                name='Latitude vs Year'
            ),
            row=2, col=1
        )
        
        # 4. Fall vs Found distribution
        fall_counts = meteorite_df.groupby(['decade', 'fall']).size().unstack(fill_value=0)
        
        if 'Fell' in fall_counts.columns:
            fig.add_trace(
                go.Bar(x=fall_counts.index, y=fall_counts['Fell'], 
                       name='Fell', marker_color='red'),
                row=2, col=2
            )
        
        if 'Found' in fall_counts.columns:
            fig.add_trace(
                go.Bar(x=fall_counts.index, y=fall_counts['Found'], 
                       name='Found', marker_color='lightblue'),
                row=2, col=2
            )
        
        fig.update_layout(
            title_text="📊 Comprehensive Temporal Analysis of Meteorite Data",
            showlegend=True,
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white')
        )
        
        fig.show()
    
    def create_risk_assessment_dashboard(self, neo_df: pd.DataFrame, risk_df: pd.DataFrame = None):
        """
        Create a comprehensive risk assessment dashboard
        """
        if neo_df.empty:
            print("No NEO data for risk assessment")
            return
        
        # Create figure with subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Risk Distribution by Size and Hazard Level',
                'Approach Timeline',
                'Distance vs Velocity Risk Map',
                'Diameter vs Miss Distance'
            ],
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ]
        )
        
        # Prepare data
        hazardous = neo_df[neo_df['potentially_hazardous'] == True]
        non_hazardous = neo_df[neo_df['potentially_hazardous'] == False]
        
        # 1. Risk scatter plot
        fig.add_trace(
            go.Scatter(
                x=non_hazardous['estimated_diameter_max_km'],
                y=non_hazardous['relative_velocity_kmh'],
                mode='markers',
                marker=dict(
                    size=np.log10(non_hazardous['miss_distance_km'] + 1),
                    color='lightblue',
                    opacity=0.6,
                    line=dict(color='white', width=1)
                ),
                name='Non-Hazardous',
                text=non_hazardous['name']
            ), row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=hazardous['estimated_diameter_max_km'],
                y=hazardous['relative_velocity_kmh'],
                mode='markers',
                marker=dict(
                    size=np.log10(hazardous['miss_distance_km'] + 1),
                    color='red',
                    opacity=0.8,
                    line=dict(color='white', width=1)
                ),
                name='Potentially Hazardous',
                text=hazardous['name']
            ), row=1, col=1
        )
        
        # 2. Timeline
        neo_df['approach_date'] = pd.to_datetime(neo_df['close_approach_date'])
        fig.add_trace(
            go.Scatter(
                x=neo_df['approach_date'],
                y=neo_df['miss_distance_km'],
                mode='markers',
                marker=dict(
                    size=neo_df['estimated_diameter_max_km'] * 1000,
                    color=neo_df['potentially_hazardous'].map({True: 'red', False: 'lightblue'}),
                    opacity=0.7
                ),
                name='Approach Timeline',
                text=neo_df['name']
            ), row=1, col=2
        )
        
        # 3. Distance vs Velocity Risk Map
        fig.add_trace(
            go.Scatter(
                x=neo_df['miss_distance_km'],
                y=neo_df['relative_velocity_kmh'],
                mode='markers',
                marker=dict(
                    size=neo_df['estimated_diameter_max_km'] * 1000,
                    color=neo_df['absolute_magnitude'],
                    colorscale='Viridis',
                    opacity=0.7,
                    colorbar=dict(title="Absolute Magnitude")
                ),
                name='Risk Map',
                text=neo_df['name']
            ), row=2, col=1
        )
        
        # 4. Diameter vs Miss Distance
        fig.add_trace(
            go.Scatter(
                x=neo_df['estimated_diameter_max_km'],
                y=neo_df['miss_distance_km'],
                mode='markers',
                marker=dict(
                    size=neo_df['relative_velocity_kmh'] / 1000,
                    color=neo_df['potentially_hazardous'].map({True: 'red', False: 'lightblue'}),
                    opacity=0.7
                ),
                name='Size vs Distance',
                text=neo_df['name']
            ), row=2, col=2
        )
        
        fig.update_layout(
            title_text="🚨 Comprehensive Asteroid Risk Assessment Dashboard",
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white')
        )
        
        fig.show()
    
    def create_correlation_heatmap(self, neo_df: pd.DataFrame):
        """
        Create correlation heatmap of asteroid properties
        """
        if neo_df.empty:
            print("No data for correlation analysis")
            return
        
        # Select numeric columns for correlation
        numeric_cols = [
            'estimated_diameter_min_km', 'estimated_diameter_max_km',
            'miss_distance_km', 'relative_velocity_kmh', 'absolute_magnitude'
        ]
        
        # Filter available columns
        available_cols = [col for col in numeric_cols if col in neo_df.columns]
        
        if len(available_cols) < 2:
            print("Insufficient numeric columns for correlation analysis")
            return
        
        correlation_matrix = neo_df[available_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create heatmap
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='RdYlBu_r',
            center=0,
            square=True,
            fmt='.2f',
            cbar_kws={'label': 'Correlation Coefficient'},
            ax=ax
        )
        
        ax.set_title('🔍 Asteroid Properties Correlation Matrix', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Asteroid Properties', fontsize=12)
        ax.set_ylabel('Asteroid Properties', fontsize=12)
        
        plt.tight_layout()
        plt.show()

def main():
    """Demo of enhanced visualizations"""
    print("🎨 Enhanced Meteorite Madness - Multi-Source Visualizations Demo")
    print("=" * 60)
    
    # Create sample data for demo
    sample_meteorites = pd.DataFrame({
        'name': ['Demo Meteorite 1', 'Demo Meteorite 2', 'Demo Meteorite 3'],
        'mass_g': [1000, 500, 2000],
        'latitude': [40.7128, 51.5074, 35.6762],
        'longitude': [-74.0060, -0.1278, 139.6503],
        'year': ['2020', '2019', '2021'],
        'fall': ['Fell', 'Found', 'Fell']
    })
    
    visualizer = MultiSourceVisualizer()
    
    print("🗺️ Demo: Global impact map would be created here")
    print("📊 Demo: Temporal analysis would be created here")
    print("🚨 Demo: Risk assessment dashboard would be created here")
    print("🔍 Demo: Correlation heatmap would be created here")
    
    print("\n✨ Enhanced visualization demo complete!")

if __name__ == "__main__":
    main()

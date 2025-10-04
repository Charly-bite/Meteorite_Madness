"""
Visualization Manager for Meteorite Madness
Handles saving and displaying visualizations with better error handling
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import os
from datetime import datetime
from typing import Dict, List, Optional

class VisualizationManager:
    """Manages visualization creation and saving"""
    
    def __init__(self, output_dir: str = "visualizations"):
        self.output_dir = output_dir
        self.ensure_output_dir()
        
        # Set up matplotlib for better rendering
        plt.style.use('dark_background')
        sns.set_palette("viridis")
        
        # Configure plotly for static export (with error handling)
        try:
            if hasattr(pio, 'kaleido') and pio.kaleido.scope is not None:
                pio.kaleido.scope.mathjax = None
        except (AttributeError, Exception) as e:
            print(f"⚠️  Kaleido configuration warning: {e}")
            print("📊 Plotly visualizations will still work, just without some static export features")
        
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created visualization directory: {self.output_dir}")
    
    def save_matplotlib_plot(self, filename: str, dpi: int = 300):
        """Save matplotlib plot with proper formatting"""
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight', 
                   facecolor='black', edgecolor='none')
        plt.close()  # Close to free memory
        print(f"💾 Saved: {filepath}")
        return filepath
    
    def save_plotly_plot(self, fig, filename: str, width: int = 1200, height: int = 800):
        """Save plotly plot as HTML and PNG"""
        base_path = os.path.join(self.output_dir, filename.replace('.html', ''))
        
        # Save as HTML for interactivity
        html_path = f"{base_path}.html"
        fig.write_html(html_path)
        print(f"💾 Saved interactive: {html_path}")
        
        # Save as PNG for static viewing
        png_path = f"{base_path}.png"
        try:
            fig.write_image(png_path, width=width, height=height)
            print(f"💾 Saved static: {png_path}")
        except Exception as e:
            print(f"⚠️ Could not save PNG (kaleido issue): {e}")
        
        return html_path, png_path
    
    def create_neo_size_distribution(self, df: pd.DataFrame):
        """Create asteroid size distribution with emoji-free titles"""
        if df.empty:
            print("No NEO data to visualize")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram of diameter sizes
        ax1.hist(df['estimated_diameter_max_km'], bins=20, alpha=0.7, 
                color='cyan', edgecolor='white')
        ax1.set_xlabel('Maximum Diameter (km)')
        ax1.set_ylabel('Number of Asteroids')
        ax1.set_title('Asteroid Size Distribution', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Box plot for hazardous vs non-hazardous
        hazardous_data = [
            df[df['potentially_hazardous'] == False]['estimated_diameter_max_km'].dropna(),
            df[df['potentially_hazardous'] == True]['estimated_diameter_max_km'].dropna()
        ]
        
        ax2.boxplot(hazardous_data, tick_labels=['Non-Hazardous', 'Potentially Hazardous'])
        ax2.set_ylabel('Maximum Diameter (km)')
        ax2.set_title('Size Comparison: Hazardous vs Non-Hazardous', 
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.save_matplotlib_plot('neo_size_distribution.png')
    
    def create_distance_velocity_scatter(self, df: pd.DataFrame):
        """Create distance vs velocity scatter plot"""
        if df.empty:
            print("No NEO data to visualize")
            return
        
        fig = plt.figure(figsize=(12, 8))
        
        # Separate hazardous and non-hazardous asteroids
        non_hazardous = df[df['potentially_hazardous'] == False]
        hazardous = df[df['potentially_hazardous'] == True]
        
        # Create scatter plot
        plt.scatter(non_hazardous['miss_distance_km'], non_hazardous['relative_velocity_kmh'], 
                   s=non_hazardous['estimated_diameter_max_km']*1000, alpha=0.6, 
                   c='lightblue', label='Non-Hazardous', edgecolors='white')
        
        if not hazardous.empty:
            plt.scatter(hazardous['miss_distance_km'], hazardous['relative_velocity_kmh'], 
                       s=hazardous['estimated_diameter_max_km']*1000, alpha=0.8, 
                       c='red', label='Potentially Hazardous', edgecolors='white')
        
        plt.xlabel('Miss Distance (km)')
        plt.ylabel('Relative Velocity (km/h)')
        plt.title('Asteroid Approach: Distance vs Velocity\n(Size indicates diameter)', 
                 fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
        plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        plt.tight_layout()
        return self.save_matplotlib_plot('distance_velocity_scatter.png')
    
    def create_interactive_3d_plot(self, df: pd.DataFrame):
        """Create interactive 3D plot using Plotly"""
        if df.empty:
            print("No NEO data to visualize")
            return
        
        # Create color mapping for hazardous asteroids
        colors = df['potentially_hazardous'].map({True: 'red', False: 'lightblue'})
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df['miss_distance_km'],
            y=df['relative_velocity_kmh'],
            z=df['estimated_diameter_max_km'],
            mode='markers',
            marker=dict(
                size=df['absolute_magnitude'].fillna(10) * 2,  # Make markers more visible
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
            title='Interactive 3D Asteroid Visualization',
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
        
        return self.save_plotly_plot(fig, 'interactive_3d_asteroids.html')
    
    def create_risk_assessment_dashboard(self, df: pd.DataFrame):
        """Create a comprehensive risk assessment dashboard"""
        if df.empty:
            print("No NEO data for risk assessment")
            return
        
        # Create risk categories based on size and distance
        df['risk_category'] = 'Low'
        df.loc[(df['estimated_diameter_max_km'] > 0.1) & 
               (df['miss_distance_km'] < 7500000), 'risk_category'] = 'Medium'
        df.loc[(df['estimated_diameter_max_km'] > 0.5) & 
               (df['miss_distance_km'] < 5000000), 'risk_category'] = 'High'
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Risk Category Distribution', 'Size vs Distance Risk Map',
                          'Velocity Distribution by Risk', 'Hazardous Asteroids Timeline'),
            specs=[[{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "box"}, {"type": "scatter"}]]
        )
        
        # Risk category pie chart
        risk_counts = df['risk_category'].value_counts()
        fig.add_trace(
            go.Pie(labels=risk_counts.index, values=risk_counts.values,
                   marker_colors=['green', 'orange', 'red']),
            row=1, col=1
        )
        
        # Size vs Distance scatter
        color_map = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        for category in df['risk_category'].unique():
            category_data = df[df['risk_category'] == category]
            fig.add_trace(
                go.Scatter(
                    x=category_data['miss_distance_km'],
                    y=category_data['estimated_diameter_max_km'],
                    mode='markers',
                    name=f'{category} Risk',
                    marker=dict(color=color_map.get(category, 'blue')),
                    text=category_data['name']
                ),
                row=1, col=2
            )
        
        # Velocity box plot by risk category
        for category in df['risk_category'].unique():
            fig.add_trace(
                go.Box(
                    y=df[df['risk_category'] == category]['relative_velocity_kmh'],
                    name=f'{category} Risk',
                    marker_color=color_map.get(category, 'blue')
                ),
                row=2, col=1
            )
        
        # Timeline of hazardous asteroids
        hazardous = df[df['potentially_hazardous'] == True]
        if not hazardous.empty:
            fig.add_trace(
                go.Scatter(
                    x=pd.to_datetime(hazardous['close_approach_date']),
                    y=hazardous['estimated_diameter_max_km'],
                    mode='markers',
                    marker=dict(
                        size=hazardous['relative_velocity_kmh'] / 5000,
                        color='red',
                        opacity=0.7
                    ),
                    text=hazardous['name'],
                    name='Hazardous Asteroids'
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title_text="Asteroid Risk Assessment Dashboard",
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white'),
            height=800
        )
        
        return self.save_plotly_plot(fig, 'risk_assessment_dashboard.html')
    
    def create_summary_report(self, df: pd.DataFrame) -> str:
        """Create a text summary report"""
        if df.empty:
            return "No data available for analysis"
        
        report_lines = [
            "=" * 60,
            "ASTEROID ANALYSIS SUMMARY REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            f"📊 Dataset Overview:",
            f"   • Total Asteroids Analyzed: {len(df)}",
            f"   • Date Range: {df['close_approach_date'].min()} to {df['close_approach_date'].max()}",
            "",
            f"🎯 Size Statistics:",
            f"   • Average Diameter: {df['estimated_diameter_max_km'].mean():.3f} km",
            f"   • Largest Asteroid: {df['estimated_diameter_max_km'].max():.3f} km",
            f"   • Smallest Asteroid: {df['estimated_diameter_max_km'].min():.3f} km",
            "",
            f"⚠️ Risk Assessment:",
            f"   • Potentially Hazardous: {df['potentially_hazardous'].sum()} ({df['potentially_hazardous'].mean()*100:.1f}%)",
            f"   • Average Miss Distance: {df['miss_distance_km'].mean():,.0f} km",
            f"   • Closest Approach: {df['miss_distance_km'].min():,.0f} km",
            "",
            f"🚀 Velocity Analysis:",
            f"   • Average Velocity: {df['relative_velocity_kmh'].mean():,.0f} km/h",
            f"   • Fastest Asteroid: {df['relative_velocity_kmh'].max():,.0f} km/h",
            f"   • Slowest Asteroid: {df['relative_velocity_kmh'].min():,.0f} km/h",
            "",
            "🔍 Key Findings:",
        ]
        
        # Add specific findings
        largest = df.loc[df['estimated_diameter_max_km'].idxmax()]
        closest = df.loc[df['miss_distance_km'].idxmin()]
        fastest = df.loc[df['relative_velocity_kmh'].idxmax()]
        
        report_lines.extend([
            f"   • Largest asteroid: {largest['name']} ({largest['estimated_diameter_max_km']:.3f} km)",
            f"   • Closest approach: {closest['name']} ({closest['miss_distance_km']:,.0f} km)",
            f"   • Fastest asteroid: {fastest['name']} ({fastest['relative_velocity_kmh']:,.0f} km/h)",
            "",
            "=" * 60
        ])
        
        report_text = "\n".join(report_lines)
        
        # Save report to file
        report_path = os.path.join(self.output_dir, 'analysis_report.txt')
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        print(f"📋 Report saved: {report_path}")
        return report_text

def create_all_visualizations(neo_df: pd.DataFrame):
    """Create all visualizations with proper error handling"""
    viz_manager = VisualizationManager()
    
    print("\n🎨 Creating all visualizations...")
    print("-" * 40)
    
    try:
        # Create visualizations
        viz_manager.create_neo_size_distribution(neo_df)
        viz_manager.create_distance_velocity_scatter(neo_df)
        viz_manager.create_interactive_3d_plot(neo_df)
        viz_manager.create_risk_assessment_dashboard(neo_df)
        
        # Create summary report
        report = viz_manager.create_summary_report(neo_df)
        print("\n" + report)
        
        print(f"\n✅ All visualizations created successfully!")
        print(f"📁 Check the '{viz_manager.output_dir}' directory for all files")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Demo with sample data
    sample_data = pd.DataFrame({
        'name': ['Demo Asteroid 1', 'Demo Asteroid 2'],
        'estimated_diameter_max_km': [0.5, 1.2],
        'miss_distance_km': [5000000, 8000000],
        'relative_velocity_kmh': [25000, 18000],
        'potentially_hazardous': [True, False],
        'close_approach_date': ['2024-10-01', '2024-10-02'],
        'absolute_magnitude': [18.5, 20.1]
    })
    
    create_all_visualizations(sample_data)

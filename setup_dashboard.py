#!/usr/bin/env python3
"""
Web Dashboard Setup Script
Copies visualization files to the main directory for web viewing
"""

import shutil
import os
from pathlib import Path

def setup_dashboard():
    """Copy visualization files to main directory for web dashboard"""
    
    print("🌐 Setting up Meteorite Madness Web Dashboard...")
    print("-" * 50)
    
    # Define paths
    viz_dir = Path("visualizations")
    main_dir = Path(".")
    
    if not viz_dir.exists():
        print("❌ Visualizations directory not found!")
        print("   Please run the main analysis first to generate visualizations.")
        return False
    
    # Files to copy for web dashboard
    files_to_copy = [
        "risk_assessment_dashboard.html",
        "interactive_3d_asteroids.html", 
        "neo_size_distribution.png",
        "distance_velocity_scatter.png",
        "analysis_report.txt"
    ]
    
    copied_files = []
    
    for filename in files_to_copy:
        source = viz_dir / filename
        destination = main_dir / filename
        
        if source.exists():
            try:
                shutil.copy2(source, destination)
                copied_files.append(filename)
                print(f"✅ Copied: {filename}")
            except Exception as e:
                print(f"❌ Error copying {filename}: {e}")
        else:
            print(f"⚠️  Not found: {filename}")
    
    print(f"\n📊 Successfully copied {len(copied_files)} files")
    print("\n🚀 Your web dashboard is ready!")
    print("   Open 'dashboard.html' in your browser to view the complete analysis")
    
    return len(copied_files) > 0

if __name__ == "__main__":
    setup_dashboard()

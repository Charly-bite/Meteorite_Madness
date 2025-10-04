#!/usr/bin/env python3
"""
Web Integration Manager for Solar System Simulator
Automatically updates dashboard with new simulator results
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

class WebIntegrationManager:
    """Manages web integration and dashboard updates"""
    
    def __init__(self, dashboard_path: str = "dashboard.html"):
        self.dashboard_path = dashboard_path
        self.simulator_files = [
            "solar_system_simulator.html",
            "asteroid_timeline.html", 
            "simulation_report.txt"
        ]
    
    def check_simulator_files(self) -> Dict[str, bool]:
        """Check if simulator files exist"""
        status = {}
        for file in self.simulator_files:
            status[file] = os.path.exists(file)
        return status
    
    def update_dashboard_timestamp(self):
        """Update the dashboard with current timestamp"""
        if not os.path.exists(self.dashboard_path):
            print(f"⚠️  Dashboard file not found: {self.dashboard_path}")
            return False
        
        try:
            with open(self.dashboard_path, 'r') as f:
                content = f.read()
            
            # Update timestamp
            current_time = datetime.now().strftime('%B %d, %Y at %H:%M')
            old_timestamp = "Generated October 4, 2025"
            new_timestamp = f"Generated {current_time}"
            
            content = content.replace(old_timestamp, new_timestamp)
            
            with open(self.dashboard_path, 'w') as f:
                f.write(content)
            
            print(f"✅ Dashboard timestamp updated to: {current_time}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating dashboard: {e}")
            return False
    
    def generate_web_status_report(self) -> str:
        """Generate a status report for web files"""
        file_status = self.check_simulator_files()
        
        report = f"""
🌐 WEB INTEGRATION STATUS REPORT
{'='*50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📁 SIMULATOR FILES:
"""
        
        for filename, exists in file_status.items():
            status_icon = "✅" if exists else "❌"
            status_text = "Available" if exists else "Missing"
            file_size = ""
            
            if exists:
                try:
                    size = os.path.getsize(filename)
                    if size > 1024*1024:
                        file_size = f" ({size/(1024*1024):.1f} MB)"
                    elif size > 1024:
                        file_size = f" ({size/1024:.1f} KB)"
                    else:
                        file_size = f" ({size} bytes)"
                except:
                    pass
            
            report += f"   {status_icon} {filename}: {status_text}{file_size}\n"
        
        # Dashboard status
        dashboard_exists = os.path.exists(self.dashboard_path)
        dashboard_icon = "✅" if dashboard_exists else "❌"
        dashboard_status = "Available" if dashboard_exists else "Missing"
        
        report += f"\n🎨 DASHBOARD:\n"
        report += f"   {dashboard_icon} {self.dashboard_path}: {dashboard_status}\n"
        
        # Server suggestions
        report += f"\n🚀 NEXT STEPS:\n"
        if all(file_status.values()) and dashboard_exists:
            report += f"   • All files ready! Start server: python server.py\n"
            report += f"   • View dashboard: http://localhost:8080/dashboard.html\n"
            report += f"   • Solar system simulator: http://localhost:8080/solar_system_simulator.html\n"
        else:
            missing_files = [f for f, exists in file_status.items() if not exists]
            report += f"   • Missing files: {', '.join(missing_files)}\n"
            report += f"   • Run: python main.py (choose option 2 or 3)\n"
        
        return report.strip()
    
    def create_simulator_index(self):
        """Create a simple index page for the simulator"""
        index_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 Solar System Simulator</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }}
        .header {{
            padding: 40px 0;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 3em;
            background: linear-gradient(45deg, #00d4ff, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}
        .link-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            text-decoration: none;
            color: white;
            transition: transform 0.3s ease;
        }}
        .link-card:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }}
        .link-card h3 {{
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌌 Solar System Simulator</h1>
            <p>Interactive 3D visualization with real NASA asteroid data</p>
            <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>
        
        <div class="link-grid">
            <a href="dashboard.html" class="link-card">
                <h3>📊 Main Dashboard</h3>
                <p>Comprehensive asteroid analysis and visualizations</p>
            </a>
            
            <a href="solar_system_simulator.html" class="link-card">
                <h3>🪐 3D Solar System</h3>
                <p>Interactive solar system with real asteroid trajectories</p>
            </a>
            
            <a href="asteroid_timeline.html" class="link-card">
                <h3>📅 Approach Timeline</h3>
                <p>Timeline of asteroid approaches to Earth</p>
            </a>
        </div>
    </div>
</body>
</html>"""
        
        try:
            with open("index.html", "w") as f:
                f.write(index_content)
            print("✅ Created index.html for easy navigation")
            return True
        except Exception as e:
            print(f"❌ Error creating index.html: {e}")
            return False

def main():
    """Main function to run web integration checks"""
    print("🌐 Web Integration Manager")
    print("="*30)
    
    manager = WebIntegrationManager()
    
    # Generate status report
    status_report = manager.generate_web_status_report()
    print(status_report)
    
    # Update dashboard timestamp
    manager.update_dashboard_timestamp()
    
    # Create index page
    manager.create_simulator_index()
    
    print("\n✨ Web integration check complete!")

if __name__ == "__main__":
    main()

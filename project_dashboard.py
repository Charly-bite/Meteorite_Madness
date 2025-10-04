#!/usr/bin/env python3
"""
Project Status Dashboard
Interactive dashboard for monitoring project progress and context
"""

import json
from datetime import datetime
from pathlib import Path
import webbrowser
import os

def create_project_status_page():
    """Create an HTML page showing project status and context"""
    
    # Load context
    try:
        with open('context.json', 'r') as f:
            context = json.load(f)
    except:
        context = {"error": "Could not load context.json"}
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Meteorite Madness - Project Status Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            padding: 30px 0;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00d4ff, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .status-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}

        .status-card:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }}

        .status-card h3 {{
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        .metric {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .metric:last-child {{
            border-bottom: none;
        }}

        .metric-label {{
            color: #ccc;
        }}

        .metric-value {{
            color: #4ecdc4;
            font-weight: bold;
        }}

        .section {{
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            border-left: 5px solid #ff6b6b;
        }}

        .section h2 {{
            color: #ff6b6b;
            margin-bottom: 20px;
            font-size: 2em;
        }}

        .timeline {{
            position: relative;
            padding-left: 30px;
        }}

        .timeline::before {{
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(to bottom, #00d4ff, #ff6b6b);
        }}

        .timeline-item {{
            position: relative;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            border-left: 3px solid #00d4ff;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -41px;
            top: 20px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00d4ff;
            border: 3px solid #0f0f1e;
        }}

        .timeline-item h4 {{
            color: #4ecdc4;
            margin-bottom: 10px;
        }}

        .timeline-item .date {{
            color: #888;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}

        .findings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}

        .finding-card {{
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #4ecdc4;
        }}

        .finding-card h4 {{
            color: #4ecdc4;
            margin-bottom: 10px;
        }}

        .data-sources {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}

        .source-card {{
            background: rgba(0, 212, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }}

        .source-card h4 {{
            color: #00d4ff;
            margin-bottom: 8px;
        }}

        .source-card p {{
            color: #ccc;
            font-size: 0.9em;
        }}

        .json-viewer {{
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
            overflow: auto;
            max-height: 400px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}

        .nav-tabs {{
            display: flex;
            margin-bottom: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 5px;
        }}

        .nav-tab {{
            flex: 1;
            padding: 10px 20px;
            text-align: center;
            background: transparent;
            color: #ccc;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .nav-tab.active {{
            background: #00d4ff;
            color: #0f0f1e;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            .status-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🚀 Project Status Dashboard</h1>
            <p>Meteorite Madness - Real-time Project Monitoring</p>
            <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <!-- Status Overview -->
        <div class="status-grid">
            <div class="status-card">
                <h3>📊 Project Overview</h3>
                <div class="metric">
                    <span class="metric-label">Name:</span>
                    <span class="metric-value">{context.get('project_info', {}).get('name', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Version:</span>
                    <span class="metric-value">{context.get('project_info', {}).get('version', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value">{context.get('project_info', {}).get('status', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Repository:</span>
                    <span class="metric-value">GitHub</span>
                </div>
            </div>

            <div class="status-card">
                <h3>📈 Latest Analysis</h3>
                <div class="metric">
                    <span class="metric-label">Date:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('date', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Asteroids:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('total_asteroids', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Hazardous:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('potentially_hazardous', 'N/A')} ({context.get('analysis_results', {}).get('latest_analysis', {}).get('hazardous_percentage', 'N/A')}%)</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Date Range:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('date_range', 'N/A')}</span>
                </div>
            </div>

            <div class="status-card">
                <h3>🎯 Key Metrics</h3>
                <div class="metric">
                    <span class="metric-label">Closest Approach:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('statistics', {}).get('distance', {}).get('closest_approach_km', 'N/A'):,} km</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Largest Asteroid:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('statistics', {}).get('size', {}).get('largest_diameter_km', 'N/A')} km</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Fastest Speed:</span>
                    <span class="metric-value">{context.get('analysis_results', {}).get('latest_analysis', {}).get('statistics', {}).get('velocity', {}).get('fastest_velocity_kmh', 'N/A'):,} km/h</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Data Sources:</span>
                    <span class="metric-value">{len(context.get('data_sources', {}).get('primary', {}))}</span>
                </div>
            </div>

            <div class="status-card">
                <h3>💻 Technical Stats</h3>
                <div class="metric">
                    <span class="metric-label">Python Files:</span>
                    <span class="metric-value">{context.get('performance_metrics', {}).get('code_statistics', {}).get('python_files', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Lines of Code:</span>
                    <span class="metric-value">{context.get('performance_metrics', {}).get('code_statistics', {}).get('python_lines', 'N/A'):,}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Total Files:</span>
                    <span class="metric-value">{context.get('performance_metrics', {}).get('code_statistics', {}).get('total_files', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Visualizations:</span>
                    <span class="metric-value">{len(context.get('visualizations', {}).get('generated_files', {}))}</span>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showTab('findings')">🔍 Key Findings</button>
            <button class="nav-tab" onclick="showTab('timeline')">📅 Timeline</button>
            <button class="nav-tab" onclick="showTab('sources')">🛸 Data Sources</button>
            <button class="nav-tab" onclick="showTab('context')">📋 Full Context</button>
        </div>

        <!-- Key Findings Tab -->
        <div id="findings" class="tab-content active">
            <div class="section">
                <h2>🔍 Key Findings & Insights</h2>
                <div class="findings-grid">
    """
    
    # Add key findings
    if 'analysis_results' in context and 'key_findings' in context['analysis_results']:
        for i, finding in enumerate(context['analysis_results']['key_findings'][:6], 1):
            html_content += f"""
                    <div class="finding-card">
                        <h4>Finding {i}</h4>
                        <p>{finding}</p>
                    </div>
            """
    
    html_content += """
                </div>
            </div>
        </div>

        <!-- Timeline Tab -->
        <div id="timeline" class="tab-content">
            <div class="section">
                <h2>📅 Project Timeline</h2>
                <div class="timeline">
    """
    
    # Add timeline items
    if 'project_timeline' in context:
        for phase, details in context['project_timeline'].items():
            html_content += f"""
                    <div class="timeline-item">
                        <div class="date">{details.get('date', 'Unknown Date')}</div>
                        <h4>{details.get('milestone', 'Unknown Milestone')}</h4>
                        <p>{details.get('description', 'No description available')}</p>
                    </div>
            """
    
    html_content += """
                </div>
            </div>
        </div>

        <!-- Data Sources Tab -->
        <div id="sources" class="tab-content">
            <div class="section">
                <h2>🛸 Data Sources</h2>
                <div class="data-sources">
    """
    
    # Add data sources
    if 'data_sources' in context and 'primary' in context['data_sources']:
        for source, details in context['data_sources']['primary'].items():
            html_content += f"""
                    <div class="source-card">
                        <h4>{source.replace('_', ' ').title()}</h4>
                        <p>{details.get('description', 'No description available')}</p>
                        <p><strong>Endpoint:</strong> {details.get('endpoint', 'N/A')}</p>
                    </div>
            """
    
    html_content += """
                </div>
            </div>
        </div>

        <!-- Full Context Tab -->
        <div id="context" class="tab-content">
            <div class="section">
                <h2>📋 Complete Project Context</h2>
                <div class="json-viewer">
                    <pre id="context-json">Loading context data...</pre>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.nav-tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        // Load full context JSON
        fetch('context.json')
            .then(response => response.json())
            .then(data => {
                document.getElementById('context-json').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('context-json').textContent = 'Error loading context.json: ' + error;
            });
    </script>
</body>
</html>
    """
    
    return html_content

def main():
    """Create and serve the project status dashboard"""
    
    print("🚀 Creating Project Status Dashboard...")
    
    # Create the HTML content
    html_content = create_project_status_page()
    
    # Save to file
    status_file = "project_status.html"
    with open(status_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Project status dashboard created: {status_file}")
    print(f"🌐 You can view it at: http://localhost:8080/{status_file}")
    
    return status_file

if __name__ == "__main__":
    main()

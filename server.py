#!/usr/bin/env python3
"""
Local Web Server for Meteorite Madness Dashboard
Serves the dashboard.html and all visualization files locally
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files with proper MIME types"""
    
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging to show what files are being served"""
        print(f"🌐 Served: {args[0]} - {args[1]}")

def start_server(port=8000):
    """Start the local web server"""
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("🚀 Starting Meteorite Madness Local Web Server")
    print("=" * 50)
    print(f"📁 Serving from: {project_dir.absolute()}")
    print(f"🌐 Port: {port}")
    print(f"🔗 URL: http://localhost:{port}")
    print(f"📋 Dashboard: http://localhost:{port}/dashboard.html")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        "dashboard.html",
        "risk_assessment_dashboard.html",
        "interactive_3d_asteroids.html",
        "analysis_report.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("⚠️  Warning: Some files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        print("   Run the analysis first to generate all files.")
        print()
    
    # List available files
    print("📂 Available files:")
    html_files = list(Path(".").glob("*.html"))
    png_files = list(Path(".").glob("*.png"))
    txt_files = list(Path(".").glob("*.txt"))
    
    for file in sorted(html_files + png_files + txt_files):
        if file.name not in ['.git', '__pycache__', '.venv']:
            print(f"   ✅ {file.name}")
    
    print("\n🌟 Starting server...")
    
    try:
        # Create server
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Server started successfully!")
            print(f"🌐 Access your dashboard at: http://localhost:{port}/dashboard.html")
            print()
            print("💡 Tips:")
            print("   • Press Ctrl+C to stop the server")
            print("   • The dashboard will auto-refresh when you reload the page")
            print("   • All interactive visualizations should work properly")
            print("   • Check the terminal for access logs")
            print()
            
            # Try to open browser automatically
            try:
                dashboard_url = f"http://localhost:{port}/dashboard.html"
                print(f"🌍 Opening browser to: {dashboard_url}")
                webbrowser.open(dashboard_url)
            except Exception as e:
                print(f"⚠️  Could not auto-open browser: {e}")
                print(f"   Please manually open: http://localhost:{port}/dashboard.html")
            
            print("🔄 Server is running... (Press Ctrl+C to stop)")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print(f"💡 Try a different port: python server.py --port 8001")
            alternative_port = port + 1
            print(f"🔄 Trying port {alternative_port}...")
            start_server(alternative_port)
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function with command line argument support"""
    
    # Default port
    port = 8000
    
    # Check for port argument
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("🌐 Meteorite Madness Local Web Server")
            print("Usage: python server.py [--port PORT]")
            print("Options:")
            print("  --port PORT    Port number (default: 8000)")
            print("  --help, -h     Show this help message")
            return
        elif sys.argv[1] == "--port" and len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("❌ Invalid port number!")
                return
    
    start_server(port)

if __name__ == "__main__":
    main()

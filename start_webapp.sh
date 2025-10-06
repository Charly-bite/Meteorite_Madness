#!/bin/bash
# Meteorite Madness Web Application Launcher
# ==========================================

echo "🚀 Starting Meteorite Madness Web Application..."
echo ""
echo "🌐 Interactive Planetary Defense Platform"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📡 Features:"
echo "   ✓ Real-time NASA NEO data visualization"
echo "   ✓ Global threat map with impact zones"
echo "   ✓ Interactive impact consequence simulator"
echo "   ✓ Comprehensive analytics and statistics"
echo "   ✓ USGS geological data integration"
echo ""
echo "🔧 Initializing..."

# Activate virtual environment
source .venv/bin/activate

# Run Flask application
echo ""
echo "✅ Server starting on http://localhost:5000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

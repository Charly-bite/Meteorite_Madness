#  Impactor-2025 - Meteorite Madness

## Hackatón GDL - NASA Challenge | Meteor Madness

A comprehensive interactive web platform that enables scientists, politicians, students, and citizens to simulate asteroid impacts using real NASA data and visualize their consequences in real-time. This project merges educational and scientific aspects, explaining complex astrophysical concepts through understandable infographics, narratives, and simulations without losing scientific accuracy.

**Problem Statement**: Currently, NASA and the USGS manage their data separately. NASA's NEO API provides data on asteroid size, velocity, and trajectory, while the USGS offers maps and data on seismic zones, elevations, and tsunami-prone regions. This separation complicates the ability to create clear simulations of asteroid impacts and their consequences. Impactor-2025 bridges this gap through interactive visualizations and a user-friendly interface.

## 🚀 Key Features

### 🎮 Real-Data Simulation
Users can simulate an asteroid's fall using real NASA data (size, speed, angle, trajectory). Interactive sliders allow adjustment of parameters like velocity or entry angle to see real-time consequences.

### 📊 Consequence Visualization
The tool shows the physical and environmental consequences of impacts in real-time, including:
- Crater size calculations
- Affected tsunami zones
- Atmospheric and local climate changes
- Population impact assessment
- Energy release measurements

### 🛡️ Mitigation Strategy Testing (Defend the Earth Mode)
Includes a 'Defend the Earth' game mode where users can test different planetary defense strategies, such as:
- Deflecting asteroids with kinetic impactors
- Nuclear deflection missions
- Gravity tractor methods
- AI-powered strategy recommendations via Google Gemini

### 🛸 NASA API Integration
- **Astronomy Picture of the Day (APOD)**
- **Near Earth Object Web Service (NeoWs)**
- **Meteorite Landing Database**

### 🌍 Multi-Source Data Integration
- **World Bank Population Data** - Global population statistics
- **NOAA Space Weather** - Solar activity and space weather conditions
- **Enhanced Meteorite Database** - Historical impact data with coordinates
- **Risk Assessment Analysis** - Population-based impact risk calculations

### 🎨 Advanced Visualizations
- **Interactive Web Dashboard** - Real-time NEO statistics and threat maps
- **Advanced Impact Simulator** - Leaflet.js powered interactive mapping
- **Global Impact Maps** - Historical meteorite impacts visualization
- **Temporal Analysis** - Historical patterns and trends over time
- **3D Interactive Plots** - Explore asteroids in 3D space
- **Atmospheric Entry Simulation** - Real-time trajectory and ablation modeling
- **Blast Wave Visualization** - Shockwave rings and overpressure zones

### 🤖 AI-Powered Features
- **Planetary Defense Strategies** - Google Gemini AI generates comprehensive defense plans
- **Impact Narratives** - Dramatic but scientifically accurate scenario descriptions
- **Threat Assessment** - AI-powered risk analysis and mission planning

### 📊 Enhanced Analytics
- **Multi-source data correlation analysis**
- **Population-based risk zone calculations**
- **Historical meteorite pattern recognition**
- **Space weather impact analysis**
- **Comprehensive reporting system**
- **Severity Classification** - Minor, Moderate, Severe, Catastrophic levels

## 📋 Requirements
- Run directly at: https://wenriverab.wixstudio.com/impactor/

Or install:

- Python 3.8+
- NASA API Key (free from https://api.nasa.gov/)
- Google Gemini API Key (for AI features)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Charly-bite/Meteorite_Madness.git
cd "Meteorite Madness"
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask flask-cors requests pandas matplotlib seaborn numpy plotly
```

4. Set up API keys:
```bash
export NASA_API_KEY="API_KEY_HERE"
export GEMINI_API_KEY="API_KEY_HERE"
```

Or configure them directly in the code files.

## 🎮 Usage

### Running the Web Application

Start the Flask server:

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**


The web application includes:
1. **Main Dashboard** - Real-time NEO statistics, asteroid browser, global threat map, and analytics
2. **Advanced Impact Simulator** - Interactive mapping with AI-powered analysis

### Using the Command-Line Tools

Run the main script for data analysis and visualizations:

```bash
python main.py
```

This will:
1. Test the NASA API connection
2. Fetch Astronomy Picture of the Day
3. Retrieve meteorite landing data
4. Get Near Earth Objects data
5. Generate interactive visualizations
6. Create analytical reports

## 📊 Visualizations

The application creates four types of visualizations:

1. **Size Distribution**: Histogram and box plots showing asteroid size patterns
2. **Distance vs Velocity**: Scatter plot correlating approach distance with speed
3. **3D Interactive Plot**: Explore asteroids in 3D space with hover details
4. **Timeline Chart**: See when asteroids will approach Earth

## 🔧 API Endpoints Used

- `https://api.nasa.gov/planetary/apod` - Astronomy Picture of the Day
- `https://api.nasa.gov/neo/rest/v1/feed` - Near Earth Object data
- `https://data.nasa.gov/resource/gh4g-9sfh.json` - Meteorite landing data

## 🎯 Technical Aspects

### Recommended Languages
- **Python** - For data handling, scientific calculations, and backend
- **JavaScript** - For browser visualization and interactivity

### Libraries & Frameworks
- **Backend**: Flask (web framework), NumPy, Pandas (data analysis)
- **Frontend**: Leaflet.js (interactive maps), Plotly.js (charts), Bootstrap 5 (UI)
- **3D Graphics**: Three.js (planned for future updates)
- **AI Integration**: Google Gemini 2.0 Flash API

### Visual Design
- Clean interface with easy-to-understand controls (sliders, buttons, interactive maps)
- Color-coded severity levels for quick threat assessment
- Responsive design for desktop and mobile devices
- Accessible color schemes and screen reader support

### Optimization
- Simulations run fast and smoothly without freezing the browser
- Efficient data loading with caching mechanisms
- Background processing for complex calculations
- Optimized rendering for real-time visualizations

### Accessibility
- Understandable for the general public
- Explanatory text and tooltips
- Multiple language support (planned)
- High contrast accessible colors
- Keyboard navigation support

## 🎨 Creative Features & Future Ideas

### Narrative Mode ✅ Implemented
A simulation mode that tells the story of 'Impactor-2025' step-by-step using AI-generated narratives.

### Regional Impact Panel 🔄 In Development
Feature showing the effects on different specific cities or ecosystems with localized assessments.

### Social Sharing 📋 Planned
Function to share simulation results on social media or download comprehensive impact reports.

### Real-Time Data Integration ✅ Implemented
Inclusion of real-time data from NASA to keep the simulator updated with the latest NEO information.

### Augmented Reality (AR) Version 🔮 Future
An AR feature that allows users to project the impact onto a physical map in a real-world environment, ideal for museums or classrooms.

## 📁 Project Structure

```
Meteorite Madness/
├── app.py                              # Flask web application with API routes
├── main.py                             # NASA API client & core data processing
├── impact_consequence_simulator.py     # Impact physics calculations
├── templates/
│   ├── index.html                      # Main dashboard with statistics & maps
│   └── impact_simulator.html           # Advanced simulator with AI features
├── static/
│   └── impact-simulator.js             # Frontend JavaScript for simulator
├── .venv/                              # Python virtual environment
├── ai_studio_code (5).txt              # Hackathon project specifications
└── README.md                           # This documentation file
```

## 🏆 Hackathon Information

- **Event**: Hackatón GDL
- **Challenge**: NASA - Meteor Madness
- **Project Name**: Impactor-2025
- **Team**: Meteorite Madness
- **Date**: October 2025
- **Goal**: Design an interactive web platform to simulate asteroid impacts and visualize consequences using real NASA and USGS data

## 📊 Scientific Accuracy

### Physics Calculations
- **Kinetic Energy**: E = ½mv² (converted to megatons TNT equivalent)
- **Crater Diameter**: Holsapple & Schmidt impact scaling laws
- **Overpressure**: Distance-based blast wave calculations
- **Atmospheric Entry**: Mass loss through ablation modeling
- **Population Impact**: Spatial density integration with risk zones

### Data Sources
- NASA NEO (Near-Earth Object) API - Real-time asteroid data
- Historical impact event database (Chelyabinsk, Tunguska, Chicxulub)
- Peer-reviewed astrophysics research papers
- USGS geological and elevation data
- World Bank population statistics

## 🌟 Usage Examples

### Example 1: Simulating the Chelyabinsk Event
1. Open Advanced Simulator
2. Click "Chelyabinsk" historical scenario button
3. Parameters auto-fill: 20m diameter, 19 km/s velocity
4. Click "Run Simulation"
5. Watch atmospheric entry and see 0.5 MT impact results

### Example 2: Custom City Impact Simulation
1. Set parameters: 100m diameter, 25 km/s, 45° angle
2. Click on map at your city location
3. Run simulation to see crater size and affected population
4. Click "Generate AI Strategy" for defense recommendations
5. Click "Generate AI Narrative" for scenario description

### Example 3: Testing Planetary Defense
1. Set large asteroid parameters (500m+)
2. Run initial simulation to assess threat
3. Use AI to generate defense strategy
4. Compare different deflection methods
5. Analyze response time windows

## 🔮 Future Enhancements

Based on creative ideas from the hackathon proposal:

1. **3D Visualization** - Three.js integration for realistic 3D asteroid rendering
2. **Multi-language Support** - Spanish, English, and additional languages
3. **Mobile Applications** - Native iOS/Android apps
4. **VR Experience** - Immersive virtual reality impact simulations
5. **Educational Curriculum** - Lesson plans for schools and universities
6. **Expanded API Integration** - ESA (European Space Agency) data
7. **Machine Learning** - Predictive models for impact probability
8. **Collaborative Mode** - Multi-user scenarios for team exercises
9. **PDF Report Generation** - Downloadable impact assessment reports
10. **AR Museum Experience** - Interactive exhibits for educational institutions

## 🤝 Contributing

We welcome contributions! This is a hackathon project designed to educate and inform the public about asteroid impacts and planetary defense.

Areas for contribution:
- Additional historical scenarios
- Enhanced physics models
- UI/UX improvements
- Translation support
- Educational content
- Bug fixes and optimizations

## 📜 License

This project was created for the Hackatón GDL - NASA Challenge 2025.

## 🌟 Acknowledgments

- **NASA** - For the NEO API and inspiring this challenge
- **USGS** - For geological and geographical data
- **Google** - For Gemini AI API access
- **Hackatón GDL** - For organizing this amazing event
- **The scientific community** - For impact physics research and open data
- **Leaflet.js** - For the amazing mapping library
- **Plotly** - For interactive data visualizations

## 📧 Contact

- **GitHub**: [@Charly-bite](https://github.com/Charly-bite)
- **Repository**: [Meteorite_Madness](https://github.com/Charly-bite/Meteorite_Madness)

---

**Made with 💫 for the NASA Meteor Madness Challenge**

*Educating the world about planetary defense, one simulation at a time.*

---

### Quick Start Commands

```bash
# Setup
git clone https://github.com/Charly-bite/Meteorite_Madness.git
cd "Meteorite Madness"
python -m venv .venv
source .venv/bin/activate
pip install flask flask-cors requests pandas matplotlib seaborn numpy plotly

# Set API Keys
export NASA_API_KEY="API_KEY_HERE"
export GEMINI_API_KEY="API_KEY_HERE"

# Run Web Application
python app.py

# Open Browser
# Navigate to http://localhost:5000
```

Enjoy exploring asteroid impacts and planetary defense strategies! 🌍🛡️

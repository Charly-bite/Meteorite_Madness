# 🌌 Meteorite Madness

A comprehensive Python application that integrates multiple data sources to analyze and visualize Near Earth Objects (NEOs), asteroids, and meteorite impacts with enhanced multi-source data analysis.

## 🚀 Features

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
- **Global Impact Maps** - Interactive world maps of meteorite impacts
- **Temporal Analysis** - Historical patterns and trends over time
- **Risk Assessment Dashboards** - Comprehensive threat analysis
- **3D Interactive Plots** - Explore asteroids in 3D space
- **Correlation Heatmaps** - Statistical relationships between properties
- **Timeline Charts** - Asteroid approach schedules

### 📊 Enhanced Analytics
- **Multi-source data correlation analysis**
- **Population-based risk zone calculations**
- **Historical meteorite pattern recognition**
- **Space weather impact analysis**
- **Comprehensive reporting system**

## 📋 Requirements

- Python 3.11+
- NASA API Key (free from https://api.nasa.gov/)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Charly-bite/Meteorite_Madness.git
cd Meteorite_Madness
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install requests pandas matplotlib seaborn numpy plotly
```

4. Get your NASA API key from https://api.nasa.gov/ and replace the placeholder in `main.py`

## 🎮 Usage

Run the main script to fetch NASA data and generate visualizations:

```bash
python main.py
```

The script will:
1. Test the NASA API connection
2. Fetch Astronomy Picture of the Day
3. Retrieve meteorite landing data
4. Get Near Earth Objects data
5. Generate interactive visualizations

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

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- NASA for providing open access to space data
- The amazing Python data visualization community

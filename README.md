# 🌌 Meteorite Madness

A Python application that connects to NASA APIs to fetch and visualize Near Earth Objects (NEOs) and asteroid data.

## 🚀 Features

- **NASA API Integration**: Connect to multiple NASA APIs including:
  - Astronomy Picture of the Day (APOD)
  - Near Earth Object Web Service (NeoWs)
  - Meteorite Landing Data

- **Interactive Visualizations**: 
  - 📊 Size distribution charts
  - 🎯 Distance vs velocity scatter plots
  - 🌌 Interactive 3D visualizations
  - 📅 Timeline charts of asteroid approaches

- **Data Analysis**: Process and analyze asteroid characteristics including:
  - Estimated diameter
  - Miss distance from Earth
  - Relative velocity
  - Potentially hazardous classification

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

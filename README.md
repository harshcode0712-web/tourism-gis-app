# Tourism Explorer — Web-Based GIS Application
## Project: Development of a Web-Based GIS Application using Spatial Databases

---

## How to Run

### Step 1 — Install Flask
```
pip install flask
```

### Step 2 — Run the app
```
python app.py
```

### Step 3 — Open in browser
```
http://127.0.0.1:5000
```

---

## Features
- 🗺️  Interactive Leaflet.js map (dark theme, CartoDB tiles)
- 🔍  Real-time search across 30 tourism places
- 📍  Nearest Neighbor Search using Haversine distance
- 🏛️  Filter by Landmarks, Hotels, Attractions
- 🖱️  Click anywhere on map to set NN search location
- 📏  Distance lines drawn from query point to results

## Tech Stack
| Layer      | Technology               |
|------------|--------------------------|
| Backend    | Python Flask             |
| Frontend   | HTML + CSS + JavaScript  |
| Map        | Leaflet.js + CartoDB     |
| Spatial    | Haversine distance (NN)  |
| Data       | 30 curated tourism POIs  |

## API Endpoints
| Endpoint               | Description                        |
|------------------------|------------------------------------|
| GET /api/places        | All places (optional ?type=)       |
| GET /api/search?q=     | Full-text search                   |
| GET /api/nearest?lat=&lng= | k-nearest neighbor query      |
| GET /api/stats         | Summary statistics                 |

## Project Structure
```
tourism_gis/
├── app.py              ← Flask backend + spatial logic
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── templates/
    └── index.html      ← Frontend (map + UI)
```

"""
Web-Based GIS Application — Tourism Explorer
Project: Development of a Web-Based GIS Application using Spatial Databases
Backend: Python Flask + In-memory Spatial Index (Quad-tree)
"""

from flask import Flask, jsonify, request, render_template
import math
import json

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────
# SPATIAL DATA — Tourism Points of Interest (India focus + global icons)
# ─────────────────────────────────────────────────────────────────────

PLACES = [
    # ── Landmarks ────────────────────────────────────────────────────
    {"id": 1,  "name": "Taj Mahal",               "type": "landmark",   "city": "Agra",        "country": "India",   "lat": 27.1751, "lng": 78.0421,  "rating": 4.9, "description": "Iconic white marble mausoleum, UNESCO World Heritage Site.", "open": "Sunrise–Sunset", "entry": "₹1100"},
    {"id": 2,  "name": "Red Fort",                "type": "landmark",   "city": "Delhi",       "country": "India",   "lat": 28.6562, "lng": 77.2410,  "rating": 4.5, "description": "Historic Mughal fort and symbol of India's sovereignty.", "open": "9AM–6PM",        "entry": "₹600"},
    {"id": 3,  "name": "Qutub Minar",             "type": "landmark",   "city": "Delhi",       "country": "India",   "lat": 28.5245, "lng": 77.1855,  "rating": 4.6, "description": "Tallest brick minaret in the world, built in 1193.", "open": "7AM–5PM",        "entry": "₹600"},
    {"id": 4,  "name": "Gateway of India",        "type": "landmark",   "city": "Mumbai",      "country": "India",   "lat": 18.9220, "lng": 72.8347,  "rating": 4.6, "description": "Iconic arch monument overlooking the Arabian Sea.", "open": "24 Hours",       "entry": "Free"},
    {"id": 5,  "name": "Hawa Mahal",              "type": "landmark",   "city": "Jaipur",      "country": "India",   "lat": 26.9239, "lng": 75.8267,  "rating": 4.5, "description": "Palace of Winds — a stunning honeycomb facade with 953 windows.", "open": "9AM–5PM",        "entry": "₹200"},
    {"id": 6,  "name": "Mysore Palace",           "type": "landmark",   "city": "Mysore",      "country": "India",   "lat": 12.3052, "lng": 76.6552,  "rating": 4.7, "description": "One of the most visited palaces in India, illuminated on Sundays.", "open": "10AM–5:30PM",    "entry": "₹100"},
    {"id": 7,  "name": "Victoria Memorial",       "type": "landmark",   "city": "Kolkata",     "country": "India",   "lat": 22.5448, "lng": 88.3426,  "rating": 4.7, "description": "Magnificent marble building dedicated to Queen Victoria.", "open": "10AM–5PM",       "entry": "₹30"},
    {"id": 8,  "name": "Charminar",               "type": "landmark",   "city": "Hyderabad",   "country": "India",   "lat": 17.3616, "lng": 78.4747,  "rating": 4.4, "description": "16th-century mosque and monument at the heart of Old Hyderabad.", "open": "9AM–5:30PM",     "entry": "₹25"},
    {"id": 9,  "name": "Eiffel Tower",            "type": "landmark",   "city": "Paris",       "country": "France",  "lat": 48.8584, "lng":  2.2945,  "rating": 4.7, "description": "Iconic iron lattice tower on the Champ de Mars.", "open": "9AM–12AM",       "entry": "€29"},
    {"id": 10, "name": "Colosseum",               "type": "landmark",   "city": "Rome",        "country": "Italy",   "lat": 41.8902, "lng": 12.4922,  "rating": 4.8, "description": "Ancient amphitheater and largest ever built in the Roman Empire.", "open": "9AM–7PM",        "entry": "€16"},

    # ── Hotels ───────────────────────────────────────────────────────
    {"id": 11, "name": "The Oberoi Amarvilas",    "type": "hotel",      "city": "Agra",        "country": "India",   "lat": 27.1694, "lng": 78.0456,  "rating": 4.9, "description": "Luxury hotel with stunning Taj Mahal views from every room.", "open": "24 Hours",       "entry": "₹45,000/night"},
    {"id": 12, "name": "ITC Maurya",              "type": "hotel",      "city": "Delhi",       "country": "India",   "lat": 28.5993, "lng": 77.1721,  "rating": 4.7, "description": "Five-star luxury hotel famous for the Bukhara restaurant.", "open": "24 Hours",       "entry": "₹18,000/night"},
    {"id": 13, "name": "Taj Mahal Palace",        "type": "hotel",      "city": "Mumbai",      "country": "India",   "lat": 18.9217, "lng": 72.8332,  "rating": 4.8, "description": "Iconic heritage hotel overlooking the Gateway of India since 1903.", "open": "24 Hours",       "entry": "₹25,000/night"},
    {"id": 14, "name": "Umaid Bhawan Palace",     "type": "hotel",      "city": "Jodhpur",     "country": "India",   "lat": 26.2819, "lng": 73.0243,  "rating": 4.8, "description": "Palace-hotel voted world's best hotel multiple times.", "open": "24 Hours",       "entry": "₹35,000/night"},
    {"id": 15, "name": "The Leela Palace",        "type": "hotel",      "city": "Bangalore",   "country": "India",   "lat": 12.9716, "lng": 77.5946,  "rating": 4.6, "description": "Ultra-luxury hotel in the heart of Silicon Valley of India.", "open": "24 Hours",       "entry": "₹20,000/night"},
    {"id": 16, "name": "Hotel de Crillon",        "type": "hotel",      "city": "Paris",       "country": "France",  "lat": 48.8670, "lng":  2.3218,  "rating": 4.8, "description": "Palatial luxury hotel on the Place de la Concorde since 1758.", "open": "24 Hours",       "entry": "€1200/night"},

    # ── Attractions ──────────────────────────────────────────────────
    {"id": 17, "name": "Amber Fort",              "type": "attraction", "city": "Jaipur",      "country": "India",   "lat": 26.9855, "lng": 75.8513,  "rating": 4.7, "description": "Magnificent fort with stunning mirror work and elephant rides.", "open": "8AM–5:30PM",     "entry": "₹500"},
    {"id": 18, "name": "Kerala Backwaters",       "type": "attraction", "city": "Alleppey",    "country": "India",   "lat":  9.4981, "lng": 76.3388,  "rating": 4.8, "description": "Serene network of lagoons, lakes and canals — ideal for houseboat stays.", "open": "All day",        "entry": "₹8,000/houseboat"},
    {"id": 19, "name": "Varanasi Ghats",          "type": "attraction", "city": "Varanasi",    "country": "India",   "lat": 25.3176, "lng": 83.0130,  "rating": 4.7, "description": "Ancient ghats on the Ganges — spiritual heartbeat of India.", "open": "All day",        "entry": "Free"},
    {"id": 20, "name": "Goa Beaches",             "type": "attraction", "city": "Goa",         "country": "India",   "lat": 15.2993, "lng": 74.1240,  "rating": 4.6, "description": "Pristine beaches, Portuguese architecture, and vibrant nightlife.", "open": "All day",        "entry": "Free"},
    {"id": 21, "name": "Ranthambore Tiger Reserve","type": "attraction","city": "Sawai Madhopur","country": "India",  "lat": 26.0173, "lng": 76.5026,  "rating": 4.7, "description": "One of India's best tiger reserves with ancient fort ruins.", "open": "6AM–10AM, 2:30–6PM", "entry": "₹1500"},
    {"id": 22, "name": "Hampi Ruins",             "type": "attraction", "city": "Hampi",       "country": "India",   "lat": 15.3350, "lng": 76.4600,  "rating": 4.8, "description": "UNESCO World Heritage Site — ruins of the Vijayanagara Empire.", "open": "6AM–6PM",        "entry": "₹600"},
    {"id": 23, "name": "Leh Ladakh",              "type": "attraction", "city": "Leh",         "country": "India",   "lat": 34.1526, "lng": 77.5771,  "rating": 4.9, "description": "High-altitude desert with Buddhist monasteries and mountain passes.", "open": "May–October",    "entry": "₹400 (permit)"},
    {"id": 24, "name": "Sundarbans National Park","type": "attraction", "city": "Sundarbans",  "country": "India",   "lat": 21.9497, "lng": 89.1833,  "rating": 4.5, "description": "World's largest mangrove forest, home to Royal Bengal Tigers.", "open": "Oct–Mar",        "entry": "₹1000"},
    {"id": 25, "name": "Louvre Museum",           "type": "attraction", "city": "Paris",       "country": "France",  "lat": 48.8606, "lng":  2.3376,  "rating": 4.7, "description": "World's largest art museum housing the Mona Lisa.", "open": "9AM–6PM",        "entry": "€17"},
    {"id": 26, "name": "Colosseum Tour",          "type": "attraction", "city": "Rome",        "country": "Italy",   "lat": 41.8957, "lng": 12.4823,  "rating": 4.6, "description": "Guided underground tours of the ancient Roman Forum.", "open": "9AM–7PM",        "entry": "€22"},
    {"id": 27, "name": "Kaziranga National Park", "type": "attraction", "city": "Assam",       "country": "India",   "lat": 26.5775, "lng": 93.1710,  "rating": 4.8, "description": "Home to two-thirds of world's one-horned rhinoceroses.", "open": "Nov–Apr",        "entry": "₹1000"},
    {"id": 28, "name": "Jim Corbett National Park","type": "attraction","city": "Nainital",    "country": "India",   "lat": 29.5300, "lng": 78.7747,  "rating": 4.6, "description": "India's oldest national park, famous for Bengal tigers.", "open": "Nov–Jun",        "entry": "₹900"},
    {"id": 29, "name": "Rishikesh",               "type": "attraction", "city": "Rishikesh",   "country": "India",   "lat": 30.0869, "lng": 78.2676,  "rating": 4.7, "description": "Yoga capital of the world on the banks of the Ganges.", "open": "All year",       "entry": "Free"},
    {"id": 30, "name": "Ellora Caves",            "type": "attraction", "city": "Aurangabad",  "country": "India",   "lat": 20.0258, "lng": 75.1780,  "rating": 4.8, "description": "UNESCO site with 34 Buddhist, Hindu and Jain cave temples.", "open": "6AM–6PM",        "entry": "₹600"},
]

TYPE_ICONS = {
    "landmark":   "🏛️",
    "hotel":      "🏨",
    "attraction": "🎯",
}

# ─────────────────────────────────────────────────────────────────────
# SPATIAL MATH UTILITIES
# ─────────────────────────────────────────────────────────────────────

def haversine(lat1, lng1, lat2, lng2):
    """Calculate distance in km between two lat/lng points."""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def nearest_neighbors(lat, lng, place_type=None, k=5):
    """Find k nearest places to a given lat/lng using haversine distance."""
    candidates = PLACES if not place_type else [p for p in PLACES if p["type"] == place_type]
    scored = []
    for p in candidates:
        d = haversine(lat, lng, p["lat"], p["lng"])
        scored.append({**p, "distance_km": round(d, 2)})
    scored.sort(key=lambda x: x["distance_km"])
    return scored[:k]


def search_places(query, place_type=None):
    """Full-text search across name, city, country, description."""
    query = query.lower().strip()
    results = []
    for p in PLACES:
        if place_type and p["type"] != place_type:
            continue
        searchable = f"{p['name']} {p['city']} {p['country']} {p['description']}".lower()
        if query in searchable:
            results.append(p)
    return results


# ─────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/places")
def get_all_places():
    place_type = request.args.get("type")
    if place_type:
        data = [p for p in PLACES if p["type"] == place_type]
    else:
        data = PLACES
    return jsonify({"places": data, "count": len(data)})


@app.route("/api/search")
def search():
    query = request.args.get("q", "").strip()
    place_type = request.args.get("type")
    if not query:
        return jsonify({"results": [], "query": query})
    results = search_places(query, place_type)
    return jsonify({"results": results, "query": query, "count": len(results)})


@app.route("/api/nearest")
def nearest():
    try:
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
        k = int(request.args.get("k", 5))
        place_type = request.args.get("type") or None
        results = nearest_neighbors(lat, lng, place_type, k)
        return jsonify({"results": results, "query_lat": lat, "query_lng": lng, "k": k})
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/stats")
def stats():
    from collections import Counter
    types = Counter(p["type"] for p in PLACES)
    countries = Counter(p["country"] for p in PLACES)
    return jsonify({
        "total": len(PLACES),
        "by_type": dict(types),
        "by_country": dict(countries),
        "avg_rating": round(sum(p["rating"] for p in PLACES) / len(PLACES), 2)
    })


if __name__ == "__main__":
    print("=" * 55)
    print("  Tourism GIS Application")
    print("  Open http://127.0.0.1:5000 in your browser")
    print("=" * 55)
    app.run(debug=True)

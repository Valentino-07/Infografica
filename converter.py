import json
import time
import requests

# --- Configurazione ---
INPUT_FILE = "aziende_cobianchi.json"    # JSON originale
OUTPUT_FILE = "aziende_cobianchi_geo.json"  # JSON aggiornato
USER_AGENT = "cobianchi-project/1.0"

# --- Funzione per ottenere lat/lon da Nominatim ---
def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": USER_AGENT
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if len(data) > 0:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"Errore geocoding per '{address}': {e}")
    return None, None

# --- Leggi il JSON ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    aziende = json.load(f)

# --- Geocode tutte le aziende ---
for i, a in enumerate(aziende):
    if "lat" not in a or "lng" not in a:
        print(f"[{i+1}/{len(aziende)}] Geocoding: {a.get('sede', '')} - {a.get('azienda','')}")
        lat, lng = geocode(a.get("sede", ""))
        if lat and lng:
            a["lat"] = lat
            a["lng"] = lng
            print(f"  -> {lat}, {lng}")
        else:
            print("  -> coordinate non trovate")
        time.sleep(1)  # rispettare limite di 1 richiesta/sec di Nominatim

# --- Salva JSON aggiornato ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(aziende, f, ensure_ascii=False, indent=4)

print(f"✅ JSON aggiornato salvato in {OUTPUT_FILE}")

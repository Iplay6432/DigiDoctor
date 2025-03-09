import googlemaps
import os
import requests

# Get API key from environment variables
api_key = os.environ.get('API_KEY')
if api_key is None:
    raise EnvironmentError('API_KEY environment variable not set')

class FindHealth:
    def __init__(self, location, radius_km=16, location_type="hospital"):
        self.location = location
        self.radius = radius_km * 1000  # Convert km to meters
        self.location_type = location_type  # Can be 'hospital', 'clinic', or 'doctors'
        self.headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress',
        }

    def get_coordinates(self, address):
        """Get latitude and longitude for an address using Google Maps API."""
        params = {"address": address, "key": api_key}
        GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"
        response = requests.get(GEOCODING_URL, params=params)
        data = response.json()
        
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            return None

    def find_health_facilities(self, lat, lon):
        """Find nearby health facilities (hospitals, clinics, or doctors) using OpenStreetMap Overpass API."""
        overpass_url = "http://overpass-api.de/api/interpreter"

        # Ensure valid OSM amenity type
        osm_types = {
            "hospital": "hospital",
            "clinic": "clinic",
            "doctors": "doctors"
        }
        osm_amenity = osm_types.get(self.location_type, "hospital")  # Default to 'hospital' if not recognized

        overpass_query = f"""
        [out:json];
        (
          node["amenity"="{osm_amenity}"](around:{self.radius},{lat},{lon});
          way["amenity"="{osm_amenity}"](around:{self.radius},{lat},{lon});
          relation["amenity"="{osm_amenity}"](around:{self.radius},{lat},{lon});
        );
        out center;
        """
        
        response = requests.get(overpass_url, params={'data': overpass_query})
        
        if response.status_code == 200:
            data = response.json()
            facilities = []
            
            for element in data['elements']:
                name = element.get('tags', {}).get('name', 'Unknown Facility')
                facility_lat = element.get('lat', element.get('center', {}).get('lat'))
                facility_lon = element.get('lon', element.get('center', {}).get('lon'))
                
                facilities.append({
                    'name': name,
                    'latitude': facility_lat,
                    'longitude': facility_lon
                })
            
            return facilities
        else:
            print("Error fetching data:", response.status_code)
            return None

    def find(self):
        """Find health facilities near the given location."""
        coords = self.get_coordinates(self.location)
        if coords:
            lat, lon = coords
            facilities = self.find_health_facilities(lat, lon)
            return facilities
        else:
            print("Invalid location or unable to get coordinates.")
            return None

# # Example usage
# find_clinic = FindHealth("6560 braddock road", radius_km=16, location_type="hospital")
# results = find_clinic.find()

# if results:
#     print(f"Found {len(results)} clinics nearby:")
#     for facility in results:
#         print(f"{facility['name']} - ({facility['latitude']}, {facility['longitude']})")
# else:
#     print("No clinics found nearby.")

import requests
from geopy.geocoders import Nominatim

def get_coordinates(region_name):
    geolocator = Nominatim(user_agent="solar_app")
    location = geolocator.geocode(region_name + ", Myanmar")
    if location:
        return location.latitude, location.longitude
    return None, None

def get_sunlight_hours(lat, lon):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "latitude": lat,
        "longitude": lon,
        "parameters": "ALLSKY_SFC_SW_DWN",
        "format": "JSON",
        "community": "RE"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        annual_irradiance = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']['ANN']
        return round(annual_irradiance / 3.6, 2)
    except Exception as e:
        print("NASA API error:", e)
        return None
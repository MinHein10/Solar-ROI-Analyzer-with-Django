from django.core.management.base import BaseCommand
from solar_analyzer.models import Region
from solar_analyzer.utils.nasa_power import get_coordinates, get_sunlight_hours


# Expanded list with 21 divisions
REGIONS_DATA = [
    ("Yangon Region", 150),
    ("Mandalay Region", 145),
    ("Ayeyarwady Region", 135),
    ("Bago Region", 140),
    ("Magway Region", 130),
    ("Sagaing Region", 132),
    ("Tanintharyi Region", 138),
    ("Kachin State", 125),
    ("Kayah State", 120),
    ("Kayin State", 128),
    ("Chin State", 115),
    ("Mon State", 135),
    ("Rakhine State", 122),
    ("Shan State", 118),
    ("Naypyidaw Union Territory", 140),
    ("Naga Self-Administered Zone", 110),
    ("Danu Self-Administered Zone", 112),
    ("Pa-O Self-Administered Zone", 114),
    ("Palaung Self-Administered Zone", 113),
    ("Kokang Self-Administered Zone", 109),
    ("Wa Self-Administered Division", 108),
]

class Command(BaseCommand):
    help = "Seeds all Myanmar regions with coordinates, sunlight hours, and electricity rates"

    def handle(self, *args, **kwargs):
        for name, rate in REGIONS_DATA:
            lat, lon = get_coordinates(name)
            if lat and lon:
                sunlight = get_sunlight_hours(lat, lon)
                Region.objects.update_or_create(
                    name=name,
                    defaults={
                        "latitude": lat,
                        "longitude": lon,
                        "sunlight_hours": sunlight,
                        "electricity_rate": rate
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Seeded: {name} | Rate: {rate} MMK/kWh"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch lat/lon: {name}"))

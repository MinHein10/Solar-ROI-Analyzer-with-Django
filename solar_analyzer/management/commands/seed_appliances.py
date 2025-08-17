from django.core.management.base import BaseCommand
from solar_analyzer.models import ApplianceProfile

class Command(BaseCommand):
    help = "Seeds ApplianceProfile data with realistic Myanmar examples"

    def handle(self, *args, **kwargs):
        APPLIANCE_DATA = [
            {
                "name": "Basic Home",
                "total_kwh_per_day": 4.2,
                "description": "4 lights, 1 fan, 1 fridge (Yangon apartment)"
            },
            {
                "name": "Small Office",
                "total_kwh_per_day": 6.5,
                "description": "3 computers, 1 printer, 1 fan, 4 LED lights"
            },
            {
                "name": "Restaurant",
                "total_kwh_per_day": 15.8,
                "description": "Rice cooker, fridge, freezer, lights, water pump"
            },
            {
                "name": "Large Apartment",
                "total_kwh_per_day": 10.3,
                "description": "2 AC units, washing machine, fridge, lights"
            },
            {
                "name": "Internet Cafe",
                "total_kwh_per_day": 20.0,
                "description": "10 computers, router, lights, 1 AC unit"
            },
            {
                "name": "Rural Shop",
                "total_kwh_per_day": 3.8,
                "description": "Light bulb, 1 fan, 1 small refrigerator"
            },
            {
                "name": "Mobile Tower Site",
                "total_kwh_per_day": 12.0,
                "description": "Signal booster, 2 batteries, lights"
            },
            {
                "name": "Hostel (8 rooms)",
                "total_kwh_per_day": 9.7,
                "description": "Shared fans, water heater, common fridge"
            },
            {
                "name": "Hospital Ward",
                "total_kwh_per_day": 25.0,
                "description": "Medical equipment, fans, lights, backup system"
            },
            {
                "name": "School Building",
                "total_kwh_per_day": 8.5,
                "description": "5 computers, 2 projectors, lights, ceiling fans"
            },
            {
                "name": "Tea Shop",
                "total_kwh_per_day": 6.9,
                "description": "Rice cooker, lights, kettle, ceiling fans"
            },
            {
                "name": "Rice Mill (Small)",
                "total_kwh_per_day": 18.0,
                "description": "1 motor, lights, fans, drying system"
            },
            {
                "name": "Village Clinic",
                "total_kwh_per_day": 7.5,
                "description": "Refrigerator (vaccines), lights, fan, autoclave"
            },
            {
                "name": "Monastery Dorm",
                "total_kwh_per_day": 5.6,
                "description": "Ceiling fans, LED lights, shared kettle"
            },
            {
                "name": "High-End Villa",
                "total_kwh_per_day": 16.5,
                "description": "3 AC units, fridge, washer, lights, smart devices"
            },
        ]

        for item in APPLIANCE_DATA:
            ApplianceProfile.objects.update_or_create(
                name=item["name"],
                defaults={
                    "total_kwh_per_day": item["total_kwh_per_day"],
                    "description": item["description"]
                }
            )

        self.stdout.write(self.style.SUCCESS("ApplianceProfile data seeded successfully."))

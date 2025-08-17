from django.core.management.base import BaseCommand
from solar_analyzer.models import InstallationPackage

class Command(BaseCommand):
    help = "Seeds InstallationPackage data with realistic Myanmar solar setup examples"

    def handle(self, *args, **kwargs):
        PACKAGES = [
            {
                "name": "1kW Starter Kit",
                "system_size": 1.0,
                "system_cost": 1800000,
                "lifespan": 20,
                "description": "Basic setup for lighting and small appliances in rural homes"
            },
            {
                "name": "2kW Home Basic",
                "system_size": 2.0,
                "system_cost": 3000000,
                "lifespan": 20,
                "description": "Small household setup ideal for apartments or rural houses"
            },
            {
                "name": "3kW Standard",
                "system_size": 3.0,
                "system_cost": 4200000,
                "lifespan": 20,
                "description": "Average home setup with fridge, fans, and lights"
            },
            {
                "name": "3.5kW Family Kit",
                "system_size": 3.5,
                "system_cost": 4800000,
                "lifespan": 25,
                "description": "Mid-size family homes or two-story houses"
            },
            {
                "name": "5kW Premium",
                "system_size": 5.0,
                "system_cost": 6500000,
                "lifespan": 25,
                "description": "Large houses, small offices or mixed residential/commercial"
            },
            {
                "name": "6.5kW Hybrid Backup",
                "system_size": 6.5,
                "system_cost": 7800000,
                "lifespan": 25,
                "description": "Home/office setup with battery backup for power outages"
            },
            {
                "name": "7kW Enterprise",
                "system_size": 7.0,
                "system_cost": 8000000,
                "lifespan": 25,
                "description": "For businesses, restaurants, or schools"
            },
            {
                "name": "10kW Industrial",
                "system_size": 10.0,
                "system_cost": 11500000,
                "lifespan": 25,
                "description": "High demand installations: hospitals, hostels, factories"
            },
            {
                "name": "12kW Hospital Kit",
                "system_size": 12.0,
                "system_cost": 13800000,
                "lifespan": 25,
                "description": "Designed for rural hospitals with equipment and refrigeration"
            },
            {
                "name": "15kW School & Monastery",
                "system_size": 15.0,
                "system_cost": 16500000,
                "lifespan": 25,
                "description": "Ideal for public institutions like schools or monasteries"
            }
        ]

        for pkg in PACKAGES:
            InstallationPackage.objects.update_or_create(
                name=pkg["name"],
                defaults={
                    "system_size": pkg["system_size"],
                    "system_cost": pkg["system_cost"],
                    "lifespan": pkg["lifespan"],
                    "description": pkg["description"]
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ InstallationPackage data seeded successfully."))

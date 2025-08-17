from django.core.management.base import BaseCommand
from solar_analyzer.models import IncentiveProgram, Region

class Command(BaseCommand):
    help = "Seeds IncentiveProgram data for different Myanmar regions"

    def handle(self, *args, **kwargs):
        programs = [
            ("Yangon 2025 Green Energy Grant", 300000, "Yangon Region"),
            ("Mandalay Solar Promotion", 350000, "Mandalay Region"),
            ("Ayeyarwady Farm Solar Aid", 400000, "Ayeyarwady Region"),
            ("Bago Clean Power Grant", 320000, "Bago Region"),
            ("Magway Off-Grid Support", 450000, "Magway Region"),
            ("Sagaing Rural PV Scheme", 400000, "Sagaing Region"),
            ("Tanintharyi Coastal Solar Plan", 370000, "Tanintharyi Region"),
            ("Kachin Solar Relief Program", 420000, "Kachin State"),
            ("Kayah Home Energy Initiative", 310000, "Kayah State"),
            ("Kayin Renewable Push", 300000, "Kayin State"),
            ("Chin Solar Village Boost", 480000, "Chin State"),
            ("Mon Grid Relief Plan", 290000, "Mon State"),
            ("Rakhine Home Solar Grant", 430000, "Rakhine State"),
            ("Shan Rural Development Subsidy", 460000, "Shan State"),
            ("Naypyidaw Eco Housing Plan", 250000, "Naypyidaw Union Territory"),
            ("Myeik Fishing Village Grant", 350000, "Tanintharyi Region"),
            ("Meiktila Township Support", 340000, "Mandalay Region"),
            ("Dawei Solar Business Aid", 370000, "Tanintharyi Region"),
            ("Hinthada Urban Solar Plan", 310000, "Ayeyarwady Region"),
            ("Lashio Hill Region Grant", 390000, "Shan State"),
            ("Hakha Remote Electrification Fund", 490000, "Chin State"),
        ]

        created_count = 0

        for name, grant, region_name in programs:
            try:
                region = Region.objects.get(name=region_name)
                IncentiveProgram.objects.update_or_create(
                    name=name,
                    region=region,
                    defaults={
                        "grant_amount": grant
                    }
                )
                created_count += 1
            except Region.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Region not found: {region_name}"))

        self.stdout.write(self.style.SUCCESS(f" {created_count} IncentiveProgram records seeded."))

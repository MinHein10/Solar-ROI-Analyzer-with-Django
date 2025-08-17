from solar_analyzer.models import Region, SolarInputSession
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed realistic Myanmar-based SolarInputSession data'

    def handle(self, *args, **kwargs):
        if Region.objects.count() == 0:
            self.stdout.write(self.style.ERROR('❌ No Region data found. Run seed_regions first.'))
            return

        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('❌ No User found. Create a user first.'))
            return

        for _ in range(15):
            region = Region.objects.order_by('?').first()

            usage_type = random.choice(['daily', 'monthly'])

            # Energy usage (more realistic)
            if usage_type == 'daily':
                energy_usage = round(random.uniform(6, 12), 2)
            else:
                energy_usage = round(random.uniform(200, 450), 2)

            # Realistic system cost and size
            system_cost = round(random.uniform(4800000, 6000000), 0)  # MMK
            incentives = random.choice([0, 200000, 300000, 500000])
            lifespan = random.choice([20, 25])

            # Estimate system size based on energy usage
            if usage_type == 'daily':
                estimated_monthly_usage = energy_usage * 30
            else:
                estimated_monthly_usage = energy_usage
            system_size = round(estimated_monthly_usage / 120, 2)  # Roughly 1kW per 120kWh/month

            sunlight_hours = region.sunlight_hours
            electricity_rate = region.electricity_rate

            annual_production = round(system_size * sunlight_hours * 365, 2)
            annual_savings = round(annual_production * electricity_rate, 2)
            total_savings = round(annual_savings * lifespan, 2)
            net_cost = round(system_cost - incentives, 2)

            payback_period = round(net_cost / annual_savings, 2) if annual_savings else None
            roi_percent = round(((total_savings - net_cost) / net_cost) * 100, 2) if net_cost else None
            cost_per_kwh = round(net_cost / (annual_production * lifespan), 4) if annual_production else None
            grid_cost = round(estimated_monthly_usage * 12 * electricity_rate * lifespan, 2)

            SolarInputSession.objects.create(
                user=user,
                region=region,
                usage_type=usage_type,
                energy_usage=energy_usage,
                electricity_rate=electricity_rate,
                system_size=system_size,
                sunlight_hours=sunlight_hours,
                system_cost=system_cost,
                incentives=incentives,
                lifespan=lifespan,
                annual_production=annual_production,
                annual_savings=annual_savings,
                total_savings=total_savings,
                net_cost=net_cost,
                payback_period=payback_period,
                roi_percent=roi_percent,
                cost_per_kwh=cost_per_kwh,
                grid_cost=grid_cost,
            )

        self.stdout.write(self.style.SUCCESS("✅ 15 realistic SolarInputSession records seeded for Myanmar."))

from django.db import models
from django.contrib.auth.models import User


class Region(models.Model):
    name = models.CharField(max_length=100)
    sunlight_hours = models.FloatField(help_text="Average sunlight per day")
    electricity_rate = models.FloatField(help_text="Electricity price in MMK/kWh")

    latitude = models.FloatField(help_text="Latitude")
    longitude = models.FloatField(help_text="Longitude")

    def __str__(self):
        return self.name

class ApplianceProfile(models.Model):
    name = models.CharField(max_length=100)
    total_kwh_per_day = models.FloatField(help_text="Estimated total daily energy usage (kWh)")
    description = models.TextField()
    image = models.ImageField(upload_to='appliance_images/', null=True, blank=True) 

    def __str__(self):
        return self.name

class InstallationPackage(models.Model):
    name = models.CharField(max_length=100)
    system_size = models.FloatField(help_text="Size in kW")
    system_cost = models.FloatField(help_text="Cost in MMK")
    lifespan = models.PositiveIntegerField(help_text="Years of operation")
    description = models.TextField()

    def __str__(self):
        return self.name

class IncentiveProgram(models.Model):
    name = models.CharField(max_length=100)
    grant_amount = models.FloatField(help_text="Discount/grant in MMK")
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class SolarInputSession(models.Model):
    USAGE_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    appliance_profile = models.ForeignKey(ApplianceProfile, on_delete=models.SET_NULL, null=True, blank=True)
    installation_package = models.ForeignKey(InstallationPackage, on_delete=models.SET_NULL, null=True, blank=True)
    incentive_program = models.ForeignKey(IncentiveProgram, on_delete=models.SET_NULL, null=True, blank=True)

    usage_type = models.CharField(max_length=10, choices=USAGE_TYPE_CHOICES)

    # Snapshots from related models
    energy_usage = models.FloatField(help_text="Energy usage in kWh (daily or monthly)")
    electricity_rate = models.FloatField(help_text="MMK per kWh")
    system_size = models.FloatField(help_text="System size in kW")
    sunlight_hours = models.FloatField(help_text="Average sunlight hours/day")
    system_cost = models.FloatField(help_text="Total system cost in MMK")
    incentives = models.FloatField(default=0, help_text="Grants or discounts in MMK")
    lifespan = models.PositiveIntegerField(default=20, help_text="Expected lifespan in years")

    created_at = models.DateTimeField(auto_now_add=True)

    # Calculated outputs
    annual_production = models.FloatField(null=True, blank=True)
    annual_savings = models.FloatField(null=True, blank=True)
    total_savings = models.FloatField(null=True, blank=True)
    net_cost = models.FloatField(null=True, blank=True)
    payback_period = models.FloatField(null=True, blank=True)
    roi_percent = models.FloatField(null=True, blank=True)
    cost_per_kwh = models.FloatField(null=True, blank=True)
    grid_cost = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Solar Input by {self.user or 'Guest'} on {self.created_at.strftime('%Y-%m-%d')}"

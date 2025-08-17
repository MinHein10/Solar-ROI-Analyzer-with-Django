from django.contrib import admin
from .models import Region, SolarInputSession, IncentiveProgram, InstallationPackage, ApplianceProfile

# Register your models here.
admin.site.register(Region)
admin.site.register(SolarInputSession)
admin.site.register(IncentiveProgram)
admin.site.register(InstallationPackage)
admin.site.register(ApplianceProfile)
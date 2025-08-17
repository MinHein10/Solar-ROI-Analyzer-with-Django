from django import forms
from .models import Region
from django.contrib.auth.models import User 
from .models import SolarInputSession

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username','password',
                  'password_confirm']

    def clean(self):
        cleaned_data = super().clean() 
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data
    



class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'sunlight_hours', 'electricity_rate']
        labels = {
            'name': 'Region Name',
            'sunlight_hours': 'Average Sunlight Hours per Day',
            'electricity_rate': 'Electricity Rate (MMK/kWh)',
        }
        help_texts = {
            'sunlight_hours': 'Average number of sunlight hours per day',
            'electricity_rate': 'Electricity price in MMK per kWh',
        }
    

class SolarInputForm(forms.ModelForm):
    class Meta:
        model = SolarInputSession
        fields = [
            'region',
            'appliance_profile',
            'installation_package',
            'incentive_program',
            'usage_type',
        ]
        labels = {
            'usage_type': 'Usage Type (Daily/Monthly)',
            'region': 'Region',
            'appliance_profile': 'Appliance Profile',
            'installation_package': 'Installation Package',
            'incentive_program': 'Incentive Program',
        }

    def __init__(self, *args, **kwargs):
        super(SolarInputForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class SolarStep1Form(forms.ModelForm):
    class Meta:
        model = SolarInputSession
        fields = ['usage_type', 'region', 'appliance_profile']
        labels = {
            'usage_type': 'Usage Type (Daily/Monthly)',
            'region': 'Region',
            'appliance_profile': 'Appliance Profile',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usage_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['region'].widget.attrs.update({'class': 'form-control'})
        self.fields['appliance_profile'].widget.attrs.update({'style': 'display:none;'})

class SolarStep2Form(forms.ModelForm):
    class Meta:
        model = SolarInputSession
        fields = ['installation_package', 'incentive_program']
        labels = {
            'installation_package': 'Installation Package',
            'incentive_program': 'Incentive Program',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['installation_package'].widget.attrs.update({
            'class': 'd-none',
            'id': 'id_installation_package'
        })

        self.fields['incentive_program'].widget.attrs.update({
            'class': 'form-control'
        })

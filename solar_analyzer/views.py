from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Region, SolarInputSession
from .forms import RegionForm, RegisterForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .utils.nasa_power import get_coordinates, get_sunlight_hours
from .forms import SolarInputForm, SolarStep1Form, SolarStep2Form
from .models import SolarInputSession, ApplianceProfile,IncentiveProgram, InstallationPackage, Region
from pprint import pprint
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def index(request):
    current_user = request.user
    solar_data = SolarInputSession.objects.filter(user=current_user.id)
    
    
    # Prepare data for visualizations
    region_names = [s.region.name for s in solar_data]
    roi_data = [float(s.roi_percent or 0) for s in solar_data]
    payback_data = [float(s.payback_period or 0) for s in solar_data]
    system_cost_data = [float(s.system_cost or 0) for s in solar_data]

    
    # context = {'solar_data':solar_data}
    context = {
        'solar_data': solar_data,
        'region_names': json.dumps(region_names, cls=DjangoJSONEncoder),
        'roi_data': json.dumps(roi_data, cls=DjangoJSONEncoder),
        'payback_data': json.dumps(payback_data, cls=DjangoJSONEncoder),
        'system_cost_data': json.dumps(system_cost_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'form/home.html',context)

@login_required
def visualize_region(request):
    regions = Region.objects.all()
    
    context = {'regions': regions}
    return render(request, 'form/visualize_region.html',context)

@login_required
def solar_detail_view(request,pk):
    session = get_object_or_404(SolarInputSession, pk=pk)
    return render(request, 'form/solar_detail.html', {'session': session})

@login_required
def download_solar_detail_pdf(request):
    # Use latest() instead of get()
    session = SolarInputSession.objects.filter(user=request.user).order_by('-created_at').first()

    if not session:
        return HttpResponse("No solar data available.")

    # template_path = 'form/solar_detail.html'
    template_path = 'form/solar_detail_pdf.html'
    
    context = {
        'solar_data': session
    }

    # Load and render HTML template
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solar_detail_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF.")
    
    return response


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')  
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request,user)
            return redirect('index')
        else: 
            # form = RegisterForm()
            return render(request, 'accounts/register.html',{'form':form})
    else:
        form = RegisterForm()
        return render(request,'accounts/register.html',{'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
        else: 
            error_message = "Invalid Credentials!"
            return render(request,'accounts/login.html',{'error':error_message})
    else:
        return render(request,'accounts/login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('index')



#Protected View
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self,request):
        return render(request, 'accounts/protected.html')


def solar_form_view(request):
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():

            region = form.save(commit=False)

            # Fetch sunlight hours automatically
            lat, lon = get_coordinates(region.name)
            if lat and lon:
                region.latitude = lat
                region.longitude = lon
                region.sunlight_hours = get_sunlight_hours(lat, lon)

            region.save()

            return redirect('index')
    else:
        form = RegionForm()
        context = {'form':form}
        return render(request,'form/form-view.html',context)

def form_success_view(request):
    return render(request,'form/form-success.html')


def calculate_outputs(session):
    # 1. Fill missing data from region
    if session.region:
        if not session.sunlight_hours:
            session.sunlight_hours = session.region.sunlight_hours
        if not session.electricity_rate:
            session.electricity_rate = session.region.electricity_rate

    # 2. Auto-estimate system size (if not given)
    if not session.system_size:
        if session.usage_type == 'monthly':
            session.system_size = session.energy_usage / 120  # rule of thumb
        else:
            session.system_size = (session.energy_usage * 30) / 120

    # 3. Annual Production
    session.annual_production = session.system_size * session.sunlight_hours * 365

    # 4. Annual Savings
    session.annual_savings = session.annual_production * session.electricity_rate

    # 5. Total Savings
    session.total_savings = session.annual_savings * session.lifespan

    # 6. Net Cost
    session.net_cost = session.system_cost - session.incentives

    # 7. Payback Period
    session.payback_period = session.net_cost / session.annual_savings if session.annual_savings else None

    # 8. ROI
    session.roi_percent = ((session.total_savings - session.net_cost) / session.net_cost) * 100 if session.net_cost else None

    # 9. Cost per kWh
    session.cost_per_kwh = session.net_cost / (session.annual_production * session.lifespan)

    # 10. Grid cost
    if session.usage_type == 'daily':
        monthly_usage = session.energy_usage * 30
    else:
        monthly_usage = session.energy_usage

    session.grid_cost = monthly_usage * 12 * session.electricity_rate * session.lifespan

    session.save()
    return session

def calculate_outputs(session):
    try:
        session.annual_production = round(session.system_size * session.sunlight_hours * 365, 2)
        session.annual_savings = round(session.annual_production * session.electricity_rate, 2)
        session.total_savings = round(session.annual_savings * session.lifespan, 2)
        session.net_cost = round(session.system_cost - session.incentives, 2)
        session.payback_period = round(session.net_cost / session.annual_savings, 2) if session.annual_savings else None
        session.roi_percent = round(((session.total_savings - session.net_cost) / session.net_cost) * 100, 2) if session.net_cost else None
        session.cost_per_kwh = round(session.net_cost / (session.annual_production * session.lifespan), 4) if session.annual_production else None
        session.grid_cost = round(session.energy_usage * 365 * session.electricity_rate * session.lifespan, 2)
    except:
        pass
    session.save()

def solar_input_view(request):
    if request.method == 'POST':
        form = SolarInputForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)

            # Get values from related tables
            if session.region:
                session.electricity_rate = session.region.electricity_rate
                session.sunlight_hours = session.region.sunlight_hours

            if session.appliance_profile:
                session.energy_usage = session.appliance_profile.total_kwh_per_day if session.usage_type == 'daily' else session.appliance_profile.total_kwh_per_day * 30

            if session.installation_package:
                session.system_size = session.installation_package.system_size
                session.system_cost = session.installation_package.system_cost
                session.lifespan = session.installation_package.lifespan

            if session.incentive_program:
                session.incentives = session.incentive_program.grant_amount

            session.user = request.user if request.user.is_authenticated else None

            calculate_outputs(session)

            return render(request, 'form/results.html', {'session': session})
    else:
        form = SolarInputForm()
    return render(request, 'form/solar_input.html', {'form': form})

def solar_step1_view(request):
    if request.method == 'POST':
        form = SolarStep1Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Store only the step1-related fields in session
            request.session['step1_data'] = {
                'usage_type': data.get('usage_type'),
                'region_id': data.get('region').id if data.get('region') else None,
                'appliance_profile_id': data.get('appliance_profile').id if data.get('appliance_profile') else None,
            }

            return redirect('solar_step2')
    else:
        form = SolarStep1Form()
        appliance_profiles = ApplianceProfile.objects.all()
    return render(request, 'form/solar_step1.html', {'form': form,'appliance_profiles': appliance_profiles})


def solar_step2_view(request):
    step1_data = request.session.get('step1_data')

    if not step1_data:
        return redirect('solar_step1')

    if request.method == 'POST':
        form = SolarStep2Form(request.POST)
        if form.is_valid():
            # Get Step 2 cleaned data
            step2_data = form.cleaned_data

            # Re-fetch model instances
            region = Region.objects.get(id=step1_data['region_id']) if step1_data.get('region_id') else None
            appliance_profile = ApplianceProfile.objects.get(id=step1_data['appliance_profile_id']) if step1_data.get('appliance_profile_id') else None
            installation_package = step2_data.get('installation_package')
            incentive_program = step2_data.get('incentive_program')

            # Create SolarInputSession object
            session = SolarInputSession(
                user=request.user if request.user.is_authenticated else None,
                usage_type=step1_data['usage_type'],
                region=region,
                appliance_profile=appliance_profile,
                installation_package=installation_package,
                incentive_program=incentive_program,
            )

            # Auto-populate from related models
            if session.region:
                session.electricity_rate = session.region.electricity_rate
                session.sunlight_hours = session.region.sunlight_hours

            if session.appliance_profile:
                session.energy_usage = (
                    session.appliance_profile.total_kwh_per_day
                    if session.usage_type == 'daily'
                    else session.appliance_profile.total_kwh_per_day * 30
                )

            if session.installation_package:
                session.system_size = session.installation_package.system_size
                session.system_cost = session.installation_package.system_cost
                session.lifespan = session.installation_package.lifespan

            if session.incentive_program:
                session.incentives = session.incentive_program.grant_amount

            # Calculate outputs
            calculate_outputs(session)

            # Save to DB
            session.save()

            # Clear session
            request.session.pop('step1_data', None)

            return render(request, 'form/results.html', {'session': session})
    else:
        form = SolarStep2Form()
        install_package_all = InstallationPackage.objects.all()
    return render(request, 'form/solar_step2.html', {'form': form, 'install_package_all':install_package_all})

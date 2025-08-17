def calculate_outputs(session):
    """
    Fill in all the calculated fields in SolarInputSession based on selected input values.
    """

    # Get values from related tables
    system_size = session.installation_package.system_size
    system_cost = session.installation_package.system_cost
    lifespan = session.installation_package.lifespan
    sunlight_hours = session.region.sunlight_hours
    electricity_rate = session.region.electricity_rate
    incentive_amount = session.incentive_program.grant_amount if session.incentive_program else 0
    energy_usage = session.appliance_profile.total_kwh_per_day

    # Estimate monthly usage
    if session.usage_type == 'daily':
        estimated_monthly_usage = energy_usage * 30
    else:
        estimated_monthly_usage = energy_usage

    # Calculations
    annual_production = system_size * sunlight_hours * 365
    annual_savings = annual_production * electricity_rate
    total_savings = annual_savings * lifespan
    net_cost = system_cost - incentive_amount
    payback_period = round(net_cost / annual_savings, 2) if annual_savings else None
    roi_percent = round(((total_savings - net_cost) / net_cost) * 100, 2) if net_cost else None
    cost_per_kwh = round(net_cost / (annual_production * lifespan), 4) if annual_production else None
    grid_cost = round(estimated_monthly_usage * 12 * electricity_rate * lifespan, 2)

    # Assign back to session
    session.system_size = system_size
    session.system_cost = system_cost
    session.sunlight_hours = sunlight_hours
    session.electricity_rate = electricity_rate
    session.energy_usage = energy_usage
    session.incentives = incentive_amount
    session.lifespan = lifespan

    session.annual_production = annual_production
    session.annual_savings = annual_savings
    session.total_savings = total_savings
    session.net_cost = net_cost
    session.payback_period = payback_period
    session.roi_percent = roi_percent
    session.cost_per_kwh = cost_per_kwh
    session.grid_cost = grid_cost

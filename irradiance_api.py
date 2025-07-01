import os
import requests
import calendar
import streamlit as st

API_KEY = st.secrets["NASA_API"]
PARAMS = "ALLSKY_SFC_SW_DWN"
COMMUNITY = "RE"
FORMAT = "JSON"


def get_monthly_irradiance(lat, lon, year):
    try:
        url = (
            f"{API_KEY}?"
            f"parameters={PARAMS}&community={COMMUNITY}"
            f"&longitude={lon}&latitude={lat}&start={year}&end={year}&format={FORMAT}"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    except Exception as e:
        return {"error": f"Monthly fetch failed: {e}"}


def format_total_energy(irradiance_data, year):
    # This function takes irradiance_data (monthly) and year as input,
    # and calculates total monthly energy (kWh/m2/month) by multiplying daily GHI * days in month
    formatted = format_irradiance_data(irradiance_data)
    energy_per_month = {}
    for month_abbr, ghi in formatted.items():
        month_num = list(calendar.month_abbr).index(month_abbr)
        days = calendar.monthrange(year, month_num)[1]
        energy_per_month[month_abbr] = round(ghi * days, 2)  # total energy in kWh/m2/month
    return energy_per_month


def format_monthly_sun_hours(irradiance_data, year):
    """Estimate average sun hours per day by dividing monthly GHI (kWh/m2/month) by days in the month."""
    formatted = format_irradiance_data(irradiance_data)
    sun_hours = {}
    for month_abbr, ghi in formatted.items():
        month_num = list(calendar.month_abbr).index(month_abbr)
        days = calendar.monthrange(year, month_num)[1]
        # Assuming 1 kW/m2 as peak sun power
        sun_hours[month_abbr] = round(ghi / 1, 2)  # average daily sun hours
    return sun_hours


def format_irradiance_data(irradiance):
    month_map = {f"{i:02d}": calendar.month_abbr[i] for i in range(1, 13)}
    return {
        month_map[k[-2:]]: v
        for k, v in irradiance.items()
        if k[-2:] in month_map
    }

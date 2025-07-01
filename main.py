import streamlit as st
import pandas as pd
import plotly.express as px
from irradiance_api import (
    get_monthly_irradiance,
    format_total_energy,
    format_monthly_sun_hours,
    format_irradiance_data
)
from style import (
    set_background_from_local,
    set_text_style,
    set_glassmorphism_style
)

NAME_KEY = st.secrets["NAME"]

st.set_page_config(page_title="SolarData", page_icon="☀️")

set_glassmorphism_style()
set_background_from_local("assets/bg.jpg")
set_text_style()

st.title("☀️ SolarData")
st.markdown(f"Created by {NAME_KEY}")  # Don't remove it, just comment out if you want to.
st.markdown("Enter latitude, longitude, and year to get monthly solar data.")

# Input fields
lat = st.number_input("🌍 Latitude", format="%.4f", value=23.8103)
lon = st.number_input("🌍 Longitude", format="%.4f", value=90.4125)
year = st.number_input("📅 Year", min_value=2000, max_value=2025, step=1, value=2023)

if st.button("🔍 Get Solar Data"):
    with st.spinner("Searching data..."):
        ghi = get_monthly_irradiance(lat, lon, year)

    if "error" in ghi:
        st.error(ghi["error"])
    else:
        formatted_ghi = format_irradiance_data(ghi)

        total_energy = format_total_energy(ghi, year)  # pass raw ghi
        sun_hours = format_monthly_sun_hours(ghi, year)  # pass raw ghi (not total_energy!)

        df = pd.DataFrame({
            "Month": list(formatted_ghi.keys()),
            "Total Energy (kWh/m²/month)": [total_energy[m] for m in formatted_ghi.keys()],
            "Sun Hours": [sun_hours[m] for m in formatted_ghi.keys()]
        })

        st.success(f"Here's the solar data for lat {lat}, lon {lon} in {year}")

        # Data Tables & Charts
        st.write("### 📋 Full Monthly Table")
        st.dataframe(df.set_index("Month"), use_container_width=True)

        st.write("### 📈 Total Monthly Energy")
        fig_energy = px.bar(df, x="Month", y="Total Energy (kWh/m²/month)", text_auto=".2s",
                            color="Total Energy (kWh/m²/month)")
        st.plotly_chart(fig_energy, use_container_width=True)

        st.write("### ☀️ Average Sun Hours")
        fig2 = px.line(df, x="Month", y="Sun Hours", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

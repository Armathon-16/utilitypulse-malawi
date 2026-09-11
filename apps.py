import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import base64
from datetime import datetime, timedelta
from pathlib import Path


def svg_icon(filename, label, size=22):
    svg_path = Path(__file__).parent / "propsvg" / filename
    encoded_svg = base64.b64encode(svg_path.read_bytes()).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{encoded_svg}" alt="{label}" width="{size}" height="{size}" style="vertical-align: middle; margin-right: 0.35rem;">'

# Page Setup
st.set_page_config(
    page_title="UtilityPulse Malawi",
    page_icon=str(Path(__file__).parent / "propsvg" / "utility-pole.svg"),
    layout="wide"
)

# Header
st.markdown(f"<h1>{svg_icon('utility-pole.svg', 'Power')}UtilityPulse Malawi</h1>", unsafe_allow_html=True)
st.caption("AI-Powered Electricity & Water Outage Early-Warning Platform")

# Sidebar - Quick Settings
st.sidebar.markdown(f"### {svg_icon('layers-arrow-down.svg', 'Controls')}Demo Controls", unsafe_allow_html=True)
selected_area = st.sidebar.selectbox("Select Business Location", ["Area 25 (Lilongwe)", "Area 47 (Lilongwe)", "Limbe (Blantyre)", "Zomba Central"])
business_type = st.sidebar.selectbox("Business Type", ["Bakery / Grocery", "Salon / Barber", "Butchery / Cold Room", "Restaurant"])

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["WhatsApp Alert Simulator", "Outage Intelligence Dashboard", "Energy Usage Monitoring"])

# ==================== TAB 1: WHATSAPP INTERFACE ====================
with tab1:
    st.markdown(f"### {svg_icon('smartphone.svg', 'WhatsApp')}WhatsApp Customer Interface", unsafe_allow_html=True)
    st.write("Simulating real-time WhatsApp alerts and crowdsourced status updates sent to business owners.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Send Crowd Report")
        st.markdown(
            f"{svg_icon('utility-pole.svg', 'Power')} Power"
            f"&nbsp;&nbsp;&nbsp;{svg_icon('droplets.svg', 'Water')} Water",
            unsafe_allow_html=True,
        )
        status_type = st.radio("Report Status for your area:", ["Power OFF", "Power ON", "Water OFF", "Water ON"])
        
        if st.button("Submit WhatsApp Report"):
            st.success(f"Report logged for {selected_area}: '{status_type}'. Thank you for contributing to the crowd-data network!")
            st.toast("AI model recalculated local outage probability to 87%.")

    with col2:
        st.markdown("### Live WhatsApp Early Warning Feed")
        
        # WhatsApp Mock UI Box
        st.markdown("""
        <div style="background-color: #075E54; color: white; padding: 10px; border-radius: 10px 10px 0 0; font-weight: bold;">
            <img src="data:image/svg+xml;base64,""" + svg_icon("smartphone.svg", "WhatsApp", 18).split("base64,")[1].split('"')[0] + """" alt="WhatsApp" width="18" height="18" style="vertical-align: middle; margin-right: 0.35rem; filter: brightness(0) invert(1);"> UtilityPulse Bot (WhatsApp)
        </div>
        <div style="background-color: #E5DDD5; padding: 15px; border-radius: 0 0 10px 10px; font-family: sans-serif;">
            <div style="background-color: #DCF8C6; color: black; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                <b><img src="data:image/svg+xml;base64,""" + svg_icon("layers-arrow-down.svg", "Warning", 18).split("base64,")[1].split('"')[0] + """" alt="Warning" width="18" height="18" style="vertical-align: middle;"> OUTAGE WARNING ALERT</b><br>
                <b>Location:</b> Area 25, Lilongwe<br>
                <b>Risk Level:</b> HIGH (85% Probability)<br>
                <b>Expected Time:</b> ~25 Minutes (10:15 AM)<br>
                <b>Utility:</b> ESCOM Grid Supply<br><br>
                <i>Action Recommended: Switch bakery ovens to generator backup or complete current batch before 10:10 AM.</i>
            </div>
            <div style="background-color: #FFFFFF; color: black; padding: 10px; border-radius: 8px;">
                <b><img src="data:image/svg+xml;base64,""" + svg_icon("droplets.svg", "Water", 18).split("base64,")[1].split('"')[0] + """" alt="Water" width="18" height="18" style="vertical-align: middle;"> WATER SERVICE UPDATE</b><br>
                Water pressure restored in Area 25. Supply stability predicted for the next 12 hours.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 2: OUTAGE INTELLIGENCE ====================
with tab2:
    st.markdown(f"### {svg_icon('layout-dashboard.svg', 'Dashboard')}Outage Analytics & Predictions: {selected_area}", unsafe_allow_html=True)
    
    # Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Predicted Power Outage Risk", "85%", "High (+12%)", delta_color="inverse")
    m2.metric("Avg Outage Lead Warning", "28 Mins", "+3 mins accuracy")
    m3.metric("Water Supply Status", "Normal (ON)", "Stable")
    m4.metric("Estimated Losses Avoided", "MWK 145,000", "+MWK 20k this week")

    # Interactive Outage Probability Chart
    hours = [f"{h}:00" for h in range(8, 20)]
    probabilities = [15, 20, 25, 85, 90, 40, 10, 15, 70, 80, 30, 20]
    
    df_prob = pd.DataFrame({"Time": hours, "Outage Probability (%)": probabilities})
    
    fig = px.bar(df_prob, x="Time", y="Outage Probability (%)", title="Today's Power Outage Probability Forecast",
                 color="Outage Probability (%)", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 3: ENERGY USAGE MONITORING ====================
with tab3:
    st.markdown(f"### {svg_icon('utility-pole.svg', 'Power')}Premium Feature: Energy Usage Monitoring", unsafe_allow_html=True)
    st.caption("Real-time power consumption tracking for subscribed commercial accounts.")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Load profile graph
        times = [f"{i}:00" for i in range(24)]
        kw_usage = [1.2, 1.1, 1.0, 1.0, 1.2, 2.5, 5.4, 8.2, 9.1, 8.8, 8.5, 9.0, 8.7, 8.9, 9.2, 7.5, 6.0, 4.5, 3.2, 2.1, 1.8, 1.5, 1.3, 1.2]
        df_energy = pd.DataFrame({"Hour": times, "Consumption (kW)": kw_usage})
        
        fig_energy = px.line(df_energy, x="Hour", y="Consumption (kW)", title="Daily Power Consumption Profile (kW)", markers=True)
        st.plotly_chart(fig_energy, use_container_width=True)
        
    with col_b:
        st.markdown(f"### {svg_icon('layers-arrow-down.svg', 'Cost')}Cost Breakdown Today", unsafe_allow_html=True)
        st.write("**Grid Power (ESCOM):** MWK 18,400")
        st.write("**Generator Fuel:** MWK 32,000")
        st.write("**Solar / Battery Contribution:** 22%")
        
        st.markdown(f"{svg_icon('layers-arrow-down.svg', 'Efficiency')} AI efficiency recommendation", unsafe_allow_html=True)
        st.info("**AI Efficiency Tip:** Shifting heavy baking cycles from 11:00 AM to 7:00 AM will reduce peak generator reliance and save approx **MWK 45,000/week**.")
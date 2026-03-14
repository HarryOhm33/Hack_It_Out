import streamlit as st
import plotly.express as px
import numpy as np
from utils.helpers import safe_stat

def render_comparison_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]
    time_dim = ctx["time_dim"]
    lat_dim = ctx["lat_dim"]
    lon_dim = ctx["lon_dim"]
    all_years = ctx["all_years"]
    lat_vals = ctx["lat_vals"]
    lon_vals = ctx["lon_vals"]

    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
        return

    if not (time_dim and lat_dim and lon_dim):
        st.warning("Comparison view requires time, latitude, and longitude dimensions.")
        return

    if len(dataset[time_dim]) <= 1:
        st.info("This dataset contains only one time step. Comparison mode is not available.")
        return

    st.markdown("<div class='section-title'>Comparison Mode</div>", unsafe_allow_html=True)

    compare_col1, compare_col2 = st.columns(2)

    min_year = int(np.min(all_years))
    max_year = int(np.max(all_years))

    yearA = st.slider("Select Time A", min_year, max_year, min_year, key="comparison_yearA")
    yearB = st.slider(
        "Select Time B",
        min_year,
        max_year,
        min(max_year, min_year + 1),
        key="comparison_yearB"
    )

    timeA = np.argmin(np.abs(all_years - yearA))
    timeB = np.argmin(np.abs(all_years - yearB))

    sliceA = dataset[variable].isel({time_dim: timeA})
    sliceB = dataset[variable].isel({time_dim: timeB})

    with compare_col1:
        st.markdown(f"#### Map for {yearA}")
        figA = px.imshow(
            sliceA.values,
            x=lon_vals,
            y=lat_vals,
            origin="lower",
            color_continuous_scale="RdYlBu_r",
            labels={"x": "Longitude", "y": "Latitude", "color": variable},
            aspect="auto",
        )
        figA.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(figA, use_container_width=True)

    with compare_col2:
        st.markdown(f"#### Map for {yearB}")
        figB = px.imshow(
            sliceB.values,
            x=lon_vals,
            y=lat_vals,
            origin="lower",
            color_continuous_scale="RdYlBu_r",
            labels={"x": "Longitude", "y": "Latitude", "color": variable},
            aspect="auto",
        )
        figB.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(figB, use_container_width=True)

    st.markdown("<div class='section-title'>Difference Summary</div>", unsafe_allow_html=True)

    try:
        difference = sliceB.values.astype(float) - sliceA.values.astype(float)
        diff_mean = safe_stat(difference, "mean")
        diff_min = safe_stat(difference, "min")
        diff_max = safe_stat(difference, "max")

        d1, d2, d3 = st.columns(3)
        d1.metric("Average Change", diff_mean)
        d2.metric("Minimum Change", diff_min)
        d3.metric("Maximum Change", diff_max)
    except Exception:
        st.info("Difference summary could not be calculated.")

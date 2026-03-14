import streamlit as st
import plotly.express as px
import numpy as np
from utils.helpers import safe_stat, format_value

def render_dashboard_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]
    data_slice = ctx["data_slice"]
    selected_year = ctx["selected_year"]
    lat_dim = ctx["lat_dim"]
    lon_dim = ctx["lon_dim"]
    lat_vals = ctx["lat_vals"]
    lon_vals = ctx["lon_vals"]
    time_dim = ctx["time_dim"]

    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
        return

    st.markdown("<div class='section-title'>Dashboard Overview</div>", unsafe_allow_html=True)

    units = dataset[variable].attrs.get("units", "")
    mean_val = safe_stat(data_slice.values, "mean")
    min_val = safe_stat(data_slice.values, "min")
    max_val = safe_stat(data_slice.values, "max")

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{variable}</div><div class='metric-label'>Selected Variable</div></div>", unsafe_allow_html=True)

    with metric2:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{format_value(selected_year) if selected_year is not None else 'N/A'}</div><div class='metric-label'>Selected Time</div></div>", unsafe_allow_html=True)

    with metric3:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{mean_val}</div><div class='metric-label'>Average Value {f'({units})' if units else ''}</div></div>", unsafe_allow_html=True)

    with metric4:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{min_val} / {max_val}</div><div class='metric-label'>Min / Max</div></div>", unsafe_allow_html=True)

    if lat_dim and lon_dim:
        fig = px.imshow(
            data_slice.values,
            x=lon_vals,
            y=lat_vals,
            origin="lower",
            color_continuous_scale="RdYlBu_r",
            labels={"x": "Longitude", "y": "Latitude", "color": variable},
            aspect="auto",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig, use_container_width=True)

    if lat_dim and lon_dim and time_dim and len(dataset[time_dim]) > 1:
        lat_value = st.slider("Latitude", float(np.min(lat_vals)), float(np.max(lat_vals)), float(np.mean(lat_vals)))
        lon_value = st.slider("Longitude", float(np.min(lon_vals)), float(np.max(lon_vals)), float(np.mean(lon_vals)))

        lat_index = np.abs(lat_vals - lat_value).argmin()
        lon_index = np.abs(lon_vals - lon_value).argmin()

        timeseries = dataset[variable][:, lat_index, lon_index]

        trend_fig = px.line(
            x=dataset[time_dim].values,
            y=timeseries.values,
            markers=True,
            labels={"x": "Time", "y": variable},
        )
        trend_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(trend_fig, use_container_width=True)

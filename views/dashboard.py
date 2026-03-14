import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
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
    all_years = ctx["all_years"]

    if dataset is None or variable is None:
        st.warning("⚠️ Please select a variable from the sidebar to view the dashboard.")
        return

    # Page header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                📊 Climate Dashboard
            </h1>
            <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
                Real-time insights and visualizations of your climate data
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key metrics in a grid
    units = dataset[variable].attrs.get("units", "")
    mean_val = safe_stat(data_slice.values, "mean")
    min_val = safe_stat(data_slice.values, "min")
    max_val = safe_stat(data_slice.values, "max")
    std_val = safe_stat(data_slice.values, "std")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Variable", variable, help="Selected climate variable")

    with col2:
        time_label = format_value(selected_year) if selected_year is not None else "N/A"
        if all_years is not None and len(all_years) > 1:
            delta = f"{len(all_years)} time steps"
        else:
            delta = None
        st.metric("Time Period", time_label, delta=delta, help="Current time slice")

    with col3:
        st.metric(
            f"Average ({units})" if units else "Average",
            mean_val,
            delta=None,
            help="Mean value across spatial domain",
        )

    with col4:
        st.metric(
            "Range",
            f"{min_val} / {max_val}",
            delta=f"σ={std_val}" if std_val != "N/A" else None,
            help="Min / Max values",
        )

    st.markdown("---")

    # Main visualization area
    if lat_dim and lon_dim:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Spatial map
            fig_map = px.imshow(
                data_slice.values,
                x=lon_vals,
                y=lat_vals,
                origin="lower",
                color_continuous_scale="RdYlBu_r",
                labels={"x": "Longitude", "y": "Latitude", "color": variable},
                aspect="auto",
                title=f"Spatial Distribution of {variable}",
            )

            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black"),
                title=dict(font=dict(size=16), x=0.5),
                coloraxis_colorbar=dict(
                    title=units if units else variable,
                ),
                height=500,
            )

            st.plotly_chart(fig_map, use_container_width=True)

        with col2:
            # Quick stats card
            st.markdown(
                """
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1); height: fit-content;">
                    <h4 style="margin-top: 0;">📈 Quick Statistics</h4>
                """,
                unsafe_allow_html=True,
            )

            valid_data = data_slice.values[~np.isnan(data_slice.values)]
            if len(valid_data) > 0:
                percentiles = np.percentile(valid_data, [25, 50, 75])

                st.metric("25th Percentile", format_value(percentiles[0]))
                st.metric("Median (50th)", format_value(percentiles[1]))
                st.metric("75th Percentile", format_value(percentiles[2]))
                st.metric("Valid Data Points", f"{len(valid_data):,}")
                st.metric("Missing Values", f"{np.isnan(data_slice.values).sum():,}")

            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("ℹ️ Spatial visualization requires latitude and longitude dimensions.")

    # Time series section
    if lat_dim and lon_dim and time_dim and len(dataset[time_dim]) > 1:
        st.markdown("---")
        st.markdown("#### 📈 Time Series Analysis")

        col1, col2 = st.columns([1, 1])

        with col1:
            lat_value = st.slider(
                "Select latitude for time series",
                float(np.min(lat_vals)),
                float(np.max(lat_vals)),
                float(np.mean(lat_vals)),
                step=0.5,
                key="dash_lat",
                format="%.1f°",
            )

        with col2:
            lon_value = st.slider(
                "Select longitude for time series",
                float(np.min(lon_vals)),
                float(np.max(lon_vals)),
                float(np.mean(lon_vals)),
                step=0.5,
                key="dash_lon",
                format="%.1f°",
            )

        lat_index = np.abs(lat_vals - lat_value).argmin()
        lon_index = np.abs(lon_vals - lon_value).argmin()

        timeseries = dataset[variable][:, lat_index, lon_index]
        years = all_years if all_years is not None else np.arange(len(timeseries))

        # Calculate trend
        z = np.polyfit(years, timeseries.values, 1)

        fig_trend = go.Figure()

        # Add time series line
        fig_trend.add_trace(
            go.Scatter(
                x=years,
                y=timeseries.values,
                mode="lines+markers",
                name="Observations",
                line=dict(color="#00c6fb", width=2),
                marker=dict(size=4),
            )
        )

        # Add trend line
        fig_trend.add_trace(
            go.Scatter(
                x=years,
                y=np.poly1d(z)(years),
                mode="lines",
                name=f"Trend (slope: {z[0]:.3f}/year)",
                line=dict(color="#ff6b6b", width=2, dash="dash"),
            )
        )

        fig_trend.update_layout(
            title=f"Time Series at {lat_value:.1f}°N, {lon_value:.1f}°E",
            xaxis_title="Year",
            yaxis_title=f"{variable} {units}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="black"),
            hovermode="x unified",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            height=400,
        )

        st.plotly_chart(fig_trend, use_container_width=True)

        # Trend statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Mean Value", format_value(np.mean(timeseries.values)))

        with col2:
            st.metric("Trend Slope", f"{z[0]:.3f}/year")

        with col3:
            st.metric("Volatility", format_value(np.std(timeseries.values)))

        with col4:
            change = timeseries.values[-1] - timeseries.values[0]
            st.metric("Total Change", format_value(change))

    # Additional insights
    st.markdown("---")
    with st.expander("🔍 Data Insights & Interpretation", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div style="background: rgba(0, 198, 251, 0.1); padding: 1rem; border-radius: 0.5rem;">
                    <h5 style="margin: 0 0 0.5rem 0;">🎯 Key Findings</h5>
                    <ul style="margin: 0; padding-left: 1.2rem;">
                """,
                unsafe_allow_html=True,
            )

            insights = []
            if mean_val != "N/A":
                insights.append(f"Average {variable} is {mean_val} {units}")
            if std_val != "N/A":
                insights.append(f"Values typically vary by ±{std_val} {units}")
            if lat_dim and lon_dim:
                insights.append("Spatial patterns show regional variations")
            if time_dim and len(dataset[time_dim]) > 1:
                insights.append(
                    f"Time series spans {len(dataset[time_dim])} time steps"
                )

            for insight in insights:
                st.markdown(f"<li>{insight}</li>", unsafe_allow_html=True)

            st.markdown("</ul></div>", unsafe_allow_html=True)

        with col2:
            st.markdown(
                """
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1rem; border-radius: 0.5rem;">
                    <h5 style="margin: 0 0 0.5rem 0;">📌 Recommendations</h5>
                    <ul style="margin: 0; padding-left: 1.2rem;">
                        <li>Use Dataset Explorer for detailed variable information</li>
                        <li>Try Story Mode for guided analysis</li>
                        <li>Compare different time periods in Comparison view</li>
                        <li>Explore 3D Globe for immersive visualization</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

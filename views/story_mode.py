import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from utils.helpers import safe_stat, format_value


def render_story_mode_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]
    data_slice = ctx["data_slice"]
    time_dim = ctx["time_dim"]
    lat_dim = ctx["lat_dim"]
    lon_dim = ctx["lon_dim"]
    all_years = ctx["all_years"]
    lat_vals = ctx["lat_vals"]
    lon_vals = ctx["lon_vals"]

    if dataset is None or variable is None:
        st.warning("⚠️ Please select a variable from the sidebar to begin your story.")
        return

    # Page header with storytelling theme
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                📖 Story Mode
            </h1>
            <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
                Follow a guided narrative to understand climate patterns and their significance
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Story progress indicator
    steps = [
        "Dataset Overview",
        "Spatial Pattern",
        "Local Trend",
        "Climate Comparison",
    ]

    current_step = st.selectbox(
        "Choose your story chapter",
        [f"Step {i+1}: {step}" for i, step in enumerate(steps)],
        key="story_step",
    )

    step_index = int(current_step.split(":")[0].replace("Step ", "")) - 1

    # Progress bar
    progress = (step_index + 1) / len(steps)
    st.progress(progress, text=f"Chapter {step_index + 1} of {len(steps)}")

    st.markdown("---")

    if "Step 1" in current_step:
        # Dataset Overview with engaging narrative
        st.markdown(
            """
            <div style="background: rgba(0, 198, 251, 0.1); padding: 1.5rem; border-radius: 1rem; 
                border-left: 4px solid #00c6fb; margin-bottom: 2rem;">
                <h3 style="margin: 0 0 0.5rem 0;">📊 Chapter 1: Understanding Your Dataset</h3>
                <p style="margin: 0; opacity: 0.9;">
                    Every climate story begins with data. Let's explore what this dataset contains and why it matters.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1);">
                    <h4>📋 Dataset Profile</h4>
                    <p><b>Variable:</b> {variable}</p>
                    <p><b>Time Range:</b> {int(np.min(all_years)) if all_years is not None else 'N/A'} - {int(np.max(all_years)) if all_years is not None else 'N/A'}</p>
                    <p><b>Spatial Coverage:</b> {len(lat_vals)}°N to {len(lon_vals)}°E</p>
                    <p><b>Resolution:</b> {len(lat_vals)} x {len(lon_vals)} grid points</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            # Quick stats
            valid_data = data_slice.values[~np.isnan(data_slice.values)]
            if len(valid_data) > 0:
                st.markdown(
                    f"""
                    <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                        border: 1px solid rgba(128, 128, 128, 0.1);">
                        <h4>📈 Key Statistics</h4>
                        <p><b>Mean:</b> {format_value(np.mean(valid_data))}</p>
                        <p><b>Std Dev:</b> {format_value(np.std(valid_data))}</p>
                        <p><b>Range:</b> {format_value(np.min(valid_data))} - {format_value(np.max(valid_data))}</p>
                        <p><b>Valid Points:</b> {len(valid_data):,}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.03); padding: 1.5rem; border-radius: 1rem; margin-top: 1rem;">
                <h4>🔍 What This Tells Us</h4>
                <p style="opacity: 0.9;">
                    This dataset provides a window into {variable} patterns across {years} years of observations.
                    By analyzing these patterns, we can identify climate trends, anomalies, and long-term changes.
                </p>
            </div>
            """.format(
                variable=variable, years=len(all_years) if all_years is not None else 0
            ),
            unsafe_allow_html=True,
        )

    elif "Step 2" in current_step:
        # Spatial Pattern with storytelling
        st.markdown(
            """
            <div style="background: rgba(0, 198, 251, 0.1); padding: 1.5rem; border-radius: 1rem; 
                border-left: 4px solid #00c6fb; margin-bottom: 2rem;">
                <h3 style="margin: 0 0 0.5rem 0;">🗺️ Chapter 2: The Global Picture</h3>
                <p style="margin: 0; opacity: 0.9;">
                    Climate doesn't look the same everywhere. Let's explore how {variable} varies across the globe.
                </p>
            </div>
            """.format(
                variable=variable
            ),
            unsafe_allow_html=True,
        )

        if lat_dim and lon_dim:
            # Time selector for spatial pattern
            if time_dim and len(dataset[time_dim]) > 1:
                year_idx = st.slider(
                    "Select time slice to visualize:",
                    0,
                    len(dataset[time_dim]) - 1,
                    len(dataset[time_dim]) // 2,
                    key="story_time_slice",
                )
                display_data = dataset[variable].isel({time_dim: year_idx})
                year_display = (
                    f" ({int(all_years[year_idx])})" if all_years is not None else ""
                )
            else:
                display_data = data_slice
                year_display = ""

            fig = px.imshow(
                display_data.values,
                x=lon_vals,
                y=lat_vals,
                origin="lower",
                color_continuous_scale="RdYlBu_r",
                aspect="auto",
                title=f"Global Distribution of {variable}{year_display}",
                labels={"x": "Longitude", "y": "Latitude", "color": variable},
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black"),
                title=dict(font=dict(size=16)),
                coloraxis_colorbar=dict(
                    title=variable,
                ),
            )

            st.plotly_chart(fig, use_container_width=True)

            # Interpretation guide
            with st.expander("📖 Understanding This Visualization", expanded=True):
                st.markdown(
                    """
                    <p>
                        <b>What to look for:</b>
                        <ul>
                            <li><span style="color: #FF6B6B;">Red areas</span> indicate higher values</li>
                            <li><span style="color: #4ECDC4;">Blue areas</span> indicate lower values</li>
                            <li>Notice the patterns across continents and oceans</li>
                        </ul>
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info(
                "ℹ️ Spatial visualization requires latitude and longitude dimensions."
            )

    elif "Step 3" in current_step:
        # Local Trend with narrative
        st.markdown(
            """
            <div style="background: rgba(0, 198, 251, 0.1); padding: 1.5rem; border-radius: 1rem; 
                border-left: 4px solid #00c6fb; margin-bottom: 2rem;">
                <h3 style="margin: 0 0 0.5rem 0;">📈 Chapter 3: A Closer Look</h3>
                <p style="margin: 0; opacity: 0.9;">
                    Let's zoom into a specific location and see how it changes through time.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if lat_dim and lon_dim and time_dim and len(dataset[time_dim]) > 1:
            col1, col2 = st.columns(2)

            with col1:
                lat_value = st.slider(
                    "📍 Select latitude",
                    float(np.min(lat_vals)),
                    float(np.max(lat_vals)),
                    float(np.mean(lat_vals)),
                    step=0.5,
                    key="story_lat",
                    format="%.1f°",
                )

            with col2:
                lon_value = st.slider(
                    "📍 Select longitude",
                    float(np.min(lon_vals)),
                    float(np.max(lon_vals)),
                    float(np.mean(lon_vals)),
                    step=0.5,
                    key="story_lon",
                    format="%.1f°",
                )

            lat_index = np.abs(lat_vals - lat_value).argmin()
            lon_index = np.abs(lon_vals - lon_value).argmin()
            timeseries = dataset[variable][:, lat_index, lon_index]

            # Trend analysis
            years = all_years if all_years is not None else np.arange(len(timeseries))

            # Calculate trend line
            z = np.polyfit(years, timeseries.values, 1)
            trend_line = np.poly1d(z)(years)
            trend_direction = "increasing" if z[0] > 0 else "decreasing"

            fig = px.scatter(
                x=years,
                y=timeseries.values,
                trendline="ols",
                labels={"x": "Year", "y": variable},
                title=f"Time Series at {lat_value:.1f}°N, {lon_value:.1f}°E",
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black"),
                title=dict(font=dict(size=16)),
                hovermode="x unified",
            )

            st.plotly_chart(fig, use_container_width=True)

            # Story interpretation
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average Value",
                    format_value(np.mean(timeseries.values)),
                    delta=None,
                )

            with col2:
                st.metric("Trend", f"{abs(z[0]):.3f}/year", delta=f"{trend_direction}")

            with col3:
                change = timeseries.values[-1] - timeseries.values[0]
                st.metric(
                    "Total Change", format_value(change), delta=format_value(change)
                )

            st.markdown(
                f"""
                <div style="background: rgba(255, 255, 255, 0.03); padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                    <p style="margin: 0;">
                        <b>📝 Story Note:</b> Over the observed period, this location shows a 
                        <span style="color: {'#FF6B6B' if z[0] > 0 else '#4ECDC4'}; font-weight: bold;">{trend_direction}</span> 
                        trend of {abs(z[0]):.3f} units per year. This suggests 
                        {'warming' if 'temperature' in variable.lower() else 'increasing'} conditions 
                        at this location.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info(
                "ℹ️ Time series analysis requires time, latitude, and longitude dimensions."
            )

    elif "Step 4" in current_step:
        # Climate Comparison with narrative
        st.markdown(
            """
            <div style="background: rgba(0, 198, 251, 0.1); padding: 1.5rem; border-radius: 1rem; 
                border-left: 4px solid #00c6fb; margin-bottom: 2rem;">
                <h3 style="margin: 0 0 0.5rem 0;">🔄 Chapter 4: Then and Now</h3>
                <p style="margin: 0; opacity: 0.9;">
                    Compare two different time periods to see how our climate has evolved.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if time_dim and lat_dim and lon_dim and len(dataset[time_dim]) > 1:
            min_year = int(np.min(all_years))
            max_year = int(np.max(all_years))

            col1, col2 = st.columns(2)

            with col1:
                yearA = st.selectbox(
                    "📅 Select first year",
                    list(range(min_year, max_year + 1)),
                    index=0,
                    key="story_yearA",
                )

            with col2:
                yearB = st.selectbox(
                    "📅 Select second year",
                    list(range(min_year, max_year + 1)),
                    index=min(len(all_years) - 1, 1),
                    key="story_yearB",
                )

            timeA = np.argmin(np.abs(all_years - yearA))
            timeB = np.argmin(np.abs(all_years - yearB))

            sliceA = dataset[variable].isel({time_dim: timeA})
            sliceB = dataset[variable].isel({time_dim: timeB})

            # Calculate difference
            difference = sliceB.values - sliceA.values

            tab1, tab2, tab3 = st.tabs(
                ["🗺️ First Period", "🗺️ Second Period", "📊 Comparison"]
            )

            with tab1:
                figA = px.imshow(
                    sliceA.values,
                    x=lon_vals,
                    y=lat_vals,
                    origin="lower",
                    color_continuous_scale="RdYlBu_r",
                    aspect="auto",
                    title=f"{yearA}",
                )
                figA.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="black"),
                )
                st.plotly_chart(figA, use_container_width=True)

            with tab2:
                figB = px.imshow(
                    sliceB.values,
                    x=lon_vals,
                    y=lat_vals,
                    origin="lower",
                    color_continuous_scale="RdYlBu_r",
                    aspect="auto",
                    title=f"{yearB}",
                )
                figB.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="black"),
                )
                st.plotly_chart(figB, use_container_width=True)

            with tab3:
                fig_diff = px.imshow(
                    difference,
                    x=lon_vals,
                    y=lat_vals,
                    origin="lower",
                    color_continuous_scale="RdBu",
                    aspect="auto",
                    title=f"Difference ({yearB} - {yearA})",
                )
                fig_diff.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="black"),
                )
                st.plotly_chart(fig_diff, use_container_width=True)

            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    f"Mean ({yearA})", format_value(safe_stat(sliceA.values, "mean"))
                )
            with col2:
                st.metric(
                    f"Mean ({yearB})", format_value(safe_stat(sliceB.values, "mean"))
                )
            with col3:
                mean_diff = safe_stat(difference, "mean")
                st.metric("Mean Difference", format_value(mean_diff))
            with col4:
                max_diff = safe_stat(difference, "max")
                st.metric("Max Change", format_value(max_diff))

            # Story conclusion
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, rgba(0,198,251,0.1), rgba(0,91,234,0.1)); 
                    padding: 1.5rem; border-radius: 1rem; margin-top: 2rem;">
                    <h4 style="margin: 0 0 0.5rem 0;">🎯 Key Takeaway</h4>
                    <p style="margin: 0; opacity: 0.9;">
                        The comparison reveals significant changes in {variable} patterns over time. 
                        Understanding these shifts helps us predict future climate scenarios and their potential impacts.
                    </p>
                </div>
                """.format(
                    variable=variable
                ),
                unsafe_allow_html=True,
            )
        else:
            st.info("ℹ️ Comparison requires time, latitude, and longitude dimensions.")

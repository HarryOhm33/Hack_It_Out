import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils.helpers import safe_stat, format_value


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
        st.warning("⚠️ Please select a variable from the sidebar to enable comparison.")
        return

    if not (time_dim and lat_dim and lon_dim):
        st.warning(
            "⚠️ Comparison view requires time, latitude, and longitude dimensions."
        )
        return

    if len(dataset[time_dim]) <= 1:
        st.info(
            "ℹ️ This dataset contains only one time step. Comparison mode is not available."
        )
        return

    # Page header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                🔄 Time Comparison
            </h1>
            <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
                Compare climate patterns across different time periods to detect changes and trends
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    min_year = int(np.min(all_years))
    max_year = int(np.max(all_years))

    # Year selection with better UI
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📅 First Period")
        yearA = st.slider(
            "Select first year",
            min_year,
            max_year,
            min_year,
            key="comparison_yearA",
            format="%d",
        )

    with col2:
        st.markdown("#### 📅 Second Period")
        yearB = st.slider(
            "Select second year",
            min_year,
            max_year,
            min(max_year, min_year + (max_year - min_year) // 2),
            key="comparison_yearB",
            format="%d",
        )

    timeA = np.argmin(np.abs(all_years - yearA))
    timeB = np.argmin(np.abs(all_years - yearB))

    sliceA = dataset[variable].isel({time_dim: timeA})
    sliceB = dataset[variable].isel({time_dim: timeB})

    # Create tabs for different comparison views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🗺️ Side by Side", "📊 Difference Map", "📈 Statistics", "📋 Data Table"]
    )

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            figA = px.imshow(
                sliceA.values,
                x=lon_vals,
                y=lat_vals,
                origin="lower",
                color_continuous_scale="RdYlBu_r",
                labels={"x": "Longitude", "y": "Latitude", "color": variable},
                aspect="auto",
                title=f"{variable} - {yearA}",
            )
            figA.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black"),
                title=dict(font=dict(size=14)),
                height=400,
            )
            st.plotly_chart(figA, use_container_width=True, key="comparison_figA")

        with col2:
            figB = px.imshow(
                sliceB.values,
                x=lon_vals,
                y=lat_vals,
                origin="lower",
                color_continuous_scale="RdYlBu_r",
                labels={"x": "Longitude", "y": "Latitude", "color": variable},
                aspect="auto",
                title=f"{variable} - {yearB}",
            )
            figB.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black"),
                title=dict(font=dict(size=14)),
                height=400,
            )
            st.plotly_chart(figB, use_container_width=True, key="comparison_figB")

    with tab2:
        # Calculate difference
        difference = sliceB.values.astype(float) - sliceA.values.astype(float)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig_diff = px.imshow(
                difference,
                x=lon_vals,
                y=lat_vals,
                origin="lower",
                color_continuous_scale="RdBu",
                labels={"x": "Longitude", "y": "Latitude", "color": "Difference"},
                aspect="auto",
                title=f"Difference ({yearB} - {yearA})",
            )
            fig_diff.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black"),
                height=500,
            )
            st.plotly_chart(fig_diff, use_container_width=True, key="comparison_diff")

        with col2:
            st.markdown(
                """
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1);">
                    <h4 style="margin-top: 0;">📊 Difference Stats</h4>
                """,
                unsafe_allow_html=True,
            )

            diff_mean = safe_stat(difference, "mean")
            diff_std = safe_stat(difference, "std")
            diff_min = safe_stat(difference, "min")
            diff_max = safe_stat(difference, "max")

            st.metric("Mean Change", format_value(diff_mean))
            st.metric("Standard Deviation", format_value(diff_std))
            st.metric("Minimum Change", format_value(diff_min))
            st.metric("Maximum Change", format_value(diff_max))

            # Color interpretation
            if diff_mean > 0:
                st.info(f"📈 Overall increase of {format_value(diff_mean)}")
            elif diff_mean < 0:
                st.warning(f"📉 Overall decrease of {format_value(abs(diff_mean))}")
            else:
                st.success("📊 No significant overall change")

            st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        # Statistical comparison
        col1, col2, col3 = st.columns(3)

        statsA = {
            "Mean": safe_stat(sliceA.values, "mean"),
            "Median": safe_stat(sliceA.values, "median"),
            "Std Dev": safe_stat(sliceA.values, "std"),
            "Min": safe_stat(sliceA.values, "min"),
            "Max": safe_stat(sliceA.values, "max"),
            "Range": (
                (safe_stat(sliceA.values, "max") - safe_stat(sliceA.values, "min"))
                if isinstance(safe_stat(sliceA.values, "max"), (int, float))
                and isinstance(safe_stat(sliceA.values, "min"), (int, float))
                else "N/A"
            ),
        }

        statsB = {
            "Mean": safe_stat(sliceB.values, "mean"),
            "Median": safe_stat(sliceB.values, "median"),
            "Std Dev": safe_stat(sliceB.values, "std"),
            "Min": safe_stat(sliceB.values, "min"),
            "Max": safe_stat(sliceB.values, "max"),
            "Range": (
                (safe_stat(sliceB.values, "max") - safe_stat(sliceB.values, "min"))
                if isinstance(safe_stat(sliceB.values, "max"), (int, float))
                and isinstance(safe_stat(sliceB.values, "min"), (int, float))
                else "N/A"
            ),
        }

        # Create comparison dataframe
        def safe_subtract(b_val, a_val):
            if isinstance(b_val, (int, float, np.integer, np.floating)) and isinstance(
                a_val, (int, float, np.integer, np.floating)
            ):
                return b_val - a_val
            return "N/A"

        comparison_df = pd.DataFrame(
            {
                "Statistic": statsA.keys(),
                f"{yearA}": [format_value(v) for v in statsA.values()],
                f"{yearB}": [format_value(v) for v in statsB.values()],
                "Change": [
                    format_value(safe_subtract(statsB[k], statsA[k]))
                    for k in statsA.keys()
                ],
            }
        )

        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        # Histogram comparison
        fig_hist = go.Figure()

        fig_hist.add_trace(
            go.Histogram(
                x=sliceA.values.flatten()[~np.isnan(sliceA.values.flatten())],
                name=str(yearA),
                opacity=0.7,
                nbinsx=30,
            )
        )

        fig_hist.add_trace(
            go.Histogram(
                x=sliceB.values.flatten()[~np.isnan(sliceB.values.flatten())],
                name=str(yearB),
                opacity=0.7,
                nbinsx=30,
            )
        )

        fig_hist.update_layout(
            title="Value Distribution Comparison",
            xaxis_title=variable,
            yaxis_title="Frequency",
            barmode="overlay",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="black"),
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        )

        st.plotly_chart(fig_hist, use_container_width=True, key="comparison_hist")

    with tab4:
        # Data table view
        st.markdown(f"#### Sample Data: {yearA} vs {yearB}")

        # Create sample data table
        sample_size = min(100, len(lat_vals) * len(lon_vals))
        lat_indices = np.random.choice(
            len(lat_vals), size=int(np.sqrt(sample_size)), replace=False
        )
        lon_indices = np.random.choice(
            len(lon_vals), size=int(np.sqrt(sample_size)), replace=False
        )

        data_rows = []
        for lat_idx in lat_indices:
            for lon_idx in lon_indices:
                data_rows.append(
                    {
                        "Latitude": round(float(lat_vals[lat_idx]), 2),
                        "Longitude": round(float(lon_vals[lon_idx]), 2),
                        f"{yearA}": round(float(sliceA.values[lat_idx, lon_idx]), 3),
                        f"{yearB}": round(float(sliceB.values[lat_idx, lon_idx]), 3),
                        "Difference": round(
                            float(
                                sliceB.values[lat_idx, lon_idx]
                                - sliceA.values[lat_idx, lon_idx]
                            ),
                            3,
                        ),
                    }
                )

        st.dataframe(pd.DataFrame(data_rows), use_container_width=True, hide_index=True)

        # Download option
        csv = pd.DataFrame(data_rows).to_csv(index=False)
        st.download_button(
            label="📥 Download Comparison Data (CSV)",
            data=csv,
            file_name=f"comparison_{yearA}_{yearB}.csv",
            mime="text/csv",
        )

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.helpers import safe_stat, format_value


def render_globe_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]
    data_slice = ctx["data_slice"]
    lat_dim = ctx["lat_dim"]
    lon_dim = ctx["lon_dim"]
    lat_vals = ctx["lat_vals"]
    lon_vals = ctx["lon_vals"]

    if dataset is None or variable is None:
        st.warning("⚠️ Please select a variable from the sidebar to view the 3D globe.")
        return

    if not (lat_dim and lon_dim):
        st.warning("⚠️ 3D globe view requires latitude and longitude dimensions.")
        return

    # Page header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                🌍 3D Globe Visualization
            </h1>
            <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
                Explore climate data on an interactive 3D globe
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Controls
    col1, col2, col3 = st.columns(3)

    with col1:
        point_density = st.slider(
            "Point Density",
            min_value=10,
            max_value=100,
            value=50,
            step=5,
            help="Higher density shows more data points but may be slower",
        )

    with col2:
        point_size = st.slider("Point Size", min_value=2, max_value=15, value=6, step=1)

    with col3:
        opacity = st.slider(
            "Opacity", min_value=0.1, max_value=1.0, value=0.8, step=0.1, format="%.1f"
        )

    try:
        globe_data = np.array(data_slice.values, dtype=float)

        # Calculate sampling based on density
        step_lat = max(1, len(lat_vals) // (point_density // 2))
        step_lon = max(1, len(lon_vals) // point_density)

        sampled_lat = lat_vals[::step_lat]
        sampled_lon = lon_vals[::step_lon]
        sampled_data = globe_data[::step_lat, ::step_lon]

        lon_grid, lat_grid = np.meshgrid(sampled_lon, sampled_lat)

        lat_flat = lat_grid.flatten()
        lon_flat = lon_grid.flatten()
        val_flat = sampled_data.flatten()

        # Remove NaN values
        valid_mask = np.isfinite(val_flat)
        lat_flat = lat_flat[valid_mask]
        lon_flat = lon_flat[valid_mask]
        val_flat = val_flat[valid_mask]

        if len(val_flat) == 0:
            st.info("ℹ️ No valid data available for globe rendering.")
            return

        # Create 3D globe visualization
        fig = go.Figure()

        fig.add_trace(
            go.Scattergeo(
                lon=lon_flat,
                lat=lat_flat,
                text=[f"{variable}: {format_value(v)}" for v in val_flat],
                mode="markers",
                marker=dict(
                    size=point_size,
                    color=val_flat,
                    colorscale="RdYlBu_r",
                    colorbar=dict(title=variable, thickness=20, len=0.8),
                    opacity=opacity,
                    line=dict(width=0),
                    showscale=True,
                ),
                hovertemplate=(
                    "<b>Latitude:</b> %{lat:.2f}°<br>"
                    "<b>Longitude:</b> %{lon:.2f}°<br>"
                    "<b>Value:</b> %{marker.color:.3f}<br>"
                    "<extra></extra>"
                ),
                name=variable,
            )
        )

        # Update globe projection and appearance
        fig.update_geos(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(50, 70, 90)",
            showocean=True,
            oceancolor="rgb(10, 20, 40)",
            showcountries=True,
            countrycolor="rgba(255,255,255,0.3)",
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.5)",
            showlakes=False,
            showrivers=False,
            bgcolor="rgba(0,0,0,0)",
            lonaxis=dict(range=[-180, 180]),
            lataxis=dict(range=[-90, 90]),
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="black", size=12),
            margin=dict(l=50, r=50, t=80, b=60),
            autosize=True,
            height=700,
            title=dict(
                text=f"{variable} Distribution on 3D Globe", x=0.5, font=dict(size=18)
            ),
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)", font_size=12, font_color="white"
            ),
        )

        st.plotly_chart(fig, use_container_width=True)

        # Statistics and information
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rendered Points", f"{len(val_flat):,}")

        with col2:
            st.metric("Minimum", format_value(float(np.min(val_flat))))

        with col3:
            st.metric("Maximum", format_value(float(np.max(val_flat))))

        with col4:
            st.metric(
                "Coverage",
                f"{(len(val_flat) / (len(lat_vals) * len(lon_vals)) * 100):.1f}%",
            )

        # Interaction guide
        with st.expander("ℹ️ How to use the 3D Globe", expanded=False):
            st.markdown(
                """
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1rem; border-radius: 0.5rem;">
                    <h5 style="margin: 0 0 0.5rem 0;">🖱️ Interaction Guide</h5>
                    <ul style="margin: 0; padding-left: 1.2rem;">
                        <li><b>Drag</b> - Rotate the globe</li>
                        <li><b>Scroll</b> - Zoom in/out</li>
                        <li><b>Double click</b> - Reset view</li>
                        <li><b>Hover</b> - See exact values at points</li>
                        <li><b>Color bar</b> - Shows value range</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.8;">
                        The globe shows {:,} data points sampled from your dataset.
                        Higher density settings show more detail but may be slower to render.
                    </p>
                </div>
                """.format(
                    len(val_flat)
                ),
                unsafe_allow_html=True,
            )

        # Additional options
        with st.expander("⚙️ Advanced Options", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                show_land = st.checkbox("Show Land", value=True)
                show_ocean = st.checkbox("Show Ocean", value=True)
                show_countries = st.checkbox("Show Countries", value=True)

            with col2:
                show_coastlines = st.checkbox("Show Coastlines", value=True)
                projection = st.selectbox(
                    "Projection",
                    ["orthographic", "natural earth", "mercator", "equirectangular"],
                )

            # Update figure with new options
            if not (
                show_land
                and show_ocean
                and show_countries
                and show_coastlines
                and projection == "orthographic"
            ):
                fig.update_geos(
                    projection_type=projection,
                    showland=show_land,
                    showocean=show_ocean,
                    showcountries=show_countries,
                    showcoastlines=show_coastlines,
                )
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Unable to render 3D globe: {str(e)}")
        st.info(
            "Try reducing the point density or check if your data contains valid values."
        )

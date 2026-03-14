import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render_globe_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]
    data_slice = ctx["data_slice"]
    lat_dim = ctx["lat_dim"]
    lon_dim = ctx["lon_dim"]
    lat_vals = ctx["lat_vals"]
    lon_vals = ctx["lon_vals"]

    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
        return

    if not (lat_dim and lon_dim):
        st.warning("3D globe view requires latitude and longitude dimensions.")
        return

    st.markdown("<div class='section-title'>3D Globe Visualization</div>", unsafe_allow_html=True)

    try:
        globe_data = np.array(data_slice.values, dtype=float)

        step_lat = max(1, len(lat_vals) // 45)
        step_lon = max(1, len(lon_vals) // 60)

        sampled_lat = lat_vals[::step_lat]
        sampled_lon = lon_vals[::step_lon]
        sampled_data = globe_data[::step_lat, ::step_lon]

        lon_grid, lat_grid = np.meshgrid(sampled_lon, sampled_lat)

        lat_flat = lat_grid.flatten()
        lon_flat = lon_grid.flatten()
        val_flat = sampled_data.flatten()

        valid_mask = np.isfinite(val_flat)
        lat_flat = lat_flat[valid_mask]
        lon_flat = lon_flat[valid_mask]
        val_flat = val_flat[valid_mask]

        if len(val_flat) == 0:
            st.info("No valid data available for globe rendering.")
            return

        fig = go.Figure()

        fig.add_trace(
            go.Scattergeo(
                lon=lon_flat,
                lat=lat_flat,
                text=[f"{variable}: {round(v, 3)}" for v in val_flat],
                mode="markers",
                marker=dict(
                    size=6,
                    color=val_flat,
                    colorscale="RdYlBu_r",
                    colorbar=dict(title=variable),
                    opacity=0.85,
                    line=dict(width=0),
                ),
                hovertemplate=(
                    "<b>Latitude:</b> %{lat}<br>"
                    "<b>Longitude:</b> %{lon}<br>"
                    "<b>Value:</b> %{marker.color:.3f}<extra></extra>"
                ),
            )
        )

        fig.update_geos(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(20, 30, 50)",
            showocean=True,
            oceancolor="rgb(5, 10, 20)",
            showcountries=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.18)",
            showlakes=False,
            showrivers=False,
            bgcolor="rgba(0,0,0,0)",
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=700,
        )

        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Rendered Points", len(val_flat))
        c2.metric("Minimum", round(float(np.min(val_flat)), 3))
        c3.metric("Maximum", round(float(np.max(val_flat)), 3))

        st.info("Tip: drag the globe to rotate and scroll to zoom.")

    except Exception as e:
        st.error(f"Unable to render 3D globe: {e}")

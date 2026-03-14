import streamlit as st
import xarray as xr
import tempfile
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    """
    <div style="background:#4f86c6;padding:15px;border-radius:5px">
    <h1 style="color:white;text-align:center;">Climate  Data Explorer</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# UPLOAD DATASET PANEL
# -----------------------------

st.markdown("### Upload Dataset")

uploaded_file = st.file_uploader("Upload NetCDF (.nc) File", type=["nc"])

if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    dataset = xr.open_dataset(tmp_path)

    # -----------------------------
    # CONTROL PANEL
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Select Variable")

        variable = st.selectbox("Choose a variable", list(dataset.data_vars))

    dims = dataset[variable].dims

    time_dim = None
    lat_dim = None
    lon_dim = None

    for d in dims:
        if "time" in d.lower():
            time_dim = d
        if "lat" in d.lower():
            lat_dim = d
        if "lon" in d.lower():
            lon_dim = d

    with col2:

        st.markdown("### Select Time Period")

        if time_dim:

            time_vals = dataset[time_dim].values

            if len(time_vals) > 1:

                time_index = st.select_slider(
                    "Select time", options=list(range(len(time_vals))), value=0
                )

            else:

                time_index = 0
                st.info("Dataset contains only one time step")

    # -----------------------------
    # DATA SLICE
    # -----------------------------

    if time_dim:
        data_slice = dataset[variable].isel({time_dim: time_index})
    else:
        data_slice = dataset[variable]

    # -----------------------------
    # GLOBAL MAP
    # -----------------------------

    st.markdown(f"### Global {variable.upper()} Map")

    if lat_dim and lon_dim:

        lat_vals = dataset[lat_dim].values
        lon_vals = dataset[lon_dim].values

        fig = px.imshow(
            data_slice.values,
            x=lon_vals,
            y=lat_vals,
            origin="lower",
            color_continuous_scale="RdYlBu_r",
            labels={"x": "Longitude", "y": "Latitude", "color": variable},
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("Dataset does not contain spatial grid")

    # -----------------------------
    # LOCATION SELECTION
    # -----------------------------

    if lat_dim and lon_dim:

        st.markdown("### Select Location")

        lat_value = st.slider(
            "Latitude",
            float(lat_vals.min()),
            float(lat_vals.max()),
            float(lat_vals.mean()),
        )

        lon_value = st.slider(
            "Longitude",
            float(lon_vals.min()),
            float(lon_vals.max()),
            float(lon_vals.mean()),
        )

        lat_index = np.abs(lat_vals - lat_value).argmin()
        lon_index = np.abs(lon_vals - lon_value).argmin()

    # -----------------------------
    # TREND OVER TIME
    # -----------------------------

    if lat_dim and lon_dim and time_dim and len(dataset[time_dim]) > 1:

        st.markdown(f"### {variable.upper()} Trend Over Time")

        timeseries = dataset[variable][:, lat_index, lon_index]

        fig2 = px.line(
            x=dataset[time_dim].values,
            y=timeseries.values,
            markers=True,
            labels={"x": "Time", "y": variable},
        )

        st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # COMPARISON MODE
    # -----------------------------

    if lat_dim and lon_dim and time_dim:

        if len(dataset[time_dim]) > 1:

            st.markdown("### Comparison Mode")

            colA, colB = st.columns(2)

            timeA = st.slider("Time A", 0, len(dataset[time_dim]) - 1, 0)

            timeB = st.slider(
                "Time B",
                0,
                len(dataset[time_dim]) - 1,
                min(1, len(dataset[time_dim]) - 1),
            )

            sliceA = dataset[variable].isel({time_dim: timeA})
            sliceB = dataset[variable].isel({time_dim: timeB})

            with colA:

                figA = px.imshow(
                    sliceA.values,
                    x=lon_vals,
                    y=lat_vals,
                    origin="lower",
                    color_continuous_scale="RdYlBu_r",
                )

                st.plotly_chart(figA, use_container_width=True)

            with colB:

                figB = px.imshow(
                    sliceB.values,
                    x=lon_vals,
                    y=lat_vals,
                    origin="lower",
                    color_continuous_scale="RdYlBu_r",
                )

                st.plotly_chart(figB, use_container_width=True)

        else:

            st.info(
                "⚠️ This dataset contains only one time step — comparison mode not available."
            )

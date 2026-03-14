import streamlit as st
import xarray as xr
import tempfile
import numpy as np
from utils.helpers import detect_dims, extract_time_info, get_variable_options

def load_dataset_from_session():
    dataset = None
    variable = None
    time_dim = None
    lat_dim = None
    lon_dim = None
    all_years = None
    unique_years = None
    time_vals = None
    time_dt = None
    selected_display = None
    data_slice = None
    lat_vals = None
    lon_vals = None
    selected_year = None
    time_index = 0

    if st.session_state.dataset_uploaded and st.session_state.uploaded_file_data:
        try:
            file_content = st.session_state.uploaded_file_data.getvalue()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmp:
                tmp.write(file_content)
                tmp_path = tmp.name

            dataset = xr.open_dataset(tmp_path)

            if st.session_state.current_page != "Home":
                var_options = get_variable_options(dataset)
                display_options = list(var_options.keys())

                if len(display_options) > 0:
                    selected_display = st.sidebar.selectbox("Select Variable", display_options)
                    variable = var_options[selected_display]

                    time_dim, lat_dim, lon_dim = detect_dims(dataset[variable])
                    time_vals, time_dt, all_years, unique_years = extract_time_info(dataset, time_dim)

                    if time_dim and unique_years and len(unique_years) > 0:
                        selected_year = st.sidebar.select_slider(
                            "Select Time",
                            options=unique_years,
                            value=unique_years[0],
                        )
                        time_index = np.where(all_years == selected_year)[0][0]
                    else:
                        selected_year = None
                        time_index = 0

                    if time_dim:
                        data_slice = dataset[variable].isel({time_dim: time_index})
                    else:
                        data_slice = dataset[variable]

                    if lat_dim:
                        lat_vals = dataset[lat_dim].values
                    if lon_dim:
                        lon_vals = dataset[lon_dim].values

        except Exception as e:
            st.error(f"Failed to load dataset: {e}")
            st.session_state.dataset_uploaded = False
            st.session_state.uploaded_file_data = None

    return {
        "dataset": dataset,
        "variable": variable,
        "time_dim": time_dim,
        "lat_dim": lat_dim,
        "lon_dim": lon_dim,
        "all_years": all_years,
        "unique_years": unique_years,
        "time_vals": time_vals,
        "time_dt": time_dt,
        "selected_display": selected_display,
        "data_slice": data_slice,
        "lat_vals": lat_vals,
        "lon_vals": lon_vals,
        "selected_year": selected_year,
    }

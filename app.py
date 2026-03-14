import streamlit as st
import xarray as xr
import tempfile
import plotly.express as px
import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
# ---------------------------------------------------
st.set_page_config(
    page_title="PyClimaExplorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",  # Start with sidebar collapsed
)

# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------
if 'dataset_uploaded' not in st.session_state:
    st.session_state.dataset_uploaded = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'uploaded_file_data' not in st.session_state:
    st.session_state.uploaded_file_data = None
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0  # For resetting uploader if needed

# ---------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #07111f 0%, #0b1020 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #08101d;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Hide sidebar by default - will be shown after upload */
    section[data-testid="stSidebar"] {
        display: block;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 4px;
    }

    .sub-title {
        font-size: 16px;
        color: #b7c9e2;
        margin-bottom: 20px;
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(59,130,246,0.08));
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }

    .glass-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 18px;
        text-align: center;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
    }

    .metric-label {
        font-size: 14px;
        color: #b7c9e2;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .small-muted {
        color: #a8b8d3;
        font-size: 14px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 10px;
        border-radius: 16px;
    }

    /* Landing page specific styles */
    .upload-hero {
        background: linear-gradient(135deg, rgba(34,211,238,0.25), rgba(59,130,246,0.15), rgba(16,185,129,0.15));
        border: 2px dashed rgba(255,255,255,0.2);
        border-radius: 32px;
        padding: 40px 30px;
        text-align: center;
        margin: 40px 0;
        transition: all 0.3s ease;
    }
    
    .upload-hero:hover {
        border-color: rgba(34,211,238,0.5);
        background: linear-gradient(135deg, rgba(34,211,238,0.3), rgba(59,130,246,0.2), rgba(16,185,129,0.2));
    }
    
    .upload-icon {
        font-size: 80px;
        margin-bottom: 20px;
    }
    
    .feature-badge {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 40px;
        padding: 8px 20px;
        display: inline-block;
        margin: 5px;
        color: #b7c9e2;
    }
    
    /* Style the file uploader to match the hero section */
    .stFileUploader {
        margin-top: 20px;
    }
    
    .stFileUploader > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stFileUploader > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
    
    .stFileUploader label {
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def detect_dims(data_array):
    dims = data_array.dims
    time_dim = None
    lat_dim = None
    lon_dim = None

    for d in dims:
        dl = d.lower()
        if "time" in dl:
            time_dim = d
        if "lat" in dl:
            lat_dim = d
        if "lon" in dl or "long" in dl:
            lon_dim = d

    return time_dim, lat_dim, lon_dim


def get_variable_options(dataset):
    var_options = {}
    for var in dataset.data_vars:
        long_name = dataset[var].attrs.get("long_name", var)
        units = dataset[var].attrs.get("units", "")
        display_name = f"{long_name} ({units})" if units else long_name
        var_options[display_name] = var
    return var_options


def extract_time_info(dataset, time_dim):
    if not time_dim:
        return None, None, None, None

    time_vals = dataset[time_dim].values

    if len(time_vals) == 0:
        return None, None, None, None

    try:
        time_dt = pd.to_datetime(time_vals)
        all_years = time_dt.year.values.astype(int)
        unique_years = sorted(np.unique(all_years).tolist())
        return time_vals, time_dt, all_years, unique_years
    except Exception:
        all_years = np.arange(len(time_vals))
        unique_years = list(all_years)
        return time_vals, None, all_years, unique_years


def safe_stat(arr, mode="mean"):
    flat = np.array(arr).astype(float).flatten()
    flat = flat[~np.isnan(flat)]

    if len(flat) == 0:
        return "N/A"

    if mode == "mean":
        return round(float(np.mean(flat)), 3)
    if mode == "min":
        return round(float(np.min(flat)), 3)
    if mode == "max":
        return round(float(np.max(flat)), 3)
    return "N/A"


def format_value(val):
    if isinstance(val, (int, float, np.integer, np.floating)):
        return f"{val}"
    return str(val)

# ---------------------------------------------------
# HANDLE FILE UPLOAD FUNCTION
# ---------------------------------------------------

def handle_file_upload(uploaded_file):
    """Process uploaded file and update session state"""
    if uploaded_file is not None:
        # Store the file data in session state using getvalue() to avoid reading issues
        st.session_state.uploaded_file_data = uploaded_file
        st.session_state.dataset_uploaded = True
        st.session_state.current_page = "Dashboard"
        # Increment uploader key to reset if needed
        st.session_state.uploader_key += 1
        st.rerun()

# ---------------------------------------------------
# SIDEBAR - Only shown after dataset is uploaded
# ---------------------------------------------------
if st.session_state.dataset_uploaded:
    with st.sidebar:
        st.markdown(
            """
            <style>
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 0.5rem;
            }

            section[data-testid="stSidebar"] .stRadio label {
                padding: 4px 0px;
            }

            section[data-testid="stSidebar"] h1 {
                margin-top: 0rem;
                padding-top: 0rem;
                font-size: 28px;
            }

            section[data-testid="stSidebar"] .stCaption {
                margin-top: -8px;
                margin-bottom: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.title("🌍 PyClimaExplorer")
        st.caption("Climate Intelligence Platform")

        st.markdown("---")

        # Navigation - use session state to track current page
        page_options = ["Home", "Dashboard", "Dataset Explorer", "Comparison", "Story Mode", "About", "3D Globe"]
        selected_page = st.radio(
            "Navigation",
            page_options,
            index=page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0,
        )
        st.session_state.current_page = selected_page

        st.markdown("---")
        st.markdown("### Upload Dataset")

        # Sidebar uploader for replacing the dataset
        sidebar_file = st.file_uploader("Replace Dataset", type=["nc"], key=f"sidebar_uploader_{st.session_state.uploader_key}")
        if sidebar_file is not None:
            handle_file_upload(sidebar_file)

        st.caption("Supported format: .nc")
else:
    # If no dataset uploaded, force page to Home
    st.session_state.current_page = "Home"

# ---------------------------------------------------
# HOME PAGE (LANDING PAGE)
# ---------------------------------------------------
if st.session_state.current_page == "Home":
    # Full-width landing page with prominent upload area
    st.markdown(
        """
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <h1 style="font-size: 56px; font-weight: 800; background: linear-gradient(135deg, #7dd3fc, #60a5fa); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">
                PyClimaExplorer
            </h1>
            <p style="font-size: 20px; color: #b7c9e2; margin-top: 5px;">
                Climate Intelligence Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main upload hero section with actual file uploader
    with st.container():
        st.markdown(
            """
            <div class="upload-hero">
                <div class="upload-icon">🌍</div>
                <h2 style="font-size: 36px; color: white; margin-bottom: 10px;">Start Your Climate Exploration</h2>
                <p style="font-size: 18px; color: #b7c9e2; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Upload a NetCDF (.nc) dataset to unlock interactive maps, temporal trends, and climate insights
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Actual file uploader in the hero section
        uploaded_file = st.file_uploader(
            "Choose a NetCDF file", 
            type=["nc"], 
            key=f"home_uploader_{st.session_state.uploader_key}",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            handle_file_upload(uploaded_file)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-size: 32px;">🌡️</div>
                <div class="metric-value">Global Maps</div>
                <div class="metric-label">Spatial distribution visualization</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-size: 32px;">📈</div>
                <div class="metric-value">Time Trends</div>
                <div class="metric-label">Location-based temporal analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-size: 32px;">🆚</div>
                <div class="metric-value">Comparison</div>
                <div class="metric-label">Side-by-side climate shifts</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-size: 32px;">🌐</div>
                <div class="metric-value">3D Globe</div>
                <div class="metric-label">Interactive globe visualization</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # How it works section
    st.markdown("<h2 style='text-align: center; color: white;'>How It Works</h2>", unsafe_allow_html=True)
    
    flow1, flow2, flow3, flow4 = st.columns(4)

    with flow1:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center; min-height:200px;">
                <div style="font-size: 40px;">📂</div>
                <h4>1. Upload Dataset</h4>
                <p class="small-muted">Import your NetCDF (.nc) climate file</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with flow2:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center; min-height:200px;">
                <div style="font-size: 40px;">🎛️</div>
                <h4>2. Select Variable</h4>
                <p class="small-muted">Choose temperature, rainfall, or any variable</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with flow3:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center; min-height:200px;">
                <div style="font-size: 40px;">🗺️</div>
                <h4>3. Explore Patterns</h4>
                <p class="small-muted">Analyze maps, coordinates, and trends</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with flow4:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center; min-height:200px;">
                <div style="font-size: 40px;">📊</div>
                <h4>4. Generate Insights</h4>
                <p class="small-muted">Compare periods and present findings</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature tags
    st.markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <span class="feature-badge">🌡️ Temperature Analysis</span>
            <span class="feature-badge">💧 Precipitation</span>
            <span class="feature-badge">🌬️ Wind Patterns</span>
            <span class="feature-badge">🌊 Ocean Data</span>
            <span class="feature-badge">📊 Time Series</span>
            <span class="feature-badge">🗺️ Spatial Mapping</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

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

if st.session_state.dataset_uploaded and st.session_state.uploaded_file_data:
    try:
        # Use getvalue() to read the file content safely
        file_content = st.session_state.uploaded_file_data.getvalue()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        dataset = xr.open_dataset(tmp_path)

        # Only show variable selection if we're past the home page and dataset is loaded
        if st.session_state.current_page != "Home" and st.session_state.dataset_uploaded and st.session_state.uploaded_file_data:
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
        # Reset upload state on error
        st.session_state.dataset_uploaded = False
        st.session_state.uploaded_file_data = None

# ---------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------

if st.session_state.current_page == "Dashboard" and st.session_state.dataset_uploaded:
    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
    else:
        st.markdown("<div class='section-title'>Dashboard Overview</div>", unsafe_allow_html=True)

        metric1, metric2, metric3, metric4 = st.columns(4)

        units = dataset[variable].attrs.get("units", "")
        mean_val = safe_stat(data_slice.values, "mean")
        min_val = safe_stat(data_slice.values, "min")
        max_val = safe_stat(data_slice.values, "max")

        with metric1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{variable}</div>
                    <div class="metric-label">Selected Variable</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{format_value(selected_year) if selected_year is not None else "N/A"}</div>
                    <div class="metric-label">Selected Time</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{mean_val}</div>
                    <div class="metric-label">Average Value {f"({units})" if units else ""}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with metric4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{min_val} / {max_val}</div>
                    <div class="metric-label">Min / Max</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("")

        top_left, top_right = st.columns([2.2, 1])

        with top_left:
            st.markdown("<div class='section-title'>Global Spatial View</div>", unsafe_allow_html=True)

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
                    margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No spatial latitude/longitude grid found in this variable.")

        with top_right:
            st.markdown("<div class='section-title'>Quick Insights</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="glass-card">
                    <p><b>Variable:</b> {variable}</p>
                    <p><b>Units:</b> {units if units else "Not available"}</p>
                    <p><b>Dimensions:</b> {", ".join(dataset[variable].dims)}</p>
                    <p><b>Shape:</b> {dataset[variable].shape}</p>
                    <p><b>Time Axis:</b> {time_dim if time_dim else "Not available"}</p>
                    <p><b>Latitude Axis:</b> {lat_dim if lat_dim else "Not available"}</p>
                    <p><b>Longitude Axis:</b> {lon_dim if lon_dim else "Not available"}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if lat_dim and lon_dim:
            st.markdown("<div class='section-title'>Location-Based Trend</div>", unsafe_allow_html=True)

            left_filter, right_filter = st.columns(2)

            with left_filter:
                lat_value = st.slider(
                    "Latitude",
                    float(np.min(lat_vals)),
                    float(np.max(lat_vals)),
                    float(np.mean(lat_vals)),
                )

            with right_filter:
                lon_value = st.slider(
                    "Longitude",
                    float(np.min(lon_vals)),
                    float(np.max(lon_vals)),
                    float(np.mean(lon_vals)),
                )

            lat_index = np.abs(lat_vals - lat_value).argmin()
            lon_index = np.abs(lon_vals - lon_value).argmin()

            if time_dim and len(dataset[time_dim]) > 1:
                try:
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
                        margin=dict(l=10, r=10, t=40, b=10),
                    )
                    st.plotly_chart(trend_fig, use_container_width=True)
                except Exception:
                    st.info("Unable to generate time trend for the selected location.")

# ---------------------------------------------------
# DATASET EXPLORER PAGE
# ---------------------------------------------------

if st.session_state.current_page == "Dataset Explorer" and st.session_state.dataset_uploaded:
    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
    else:
        st.markdown("<div class='section-title'>Dataset Explorer</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                f"""
                <div class="glass-card">
                    <h4>Dataset Summary</h4>
                    <p><b>Variables:</b> {len(dataset.data_vars)}</p>
                    <p><b>Coordinates:</b> {len(dataset.coords)}</p>
                    <p><b>Selected Variable:</b> {variable}</p>
                    <p><b>Selected Shape:</b> {dataset[variable].shape}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            dims_text = "<br>".join([f"<b>{k}</b>: {v}" for k, v in dataset.dims.items()])
            st.markdown(
                f"""
                <div class="glass-card">
                    <h4>Dimensions</h4>
                    <p>{dims_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div class='section-title'>Available Variables</div>", unsafe_allow_html=True)

        var_data = []
        for var in dataset.data_vars:
            var_data.append(
                {
                    "Variable": var,
                    "Dimensions": ", ".join(dataset[var].dims),
                    "Shape": str(dataset[var].shape),
                    "Units": dataset[var].attrs.get("units", ""),
                    "Long Name": dataset[var].attrs.get("long_name", ""),
                }
            )

        st.dataframe(pd.DataFrame(var_data), use_container_width=True)

        st.markdown("<div class='section-title'>Selected Variable Preview</div>", unsafe_allow_html=True)

        try:
            preview_df = dataset[variable].to_dataframe().reset_index().head(100)
            st.dataframe(preview_df, use_container_width=True)
        except Exception:
            st.info("Preview table could not be generated for this variable.")

# ---------------------------------------------------
# COMPARISON PAGE
# ---------------------------------------------------

if st.session_state.current_page == "Comparison" and st.session_state.dataset_uploaded:
    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
    elif not (time_dim and lat_dim and lon_dim):
        st.warning("Comparison view requires time, latitude, and longitude dimensions.")
    elif len(dataset[time_dim]) <= 1:
        st.info("This dataset contains only one time step. Comparison mode is not available.")
    else:
        st.markdown("<div class='section-title'>Comparison Mode</div>", unsafe_allow_html=True)

        compare_col1, compare_col2 = st.columns(2)

        min_year = int(np.min(all_years))
        max_year = int(np.max(all_years))

        yearA = st.slider("Select Time A", min_year, max_year, min_year)
        yearB = st.slider("Select Time B", min_year, max_year, min(max_year, min_year + 1))

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

# ---------------------------------------------------
# STORY MODE PAGE
# ---------------------------------------------------

if st.session_state.current_page == "Story Mode" and st.session_state.dataset_uploaded:
    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
    else:
        st.markdown("<div class='section-title'>Story Mode</div>", unsafe_allow_html=True)

        step = st.selectbox(
            "Choose story step",
            [
                "Step 1: Dataset Overview",
                "Step 2: Spatial Pattern",
                "Step 3: Local Trend",
                "Step 4: Climate Comparison",
            ],
        )

        if step == "Step 1: Dataset Overview":
            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>What are we looking at?</h3>
                    <p>
                    This dataset contains climate information for the variable <b>{variable}</b>.
                    The goal is to understand how this variable behaves across geography and time.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif step == "Step 2: Spatial Pattern":
            st.markdown(
                """
                <div class="glass-card">
                    <h3>How is the variable distributed globally?</h3>
                    <p>
                    The map below helps identify regions with lower and higher values for the selected climate variable.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if lat_dim and lon_dim:
                fig = px.imshow(
                    data_slice.values,
                    x=lon_vals,
                    y=lat_vals,
                    origin="lower",
                    color_continuous_scale="RdYlBu_r",
                    aspect="auto",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                )
                st.plotly_chart(fig, use_container_width=True)

        elif step == "Step 3: Local Trend":
            if lat_dim and lon_dim and time_dim and len(dataset[time_dim]) > 1:
                lat_value = st.slider(
                    "Story Latitude",
                    float(np.min(lat_vals)),
                    float(np.max(lat_vals)),
                    float(np.mean(lat_vals)),
                    key="story_lat",
                )
                lon_value = st.slider(
                    "Story Longitude",
                    float(np.min(lon_vals)),
                    float(np.max(lon_vals)),
                    float(np.mean(lon_vals)),
                    key="story_lon",
                )

                lat_index = np.abs(lat_vals - lat_value).argmin()
                lon_index = np.abs(lon_vals - lon_value).argmin()
                timeseries = dataset[variable][:, lat_index, lon_index]

                st.markdown(
                    """
                    <div class="glass-card">
                        <h3>How does it change over time at one location?</h3>
                        <p>
                        This chart highlights the trend of the selected variable for the chosen coordinates.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                fig = px.line(
                    x=dataset[time_dim].values,
                    y=timeseries.values,
                    markers=True,
                    labels={"x": "Time", "y": variable},
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Story trend requires time, latitude, and longitude dimensions.")

        elif step == "Step 4: Climate Comparison":
            if time_dim and lat_dim and lon_dim and len(dataset[time_dim]) > 1:
                min_year = int(np.min(all_years))
                max_year = int(np.max(all_years))

                yearA = st.selectbox("Story Year A", list(range(min_year, max_year + 1)))
                yearB = st.selectbox("Story Year B", list(range(min_year, max_year + 1)), index=min(1, max_year - min_year))

                timeA = np.argmin(np.abs(all_years - yearA))
                timeB = np.argmin(np.abs(all_years - yearB))

                sliceA = dataset[variable].isel({time_dim: timeA})
                sliceB = dataset[variable].isel({time_dim: timeB})

                cc1, cc2 = st.columns(2)

                with cc1:
                    figA = px.imshow(
                        sliceA.values,
                        x=lon_vals,
                        y=lat_vals,
                        origin="lower",
                        color_continuous_scale="RdYlBu_r",
                        aspect="auto",
                    )
                    figA.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white",
                    )
                    st.plotly_chart(figA, use_container_width=True)

                with cc2:
                    figB = px.imshow(
                        sliceB.values,
                        x=lon_vals,
                        y=lat_vals,
                        origin="lower",
                        color_continuous_scale="RdYlBu_r",
                        aspect="auto",
                    )
                    figB.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white",
                    )
                    st.plotly_chart(figB, use_container_width=True)
            else:
                st.info("Story comparison requires time, latitude, and longitude dimensions.")

# ---------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------

if st.session_state.current_page == "About" and st.session_state.dataset_uploaded:
    st.markdown("<div class='section-title'>About PyClimaExplorer</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-card">
            <h3>Project Goal</h3>
            <p>
            PyClimaExplorer is an interactive climate data visualization platform designed
            to transform NetCDF climate datasets into understandable maps, trends, and
            comparison stories.
            </p>

            <h3>Core Features</h3>
            <ul>
                <li>Interactive global heatmaps</li>
                <li>Location-based time trend analysis</li>
                <li>Dataset exploration</li>
                <li>Time comparison mode</li>
                <li>Storytelling mode for presentations</li>
            </ul>

            <h3>Suggested Stack</h3>
            <p>Streamlit, Xarray, Pandas, NumPy, Plotly</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------
# 3D GLOBE PAGE
# ---------------------------------------------------

if st.session_state.current_page == "3D Globe" and st.session_state.dataset_uploaded:
    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
    elif not (lat_dim and lon_dim):
        st.warning("3D globe view requires latitude and longitude dimensions.")
    else:
        st.markdown("<div class='section-title'>3D Globe Visualization</div>", unsafe_allow_html=True)

        try:
            globe_data = np.array(data_slice.values, dtype=float)

            step_lat = max(1, len(lat_vals) // 45)
            step_lon = max(1, len(lon_vals) // 60)

            sampled_lat = lat_vals[::step_lat]
            sampled_lon = lon_vals[::step_lon]
            sampled_data = globe_data[::step_lat, ::step_lon]

            lon_grid, lat_grid = np.meshgrid(sampled_lon, sampled_lat)
            value_grid = sampled_data

            lat_flat = lat_grid.flatten()
            lon_flat = lon_grid.flatten()
            val_flat = value_grid.flatten()

            valid_mask = np.isfinite(val_flat)
            lat_flat = lat_flat[valid_mask]
            lon_flat = lon_flat[valid_mask]
            val_flat = val_flat[valid_mask]

            if len(val_flat) == 0:
                st.info("No valid data available for globe rendering.")
            else:
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
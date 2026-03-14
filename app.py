import streamlit as st
from utils.session import init_session_state
from components.styles import load_global_styles
from components.sidebar import render_sidebar
from utils.dataset import load_dataset_from_session
from views.home import render_home_page
from views.dashboard import render_dashboard_page
from views.dataset_explorer import render_dataset_explorer_page
from views.comparison import render_comparison_page
from views.story_mode import render_story_mode_page
from views.about import render_about_page
from views.globe_3d import render_globe_page


st.set_page_config(
    page_title="PyClimaExplorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()
load_global_styles()

# Sidebar
if st.session_state.dataset_uploaded:
    render_sidebar()
else:
    st.session_state.current_page = "Home"

# Load dataset
dataset_context = load_dataset_from_session()

# Route pages

current_page = st.session_state.current_page

if current_page == "Home":
    render_home_page()

elif current_page == "Dashboard":
    render_dashboard_page(dataset_context)

elif current_page == "Dataset Explorer":
    render_dataset_explorer_page(dataset_context)

elif current_page == "Comparison":
    render_comparison_page(dataset_context)

elif current_page == "Story Mode":
    render_story_mode_page(dataset_context)

elif current_page == "About":
    render_about_page()

elif current_page == "3D Globe":
    render_globe_page(dataset_context)

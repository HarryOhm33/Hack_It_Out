import streamlit as st
from components.uploader import handle_file_upload

PAGE_OPTIONS = [
    "Home",
    "Dashboard",
    "Dataset Explorer",
    "Comparison",
    "Story Mode",
    "About",
    "3D Globe",
]

def change_page():
    st.session_state.current_page = st.session_state.sidebar_page

def render_sidebar():
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

        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"

        if "sidebar_page" not in st.session_state:
            st.session_state.sidebar_page = st.session_state.current_page

        if st.session_state.sidebar_page != st.session_state.current_page:
            st.session_state.sidebar_page = st.session_state.current_page

        st.radio(
            "Navigation",
            PAGE_OPTIONS,
            key="sidebar_page",
            on_change=change_page,
        )

        st.markdown("---")
        st.markdown("### Upload Dataset")

        sidebar_file = st.file_uploader(
            "Replace Dataset",
            type=["nc"],
            key=f"sidebar_uploader_{st.session_state.uploader_key}",
        )

        if sidebar_file is not None:
            handle_file_upload(sidebar_file)

        st.caption("Supported format: .nc")

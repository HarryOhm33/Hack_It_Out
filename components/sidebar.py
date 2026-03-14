import streamlit as st
from components.uploader import handle_file_upload

PAGE_OPTIONS = [
    "Dashboard",
    "Dataset Explorer",
    "Comparison",
    "Story Mode",
    "3D Globe",
]


def change_page():
    st.session_state.current_page = st.session_state.sidebar_page


def render_sidebar():
    with st.sidebar:
        # Enhanced sidebar styling
        st.markdown(
            """
            <style>
            /* Sidebar styling - aggressive space reduction */
            section[data-testid="stSidebar"] > div {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
                background: rgba(128, 128, 128, 0.02);
            }
            
            /* Remove gaps between sidebar elements */
            section[data-testid="stSidebar"] [class*="stVerticalBlock"] {
                gap: 0 !important;
            }
            
            /* Navigation items */
            section[data-testid="stSidebar"] .stRadio > div {
                gap: 0 !important;
            }
            
            section[data-testid="stSidebar"] .stRadio label {
                padding: 0.3rem 0.5rem !important;
                border-radius: 0.5rem;
                transition: all 0.2s;
                margin: 0 !important;
                font-weight: 500;
                font-size: 0.95rem;
            }
            
            section[data-testid="stSidebar"] .stRadio label:hover {
                background: rgba(0, 198, 251, 0.1);
                transform: translateX(3px);
            }
            
            section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
                background: transparent;
                padding: 0 !important;
                border-radius: 0;
                gap: 0 !important;
            }
            
            /* Selected radio item */
            section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] > div:first-child {
                background-color: #00c6fb !important;
            }
            
            /* Uploader styling */
            section[data-testid="stSidebar"] .stFileUploader > div {
                padding: 0 !important;
                margin: 0 !important;
            }
            
            section[data-testid="stSidebar"] .stFileUploader > div > div {
                border: 2px dashed rgba(0, 198, 251, 0.3) !important;
                border-radius: 0.75rem !important;
                padding: 0.75rem !important;
                background: rgba(0, 198, 251, 0.03) !important;
                transition: all 0.3s;
                margin: 0 !important;
            }
            
            section[data-testid="stSidebar"] .stFileUploader > div > div:hover {
                border-color: #00c6fb !important;
                background: rgba(0, 198, 251, 0.05) !important;
            }
            
            /* Divider */
            hr {
                margin: 0.1rem 0 !important;
                opacity: 0.2;
                border: none;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(128,128,128,0.3), transparent);
            }
            
            /* Headers */
            h3 {
                font-size: 1rem;
                font-weight: 600;
                margin: 0.1rem 0 0.05rem 0 !important;
                opacity: 0.9;
            }
            
            /* Caption */
            .stCaption {
                font-size: 0.85rem;
                opacity: 0.6;
                margin: 0 !important;
            }
            
            /* Tooltip */
            [data-testid="stTooltipIcon"] {
                opacity: 0.5;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # App title with icon
        st.markdown(
            """
            <div style="margin-bottom: 0.3rem; text-align: center;">
                <h1 style="font-size: 2rem; font-weight: 700; margin: 0; 
                    background: linear-gradient(120deg, #00c6fb, #005bea);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    🌍 PyClimaExplorer
                </h1>
                <p style="font-size: 0.85rem; opacity: 0.7; margin: 0.05rem 0 0 0;">Climate Intelligence Platform</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation state management
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"

        if "sidebar_page" not in st.session_state:
            st.session_state.sidebar_page = st.session_state.current_page

        if st.session_state.sidebar_page != st.session_state.current_page:
            st.session_state.sidebar_page = st.session_state.current_page

        # Navigation section
        st.markdown("### 🧭 Navigation")
        st.radio(
            "Navigation",
            PAGE_OPTIONS,
            key="sidebar_page",
            on_change=change_page,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Upload section
        st.markdown("### 📤 Upload Dataset")

        sidebar_file = st.file_uploader(
            "Upload NetCDF file",
            type=["nc"],
            key=f"sidebar_uploader_{st.session_state.uploader_key}",
            help="Supported format: .nc (NetCDF files only)",
        )

        if sidebar_file is not None:
            handle_file_upload(sidebar_file)

        st.caption("Supported format: NetCDF (.nc) only")

        # Show current dataset info if available
        if st.session_state.get("dataset_uploaded", False):
            st.markdown("---")
            st.markdown("### 📊 Current Dataset")
            st.info(f"✅ Dataset loaded")

            if st.button("🔄 Clear Dataset", use_container_width=True):
                st.session_state.dataset_uploaded = False
                st.session_state.uploaded_file_data = None
                st.session_state.uploader_key += 1
                st.rerun()

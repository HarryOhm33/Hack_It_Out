import streamlit as st
from components.uploader import handle_file_upload


def render_home_page():
    # Hero section with centered content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem 0 1rem 0;">
                <h1 style="font-size: 4rem; font-weight: 700; margin-bottom: 0.5rem; 
                    background: linear-gradient(120deg, #00c6fb 0%, #005bea 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    PyClimaExplorer
                </h1>
                <p style="font-size: 1.3rem; opacity: 0.8; margin-bottom: 2rem;">
                    Climate Intelligence Platform
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature cards in a grid
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.markdown(
                """
                <div style="text-align: center; padding: 2rem 1.5rem; border-radius: 1rem; 
                    border: 1px solid rgba(128, 128, 128, 0.2); background: rgba(128, 128, 128, 0.03);
                    transition: transform 0.3s, box-shadow 0.3s; height: 100%;"
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 20px rgba(0,0,0,0.2)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                    <span style="font-size: 3rem;">🌍</span>
                    <h3 style="margin: 1rem 0 0.5rem 0;">Interactive Maps</h3>
                    <p style="opacity: 0.7; font-size: 1rem; margin: 0;">
                        Explore climate data with dynamic 2D and 3D visualizations
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col2:
        with st.container():
            st.markdown(
                """
                <div style="text-align: center; padding: 2rem 1.5rem; border-radius: 1rem; 
                    border: 1px solid rgba(128, 128, 128, 0.2); background: rgba(128, 128, 128, 0.03);
                    transition: transform 0.3s, box-shadow 0.3s; height: 100%;"
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 20px rgba(0,0,0,0.2)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                    <span style="font-size: 3rem;">📊</span>
                    <h3 style="margin: 1rem 0 0.5rem 0;">Time Series Analysis</h3>
                    <p style="opacity: 0.7; font-size: 1rem; margin: 0;">
                        Track climate patterns and trends over decades
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col3:
        with st.container():
            st.markdown(
                """
                <div style="text-align: center; padding: 2rem 1.5rem; border-radius: 1rem; 
                    border: 1px solid rgba(128, 128, 128, 0.2); background: rgba(128, 128, 128, 0.03);
                    transition: transform 0.3s, box-shadow 0.3s; height: 100%;"
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 20px rgba(0,0,0,0.2)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                    <span style="font-size: 3rem;">🔍</span>
                    <h3 style="margin: 1rem 0 0.5rem 0;">Dataset Explorer</h3>
                    <p style="opacity: 0.7; font-size: 1rem; margin: 0;">
                        Deep dive into NetCDF data structures and metadata
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Upload area with prominent design
    with st.container():

        uploaded_file = st.file_uploader(
            "Choose a NetCDF file",
            type=["nc"],
            key=f"home_uploader_{st.session_state.uploader_key}",
            label_visibility="collapsed",
        )

        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem; border-radius: 2rem; 
                border: 3px dashed rgba(0, 198, 251, 0.3); background: linear-gradient(135deg, rgba(0,198,251,0.05), rgba(0,91,234,0.05));
                margin: 3rem 0;">
                <div style="font-size: 5rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;">📤</div>
                <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Start Your Climate Exploration</h2>
                <p style="opacity: 0.8; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto; font-size: 1.1rem;">
                    Upload a NetCDF (.nc) dataset to unlock interactive maps, temporal trends, and climate insights
                </p>
            </div>
            
            <style>
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0px); }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if uploaded_file is not None:
            handle_file_upload(uploaded_file)

    # Quick start guide
    with st.expander("🚀 Quick Start Guide", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 0.5rem;">1️⃣ Upload Data</h4>
                    <p style="opacity: 0.7;">Upload your NetCDF file using the button above</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 0.5rem;">2️⃣ Select Variable</h4>
                    <p style="opacity: 0.7;">Choose a climate variable from the sidebar</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 0.5rem;">3️⃣ Explore</h4>
                    <p style="opacity: 0.7;">Navigate through different visualization modes</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

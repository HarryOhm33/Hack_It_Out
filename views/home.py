import streamlit as st
from components.uploader import handle_file_upload

def render_home_page():
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

        uploaded_file = st.file_uploader(
            "Choose a NetCDF file",
            type=["nc"],
            key=f"home_uploader_{st.session_state.uploader_key}",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            handle_file_upload(uploaded_file)

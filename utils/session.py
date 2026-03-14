import streamlit as st

def init_session_state():
    if "dataset_uploaded" not in st.session_state:
        st.session_state.dataset_uploaded = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    if "uploaded_file_data" not in st.session_state:
        st.session_state.uploaded_file_data = None
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

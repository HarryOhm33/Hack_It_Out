import streamlit as st

def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        st.session_state.uploaded_file_data = uploaded_file
        st.session_state.dataset_uploaded = True
        st.session_state.current_page = "Dashboard"
        st.session_state.uploader_key += 1
        st.rerun()

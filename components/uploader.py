import streamlit as st


def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        st.session_state.uploaded_file_data = uploaded_file
        st.session_state.dataset_uploaded = True
        st.session_state.current_page = "Dashboard"
        st.session_state.uploader_key += 1

        # Show success message with animation
        st.balloons()
        st.success(
            f"✅ **Success!** File '{uploaded_file.name}' has been uploaded and processed."
        )
        st.info("🔄 Redirecting to Dashboard...")

        # Rerun after a small delay to show the success message
        st.rerun()

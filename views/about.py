import streamlit as st

def render_about_page():
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
                <li>3D globe visualization</li>
            </ul>

            <h3>Suggested Stack</h3>
            <p>Streamlit, Xarray, Pandas, NumPy, Plotly</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

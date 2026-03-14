import streamlit as st
import plotly.express as px
import numpy as np

def render_story_mode_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]
    data_slice = ctx["data_slice"]
    time_dim = ctx["time_dim"]
    lat_dim = ctx["lat_dim"]
    lon_dim = ctx["lon_dim"]
    all_years = ctx["all_years"]
    lat_vals = ctx["lat_vals"]
    lon_vals = ctx["lon_vals"]

    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
        return

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
        else:
            st.info("Spatial pattern requires latitude and longitude dimensions.")

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

            yearA = st.selectbox("Story Year A", list(range(min_year, max_year + 1)), key="story_yearA")
            yearB = st.selectbox(
                "Story Year B",
                list(range(min_year, max_year + 1)),
                index=min(1, max_year - min_year),
                key="story_yearB"
            )

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

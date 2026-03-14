import streamlit as st
import pandas as pd

def render_dataset_explorer_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]

    if dataset is None or variable is None:
        st.warning("Please select a variable from the sidebar.")
        return

    st.markdown("<div class='section-title'>Dataset Explorer</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="glass-card">
                <h4>Dataset Summary</h4>
                <p><b>Variables:</b> {len(dataset.data_vars)}</p>
                <p><b>Coordinates:</b> {len(dataset.coords)}</p>
                <p><b>Selected Variable:</b> {variable}</p>
                <p><b>Selected Shape:</b> {dataset[variable].shape}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        dims_text = "<br>".join([f"<b>{k}</b>: {v}" for k, v in dataset.sizes.items()])
        st.markdown(
            f"""
            <div class="glass-card">
                <h4>Dimensions</h4>
                <p>{dims_text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-title'>Available Variables</div>", unsafe_allow_html=True)

    var_data = []
    for var in dataset.data_vars:
        var_data.append(
            {
                "Variable": var,
                "Dimensions": ", ".join(dataset[var].dims),
                "Shape": str(dataset[var].shape),
                "Units": dataset[var].attrs.get("units", ""),
                "Long Name": dataset[var].attrs.get("long_name", ""),
            }
        )

    st.dataframe(pd.DataFrame(var_data), use_container_width=True)

    st.markdown("<div class='section-title'>Selected Variable Preview</div>", unsafe_allow_html=True)

    try:
        preview_df = dataset[variable].to_dataframe().reset_index().head(100)
        st.dataframe(preview_df, use_container_width=True)
    except Exception:
        st.info("Preview table could not be generated for this variable.")

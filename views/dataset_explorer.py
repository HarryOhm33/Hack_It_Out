import streamlit as st
import pandas as pd
import numpy as np


def render_dataset_explorer_page(ctx):
    dataset = ctx["dataset"]
    variable = ctx["variable"]

    if dataset is None or variable is None:
        st.warning(
            "⚠️ Please select a variable from the sidebar to explore the dataset."
        )
        return

    # Page header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;">
                🔍 Dataset Explorer
            </h1>
            <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto;">
                Dive deep into your NetCDF data structure and metadata
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dataset overview cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Variables",
            len(dataset.data_vars),
            help="Number of data variables in the dataset",
        )

    with col2:
        st.metric(
            "Coordinates", len(dataset.coords), help="Number of coordinate variables"
        )

    with col3:
        total_size = sum(dataset[var].size for var in dataset.data_vars)
        st.metric(
            "Total Elements",
            f"{total_size:,}",
            help="Total number of data points across all variables",
        )

    with col4:
        dims = len(dataset.dims)
        st.metric("Dimensions", dims, help="Number of dimensions in the dataset")

    st.markdown("---")

    # Main content in tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📋 Dataset Summary",
            "📊 Variables Explorer",
            "📐 Dimensions & Coordinates",
            "🔬 Current Variable",
        ]
    )

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1);">
                    <h4 style="margin-top: 0;">📁 Dataset Information</h4>
                """,
                unsafe_allow_html=True,
            )

            # Dataset attributes
            attrs_df = (
                pd.DataFrame(
                    [
                        {"Attribute": k, "Value": str(v)}
                        for k, v in dataset.attrs.items()
                    ]
                )
                if dataset.attrs
                else pd.DataFrame({"Attribute": ["No attributes"], "Value": [""]})
            )

            st.dataframe(attrs_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(
                """
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1);">
                    <h4 style="margin-top: 0;">📏 Dataset Shape</h4>
                """,
                unsafe_allow_html=True,
            )

            # Dimension sizes
            dims_df = pd.DataFrame(
                [
                    {"Dimension": dim, "Size": size}
                    for dim, size in dataset.sizes.items()
                ]
            )
            st.dataframe(dims_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("#### All Variables")

        # Prepare variables data
        var_data = []
        for var in dataset.data_vars:
            var_data.append(
                {
                    "Variable": var,
                    "Dimensions": ", ".join(dataset[var].dims),
                    "Shape": str(dataset[var].shape),
                    "Size": f"{dataset[var].size:,}",
                    "Units": dataset[var].attrs.get("units", "N/A"),
                    "Long Name": dataset[var].attrs.get("long_name", "N/A"),
                    "Standard Name": dataset[var].attrs.get("standard_name", "N/A"),
                }
            )

        df_vars = pd.DataFrame(var_data)
        st.dataframe(
            df_vars,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Variable": st.column_config.TextColumn("Variable", width="medium"),
                "Dimensions": st.column_config.TextColumn("Dimensions", width="small"),
                "Shape": st.column_config.TextColumn("Shape", width="small"),
                "Size": st.column_config.TextColumn("Size", width="small"),
                "Units": st.column_config.TextColumn("Units", width="small"),
                "Long Name": st.column_config.TextColumn("Long Name", width="large"),
            },
        )

        # Variable selection for quick view
        st.markdown("#### Quick Variable Inspector")
        selected_var = st.selectbox(
            "Select a variable to inspect",
            list(dataset.data_vars),
            key="explorer_var_select",
        )

        if selected_var:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <div style="background: rgba(0, 198, 251, 0.1); padding: 1rem; border-radius: 0.5rem;">
                        <h5 style="margin: 0 0 0.5rem 0;">{selected_var} Properties</h5>
                        <p><b>Dimensions:</b> {', '.join(dataset[selected_var].dims)}</p>
                        <p><b>Shape:</b> {dataset[selected_var].shape}</p>
                        <p><b>Size:</b> {dataset[selected_var].size:,} elements</p>
                        <p><b>Data type:</b> {dataset[selected_var].dtype}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                # Show statistics for numeric data
                if np.issubdtype(dataset[selected_var].dtype, np.number):
                    data_flat = dataset[selected_var].values.flatten()
                    data_flat = data_flat[~np.isnan(data_flat)]
                    if len(data_flat) > 0:
                        st.markdown(
                            f"""
                            <div style="background: rgba(128, 128, 128, 0.05); padding: 1rem; border-radius: 0.5rem;">
                                <h5 style="margin: 0 0 0.5rem 0;">Statistics</h5>
                                <p><b>Mean:</b> {np.mean(data_flat):.3f}</p>
                                <p><b>Std Dev:</b> {np.std(data_flat):.3f}</p>
                                <p><b>Min:</b> {np.min(data_flat):.3f}</p>
                                <p><b>Max:</b> {np.max(data_flat):.3f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Dimensions")
            dims_data = []
            for dim, size in dataset.sizes.items():
                dims_data.append(
                    {
                        "Dimension": dim,
                        "Size": size,
                        "Coordinates": (
                            len(dataset[dim].values) if dim in dataset.coords else 0
                        ),
                        "Min": (
                            float(np.min(dataset[dim].values))
                            if dim in dataset.coords
                            else "N/A"
                        ),
                        "Max": (
                            float(np.max(dataset[dim].values))
                            if dim in dataset.coords
                            else "N/A"
                        ),
                    }
                )
            st.dataframe(
                pd.DataFrame(dims_data), use_container_width=True, hide_index=True
            )

        with col2:
            st.markdown("#### Coordinates")
            coords_data = []
            for coord in dataset.coords:
                coord_values = dataset[coord].values
                # Handle both array and scalar values
                try:
                    num_points = len(coord_values)
                except TypeError:
                    num_points = 1

                coords_data.append(
                    {
                        "Coordinate": coord,
                        "Dimensions": ", ".join(dataset[coord].dims),
                        "Shape": str(dataset[coord].shape),
                        "Values": f"{num_points} points",
                    }
                )
            st.dataframe(
                pd.DataFrame(coords_data), use_container_width=True, hide_index=True
            )

    with tab4:
        st.markdown(f"#### Current Variable: {variable}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1);">
                    <h4 style="margin-top: 0;">Variable Attributes</h4>
                """,
                unsafe_allow_html=True,
            )

            # Variable attributes
            var_attrs = []
            for k, v in dataset[variable].attrs.items():
                var_attrs.append({"Attribute": k, "Value": str(v)})

            if var_attrs:
                st.dataframe(
                    pd.DataFrame(var_attrs), use_container_width=True, hide_index=True
                )
            else:
                st.info("No attributes found for this variable")

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"""
                <div style="background: rgba(128, 128, 128, 0.05); padding: 1.5rem; border-radius: 1rem;
                    border: 1px solid rgba(128, 128, 128, 0.1);">
                    <h4 style="margin-top: 0;">Data Preview</h4>
                """,
                unsafe_allow_html=True,
            )

            try:
                # Show first few rows of data
                preview_df = dataset[variable].to_dataframe().reset_index()
                preview_df = preview_df.head(100)

                st.dataframe(
                    preview_df, use_container_width=True, hide_index=True, height=300
                )

                st.caption(
                    f"Showing first 100 of {len(dataset[variable].values.flatten()):,} total values"
                )
            except Exception as e:
                st.info("Preview could not be generated for this variable")

            st.markdown("</div>", unsafe_allow_html=True)

        # Download option
        st.markdown("---")
        try:
            csv_data = (
                dataset[variable]
                .to_dataframe()
                .reset_index()
                .head(1000)
                .to_csv(index=False)
            )
            st.download_button(
                label="📥 Download Sample Data (CSV)",
                data=csv_data,
                file_name=f"{variable}_sample.csv",
                mime="text/csv",
            )
        except:
            pass

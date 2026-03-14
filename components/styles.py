import streamlit as st

def load_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #07111f 0%, #0b1020 100%);
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: #08101d;
            border-right: 1px solid rgba(255,255,255,0.08);
            display: block;
        }

        .main-title {
            font-size: 42px;
            font-weight: 800;
            color: white;
            margin-bottom: 4px;
        }

        .sub-title {
            font-size: 16px;
            color: #b7c9e2;
            margin-bottom: 20px;
        }

        .hero-box {
            background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(59,130,246,0.08));
            padding: 28px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 20px;
        }

        .glass-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 18px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        }

        .metric-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03));
            border: 1px solid rgba(255,255,255,0.08);
            padding: 18px;
            border-radius: 18px;
            text-align: center;
        }

        .metric-value {
            font-size: 28px;
            font-weight: 800;
            color: #ffffff;
        }

        .metric-label {
            font-size: 14px;
            color: #b7c9e2;
        }

        .section-title {
            font-size: 24px;
            font-weight: 700;
            color: white;
            margin-top: 10px;
            margin-bottom: 12px;
        }

        .small-muted {
            color: #a8b8d3;
            font-size: 14px;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 10px;
            border-radius: 16px;
        }

        .upload-hero {
            background: linear-gradient(135deg, rgba(34,211,238,0.25), rgba(59,130,246,0.15), rgba(16,185,129,0.15));
            border: 2px dashed rgba(255,255,255,0.2);
            border-radius: 32px;
            padding: 40px 30px;
            text-align: center;
            margin: 40px 0;
            transition: all 0.3s ease;
        }

        .upload-hero:hover {
            border-color: rgba(34,211,238,0.5);
            background: linear-gradient(135deg, rgba(34,211,238,0.3), rgba(59,130,246,0.2), rgba(16,185,129,0.2));
        }

        .upload-icon {
            font-size: 80px;
            margin-bottom: 20px;
        }

        .feature-badge {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 40px;
            padding: 8px 20px;
            display: inline-block;
            margin: 5px;
            color: #b7c9e2;
        }

        .stFileUploader {
            margin-top: 20px;
        }

        .stFileUploader > div {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        .stFileUploader > div > div {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 16px !important;
            padding: 20px !important;
        }

        .stFileUploader label {
            color: white !important;
            font-size: 18px !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

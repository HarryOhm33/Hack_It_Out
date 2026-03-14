import streamlit as st


def load_global_styles():
    st.markdown(
        """
        <style>
        /* Main app styling - works with both light/dark mode */
        .stApp {
            transition: all 0.3s ease;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 600;
            letter-spacing: -0.01em;
        }
        
        /* Metric cards */
        div[data-testid="stMetric"] {
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.1);
            border-radius: 1rem;
            padding: 1.25rem;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            border-color: rgba(0, 198, 251, 0.3);
        }
        
        div[data-testid="stMetric"] > div {
            color: inherit !important;
        }
        
        div[data-testid="stMetric"] label {
            font-size: 0.9rem !important;
            opacity: 0.7;
        }
        
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700;
        }
        
        /* DataFrames */
        .stDataFrame {
            border-radius: 0.75rem;
            overflow: hidden;
            border: 1px solid rgba(128, 128, 128, 0.1);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .stDataFrame [data-testid="stDataFrameResizable"] {
            border-radius: 0.75rem;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: rgba(128, 128, 128, 0.05);
            padding: 0.5rem;
            border-radius: 2rem;
            border: 1px solid rgba(128, 128, 128, 0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 2rem;
            padding: 0.6rem 1.8rem;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #00c6fb, #005bea) !important;
            color: white !important;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 2rem;
            padding: 0.6rem 2rem;
            font-weight: 600;
            border: 1px solid rgba(128, 128, 128, 0.2);
            transition: all 0.3s;
            background: rgba(128, 128, 128, 0.05);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .stButton > button:hover {
            border-color: #00c6fb;
            box-shadow: 0 8px 15px rgba(0, 198, 251, 0.2);
            transform: translateY(-2px);
            background: linear-gradient(135deg, #00c6fb, #005bea);
            color: white !important;
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            border-radius: 0.75rem;
            border: 1px solid rgba(128, 128, 128, 0.2);
            transition: all 0.3s;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #00c6fb;
            box-shadow: 0 0 0 2px rgba(0, 198, 251, 0.1);
        }
        
        /* Sliders */
        .stSlider [data-baseweb="slider"] {
            margin-top: 0.75rem;
        }
        
        .stSlider [data-baseweb="slider"] > div {
            background: linear-gradient(90deg, #00c6fb, #005bea) !important;
            border-radius: 0.5rem;
            height: 8px !important;
        }
        
        /* Slider thumb/handle styling */
        .stSlider [role="slider"] {
            width: 20px !important;
            height: 20px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #00c6fb, #005bea) !important;
            border: 2px solid white !important;
            box-shadow: 0 2px 8px rgba(0, 198, 251, 0.4) !important;
            cursor: pointer;
            transition: all 0.2s ease !important;
        }
        
        .stSlider [role="slider"]:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(0, 198, 251, 0.6) !important;
        }
        
        .stSlider [role="slider"]:active {
            transform: scale(1.15);
        }
        
        /* Slider label styling */
        .stSlider > div > div > label {
            font-weight: 500;
            color: inherit;
            margin-bottom: 0.5rem;
        }
        
        /* Slider value display */
        .stSlider > div > div > span {
            font-weight: 600;
            color: #00c6fb;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600;
            background: rgba(128, 128, 128, 0.03);
            border-radius: 0.75rem;
            border: 1px solid rgba(128, 128, 128, 0.1);
            padding: 0.75rem 1rem;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(0, 198, 251, 0.05);
        }
        
        /* Progress bars */
        .stProgress > div > div {
            background: linear-gradient(90deg, #00c6fb, #005bea);
            border-radius: 1rem;
        }
        
        /* Success/Warning/Info messages */
        .stAlert {
            border-radius: 0.75rem;
            border-left-width: 4px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        /* Cards for content */
        .custom-card {
            background: rgba(128, 128, 128, 0.03);
            border: 1px solid rgba(128, 128, 128, 0.1);
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s;
        }
        
        .custom-card:hover {
            border-color: rgba(0, 198, 251, 0.3);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Responsive containers */
        @media (max-width: 768px) {
            .stApp header {
                padding-top: 0;
            }
            
            .stButton > button {
                width: 100%;
            }
            
            div[data-testid="column"] {
                margin-bottom: 1rem;
            }
            
            h1 {
                font-size: 2rem !important;
            }
        }
        
        /* Code blocks */
        .stCode {
            border-radius: 0.75rem;
            border: 1px solid rgba(128, 128, 128, 0.1);
            background: rgba(128, 128, 128, 0.02) !important;
        }
        
        /* Tooltips */
        [data-testid="stTooltipIcon"] {
            opacity: 0.5;
            transition: opacity 0.2s;
        }
        
        [data-testid="stTooltipIcon"]:hover {
            opacity: 1;
        }
        
        /* Checkbox */
        .stCheckbox {
            gap: 0.5rem;
        }
        
        .stCheckbox label {
            font-weight: 500;
        }
        
        /* Radio buttons */
        .stRadio > div {
            gap: 0.5rem;
        }
        
        /* Plotly charts - ensure full width rendering */
        [data-testid="plotly-container"] {
            width: 100% !important;
            overflow-x: visible !important;
        }
        
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Theme-specific adjustments - respect Streamlit's theme setting */
        @media (prefers-color-scheme: dark) {
            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.03);
            }
            
            .stDataFrame {
                background: rgba(255, 255, 255, 0.02);
            }
        }
        
        /* Light mode specific adjustments */
        @media (prefers-color-scheme: light) {
            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
            
            .stDataFrame {
                background: white;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background: rgba(0, 0, 0, 0.03);
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .stApp {
            animation: fadeIn 0.6s ease-out;
        }
        
        div[data-testid="stMetric"] {
            animation: slideIn 0.4s ease-out;
            animation-fill-mode: both;
        }
        
        div[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.1s; }
        div[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.2s; }
        div[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }
        div[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.4s; }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(128, 128, 128, 0.05);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(128, 128, 128, 0.2);
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #00c6fb, #005bea);
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-color: #00c6fb transparent #005bea transparent !important;
        }
        
        /* Plotly chart containers */
        .js-plotly-plot {
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s;
        }
        
        .js-plotly-plot:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* File uploader */
        .stFileUploader {
            margin: 1rem 0;
        }
        
        .stFileUploader > div > div {
            border-radius: 1rem !important;
            border: 2px dashed rgba(0, 198, 251, 0.3) !important;
            padding: 2rem !important;
            text-align: center !important;
            transition: all 0.3s !important;
        }
        
        .stFileUploader > div > div:hover {
            border-color: #00c6fb !important;
            background: rgba(0, 198, 251, 0.02) !important;
        }
        
        .stFileUploader [data-testid="stMarkdownContainer"] p {
            font-size: 1.1rem !important;
            font-weight: 500 !important;
        }
        
        /* Input fields */
        .stTextInput > div > div {
            border-radius: 0.75rem;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
        
        .stTextInput > div > div:focus-within {
            border-color: #00c6fb;
            box-shadow: 0 0 0 2px rgba(0, 198, 251, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

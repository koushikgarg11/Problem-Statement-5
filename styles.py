import streamlit as st
import plotly.io as pio

def apply_custom_css():
    pio.templates.default = "plotly_dark"
    
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* Global App Dark Theme */
        html, body, [data-testid="stAppViewContainer"], .main, .stApp {
            background-color: #0E1117 !important;
            background: #0E1117 !important;
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif;
        }

        /* Force ALL text elements to Pure White */
        p, span, label, li, h1, h2, h3, h4, h5, h6, td, th, div, a {
            color: #FFFFFF !important;
        }
        
        /* Top Header Toolbar */
        header[data-testid="stHeader"],
        [data-testid="stHeader"],
        .stAppHeader,
        .stHeader,
        div[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        .stApp > header {
            background-color: #0E1117 !important;
            background: #0E1117 !important;
            color: #FFFFFF !important;
        }
        
        div[data-testid="stDecoration"] {
            background-image: none !important;
            background-color: #0E1117 !important;
        }

        /* Sidebar Customization - Pure Black */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            background: #000000 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 6px 0 30px rgba(0, 0, 0, 0.9) !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-left: 12px !important;
            padding-right: 12px !important;
            padding-top: 10px !important;
        }

        /* Sidebar Radio Navigation Pill Buttons */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 8px !important;
            display: flex !important;
            flex-direction: column !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            background-color: #111827 !important;
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            transition: all 0.2s ease-in-out !important;
            margin: 0 !important;
            width: 100% !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            border-color: #00E676 !important;
            background-color: #1F2937 !important;
            color: #00E676 !important;
        }

        /* Selected Active Radio Button */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(90deg, rgba(0, 230, 118, 0.25) 0%, #111827 100%) !important;
            border: 2px solid #00E676 !important;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.35) !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }

        /* Hide radio circle elements cleanly */
        section[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"],
        section[data-testid="stSidebar"] div[role="radiogroup"] div[data-testid="stRadioButton"] > div > div:first-child {
            display: none !important;
        }

        /* Expander Header Dark Override */
        div[data-testid="stExpander"],
        [data-testid="stExpander"],
        details {
            background-color: #09101F !important;
            background: #09101F !important;
            border: 1px solid #1E293B !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
            overflow: hidden !important;
            margin-bottom: 12px !important;
        }

        div[data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary,
        details summary {
            background-color: #09101F !important;
            background: #09101F !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            padding: 12px 16px !important;
            border-bottom: 1px solid #1E293B !important;
        }

        div[data-testid="stExpander"] summary *,
        [data-testid="stExpander"] summary *,
        details summary * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* BaseWeb Selectbox & Dropdown Popover Absolute Dark Override */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] *,
        div[data-baseweb="popover"] div,
        div[data-baseweb="popover"] ul,
        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] span,
        ul[data-baseweb="menu"],
        ul[data-baseweb="menu"] *,
        li[data-baseweb="option"],
        li[data-baseweb="option"] *,
        div[role="listbox"],
        div[role="listbox"] *,
        ul[role="listbox"],
        ul[role="listbox"] *,
        div[role="option"],
        div[role="option"] * {
            background-color: #0F172A !important;
            background: #0F172A !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* Hover state on dropdown options */
        li[data-baseweb="option"]:hover,
        li[data-baseweb="option"]:hover *,
        div[role="option"]:hover,
        div[role="option"]:hover * {
            background-color: #1E293B !important;
            background: #1E293B !important;
            color: #00E676 !important;
            -webkit-text-fill-color: #00E676 !important;
        }

        /* BaseWeb Select Input Box inside Streamlit */
        div[data-baseweb="select"],
        div[data-baseweb="select"] *,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] span {
            background-color: #0F172A !important;
            background: #0F172A !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        div[data-baseweb="select"] > div {
            border: 1.5px solid #38BDF8 !important;
            border-radius: 10px !important;
        }

        /* Sleek Glowing Cyan Multiselect Pills/Tags */
        span[data-baseweb="tag"],
        div[data-baseweb="tag"] {
            background: rgba(56, 189, 248, 0.18) !important;
            background-color: rgba(56, 189, 248, 0.18) !important;
            border: 1px solid #38BDF8 !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
            padding: 2px 8px !important;
            font-weight: 600 !important;
        }

        span[data-baseweb="tag"] *,
        div[data-baseweb="tag"] * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* Plotly Chart Container Fix */
        .stPlotlyChart,
        div[data-testid="stPlotlyChart"] {
            background-color: #0E1117 !important;
            background: #0E1117 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            padding: 8px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }

        /* Metric Cards */
        div[data-testid="metric-container"], [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03)) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 14px !important;
            padding: 14px 16px !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            min-height: 105px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
        }
        
        [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *, [data-testid="stMetricLabel"] label, [data-testid="stMetricLabel"] p, div[data-testid="metric-container"] label {
            color: #FFFFFF !important;
            font-size: 0.88rem !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }
        
        [data-testid="stMetricValue"], [data-testid="stMetricValue"] *, [data-testid="stMetricValue"] div, [data-testid="stMetricValue"] span, div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #00E676 !important;
            font-size: 1.7rem !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }
        
        /* Section Cards */
        .glass-card {
            background: rgba(22, 27, 34, 0.85) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5) !important;
            color: #FFFFFF !important;
        }
        
        .glass-card p, .glass-card li, .glass-card ul, .glass-card b, .glass-card strong {
            color: #FFFFFF !important;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

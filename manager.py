import streamlit as st

# ------------------ Access Manager ------------------
def require_login():
    if not st.session_state.get("signed_in", False):
        st.warning("🔒 You must be logged in to access this page.")
        st.stop()

# ------------------ Navigation Manager ------------------
class NavigationManager:
    def __init__(self):
        self.pages = ['Home', 'IndividualAnalyzer', 'Account']

    def top_nav(self):
        col1, col2, col3, _ = st.columns([1.2, 3.1, 1, 10])

        with col1:
            st.page_link("Home.py", label="Home")

        with col2:
            if st.session_state.get("signed_in", False):
                st.page_link("pages/Individual_Analyzer.py", label="IndividualAnalyzer")

        with col3:
            if st.session_state.get("signed_in", False):
                st.page_link("pages/Account.py", label="Account")

# ------------------ Sidebar Styling ------------------
def apply_sidebar_style():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: #1c1c3c;
            padding-top: 20px;
            border-right: 1px solid #5a189a;
        }

        [data-testid="stSidebarNav"] > div {
            font-size: 18px;
            font-weight: bold;
            color: #f8f8f2;
        }

        section[data-testid="stSidebar"] a {
            color: #dcdcdc !important;
            font-size: 16px;
            padding: 8px 12px;
            display: block;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"] a:hover {
            background-color: #5a189a22;
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLinkActive"] {
            background-color: #5a189a88;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------------ Background & Component Styling ------------------
def set_background_css():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #240046 0%, #3c096c 50%, #5a189a 70%, #006494 90%) !important;
        position: relative;
        overflow-x: hidden;
        overflow-y: auto;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
        opacity: 0.65;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 800 600' xmlns='http://www.w3.org/2000/svg'%3E%3Cg stroke='%23ffffff44' stroke-width='1' fill='none'%3E%3Cpolygon points='100,100 200,80 250,180 150,200'/%3E%3Cpolygon points='300,200 400,180 450,280 350,300'/%3E%3Cpolygon points='600,100 700,80 750,180 650,200'/%3E%3Cpolygon points='500,350 600,330 650,430 550,450'/%3E%3Cline x1='100' y1='100' x2='400' y2='180'/%3E%3Cline x1='300' y1='200' x2='650' y2='200'/%3E%3Cline x1='150' y1='200' x2='350' y2='300'/%3E%3Cline x1='450' y1='280' x2='600' y2='330'/%3E%3C/g%3E%3Cg fill='%23ffffff22'%3E%3Ccircle cx='100' cy='100' r='4'/%3E%3Ccircle cx='200' cy='80' r='4'/%3E%3Ccircle cx='250' cy='180' r='4'/%3E%3Ccircle cx='150' cy='200' r='4'/%3E%3Ccircle cx='300' cy='200' r='4'/%3E%3Ccircle cx='400' cy='180' r='4'/%3E%3Ccircle cx='450' cy='280' r='4'/%3E%3Ccircle cx='350' cy='300' r='4'/%3E%3Ccircle cx='600' cy='100' r='4'/%3E%3Ccircle cx='700' cy='80' r='4'/%3E%3Ccircle cx='750' cy='180' r='4'/%3E%3Ccircle cx='650' cy='200' r='4'/%3E%3Ccircle cx='500' cy='350' r='4'/%3E%3Ccircle cx='600' cy='330' r='4'/%3E%3Ccircle cx='650' cy='430' r='4'/%3E%3Ccircle cx='550' cy='450' r='4'/%3E%3C/g%3E%3C/svg%3E");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }

    .block-container {
        position: relative;
        z-index: 1;
        padding-bottom: 0px;
        margin-bottom: 300px !important;
        min-height: 100vh !important;
    }

    main > div:has(.block-container) {
        padding-bottom: 0 !important;
    }

    .block-container > div:last-child {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    footer, footer:before, .st-emotion-cache-1avcm0n, .st-emotion-cache-q8sbsg {
        display: none;
        visibility: hidden;
        padding: 0;
        height: 0;
        margin: 0;
    }

    textarea, input[type="text"], .stTextInput input, .stTextArea textarea {
        background-color: #1c1c3c !important;
        color: #ffffff !important;
        border: 1px solid #5a189a !important;
        border-radius: 6px;
    }

    .stFileUploader {
        background-color: #1c1c3c !important;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #5a189a44;
        color: white;
    }

    button[kind="primary"] {
        background-color: #5a189a !important;
        color: white !important;
        border-radius: 8px;
        border: none;
    }

    button[kind="primary"]:hover {
        background-color: #7b2cbf !important;
    }

    label, .stTextInput label, .stTextArea label, .stFileUploader label {
        color: #eeeeee !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

#----------------hide sidebar elements-----------------
def hide_sidebar_pages():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] ul {
            display: flex;
            flex-direction: column;
        }

        /* Hide specific sidebar page links based on visible text */
        [data-testid="stSidebarNav"] li:has(a[href*="Form"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Dashboard"]),
        [data-testid="stSidebarNav"] li:has(a[href*="DataCollector"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Filter"]) {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


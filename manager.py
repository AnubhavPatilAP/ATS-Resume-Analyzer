import streamlit as st

# ------------------ Access Manager ------------------
def require_login():
    if st.session_state.get("current_page") == "Home":
        return
    if not st.session_state.get("signed_in", False):
        st.warning("🔒 You must be logged in to access this page.")
        st.stop()


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
        scroll-behavior: smooth;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
        opacity: 0.15;
        background-image: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
                          radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
                          radial-gradient(circle at 40% 20%, rgba(255,255,255,0.08) 0%, transparent 40%);
    }

    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 2rem !important;
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
        [data-testid="stSidebarNav"] li:has(a[href*="Individual_Analyzer"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Dashboard"]),
        [data-testid="stSidebarNav"] li:has(a[href*="DataCollector"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Filter"]) {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


import streamlit as st

# Access Manager
def require_login():
    if not st.session_state.get("signed_in", False):
        st.warning("🔒 You must be logged in to access this page.")
        st.stop()


# Navigation Manager
class NavigationManager:
    def __init__(self):
        self.pages = ['Home', 'IndividualAnalyzer', 'Account']

    def top_nav(self):
        col1, col2, col3, spacer = st.columns([1.2, 3.1, 1, 10])

        with col1:
            st.page_link("Home.py", label="Home")

        with col2:
            if st.session_state.get("signed_in", False):
                st.page_link("pages/Individual_Analyzer.py", label="IndividualAnalyzer")
            else:
                st.markdown("")

        with col3:
            if st.session_state.get("signed_in", False):
                st.page_link("pages/Account.py", label="Account")
            else:
                st.markdown("")
                
#Sidebar Styling
def apply_sidebar_style():
    st.markdown("""
        <style>
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #2C3E50;  /* Dark blue background */
                padding-top: 20px;
                border-right: 1px solid #5F4B8B;  /* Dark violet / purple border */
            }

            /* Sidebar Title */
            [data-testid="stSidebarNav"] {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #ecf0f1;  /* Light text color */
            }

            /* Sidebar Links */
            .css-1f6ctth {
                font-size: 16px;
                color: #ecf0f1;  /* Light text color for links */
            }

            /* Hover effect for sidebar links */
            .css-1f6ctth:hover {
                background-color: #5F4B8B;  /* Dark violet / purple hover background */
                border-radius: 4px;
                color: #ffffff;  /* White text on hover */
            }

            /* Active page link (optional) */
            .css-1f6ctth.stSelected {
                background-color: #5F4B8B;  /* Dark violet / purple active link background */
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
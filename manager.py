import streamlit as st

class NavigationManager:
    def __init__(self):
        self.pages = ['Home', 'IndividualAnalyzer', 'Account']

    def top_nav(self):
        # Use tighter column widths to avoid large gaps
        col1, col2, col3, spacer = st.columns([1.2, 3.1, 1, 10])

        with col1:
            st.page_link("Home.py", label="Home")

        with col2:
            st.page_link("pages/IndividualAnalyzer.py", label="IndividualAnalyzer")

        with col3:
            st.page_link("pages/account.py", label="Account")

import streamlit as st

st.set_page_config(page_title="Homepage", page_icon="🏡")
from manager import NavigationManager  

# Navigator
nav_manager = NavigationManager()
nav_manager.top_nav()

# Main content
st.title("🎯 Welcome to the Resume Analyzer")
st.write("Click below to analyze your resume.")

    


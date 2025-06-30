import streamlit as st
from manager import NavigationManager, apply_sidebar_style, set_background_css, hide_sidebar_pages

st.set_page_config(page_title="Homepage", page_icon="🏡")

# Styling
set_background_css()
apply_sidebar_style()
hide_sidebar_pages()
# Navigation bar
nav_manager = NavigationManager()
nav_manager.top_nav()

# Main page content
st.title("Welcome to the Resume Analyzer")
st.write("Choose your role below to get started:")

col1, col2 = st.columns(2)

with col1:
    st.subheader("For Individual")
    st.write("Upload and analyze your resume to get AI-based insights like ATS score, skill matching, and more.")
    if st.button("Analyze", key="individual"):
        st.switch_page("pages/Individual_Analyzer.py")


with col2:
    st.subheader("For Recruiter")
    st.write("Upload and filter multiple resumes, shortlist candidates by experience, skills, and qualifications.")
    if st.button("Analyze", key="recruiter"):
        st.switch_page("pages/Form.py")
 
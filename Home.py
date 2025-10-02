import streamlit as st
from manager import  apply_sidebar_style, set_background_css, hide_sidebar_pages

st.set_page_config(page_title="Homepage", page_icon="🏡")


# Styling
set_background_css()
apply_sidebar_style()
hide_sidebar_pages()



# Main page content
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 2.5em; margin-top: 0; margin-bottom: 0.3em;'>🎯 Welcome to Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #dcdcdc; font-size: 1.1em; margin-bottom: 1.5em;'>AI-Powered Resume Analysis for Job Seekers & Recruiters</p>", unsafe_allow_html=True)

# Create two columns with gap
col1, col2 = st.columns(2, gap="large")

with col1:
    # Individual Card
    st.markdown("""
        <div style='background: linear-gradient(135deg, #5a189a 0%, #7b2cbf 100%); 
                    padding: 1.5em; 
                    border-radius: 15px; 
                    border: 2px solid #9d4edd;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                    height: 330px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    margin-bottom: 1em;
                    overflow: hidden;'>
            <h2 style='color: #ffffff; text-align: center; margin-bottom: 0.5em; margin-top: 0;'>👤 For Individuals</h2>
            <p style='color: #e0e0e0; text-align: center; line-height: 1.5; font-size: 0.95em; margin-bottom: 0.8em;'>
                Get instant AI-powered feedback on your resume! Discover your ATS score, 
                skill matches, and personalized tips to land your dream job.
            </p>
            <ul style='color: #e0e0e0; margin: 0; padding-left: 2em; font-size: 0.9em; line-height: 1.8;'>
                <li>📊 ATS Score Analysis</li>
                <li>🎯 Skill Matching</li>
                <li>💡 Improvement Tips</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Analysis", key="individual", use_container_width=True):
        st.switch_page("pages/Individual_Analyzer.py")


with col2:
    # Recruiter Card
    st.markdown("""
        <div style='background: linear-gradient(135deg, #006494 0%, #0077b6 100%); 
                    padding: 1.5em; 
                    border-radius: 15px; 
                    border: 2px solid #0096c7;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                    height: 330px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    margin-bottom: 1em;
                    overflow: hidden;'>
            <h2 style='color: #ffffff; text-align: center; margin-bottom: 0.5em; margin-top: 0;'>💼 For Recruiters</h2>
            <p style='color: #e0e0e0; text-align: center; line-height: 1.5; font-size: 0.95em; margin-bottom: 0.8em;'>
                Screen hundreds of resumes in minutes! Smart filtering, ranking, 
                and shortlisting based on your job requirements.
            </p>
            <ul style='color: #e0e0e0; margin: 0; padding-left: 2em; font-size: 0.9em; line-height: 1.8;'>
                <li>📁 Bulk Resume Upload</li>
                <li>🔍 Smart Filtering</li>
                <li>📈 Candidate Ranking</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Start Screening", key="recruiter", use_container_width=True):
        st.switch_page("pages/Form.py")

# Add a features section
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #ffffff; margin-top: 1em; margin-bottom: 1em;'>✨ Why Choose Resume Analyzer?</h3>", unsafe_allow_html=True)

feat1, feat2, feat3, feat4 = st.columns(4)

with feat1:
    st.markdown("""
        <div style='text-align: center; padding: 1em;'>
            <div style='font-size: 3em;'>🤖</div>
            <h4 style='color: #ffffff;'>AI-Powered</h4>
            <p style='color: #dcdcdc; font-size: 0.9em;'>Advanced NLP technology</p>
        </div>
    """, unsafe_allow_html=True)

with feat2:
    st.markdown("""
        <div style='text-align: center; padding: 1em;'>
            <div style='font-size: 3em;'>⚡</div>
            <h4 style='color: #ffffff;'>Lightning Fast</h4>
            <p style='color: #dcdcdc; font-size: 0.9em;'>Results in seconds</p>
        </div>
    """, unsafe_allow_html=True)

with feat3:
    st.markdown("""
        <div style='text-align: center; padding: 1em;'>
            <div style='font-size: 3em;'>🔒</div>
            <h4 style='color: #ffffff;'>Secure</h4>
            <p style='color: #dcdcdc; font-size: 0.9em;'>Your data is safe</p>
        </div>
    """, unsafe_allow_html=True)

with feat4:
    st.markdown("""
        <div style='text-align: center; padding: 1em;'>
            <div style='font-size: 3em;'>📊</div>
            <h4 style='color: #ffffff;'>Accurate</h4>
            <p style='color: #dcdcdc; font-size: 0.9em;'>Professional insights</p>
        </div>
    """, unsafe_allow_html=True)

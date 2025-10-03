import streamlit as st
from manager import apply_sidebar_style, set_background_css, hide_sidebar_pages

# Page config
st.set_page_config(page_title="About", page_icon="ℹ️")

# Styling
set_background_css()
apply_sidebar_style()
hide_sidebar_pages()

# Page content
st.markdown("<h1 style='text-align: center; color: #ffffff; margin-bottom: 0.5em;'>ℹ️ About Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #dcdcdc; font-size: 1.1em; margin-bottom: 2em;'>Your AI Partner in Smart Hiring & Career Success</p>", unsafe_allow_html=True)

# Overview Section with Card
st.markdown("""
<div style='background: linear-gradient(135deg, #5a189a 0%, #7b2cbf 100%); 
            padding: 2em; 
            border-radius: 15px; 
            border: 2px solid #9d4edd;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            margin-bottom: 2em;'>
    <h2 style='color: #ffffff; margin-bottom: 1em;'>📌 Overview</h2>
    <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.8;'>
        The <strong>Resume Analyzer</strong> is a powerful AI-driven platform designed to help both 
        <strong>job seekers</strong> and <strong>recruiters</strong> make smarter hiring decisions.  
        It uses <strong>advanced natural language processing</strong> to extract, analyze, and compare 
        candidate data with job requirements, providing <strong>ATS-style scoring</strong>, 
        <strong>skill matching</strong>, and <strong>shortlisting recommendations</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# Who is this for section
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div style='background: rgba(90, 24, 154, 0.3); 
                padding: 1.5em; 
                border-radius: 12px; 
                border-left: 4px solid #9d4edd;
                height: 100%;'>
        <h3 style='color: #ffffff; margin-bottom: 1em;'>👤 For Job Seekers</h3>
        <p style='color: #e0e0e0; line-height: 1.6;'>
            Understand how your resume performs against job descriptions and identify improvement areas.
        </p>
        <ul style='color: #dcdcdc; margin-top: 1em;'>
            <li>Get instant ATS score</li>
            <li>Identify missing skills</li>
            <li>Receive actionable tips</li>
            <li>Stand out from competition</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: rgba(0, 100, 148, 0.3); 
                padding: 1.5em; 
                border-radius: 12px; 
                border-left: 4px solid #0096c7;
                height: 100%;'>
        <h3 style='color: #ffffff; margin-bottom: 1em;'>💼 For Recruiters</h3>
        <p style='color: #e0e0e0; line-height: 1.6;'>
            Quickly filter through hundreds of resumes, find the most relevant candidates, and make data-backed hiring choices.
        </p>
        <ul style='color: #dcdcdc; margin-top: 1em;'>
            <li>Process hundreds of resumes</li>
            <li>Smart filtering & ranking</li>
            <li>Visual analytics dashboard</li>
            <li>Export shortlisted candidates</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# How it Works
st.markdown("<h2 style='color: #ffffff; text-align: center; margin: 2em 0 1em 0;'>⚙️ How It Works</h2>", unsafe_allow_html=True)

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown("""
    <div style='text-align: center; padding: 1em; background: rgba(255,255,255,0.05); border-radius: 10px;'>
        <div style='font-size: 3em; margin-bottom: 0.5em;'>📤</div>
        <h4 style='color: #ffffff;'>1. Upload</h4>
        <p style='color: #dcdcdc; font-size: 0.9em;'>Upload your resume in PDF, Word, or Image format</p>
    </div>
    """, unsafe_allow_html=True)

with step2:
    st.markdown("""
    <div style='text-align: center; padding: 1em; background: rgba(255,255,255,0.05); border-radius: 10px;'>
        <div style='font-size: 3em; margin-bottom: 0.5em;'>🤖</div>
        <h4 style='color: #ffffff;'>2. AI Parse</h4>
        <p style='color: #dcdcdc; font-size: 0.9em;'>Extract skills, experience, and qualifications</p>
    </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
    <div style='text-align: center; padding: 1em; background: rgba(255,255,255,0.05); border-radius: 10px;'>
        <div style='font-size: 3em; margin-bottom: 0.5em;'>🎯</div>
        <h4 style='color: #ffffff;'>3. Match</h4>
        <p style='color: #dcdcdc; font-size: 0.9em;'>Compare against job requirements</p>
    </div>
    """, unsafe_allow_html=True)

with step4:
    st.markdown("""
    <div style='text-align: center; padding: 1em; background: rgba(255,255,255,0.05); border-radius: 10px;'>
        <div style='font-size: 3em; margin-bottom: 0.5em;'>📊</div>
        <h4 style='color: #ffffff;'>4. Score</h4>
        <p style='color: #dcdcdc; font-size: 0.9em;'>Get ATS score and insights</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Key Features
st.markdown("<h2 style='color: #ffffff; text-align: center; margin: 2em 0 1em 0;'>💡 Key Features</h2>", unsafe_allow_html=True)

st.markdown("""
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1em; margin-bottom: 2em;'>
    <div style='background: rgba(90, 24, 154, 0.2); padding: 1.5em; border-radius: 10px; border: 1px solid #5a189a;'>
        <h4 style='color: #ffffff;'>🔍 Resume Parsing</h4>
        <p style='color: #dcdcdc;'>Extracts structured data from any resume format with high accuracy</p>
    </div>
    <div style='background: rgba(90, 24, 154, 0.2); padding: 1.5em; border-radius: 10px; border: 1px solid #5a189a;'>
        <h4 style='color: #ffffff;'>📊 AI Scoring</h4>
        <p style='color: #dcdcdc;'>Calculates an ATS-style score for each resume automatically</p>
    </div>
    <div style='background: rgba(90, 24, 154, 0.2); padding: 1.5em; border-radius: 10px; border: 1px solid #5a189a;'>
        <h4 style='color: #ffffff;'>⚖️ Candidate Comparison</h4>
        <p style='color: #dcdcdc;'>Rank and shortlist based on multiple weighted criteria</p>
    </div>
    <div style='background: rgba(90, 24, 154, 0.2); padding: 1.5em; border-radius: 10px; border: 1px solid #5a189a;'>
        <h4 style='color: #ffffff;'>📈 Visual Dashboard</h4>
        <p style='color: #dcdcdc;'>Visualize trends in location, skills, qualifications and export to Excel</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Privacy & Why Use sections
st.markdown("""
<div style='background: linear-gradient(135deg, #006494 0%, #0077b6 100%); 
            padding: 2em; 
            border-radius: 15px; 
            border: 2px solid #0096c7;
            margin-bottom: 2em;'>
    <h2 style='color: #ffffff; margin-bottom: 1em;'>🔐 Data Privacy & Security</h2>
    <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.8;'>
        We value your privacy. All resumes and extracted data are stored securely in the cloud 
        and used <strong>only for analysis purposes</strong>. Your data is never shared with third parties.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: rgba(90, 24, 154, 0.3); 
            padding: 2em; 
            border-radius: 15px; 
            border: 2px solid #9d4edd;
            text-align: center;'>
    <h2 style='color: #ffffff; margin-bottom: 1em;'>🚀 Why Use Resume Analyzer?</h2>
    <p style='color: #e0e0e0; font-size: 1.1em; line-height: 1.8;'>
        Whether you're a <strong>fresh graduate</strong>, an <strong>experienced professional</strong>, 
        or a <strong>recruiter handling hundreds of applications</strong>, the Resume Analyzer saves time, 
        improves decision-making, and helps you focus on the <strong>right opportunities</strong>.
    </p>
    <p style='color: #dcdcdc; font-size: 1.2em; margin-top: 1em; font-weight: bold;'>
        ⚡ Save Time • 🎯 Make Better Decisions • 📈 Improve Success Rate
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")
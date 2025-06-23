import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Resume Insights Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Resume Insights Dashboard")
st.markdown("_Powered by Gemini & Streamlit_")

with st.sidebar:
    st.header("Upload Resume Excel")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx"])

if uploaded_file is None:
    st.info("Upload an Excel file generated from the resume parser", icon="ℹ️")
    st.stop()

@st.cache_data

def load_data(file):
    return pd.read_excel(file)

df = load_data(uploaded_file)

# Data Preview
with st.expander("▼ View Raw Data"):
    st.dataframe(df)

# Clean and preprocess
if 'total_experience' in df.columns:
    df['total_experience'] = pd.to_numeric(df['total_experience'], errors='coerce')

if 'key_skills' in df.columns:
    df['key_skills'] = df['key_skills'].astype(str)

#############################################
# Metric cards
#############################################
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Applicants", len(df))

with col2:
    avg_exp = df['total_experience'].mean().round(2) if 'total_experience' in df else 'N/A'
    st.metric("Avg. Experience (yrs)", avg_exp)

with col3:
    top_location = df['location'].mode()[0] if 'location' in df and not df['location'].isnull().all() else 'N/A'
    st.metric("Top Location", top_location)

with col4:
    top_job = df['recent_job_title'].mode()[0] if 'recent_job_title' in df and not df['recent_job_title'].isnull().all() else 'N/A'
    st.metric("Top Job Title", top_job)

#############################################
# Charts
#############################################

st.subheader("Applicant Distribution")

if 'location' in df.columns:
    top_locations = df['location'].value_counts().nlargest(10).reset_index()
    top_locations.columns = ['Location', 'Count']
    fig1 = px.bar(top_locations, x='Location', y='Count', title="Top Locations")
    st.plotly_chart(fig1, use_container_width=True)

if 'recent_job_title' in df.columns:
    job_counts = df['recent_job_title'].value_counts().nlargest(8).reset_index()
    job_counts.columns = ['Job Title', 'Count']
    fig2 = px.pie(job_counts, names='Job Title', values='Count', title="Recent Job Titles")
    st.plotly_chart(fig2, use_container_width=True)

if 'highest_qualification' in df.columns:
    edu_counts = df['highest_qualification'].value_counts().nlargest(7).reset_index()
    edu_counts.columns = ['Qualification', 'Count']
    fig3 = px.bar(edu_counts, x='Qualification', y='Count', title="Highest Qualification")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Key Skills Word Cloud")

if 'key_skills' in df.columns:
    text = ', '.join(df['key_skills'].dropna())
    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

st.markdown("---")
st.caption("Dashboard built for visualizing structured resume insights. Customize as needed!")

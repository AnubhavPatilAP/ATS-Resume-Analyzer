import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Resume Filter", page_icon="🧠", layout="wide")

@st.cache_data
def load_data(file):
    return pd.read_excel(file)

st.sidebar.title("📄 Upload Resume Data")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)

    # Show columns for debug
    st.write("📊 Columns in file:", df.columns.tolist())

    # Clean column names if needed
    df.columns = df.columns.str.strip()

    # Sidebar filters based on your criteria
    st.sidebar.header("🔍 Filter Candidates")

    genders = df["Gender"].dropna().unique() if "Gender" in df.columns else []
    locations = df["Location"].dropna().unique() if "Location" in df.columns else []
    qualifications = df["Highest Qualification"].dropna().unique() if "Highest Qualification" in df.columns else []
    titles = df["Most Recent Job Title"].dropna().unique() if "Most Recent Job Title" in df.columns else []

    selected_gender = st.sidebar.multiselect("Gender", options=genders, default=genders)
    selected_location = st.sidebar.multiselect("Location", options=locations, default=locations)
    selected_qualification = st.sidebar.multiselect("Highest Qualification", options=qualifications, default=qualifications)
    selected_titles = st.sidebar.multiselect("Recent Job Title", options=titles, default=titles)
    min_experience = st.sidebar.slider("Minimum Experience (Years)", 0, 30, 2)

    # Apply filters safely
    df_filtered = df[
        (df["Gender"].isin(selected_gender) if "Gender" in df.columns else True) &
        (df["Location"].isin(selected_location) if "Location" in df.columns else True) &
        (df["Highest Qualification"].isin(selected_qualification) if "Highest Qualification" in df.columns else True) &
        (df["Most Recent Job Title"].isin(selected_titles) if "Most Recent Job Title" in df.columns else True) &
        (df["Total Experience (in years)"] >= min_experience if "Total Experience (in years)" in df.columns else True)
    ]

    # Page title
    st.title("📋 Filtered Candidate Dashboard")

    if df_filtered.empty:
        st.warning("No candidates match the current filters.")
        st.stop()

    # Metrics
    st.markdown("### 📈 Overview")
    st.metric("Total Candidates", len(df_filtered))
    st.metric("Average Experience", round(df_filtered["Total Experience (in years)"].mean(), 2) if "Total Experience (in years)" in df_filtered.columns else "N/A")

    st.markdown("---")

    # Visuals
    if "Total Experience (in years)" in df_filtered.columns:
        exp_chart = px.histogram(df_filtered, x="Total Experience (in years)", nbins=10, title="Experience Distribution")
        st.plotly_chart(exp_chart, use_container_width=True)

    if "Key Skills (comma-separated)" in df_filtered.columns:
        skill_series = df_filtered["Key Skills (comma-separated)"].dropna().str.split(",").explode().str.strip().str.lower()
        top_skills = skill_series.value_counts().head(10)
        skill_chart = px.bar(
            top_skills,
            x=top_skills.values,
            y=top_skills.index,
            orientation="h",
            title="Top 10 Skills",
            labels={"x": "Count", "y": "Skill"},
            color_discrete_sequence=["#0083B8"]
        )
        st.plotly_chart(skill_chart, use_container_width=True)

    st.markdown("### 🧾 Matched Candidate Table")
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

else:
    st.info("Upload a parsed resume Excel file.")

# Hide Streamlit's default UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

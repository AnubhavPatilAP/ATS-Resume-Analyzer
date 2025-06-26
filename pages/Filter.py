import streamlit as st
import pandas as pd
import plotly.express as px
import io
from manager import NavigationManager, require_login, apply_sidebar_style, set_background_css
st.set_page_config(page_title="Resume Filter", page_icon="🧠", layout="wide")

# Apply styling
apply_sidebar_style()
set_background_css()
require_login()

EXPECTED_FIELDS = [
    "Full Name", "Gender", "Phone Number", "Email Address", "Location",
    "Total Experience", "Most Recent Job Title", "Highest Qualification", "Key Skills"
]

@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    return df

def clean_data(df):
    for field in EXPECTED_FIELDS:
        if field in df.columns:
            df[field] = df[field].astype(str).str.strip().str.lower()
            df = df[~df[field].isin(["", "n/a", "na", "none", "nan"])]
    return df.reset_index(drop=True)

def to_excel_download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Filtered")
    output.seek(0)
    return output

# Sidebar upload
st.sidebar.title("📄 Upload Resume Data")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    raw_df = load_data(uploaded_file)
    before_rows = len(raw_df)
    cleaned_df = clean_data(raw_df)
    after_rows = len(cleaned_df)

    st.title("📋 Cleaned Resume Data Preview")
    st.success(f"Cleaned data: removed {before_rows - after_rows} rows with invalid values.")
    st.dataframe(cleaned_df, use_container_width=True)

    # Sidebar filters
    st.sidebar.header("🔍 Filter Candidates")

    genders = sorted(set(cleaned_df["Gender"].dropna().astype(str).str.strip().str.title()))
    locations = sorted(set(cleaned_df["Location"].dropna().astype(str).str.strip().str.title()))
    qualifications = sorted(set(cleaned_df["Highest Qualification"].dropna().astype(str).str.strip().str.title()))
    titles = sorted(set(cleaned_df["Most Recent Job Title"].dropna().astype(str).str.strip().str.title()))

    # Extract skills from comma-separated "Key Skills"
    skill_series = cleaned_df["Key Skills"].dropna().str.split(",").explode().str.strip().str.lower()
    skill_options = sorted(set(skill_series))

    selected_gender = st.sidebar.multiselect("Gender", options=genders)
    selected_location = st.sidebar.multiselect("Location", options=locations)
    selected_qualification = st.sidebar.multiselect("Highest Qualification", options=qualifications)
    selected_titles = st.sidebar.multiselect("Recent Job Title", options=titles)
    selected_skills = st.sidebar.multiselect("Skills", options=skill_options)
    min_experience = st.sidebar.slider("Minimum Experience (Years)", 0, 30, 0)

    if st.sidebar.button("🔍 Apply Filters"):
        df_filtered = cleaned_df.copy()

        if selected_gender:
            df_filtered = df_filtered[
                df_filtered["Gender"].astype(str).str.strip().str.lower().isin(
                    [g.strip().lower() for g in selected_gender]
                )
            ]
        if selected_location:
            df_filtered = df_filtered[
                df_filtered["Location"].astype(str).str.strip().str.lower().isin(
                    [l.strip().lower() for l in selected_location]
                )
            ]
        if selected_qualification:
            df_filtered = df_filtered[
                df_filtered["Highest Qualification"].astype(str).str.strip().str.lower().isin(
                    [q.strip().lower() for q in selected_qualification]
                )
            ]
        if selected_titles:
            df_filtered = df_filtered[
                df_filtered["Most Recent Job Title"].astype(str).str.strip().str.lower().isin(
                    [t.strip().lower() for t in selected_titles]
                )
            ]
        if selected_skills:
            df_filtered = df_filtered[
                df_filtered["Key Skills"].apply(
                    lambda ks: any(skill in ks for skill in selected_skills)
                )
            ]
        if "Total Experience" in df_filtered.columns:
            df_filtered["Total Experience"] = pd.to_numeric(df_filtered["Total Experience"], errors="coerce")
            df_filtered = df_filtered[df_filtered["Total Experience"] >= min_experience]

        # Dashboard
        st.markdown("## 📊 Filtered Candidate Dashboard")

        if df_filtered.empty:
            st.warning("No candidates match the current filters.")
            st.stop()

        st.metric("Total Candidates", len(df_filtered))
        st.metric("Average Experience", round(df_filtered["Total Experience"].mean(), 2))

        exp_chart = px.histogram(df_filtered, x="Total Experience", nbins=10, title="Experience Distribution")
        st.plotly_chart(exp_chart, use_container_width=True)

        # Top skills bar chart
        if "Key Skills" in df_filtered.columns:
            skill_series = df_filtered["Key Skills"].dropna().str.split(",").explode().str.strip().str.lower()
            top_skills = skill_series.value_counts().head(10)
            if not top_skills.empty:
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

        st.download_button(
            label="📥 Download Filtered Data as Excel",
            data=to_excel_download(df_filtered),
            file_name="filtered_candidates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Upload a parsed resume Excel file to begin.")

# Hide Streamlit branding
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

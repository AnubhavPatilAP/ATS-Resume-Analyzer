import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Resume Filter", page_icon="🧠", layout="wide")

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
    # Drop rows with N/A or empty strings for expected fields
    for field in EXPECTED_FIELDS:
        if field in df.columns:
            df = df[df[field].astype(str).str.strip().str.upper() != "N/A"]
            df = df[df[field].astype(str).str.strip() != ""]
    return df.reset_index(drop=True)

def to_excel_download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Filtered")
    output.seek(0)
    return output

# Upload section
st.sidebar.title("📄 Upload Resume Data")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    raw_df = load_data(uploaded_file)
    cleaned_df = clean_data(raw_df)

    st.title("📋 Cleaned Resume Data Preview")
    st.dataframe(cleaned_df, use_container_width=True)

    # Sidebar filters
    st.sidebar.header("🔍 Filter Candidates")

    genders = sorted(set(cleaned_df["Gender"].dropna().astype(str).str.strip().str.title()))
    locations = sorted(set(cleaned_df["Location"].dropna().astype(str).str.strip().str.title()))
    qualifications = sorted(set(cleaned_df["Highest Qualification"].dropna().astype(str).str.strip().str.title()))
    titles = sorted(set(cleaned_df["Most Recent Job Title"].dropna().astype(str).str.strip().str.title()))

    selected_gender = st.sidebar.multiselect("Gender", options=genders)
    selected_location = st.sidebar.multiselect("Location", options=locations)
    selected_qualification = st.sidebar.multiselect("Highest Qualification", options=qualifications)
    selected_titles = st.sidebar.multiselect("Recent Job Title", options=titles)
    min_experience = st.sidebar.slider("Minimum Experience (Years)", 0, 30, 0)

    if st.sidebar.button("🔍 Apply Filters"):
        df_filtered = cleaned_df.copy()

        if selected_gender:
            df_filtered = df_filtered[
                df_filtered["Gender"].astype(str).str.strip().str.lower().isin(
                    [g.lower().strip() for g in selected_gender]
                )
            ]

        if selected_location:
            df_filtered = df_filtered[
                df_filtered["Location"].astype(str).str.strip().str.lower().isin(
                    [l.lower().strip() for l in selected_location]
                )
            ]

        if selected_qualification:
            df_filtered = df_filtered[
                df_filtered["Highest Qualification"].astype(str).str.strip().str.lower().isin(
                    [q.lower().strip() for q in selected_qualification]
                )
            ]

        if selected_titles:
            df_filtered = df_filtered[
                df_filtered["Most Recent Job Title"].astype(str).str.strip().str.lower().isin(
                    [t.lower().strip() for t in selected_titles]
                )
            ]

        if "Total Experience" in df_filtered.columns:
            df_filtered["Total Experience"] = pd.to_numeric(df_filtered["Total Experience"], errors="coerce")
            df_filtered = df_filtered[df_filtered["Total Experience"] >= min_experience]

        # Filtered data
        st.markdown("## 📊 Filtered Candidate Dashboard")

        if df_filtered.empty:
            st.warning("No candidates match the current filters.")
            st.stop()

        st.metric("Total Candidates", len(df_filtered))
        st.metric("Average Experience", round(df_filtered["Total Experience"].mean(), 2))

        # Charts
        exp_chart = px.histogram(df_filtered, x="Total Experience", nbins=10, title="Experience Distribution")
        st.plotly_chart(exp_chart, use_container_width=True)

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

        # Final table and download
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

# Hide Streamlit UI branding
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

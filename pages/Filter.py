import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from manager import NavigationManager, require_login, apply_sidebar_style, set_background_css, hide_sidebar_pages

# --- Page setup ---
st.set_page_config(page_title="Resume Filter", page_icon="🧠", layout="wide")

# Apply styling
apply_sidebar_style()
set_background_css()

hide_sidebar_pages()
require_login()

st.title("🔍 Manually Filter Applicants")

# --- Load Cleaned Data from Session ---
if "df" not in st.session_state:
    st.warning("No data found. Please visit the Dashboard first.")
    st.stop()

df = st.session_state.df.copy()
df.columns = df.columns.str.strip().str.lower()

# --- Helper to find matching columns dynamically ---
def get_matching_column(possible_keywords):
    for col in df.columns:
        if any(keyword in col for keyword in possible_keywords):
            return col
    return None

# --- Filters ---
st.subheader("📋 Filter Criteria")

col1, col2 = st.columns(2)

with col1:
    gender_col = get_matching_column(["gender"])
    if gender_col:
        genders = sorted(set(df[gender_col].dropna().astype(str).str.strip().str.title()))
        selected_gender = st.multiselect("Gender", options=genders)
    else:
        selected_gender = []

    qualification_col = get_matching_column(["qualification", "education"])
    if qualification_col:
        qualifications = sorted(set(df[qualification_col].dropna().astype(str).str.strip().str.title()))
        selected_qualification = st.multiselect("Qualification", options=qualifications)
    else:
        selected_qualification = []

    experience_col = get_matching_column(["experience"])
    if experience_col:
        exp_values = pd.to_numeric(df[experience_col], errors="coerce")
        min_exp, max_exp = (int(exp_values.min()), int(exp_values.max())) if not exp_values.empty else (0, 30)
        selected_exp = st.slider("Experience (Years)", min_exp, max_exp, (min_exp, max_exp))
    else:
        selected_exp = (0, 30)

with col2:
    title_col = get_matching_column(["job title"])
    if title_col:
        titles = sorted(set(df[title_col].dropna().astype(str).str.strip().str.title()))
        selected_titles = st.multiselect("Job Title", options=titles)
    else:
        selected_titles = []

    location_col = get_matching_column(["location"])
    if location_col:
        locations = sorted(set(df[location_col].dropna().astype(str).str.strip().str.title()))
        selected_locations = st.multiselect("Location", options=locations)
    else:
        selected_locations = []

    skills_col = get_matching_column(["skill"])
    if skills_col:
        skill_series = df[skills_col].dropna().str.split(",").explode().str.strip().str.title()
        skill_options = sorted(set(skill_series))
        selected_skills = st.multiselect("Skills", options=skill_options)
    else:
        selected_skills = []

# --- Apply Filters ---
if st.button("Apply Filters"):
    df_filtered = df.copy()

    if selected_gender and gender_col:
        df_filtered = df_filtered[df_filtered[gender_col].str.title().isin(selected_gender)]

    if selected_qualification and qualification_col:
        df_filtered = df_filtered[df_filtered[qualification_col].str.title().isin(selected_qualification)]

    if selected_titles and title_col:
        df_filtered = df_filtered[df_filtered[title_col].str.title().isin(selected_titles)]

    if selected_locations and location_col:
        df_filtered = df_filtered[df_filtered[location_col].str.title().isin(selected_locations)]

    if selected_skills and skills_col:
        df_filtered = df_filtered[df_filtered[skills_col].apply(lambda ks: any(skill in ks.title() for skill in selected_skills))]

    if experience_col:
        df_filtered[experience_col] = pd.to_numeric(df_filtered[experience_col], errors="coerce")
        df_filtered = df_filtered[df_filtered[experience_col].between(selected_exp[0], selected_exp[1])]

    st.markdown("## 🧾 Filtered Results")

    if df_filtered.empty:
        st.warning("No applicants match the selected filters.")
    else:
        st.success(f"Filtered {len(df_filtered)} applicants.")
        st.dataframe(df_filtered, use_container_width=True)

        st.download_button(
            label="Download Filtered Data",
            data=df_filtered.to_csv(index=False).encode("utf-8"),
            file_name="filtered_applicants.csv",
            mime="text/csv"
        )
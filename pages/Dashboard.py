import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from manager import NavigationManager, require_login, apply_sidebar_style, set_background_css
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# --- Page setup ---
st.set_page_config(page_title="Resume Insights Dashboard", page_icon=":bar_chart:", layout="wide")

# --- Styling & Auth ---
set_background_css()
apply_sidebar_style()
require_login()

# --- Navigator ---
nav_manager = NavigationManager()
nav_manager.top_nav()

# --- Title ---
st.title("Resume Insights Dashboard")
st.markdown("_Powered by Groq, Firebase & Streamlit_")

# --- Get Job Criteria from Session ---
job_criteria = st.session_state.get("prefill_criteria") or st.session_state.get("selected_job_criteria")

if not job_criteria:
    st.warning("⚠️ Job criteria not found. Please fill the form or select from your history.")
    st.stop()
 

# --- Load data from session_state ---
if "df" not in st.session_state or st.session_state.df.empty:
    st.error("❌ No resume data found. Please upload or parse resumes first on the parser page.")
    st.stop()

df = st.session_state.df.copy()

# -------------------------------------
# 🧹 Advanced Filter & Rank Candidates
# -------------------------------------
min_experience = float(job_criteria.get("min_experience", 0))
required_skills = job_criteria.get("must_have_skills", [])
is_remote_allowed = job_criteria.get("is_remote", True)
job_location = job_criteria.get("location", "").strip().lower()

# --- Identify column containing 'experience' ---
exp_col = next((col for col in df.columns if 'experience' in col.lower()), None)

if exp_col:
    df[exp_col] = pd.to_numeric(df[exp_col], errors='coerce').fillna(0)
    df.rename(columns={exp_col: "total_experience"}, inplace=True)
else:
    st.error("❌ No column with 'experience' found. Please check your uploaded data.")
    st.stop()

# Identify and normalize 'ats' column
ats_col = next((col for col in df.columns if 'ats' in col.lower()), None)
if ats_col:
    df[ats_col] = pd.to_numeric(df[ats_col], errors='coerce')
    df.rename(columns={ats_col: "ats_score"}, inplace=True)
else:
    st.error("❌ No column containing 'ATS score' found.")
    st.stop()

# Identify the skills column
skills_col = next((col for col in df.columns if 'skill' in col.lower()), None)

if skills_col:
    df[skills_col] = df[skills_col].astype(str)
    df.rename(columns={skills_col: "key_skills"}, inplace=True)
else:
    st.error("❌ No column containing 'skills' found.")
    st.stop()

# Identify the location column
location_col = next((col for col in df.columns if 'location' in col.lower()), None)

if location_col:
    df.rename(columns={location_col: "location"}, inplace=True)
else:
    st.error("❌ No column containing 'location' found in the uploaded data.")
    st.stop()


# Clean data
cleaned_df = df[df['ats_score'].notnull()].copy()


# 🧾 Display Cleaned-Out Applicants
st.subheader("🧹 Cleaned Data (Removed Applicants)")
removed_rows = df[~df.index.isin(cleaned_df.index)]

if removed_rows.empty:
    st.info("No rows were removed during cleaning.")
else:
    with st.expander("📂 View Removed Applicants"):
        st.dataframe(removed_rows)



# Normalize and calculate skill match %
def compute_skill_match_percent(skills_string):
    candidate_skills = [s.strip().lower() for s in skills_string.split(",") if s.strip()]
    matched = sum(1 for skill in required_skills if skill.lower() in candidate_skills)
    return round((matched / len(required_skills)) * 100, 2) if required_skills else 0

cleaned_df["skill_match_pct"] = cleaned_df["key_skills"].apply(compute_skill_match_percent)

# Location check
def location_matches(candidate_location):
    if is_remote_allowed:
        return 1  # Always match
    return 1 if candidate_location.strip().lower() == job_location else 0

cleaned_df["location_match"] = cleaned_df["location"].apply(location_matches)

# Filter shortlisted
shortlisted_df = cleaned_df[
    (cleaned_df["total_experience"] >= min_experience) &
    (cleaned_df["skill_match_pct"] >= 70) &
    (cleaned_df["location_match"] == 1)
].copy()

# Rank candidates: ATS (high), Experience (high), Skill Match (high), Location Match
shortlisted_df = shortlisted_df.sort_values(
    by=["ats_score", "total_experience", "skill_match_pct", "location_match"],
    ascending=[False, False, False, False]
).reset_index(drop=True)

# ---------------------------
# 📊 Analysis Section
# ---------------------------
st.header("📊 Analysis Overview")

# 1. Total Applicants vs Shortlisted
col1, col2 = st.columns(2)
col1.metric("Total Applicants", len(df))
col2.metric("Shortlisted Applicants", len(shortlisted_df))

# 2. Ranked Shortlisted Excel View
st.subheader("📋 Ranked Shortlisted Applicants")
st.dataframe(shortlisted_df)

# 3. Rejected Applicants
rejected_df = cleaned_df[~cleaned_df.index.isin(shortlisted_df.index)]
with st.expander("📂 View Rejected Applicants"):
    st.dataframe(rejected_df)

# 4. Gender Ratio
if 'gender' in shortlisted_df.columns:
    gender_counts = shortlisted_df['gender'].value_counts()
    st.subheader("⚖️ Gender Ratio (Shortlisted)")
    fig_gender = px.pie(names=gender_counts.index, values=gender_counts.values, title="Gender Distribution")
    st.plotly_chart(fig_gender)

# 5. Average Experience
avg_exp = df['total_experience'].mean().round(2)
st.metric("📊 Average Experience (yrs)", avg_exp)

# 6. Top 5% Applicants
top_5pct = int(len(shortlisted_df) * 0.05)
top_5_df = shortlisted_df.head(top_5pct if top_5pct > 0 else 1)
with st.expander("🏅 Top 5% Applicants (by Rank)"):
    st.dataframe(top_5_df)

# 7. Unmatched Skills
st.subheader("🔍 Skills Not in Criteria")
all_candidate_skills = pd.Series(
    skill.strip().lower()
    for skills in cleaned_df['key_skills'].dropna()
    for skill in skills.split(',') if skill.strip()
)
criteria_skills = set(skill.lower() for skill in required_skills)
unmatched_skills = all_candidate_skills[~all_candidate_skills.isin(criteria_skills)]
if not unmatched_skills.empty:
    unmatched_counts = unmatched_skills.value_counts().nlargest(10)
    fig_unmatched = px.bar(
        unmatched_counts.reset_index(),
        x='index', y='count',
        labels={'index': 'Skill', 'count': 'Occurrences'},
        title="Top Skills Not in Job Criteria"
    )
    st.plotly_chart(fig_unmatched)
else:
    st.info("All listed skills were in the job criteria.")

# 8. Applicant Location Map (Each Applicant)
st.subheader("🗺️ Applicant Location Map (Each Applicant)")

if "location" in df.columns and not df["location"].dropna().empty:
    # Clean and prepare location data
    location_df = df[["location"]].dropna().copy()
    location_df["location_clean"] = location_df["location"].astype(str).str.strip()
    location_df = location_df.drop_duplicates().reset_index(drop=True)

    # Geocoder setup (OpenStreetMap / Nominatim)
    geolocator = Nominatim(user_agent="resume_mapper")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    @st.cache_data(show_spinner="Geocoding applicant locations...")
    def get_lat_lon_map(locations):
        lat_lon_map = {}
        for loc in locations:
            try:
                g = geocode(loc)
                if g:
                    lat_lon_map[loc] = (g.latitude, g.longitude)
                else:
                    lat_lon_map[loc] = (None, None)
            except:
                lat_lon_map[loc] = (None, None)
        return lat_lon_map

    coords_map = get_lat_lon_map(location_df["location_clean"])
    location_df["latitude"] = location_df["location_clean"].map(lambda x: coords_map[x][0])
    location_df["longitude"] = location_df["location_clean"].map(lambda x: coords_map[x][1])

    # Drop any that failed geocoding
    location_df = location_df.dropna(subset=["latitude", "longitude"])

    if not location_df.empty:
        location_df["Applicant ID"] = location_df.index + 1
        fig_map = px.scatter_geo(
            location_df,
            lat="latitude",
            lon="longitude",
            hover_name="location_clean",  # Only show location on hover
            projection="natural earth",
            title="📍 Locations of All Applicants (Geocoded)",
            template="plotly_dark"
        )
        # Show dots only
        fig_map.update_traces(marker=dict(size=6, color='deepskyblue'))

        fig_map.update_geos(showframe=False, showcoastlines=True)
        fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ No valid geocoded locations to display.")
else:
    st.info("🌐 Location data is missing or invalid for applicants.")


# --- Spacing before footer action ---
st.markdown("###")  # Adds vertical space

# --- Manual Filter Button ---
st.markdown(
    """
    <div style="text-align: center; padding: 30px 0;">
        <a href="#" style="
            background-color: #5a189a;
            color: white;
            padding: 15px 40px;
            font-size: 18px;
            text-decoration: none;
            border-radius: 12px;
            font-weight: bold;
            transition: background-color 0.3s ease;">
            🔍 Manually Filter Applicants
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("###")
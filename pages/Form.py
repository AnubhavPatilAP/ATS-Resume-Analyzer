import streamlit as st

st.title("🎯 Resume Shortlisting Criteria")

with st.form("shortlisting_form"):
    st.subheader("📌 Basic Job Criteria")
    role = st.text_input("Job Title / Role", placeholder="e.g. Backend Developer")
    must_have_skills = st.text_area("Must-Have Skills", placeholder="Comma-separated, e.g. Python, Django, PostgreSQL")
    nice_to_have_skills = st.text_area("Nice-to-Have Skills", placeholder="Optional, e.g. AWS, Docker")

    st.subheader("📈 Experience")
    min_experience = st.slider("Minimum Required Years of Experience", 0, 20, 2)

    st.subheader("🎓 Education")
    education_level = st.selectbox("Minimum Education Level", ["Any", "Bachelor's", "Master's", "PhD"])

    st.subheader("📜 Certifications")
    required_certs = st.text_area("Required Certifications", placeholder="Optional, e.g. AWS Certified Developer")

    st.subheader("📍 Location")
    preferred_locations = st.text_area("Preferred Locations", placeholder="e.g. Bangalore, Remote")
    remote_allowed = st.checkbox("Remote Work Allowed", value=True)

    st.subheader("⚠️ Red Flags to Avoid")
    red_flags = st.text_area("e.g. Frequent job changes, long employment gaps")

    st.subheader("⚙️ Shortlisting Logic")
    strict_filter = st.checkbox("Disqualify if must-have skills are missing", value=True)
    weightage = st.select_slider("Scoring Preference", options=["Skills", "Balanced", "Experience"], value="Balanced")

    submitted = st.form_submit_button("✅ Submit Criteria")

if submitted:
    criteria = {
        "role": role,
        "must_have_skills": [s.strip().lower() for s in must_have_skills.split(",") if s.strip()],
        "nice_to_have_skills": [s.strip().lower() for s in nice_to_have_skills.split(",") if s.strip()],
        "min_experience": min_experience,
        "education_level": education_level,
        "required_certs": [s.strip().lower() for s in required_certs.split(",") if s.strip()],
        "preferred_locations": [s.strip().lower() for s in preferred_locations.split(",") if s.strip()],
        "remote_allowed": remote_allowed,
        "red_flags": [s.strip().lower() for s in red_flags.split(",") if s.strip()],
        "strict_filtering": strict_filter,
        "weightage_pref": weightage
    }

    st.success("Shortlisting criteria submitted!")
    st.json(criteria)

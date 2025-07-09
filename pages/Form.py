import streamlit as st
from manager import require_login, apply_sidebar_style, set_background_css, hide_sidebar_pages
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import os

# Apply styling
apply_sidebar_style()
set_background_css()
hide_sidebar_pages()
require_login()

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('test-23ffe-cf207eed55fe.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Safe redirection if redirected from another page
if "redirect_to" in st.session_state:
    target_page = st.session_state.pop("redirect_to")
    try:
        st.switch_page(f"pages/{target_page}.py")
    except Exception as e:
        st.error(f"Failed to redirect to page '{target_page}': {e}")
        st.stop()

# Get user ID from session
user_id = st.session_state.get("user_id")
if not user_id:
    st.error("User ID not found in session. Please log in again.")
    st.stop()

# Pre-fill criteria if editing
prefill = st.session_state.get("prefill_criteria", {})
if not isinstance(prefill, dict):
    prefill = {}

st.title("Resume Shortlisting Criteria")

# --- Form ---
with st.form("shortlisting_form"):
    st.subheader("Basic Job Criteria")

    role = st.text_input("Job Title / Role", value=prefill.get("role", ""), placeholder="e.g. Backend Developer")

    job_description = st.text_area(
        "Job Description (Roles and Responsibilities)",
        value=prefill.get("job_description", ""),
        placeholder="Describe in short",
        help="Limit to around 500 words"
    )

    must_have_skills = st.text_area(
        "Must-Have Skills",
        value=", ".join(prefill.get("must_have_skills", [])),
        placeholder="Comma-separated, e.g. Python, Django, PostgreSQL"
    )

    st.subheader("Experience")
    min_experience = st.text_input(
        "Minimum Required Years of Experience",
        value=str(prefill.get("min_experience", "")),
        placeholder="e.g. 2",
        help="Enter a number only"
    )

    st.subheader("Education")
    education_options = ["Any", "Diploma", "Bachelor's", "Master's", "PhD"]
    default_education = prefill.get("education_level", "Any")
    if default_education not in education_options:
        default_education = "Any"
    education_level = st.selectbox("Minimum Education Level", education_options, index=education_options.index(default_education))

    st.subheader("Certifications")
    required_certs = st.text_area(
        "Required Certifications",
        value=", ".join(prefill.get("required_certs", [])),
        placeholder="Optional, e.g. AWS Certified Developer"
    )

    st.subheader("Location")
    preferred_locations = st.text_area(
        "Preferred Locations",
        value=", ".join(prefill.get("preferred_locations", [])),
        placeholder="e.g. Bangalore, Remote"
    )

    remote_allowed = st.checkbox("Remote Work Allowed", value=prefill.get("remote_allowed", True))

    submitted = st.form_submit_button("Submit Criteria")

# --- On Submit ---
if submitted:
    try:
        min_experience_int = int(min_experience)
    except ValueError:
        st.error("Minimum experience must be a valid number.")
    else:
        criteria = {
            "role": role,
            "job_description": job_description,
            "must_have_skills": [s.strip().lower() for s in must_have_skills.split(",") if s.strip()],
            "min_experience": min_experience_int,
            "education_level": education_level,
            "required_certs": [s.strip().lower() for s in required_certs.split(",") if s.strip()],
            "preferred_locations": [s.strip().lower() for s in preferred_locations.split(",") if s.strip()],
            "remote_allowed": remote_allowed
        }

        try:
            # Save to Firestore
            criteria_id = str(uuid.uuid4())
            db.collection("criteria").document(user_id).collection("submissions").document(criteria_id).set(criteria)

            # Save to session state for next page
            st.session_state["current_criteria"] = criteria

            # Clear any previously prefilling state
            st.session_state.pop("prefill_criteria", None)

            # Just rerun the script, let Form.py's top section handle the redirection
            st.session_state["redirect_to"] = "DataCollector"
            st.rerun()

        except Exception as e:
            st.error(f"Error saving to Firestore: {e}")



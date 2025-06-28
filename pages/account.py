import streamlit as st
import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import uuid
from manager import NavigationManager, require_login, apply_sidebar_style, set_background_css
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Apply global styling and navigation
apply_sidebar_style()
set_background_css()
nav_manager = NavigationManager()
nav_manager.top_nav()

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('test-23ffe-cf207eed55fe.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Firebase REST login using email/password
def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    return requests.post(url, json=payload).json()

# Clear session on logout
def logout():
    for key in ["signed_in", "username", "useremail", "user_id", "prefill_criteria", "selected_job_criteria"]:
        st.session_state.pop(key, None)

# App Entry
def app():
    st.title("Get Started")

    # Init session
    for key in ["signed_in", "username", "useremail", "user_id", "prefill_criteria", "selected_job_criteria"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key != "signed_in" else False

    # --- Auth Section ---
    if not st.session_state.signed_in:
        choice = st.selectbox("Login / Sign Up", ["Login", "Sign Up"])

        # Login flow
        if choice == "Login":
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if not email or not password:
                    st.warning("Please fill in both fields.")
                else:
                    result = login_user(email, password)
                    if "idToken" in result:
                        st.session_state.signed_in = True
                        st.session_state.useremail = email

                        # Fetch UID from Firestore
                        users_ref = db.collection("users")
                        docs = users_ref.where("email", "==", email).stream()
                        for doc in docs:
                            user_data = doc.to_dict()
                            st.session_state.username = user_data.get("username")
                            st.session_state.user_id = doc.id
                            break
                        else:
                            st.error("User ID not found. Please sign up again.")
                            st.session_state.signed_in = False
                            return

                        st.success("Logged in successfully!")
                        st.switch_page("Home.py")
                    else:
                        st.error(f"Login failed: {result.get('error', {}).get('message', 'Unknown error')}")

        # Sign-up flow
        else:
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            username = st.text_input("Choose a Username")

            if st.button("Create"):
                if not email or not password or not username:
                    st.warning("Please fill in all fields.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    try:
                        uid = str(uuid.uuid4())
                        auth.create_user(email=email, password=password, uid=uid)

                        db.collection("users").document(uid).set({
                            "email": email,
                            "username": username
                        })

                        st.success("Account created! You can now log in.")
                        st.balloons()
                    except Exception as e:
                        err_msg = str(e)
                        if "email-already-exists" in err_msg:
                            st.error("This email is already registered.")
                        else:
                            st.error(f"Error: {err_msg}")

    # --- Logged In View ---
    else:
        st.subheader("You're logged in!")
        st.text(f"Username: {st.session_state.username}")
        st.text(f"Email: {st.session_state.useremail}")
        st.button("Sign Out", on_click=logout)

        st.markdown("---")
        st.subheader("Your Previous Shortlisting Criteria")

        user_id = st.session_state.get("user_id")
        if not user_id:
            st.error("User ID missing in session.")
            return

        # Fetch saved criteria
        submissions_ref = db.collection("criteria").document(user_id).collection("submissions")
        submissions = submissions_ref.stream()

        found = False
        for doc in submissions:
            found = True
            data = doc.to_dict()
            submission_id = doc.id

            with st.expander(f"Role: {data.get('role', 'N/A')}"):
                st.write(f"**Job Description:** {data.get('job_description', '')[:200]}...")
                st.write(f"**Experience:** {data.get('min_experience')} years")
                st.write(f"**Education:** {data.get('education_level')}")
                st.write(f"**Must-Have Skills:** {', '.join(data.get('must_have_skills', []))}")
                st.write(f"**Preferred Locations:** {', '.join(data.get('preferred_locations', []))}")

                col1, col2 = st.columns(2)

                # Use this criteria
                with col1:
                    if st.button("Use Criteria to Analyze Resumes", key=f"use_{submission_id}"):
                        st.session_state.selected_job_criteria = data
                        st.switch_page("pages/DataCollector.py")

                # Delete criteria
                with col2:
                    if st.button("Delete", key=f"delete_{submission_id}"):
                        db.collection("criteria").document(user_id).collection("submissions").document(submission_id).delete()
                        st.success("Entry deleted.")
                        st.rerun()

        if not found:
            st.info("No shortlisting criteria found.")

# Run app
app()

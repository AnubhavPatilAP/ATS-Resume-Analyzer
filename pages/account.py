import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
from manager import NavigationManager  

# Navigator
nav_manager = NavigationManager()
nav_manager.top_nav()



# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('test-23ffe-cf207eed55fe.json')
    firebase_admin.initialize_app(cred)

# Firebase Web API Key
FIREBASE_API_KEY = "AIzaSyB0mtsBJvRdMI-c7mIrqmCaEb9T_eqOf-E"

# Function to handle login
def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

# Sign out function
def logout():
    st.session_state.signed_in = False
    st.session_state.username = ""
    st.session_state.useremail = ""

# App start
def app():
    st.title("Get Started")

    # Session state initialization
    if "signed_in" not in st.session_state:
        st.session_state.signed_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "useremail" not in st.session_state:
        st.session_state.useremail = ""

    # Show login/signup only if not signed in
    if not st.session_state.signed_in:
        choice = st.selectbox("Login / Sign Up", ["Login", "Sign Up"])

        if choice == "Login":
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if not email or not password:
                    st.warning("Please fill in both fields.")
                else:
                    result = login_user(email, password)
                    if "idToken" in result:
                        st.success(f"Welcome back, {email}!")
                        st.session_state.signed_in = True
                        st.session_state.useremail = email
                        st.session_state.username = email.split("@")[0]
                    else:
                        error_msg = result.get("error", {}).get("message", "Login failed")
                        st.error(f"Login failed: {error_msg}")

        elif choice == "Sign Up":
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            username = st.text_input("Enter your username (used as UID)")

            if st.button("Create"):
                if not email or not password or not username:
                    st.warning("Please fill in all fields.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    try:
                        user = auth.create_user(
                            email=email,
                            password=password,
                            uid=username
                        )
                        st.success("Account created successfully!")
                        st.markdown("You can now log in using your credentials.")
                        st.balloons()
                    except Exception as e:
                        err_msg = str(e)
                        if "email-already-exists" in err_msg:
                            st.error("This email is already registered.")
                        elif "uid-already-exists" in err_msg:
                            st.error("This username (UID) is already taken.")
                        else:
                            st.error(f"Error: {err_msg}")
    else:
        # Show this only when signed in
        st.subheader("You're logged in!")
        st.text(f"Name: {st.session_state.username}")
        st.text(f"Email: {st.session_state.useremail}")
        st.button("Sign Out", on_click=logout)

app()

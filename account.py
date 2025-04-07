import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate('test-23ffe-cf207eed55fe.json')
    firebase_admin.initialize_app(cred)

# Your Firebase Web API Key
FIREBASE_API_KEY = "AIzaSyB0mtsBJvRdMI-c7mIrqmCaEb9T_eqOf-E"

# Function to handle login using Firebase REST API
def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

# Streamlit App
def app():
    st.title('Get Started')

    choice = st.selectbox('Login / Sign Up', ['Login', 'Sign Up'])

    if choice == 'Login':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            if not email or not password:
                st.warning("Please fill in both fields.")
            else:
                result = login_user(email, password)
                if 'idToken' in result:
                    st.success(f"Welcome back, {result['email']}!")
                else:
                    error_msg = result.get("error", {}).get("message", "Login failed")
                    st.error(f"Login failed: {error_msg}")

    else:  # Sign Up
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input('Enter your username (used as UID)')

        if st.button('Create'):
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
                except auth.EmailAlreadyExistsError:
                    st.error("This email is already registered.")
                except auth.UidAlreadyExistsError:
                    st.error("This username (UID) is already taken.")
                except Exception as e:
                    st.error(f"Error: {e}")

app()

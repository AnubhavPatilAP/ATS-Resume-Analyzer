import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import tempfile
import pdfplumber
from PIL import Image
import pytesseract
import firebase_admin
from firebase_admin import credentials, firestore
import time  # Import the time module

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Firebase
FIREBASE_JSON = "D:/Resume Analyzer/test-23ffe-cf207eed55fe.json"  # Update with your path

db = None
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_JSON)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
else:
    db = firestore.client()

# Configure Gemini API
model = None
available_models = []
if google_api_key:
    try:
        genai.configure(api_key=google_api_key)

        # --- List Available Models (TEMPORARY - CRITICAL FIX) ---
        try:
            available_models = [m.name for m in genai.list_models()]
            st.info(f"Available Gemini models: {available_models}")  # Show models to user
            if not available_models:  # Check if the list is empty
                st.error("No Gemini models found. Please check your API key and connection.")
                st.stop()  # Stop execution if no models are available
        except Exception as e_list:
            st.error(f"Error listing models: {e_list}")
            st.stop()  # Stop execution if listing models fails
        # --- End of List Available Models ---

        model_name_to_try = ['models/gemini-1.5-pro-latest', 'models/gemini-1.5-pro', 'models/gemini-1.0-pro-vision-latest', 'models/gemini-pro-vision']  # <--- UPDATE THIS LINE

        for model_name in model_name_to_try:
            if model_name in available_models: # Check if the model is in the list
                try:
                    model = genai.GenerativeModel(model_name)
                    st.info(f"Successfully initialized model: {model_name}")
                    break  # Exit the loop once a model is successfully initialized
                except Exception as e:
                    st.error(f"Error initializing model '{model_name}': {e}")
            else:
                st.error(f"Model '{model_name}' not found in available models.")

        if not model:
            st.error("Failed to initialize any of the specified Gemini models.  The application cannot proceed.")
            st.stop() # Stop if no model

    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        st.stop()
else:
    st.error("GOOGLE_API_KEY not found in the environment variables or .env file.")
    st.stop()


def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF {file.name}: {e}")
        return ""


def extract_text_from_image(file):
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error extracting text from image {file.name}: {e}")
        return ""


def extract_info_with_gemini(resume_text, timeout=90):
    if not model:
        st.warning("Gemini API is not configured.")
        return None

    prompt = f"""
    Extract the following information from the resume text provided below.
    Format the output to be easily parsed into an Excel sheet, with each field on a new line
    and the field name followed by a colon and the extracted value. If a field is not found, write "N/A".

    Full Name:
    Phone Number:
    Email Address:
    Current Location:
    Total Experience (in years, if explicitly mentioned):
    Most Recent Job Title:
    Most Recent Employer:
    Highest Qualification:
    Key Skills (list them as comma-separated values):
    Notice Period (if mentioned):

    Resume Text:
    ```
    {resume_text}
    ```
    """

    try:
        generation_config = genai.types.GenerationConfig()
        generation_config.timeout_seconds = timeout
        response = model.generate_content(prompt, generation_config=generation_config)
        if response.parts:
            return response.parts[0].text.strip()
        else:
            st.warning("Gemini did not return any content for this resume.")
            return None
    except Exception as e:
        st.error(f"Error during Gemini API call: {e}")
        return None


def save_to_firestore(user_id, applicants, excel_data):
    if not db:
        st.warning("Firestore is not initialized.")
        return

    user_ref = db.collection("users").document(user_id)

    try:
        # Store individual applicants
        for idx, applicant in enumerate(applicants):
            doc_id = f"applicant_{idx+1}"
            user_ref.collection("applicants").document(doc_id).set(applicant)

        # Store aggregate Excel file as base64 or raw text
        user_ref.set({"excel_data": excel_data}, merge=True)
        st.success("Uploaded applicant data and Excel to Firestore.")
    except Exception as e:
        st.error(f"Error saving to Firestore: {e}")


# Streamlit UI
st.title("Upload Data")

# Dummy login state (replace with your actual authentication)
if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = True  # Set to True for testing

# Dummy user ID (replace with actual user identification)
if "username" not in st.session_state:
    st.session_state["username"] = "test_user"

# Ensure user is logged in
if not st.session_state.get("signed_in"):
    st.warning("You must be logged in to use this feature.")
    st.stop()

# Get user ID from session
user_id = st.session_state.username

uploaded_files = st.file_uploader(
    "Upload Resume Files (PDFs or Images)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info("Processing files with Gemini. Please wait...")
    rows = []
    output_box = st.empty()  # Create an empty container for the output

    for i, file in enumerate(uploaded_files):
        file_ext = file.name.split('.')[-1].lower()
        text = ""
        try:
            if file_ext == "pdf":
                text = extract_text_from_pdf(file)
            elif file_ext in ["png", "jpg", "jpeg"]:
                text = extract_text_from_image(file)

            if text:
                extracted_text = extract_info_with_gemini(text, timeout=90)
                if extracted_text:
                    extracted_info = {}
                    for line in extracted_text.split('\n'):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            extracted_info[key.strip()] = value.strip()
                    extracted_info["Resume File"] = file.name
                    rows.append(extracted_info)

                    # Display the result in the output box
                    output_box.write(f"Processed {file.name}:\n{extracted_text}")
                    time.sleep(5)  # Wait for 5 seconds

                else:
                    st.warning(f"Could not extract information from {file.name} using Gemini.")
                    output_box.warning(f"Could not extract information from {file.name} using Gemini.")  # show in output box
            else:
                st.warning(f"Could not extract text from {file.name}.")
                output_box.warning(f"Could not extract text from {file.name}.") # show in output box

        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
            output_box.error(f"Error processing {file.name}: {e}") # show in output box

    if rows:
        df = pd.DataFrame(rows)
        st.success(f"Processed {len(rows)} files successfully using Gemini.")
        st.dataframe(df)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            df.to_excel(tmp.name, index=False, sheet_name="Applicants")
            excel_path = tmp.name

        with open(excel_path, "rb") as f:
            st.download_button(
                label="Download Aggregated Excel",
                data=f,
                file_name="aggregated_resumes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        if st.button("Upload to Firestore"):
            with open(excel_path, "rb") as f:
                excel_data = f.read()
            save_to_firestore(user_id, rows, excel_data.decode('latin1'))
    else:
        st.warning("No data extracted from the uploaded files.")

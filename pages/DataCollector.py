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
import time
from openpyxl.utils import get_column_letter
import io

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
        try:
            available_models = [m.name for m in genai.list_models()]
            if not available_models:
                st.error("No Gemini models found.")
                st.stop()
        except Exception as e_list:
            st.error(f"Error listing models: {e_list}")
            st.stop()

        model_name_to_try = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-pro-vision',
            'models/gemini-1.0-pro-vision-latest'
        ]
        for model_name in model_name_to_try:
            if model_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    st.info(f"Using model: {model_name}")
                    break
                except Exception as e:
                    st.error(f"Error initializing model '{model_name}': {e}")
        if not model:
            st.error("Failed to initialize Gemini model.")
            st.stop()
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        st.stop()
else:
    st.error("GOOGLE_API_KEY not found.")
    st.stop()


def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ''.join([page.extract_text() or '' for page in pdf.pages])
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF {file.name}: {e}")
        return ""


def extract_text_from_image(file):
    try:
        image = Image.open(file)
        return pytesseract.image_to_string(image)
    except Exception as e:
        st.error(f"Error extracting text from image {file.name}: {e}")
        return ""


def extract_info_with_gemini(resume_text, timeout=90):
    if not model:
        st.warning("Gemini API not configured.")
        return None

    prompt = f"""
    Extract the following information from the resume text.
    Output each item on a new line as 'Field: Value'. Write 'N/A' if unknown.

    Full Name:
    Gender:(Assume gender based on name only give male or female in response no other text)
    Phone Number:
    Email Address:
    Location:
    Total Experience (in years): (use numbers only dont give any string in this field)
    Most Recent Job Title:
    Highest Qualification:
    Key Skills (comma-separated):
    dont add resume pdf field.
    Resume Text:
    ```
    {resume_text}
    ```
    """

    try:
        generation_config = genai.types.GenerationConfig()
        generation_config.timeout_seconds = timeout
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.parts[0].text.strip() if response.parts else None
    except Exception as e:
        st.error(f"Gemini API call failed: {e}")
        return None


# Streamlit UI
st.title("Resume Parser")

if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = True

if "username" not in st.session_state:
    st.session_state["username"] = "test_user"

if not st.session_state.get("signed_in"):
    st.warning("Please log in.")
    st.stop()

if "processed" not in st.session_state:
    st.session_state["processed"] = False

user_id = st.session_state.username

uploaded_files = st.file_uploader(
    "Upload Resume Files (PDFs or Images)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ✅ Process resumes only once
if uploaded_files and not st.session_state["processed"]:
    st.info("Processing resumes. Please wait...")
    rows = []
    output_box = st.empty()
    progress_bar = st.progress(0)
    progress_text = st.empty()
    total_files = len(uploaded_files)

    for i, file in enumerate(uploaded_files):
        file_ext = file.name.split('.')[-1].lower()
        text = ""

        try:
            if file_ext == "pdf":
                text = extract_text_from_pdf(file)
            elif file_ext in ["png", "jpg", "jpeg"]:
                text = extract_text_from_image(file)

            if text:
                extracted_text = extract_info_with_gemini(text)
                if extracted_text:
                    extracted_info = {}
                    for line in extracted_text.split('\n'):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            extracted_info[key.strip()] = value.strip()
                    extracted_info["Resume File"] = file.name
                    rows.append(extracted_info)
                else:
                    st.warning(f"Gemini failed on {file.name}")
            else:
                st.warning(f"Could not extract text from {file.name}")
        except Exception as e:
            st.error(f"Error on {file.name}: {e}")

        progress = (i + 1) / total_files
        progress_bar.progress(progress)
        progress_text.text(f"Processed {i + 1} of {total_files} files.")

    if rows:
        df = pd.DataFrame(rows)
        st.session_state.df = df

        # Create Excel file in memory and auto-adjust column widths
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Applicants")
            worksheet = writer.book["Applicants"]
            for column_cells in worksheet.columns:
                max_length = 0
                column_letter = get_column_letter(column_cells[0].column)
                for cell in column_cells:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                worksheet.column_dimensions[column_letter].width = max_length + 2

        excel_buffer.seek(0)
        st.session_state.excel_data = excel_buffer.read()
        st.session_state["processed"] = True

        st.success(f"Parsed {len(rows)} resumes.")
    else:
        st.warning("No data extracted.")

# ✅ Show parsed data and download option if processing is complete
if st.session_state.get("processed") and "df" in st.session_state:
    st.subheader("Parsed Resume Data")
    st.dataframe(st.session_state.df)

    st.download_button(
        label="Download Aggregated Excel",
        data=st.session_state.excel_data,
        file_name="aggregated_resumes.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    if st.button("Reset"):
        st.session_state["processed"] = False
        st.session_state.pop("df", None)
        st.session_state.pop("excel_data", None)

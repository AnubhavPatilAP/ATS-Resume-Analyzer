import streamlit as st
import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv
import pdfplumber
from PIL import Image
import pytesseract
import firebase_admin
from firebase_admin import credentials, firestore
import time
from openpyxl.utils import get_column_letter
import io
import requests
from requests.exceptions import HTTPError

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

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

# Configure Groq API
client = None
if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
        st.info("Groq API configured successfully.")
    except Exception as e:
        st.error(f"Error configuring Groq API: {e}")
        st.stop()
else:
    st.error("GROQ_API_KEY not found.")
    st.stop()

# Define expected fields for the DataFrame
EXPECTED_FIELDS = [
    "Full Name",
    "Gender",
    "Phone Number",
    "Email Address",
    "Location",
    "Total Experience (in years)",
    "Most Recent Job Title",
    "Highest Qualification",
    "Key Skills",
    "Resume File"
]

def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ''.join([page.extract_text() or '' for page in pdf.pages])
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from PDF {file.name}: {e}")
        return ""

def extract_text_from_image(file):
    try:
        image = Image.open(file)
        # Preprocess image for better OCR (optional: resize, grayscale)
        image = image.convert("L")  # Convert to grayscale
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from image {file.name}: {e}")
        return ""

def extract_info_with_groq(resume_text, timeout=90):
    if not client:
        st.warning("Groq API not configured.")
        return None

    prompt = f"""
    You are an expert resume parser. Extract the following information from the resume text provided below. 
    Output each item on a new line in the format 'Field: Value'. 
    Use 'N/A' for any field that cannot be determined. 
    Do not include any additional fields beyond those listed. 
    Ensure 'Gender' is either 'male' or 'female' based on name (if ambiguous, use 'N/A'). 
    For 'Total Experience (in years)', output only a number (e.g., '5') or 'N/A' calculate using given previous job experience timeline. 
    For 'Key Skills', provide a comma-separated list (e.g., 'Python, SQL, AWS').

    Fields to extract:
    - Full Name
    - Gender
    - Phone Number
    - Email Address
    - Location
    - Total Experience (in years)
    - Most Recent Job Title
    - Highest Qualification
    - Key Skills

    Example output:
    Full Name: John Doe
    Gender: male
    Phone Number: (123) 456-7890
    Email Address: john.doe@example.com
    Location: New York, NY
    Total Experience (in years): 5
    Most Recent Job Title: Software Engineer
    Highest Qualification: Bachelor of Science
    Key Skills: Python, Java, AWS

    Resume Text:
    ```
    {resume_text}
    ```
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Can switch to mixtral-8x7b-32768
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            timeout=timeout
        )
        output = response.choices[0].message.content.strip()
        # Validate output
        lines = [line for line in output.split('\n') if ':' in line]
        extracted_info = {}
        for line in lines:
            try:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key in [f.strip() for f in EXPECTED_FIELDS if f != "Resume File"]:
                    extracted_info[key] = value if value else "N/A"
            except ValueError:
                continue
        # Ensure all expected fields are present
        for field in EXPECTED_FIELDS:
            if field != "Resume File" and field not in extracted_info:
                extracted_info[field] = "N/A"
        return extracted_info
    except HTTPError as e:
        if e.response.status_code == 429:
            st.warning("Rate limit exceeded. Retrying after 10 seconds...")
            time.sleep(10)
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    timeout=timeout
                )
                output = response.choices[0].message.content.strip()
                lines = [line for line in output.split('\n') if ':' in line]
                extracted_info = {}
                for line in lines:
                    try:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in [f.strip() for f in EXPECTED_FIELDS if f != "Resume File"]:
                            extracted_info[key] = value if value else "N/A"
                    except ValueError:
                        continue
                for field in EXPECTED_FIELDS:
                    if field != "Resume File" and field not in extracted_info:
                        extracted_info[field] = "N/A"
                return extracted_info
            except Exception as retry_e:
                st.error(f"Groq API retry failed: {retry_e}")
                return None
        else:
            st.error(f"Groq API call failed: {e}")
            return None
    except Exception as e:
        st.error(f"Groq API call failed: {e}")
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

# Process resumes only once
if uploaded_files and not st.session_state["processed"]:
    st.info("Processing resumes. Please wait...")
    rows = []
    output_box = st.empty()
    progress_bar = st.progress(0)
    progress_text = st.empty()
    total_files = len(uploaded_files)
    failed_files = []

    for i, file in enumerate(uploaded_files):
        file_ext = file.name.split('.')[-1].lower()
        text = ""

        try:
            if file_ext == "pdf":
                text = extract_text_from_pdf(file)
            elif file_ext in ["png", "jpg", "jpeg"]:
                text = extract_text_from_image(file)

            if text:
                extracted_info = extract_info_with_groq(text)
                if extracted_info:
                    extracted_info["Resume File"] = file.name
                    rows.append(extracted_info)
                else:
                    st.warning(f"Groq failed to extract info from {file.name}")
                    failed_files.append(file.name)
            else:
                st.warning(f"Could not extract text from {file.name}")
                failed_files.append(file.name)
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
            failed_files.append(file.name)

        progress = (i + 1) / total_files
        progress_bar.progress(progress)
        progress_text.text(f"Processed {i + 1} of {total_files} files.")

    if rows:
        # Create DataFrame with fixed columns
        df = pd.DataFrame(rows, columns=EXPECTED_FIELDS)
        st.session_state.df = df

        # Create Excel file in memory
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

        st.success(f"Parsed {len(rows)} resumes successfully.")
        if failed_files:
            st.warning(f"Failed to process {len(failed_files)} files: {', '.join(failed_files)}")
    else:
        st.warning("No data extracted.")

# Show parsed data and download option
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
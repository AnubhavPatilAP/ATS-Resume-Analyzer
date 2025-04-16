import streamlit as st
import pandas as pd
import tempfile
import os
import pdfplumber
from PIL import Image
import pytesseract
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
FIREBASE_JSON = "D:/Resume Analyzer/test-23ffe-cf207eed55fe.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_JSON)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Dummy extractor (replace with proper resume parser)
def extract_info_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return extract_fields(text)

def extract_info_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return extract_fields(text)

def extract_fields(text):
    name = extract_value(text, ["Name", "Full Name"])
    phone = extract_value(text, ["Phone", "Contact"])
    email = extract_value(text, ["Email"])
    location = extract_value(text, ["Location", "City"])
    exp = extract_value(text, ["Experience"])
    job = extract_value(text, ["Job Title", "Position"])
    employer = extract_value(text, ["Employer", "Company"])
    qual = extract_value(text, ["Qualification", "Degree"])
    skills = extract_value(text, ["Skills"])
    notice = extract_value(text, ["Notice Period"])

    return {
        "Full Name": name,
        "Phone Number": phone,
        "Email Address": email,
        "Current Location": location,
        "Total Experience (Years)": exp,
        "Most Recent Job Title": job,
        "Most Recent Employer": employer,
        "Highest Qualification": qual,
        "Key Skills": skills,
        "Notice Period": notice,
    }

def extract_value(text, keywords):
    for line in text.split("\n"):
        for key in keywords:
            if key.lower() in line.lower():
                parts = line.split(":")
                if len(parts) > 1:
                    return parts[1].strip()
    return ""

def save_to_firestore(user_id, applicants, excel_data):
    user_ref = db.collection("users").document(user_id)
    
    # Store individual applicants
    for idx, applicant in enumerate(applicants):
        doc_id = f"applicant_{idx+1}"
        user_ref.collection("applicants").document(doc_id).set(applicant)
    
    # Store aggregate Excel file as base64 or raw text
    user_ref.set({"excel_data": excel_data}, merge=True)

# Streamlit UI
st.title("Upload Data")

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
    st.info("Processing files. Please wait...")

    rows = []

    for file in uploaded_files:
        file_ext = file.name.split('.')[-1].lower()
        try:
            if file_ext == "pdf":
                row = extract_info_from_pdf(file)
            else:
                row = extract_info_from_image(file)
            row["Resume File"] = file.name
            rows.append(row)
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    if rows:
        df = pd.DataFrame(rows)
        st.success(f"Processed {len(rows)} files successfully.")
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
            save_to_firestore(user_id, rows, excel_data.decode('latin1'))  # Firestore does not support binary
            st.success("Uploaded applicant data and Excel to Firestore.")
    else:
        st.warning("No data extracted from the uploaded files.")

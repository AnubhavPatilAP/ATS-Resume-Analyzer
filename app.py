import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Pro response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):  # Fixed typo here (changed 'age' to 'page_num')
        page = reader.pages[page_num]  # Corrected the page extraction
        text += str(page.extract_text())  # Corrected method name to 'extract_text'
    return text

# Prompts for different actions
input_prompt = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage, then list missing keywords, and finally provide your final thoughts.
Assign the percentage matching based on jd and the missing keyword with high accuracy
resume:{text}
description:{jd}
Give the following data in detail:
Name:
Contact: 
Profile match :
Missing keywords:
Profile Summary:
Tips: (In this section give tips to improve resume.)
What You did well: (Analyze the resume and point out the strengths of the resume, its structure, etc and give feedback)
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
The resume is: {text}
Analyze the resume uploaded and answer to the following in detail:

{cust}

"""


## streamlit app
st.title("AtsProject")
st.text("Resume Analyzer")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload Your resume", type="pdf", help="Please upload your pdf")

submit = st.button("Analyze")
cust = st.text_area("Ask what you want to know about your resume: ")
submit2 = st.button("Submit")
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))  # Passed the 'text' and 'jd' values
        st.subheader(response)

if submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt2.format(text=text,cust=cust))  # Passed the 'text' and 'jd' values
        st.subheader(response)
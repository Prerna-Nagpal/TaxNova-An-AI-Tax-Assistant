import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq
import pdfkit
import pdfplumber
import re
import requests

def parse_groq_stream(stream):
    response_content = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            response_content += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content
    return response_content

def extract_form16_data(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    # Enhanced extraction with improved regex patterns
    gross_salary = re.search(r'Gross Salary.*?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', extracted_text, re.IGNORECASE)
    tds = re.search(r'Tax Deducted at Source.*?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', extracted_text, re.IGNORECASE)
    taxable_income = re.search(r'Taxable Income.*?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', extracted_text, re.IGNORECASE)
    
    return {
        "Gross Salary": float(gross_salary.group(1).replace(',', '')) if gross_salary else 0,
        "TDS Deducted": float(tds.group(1).replace(',', '')) if tds else 0,
        "Taxable Income": float(taxable_income.group(1).replace(',', '')) if taxable_income else 0,
    }

def identify_deductions(income):
    deductions = {
        "Section 80C (Investments)": min(income * 0.1, 150000),
        "Section 80D (Health Insurance)": 25000,
        "Section 24 (Home Loan Interest)": 200000
    }
    return deductions

def auto_fill_itr(data):
    """Simulates automatic ITR filing using an API"""
    return {
        "status": "Success",
        "message": "Your ITR has been successfully filed!",
        "reference_id": "ITR123456789"
    }

st.set_page_config(page_title="Tax Assistant 🧑‍💼", page_icon="💰", layout="centered")

try:
    secrets = dotenv_values(".env")
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except Exception:
    secrets = st.secrets
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
INITIAL_RESPONSE = secrets.get("INITIAL_RESPONSE", "Hello! I’m here to help with tax finalization.")
CHAT_CONTEXT = secrets.get("CHAT_CONTEXT", "You are a tax assistant helping users navigate tax finalization. Offer guidance on tax forms, deductions, credits, and filing deadlines.")

client = Groq(api_key=GROQ_API_KEY)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": INITIAL_RESPONSE}]

st.title("Welcome to Your Automated Tax Assistant! 💰")
st.caption("Fully automating your tax filing process.")

for message in st.session_state.chat_history:
    role = "user" if message["role"] == "user" else "assistant"
    avatar = "🗨️" if role == "user" else "💼"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask me any tax-related question...")

st.sidebar.title("Automated Tax Filing")
st.sidebar.subheader("Upload Your Form 16")
uploaded_file = st.sidebar.file_uploader("Upload your Form 16 (PDF)", type=["pdf"])

if uploaded_file:
    extracted_data = extract_form16_data(uploaded_file)
    st.sidebar.write("Extracted Data from Form 16:")
    st.sidebar.write(extracted_data)

    # Tax Calculation
    income = extracted_data.get("Taxable Income", 0)
    tds_paid = extracted_data.get("TDS Deducted", 0)
    deductions = identify_deductions(income)
    total_deductions = sum(deductions.values())
    taxable_income_after_deductions = max(0, income - total_deductions)
    tax_liability = 0
    
    if taxable_income_after_deductions <= 250000:
        tax_liability = 0
    elif taxable_income_after_deductions <= 500000:
        tax_liability = (taxable_income_after_deductions - 250000) * 0.05
    elif taxable_income_after_deductions <= 1000000:
        tax_liability = 12500 + (taxable_income_after_deductions - 500000) * 0.2
    else:
        tax_liability = 112500 + (taxable_income_after_deductions - 1000000) * 0.3
    
    tax_due = max(0, tax_liability - tds_paid)
    st.sidebar.write("Deductions Applied:")
    st.sidebar.write(deductions)
    st.sidebar.write(f"Total Tax Liability: ₹{tax_liability:,.2f}")
    st.sidebar.write(f"Remaining Tax Payable: ₹{tax_due:,.2f}")

    # Auto-fill ITR Form
    if st.sidebar.button("Auto-File ITR"):
        itr_response = auto_fill_itr(extracted_data)
        st.sidebar.write("ITR Filing Status:", itr_response)

st.sidebar.subheader("Tax Resources")
st.sidebar.write("[Income Tax e-Filing Portal](https://www.incometax.gov.in/iec/foportal/)")
st.sidebar.write("[Tax Slabs and Deductions](https://www.incometaxindia.gov.in/)")

if st.sidebar.button("Export Chat as PDF"):
    chat_content = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
    pdfkit.from_string(chat_content, "Tax_Assistant_Chat.pdf")
    st.sidebar.success("Chat exported as PDF!")

if user_prompt:
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [{"role": "system", "content": CHAT_CONTEXT},
                {"role": "assistant", "content": INITIAL_RESPONSE},
                *st.session_state.chat_history]

    with st.chat_message("assistant", avatar="💼"):
        stream = client.chat.completions.create(model="llama3-8b-8192", messages=messages, stream=True)
        response_content = "".join(parse_groq_stream(stream))
        st.markdown(response_content)
        st.session_state.chat_history.append({"role": "assistant", "content": response_content})

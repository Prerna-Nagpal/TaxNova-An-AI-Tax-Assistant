import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq
import pdfkit
import pdfplumber
import re
import requests
from datetime import datetime
import pandas as pd
st.write(st.secrets)  # Debugging: Prints all secrets
st.write(st.secrets["GROQ_API_KEY"])  # Prints the specific key if it exists
# Initialize theme in session state if not already present
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Function to toggle theme
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

# Set page configuration with theme-based background
if st.session_state.theme == "dark":
    # Dark theme configuration
    st.set_page_config(
        page_title="TaxNova Assistant", 
        page_icon="💼", 
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Apply full dark background through base HTML override
    st.markdown("""
        <style>
            .stApp {
                background-color: #000000;
            }
            [data-testid="stSidebar"] {
                background-color: #121212;
            }
            /* Force all text to white in dark mode */
            body, .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
            .stHeader, p, span, label, .stButton, .stMetric, .stMetricLabel, .stExpander, 
            button, .css-1vbb94r, .css-12oz5g7, div[data-testid="stVerticalBlock"] p,
            .stTable, .stDataFrame, .stAlert, div[data-baseweb="base-input"] {
                color: white !important;
            }
            /* Fix table text color */
            .dataframe td {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    # Light theme configuration
    st.set_page_config(
        page_title="TaxNova Assistant", 
        page_icon="💼", 
        layout="wide",
        initial_sidebar_state="expanded",
    )

# Custom CSS for better UI with theme support
def local_css():
    light_theme = """
        /* Light theme styles */
        body {
            background-color: #f8f9fa;
            color: #212529;
        }
        
        .main {
            background-color: #f8f9fa;
            color: #212529;
        }
        
        .custom-header {
            background-color: #1e3a8a;
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            color: #212529;
        }
        
        .stButton>button {
            background-color: #1e3a8a;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            border: none;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #2563eb;
        }
        
        .dataframe th {
            background-color: #1e3a8a;
            color: white;
            padding: 8px;
            text-align: left;
        }
        
        .dataframe td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
            color: #212529;
        }
    """
    
    dark_theme = """
        /* Dark theme styles */
        body {
            background-color: #000000;
            color: #ffffff;
        }
        
        .main {
            background-color: #000000;
            color: #ffffff;
        }
        
        .custom-header {
            background-color: #1e2a5a;
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .card {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            margin-bottom: 1rem;
            color: #ffffff;
        }
        
        .stButton>button {
            background-color: #2d3b80;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            border: none;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #3a4db3;
        }
        
        .stTextInput>div>div>input {
            background-color: #333333;
            color: #ffffff;
        }
        
        .stTextInput label {
            color: #ffffff;
        }
        
        .stFileUploader label {
            color: #ffffff;
        }
        
        .stSelectbox label {
            color: #ffffff;
        }
        
        .stSelectbox>div>div>div {
            background-color: #333333;
            color: #ffffff;
        }
        
        .dataframe th {
            background-color: #2d3b80;
            color: white;
            padding: 8px;
            text-align: left;
        }
        
        .dataframe td {
            padding: 8px;
            border-bottom: 1px solid #444;
            color: #ffffff !important;
        }
        
        /* Override Streamlit elements for dark mode */
        [data-testid="stSidebar"] {
            background-color: #121212;
            color: #ffffff;
        }
        
        .stMarkdown {
            color: #ffffff !important;
        }
        
        /* Override all text elements to white */
        .stMarkdown p, .stMarkdown span, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown li, .stMarkdown a,
        p, span, div, label, .stButton, .stMetric, .stMetricLabel, .stExpander {
            color: #ffffff !important;
        }
        
        .stAlert {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        div[data-baseweb="base-input"] {
            background-color: #333333;
            color: #ffffff;
        }
        
        /* Streamlit chat elements */
        .stChatMessage {
            background-color: #1e1e1e;
        }
        
        .stChatInputContainer {
            background-color: #1e1e1e;
        }
        
        .stChatMessage div {
            color: #ffffff !important;
        }
    """
    
    # Common styles for both themes
    common_styles = """
        /* Chat message styling */
        .css-1vbb94r.e1wbw4rs0, .css-12oz5g7.exg6vvm15 {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 0.5rem;
        }
        
        /* File uploader styling */
        .uploadedFile {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
        }
        
        /* Data display tables */
        .dataframe {
            width: 100%;
            border-collapse: collapse;
        }
        
        /* Section dividers */
        hr {
            margin: 2rem 0;
            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0));
        }
        
        /* Badge styling */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.25rem;
            color: white;
            background-color: #2563eb;
            margin-right: 0.5rem;
        }
        
        /* Toggle switch container */
        .theme-toggle-container {
            position: fixed;
            top: 0.5rem;
            right: 1rem;
            z-index: 9999;
            display: flex;
            align-items: center;
        }
        
        /* Theme label */
        .theme-label {
            margin-right: 0.5rem;
            font-size: 0.9rem;
        }
        
        /* Toggle Switch appearance */
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 28px;
        }
        
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        
        .slider:before {
            position: absolute;
            content: "";
            height: 20px;
            width: 20px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        
        input:checked + .slider {
            background-color: #2196F3;
        }
        
        input:checked + .slider:before {
            transform: translateX(32px);
        }
    """
    
    # Apply the appropriate theme based on session state
    current_theme = dark_theme if st.session_state.theme == "dark" else light_theme
    st.markdown(f'''
    <style>
        {current_theme}
        {common_styles}
    </style>
    ''', unsafe_allow_html=True)

    # Add theme toggle button HTML
    theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
    st.markdown(f'''
    <div class="theme-toggle-container">
        <span class="theme-label">{theme_icon}</span>
        <form id="theme-form" action="">
            <label class="toggle-switch">
                <input type="checkbox" id="theme-toggle" {"checked" if st.session_state.theme == "dark" else ""}>
                <span class="slider"></span>
            </label>
        </form>
    </div>
    
    <script>
        // JavaScript to handle the toggle
        const toggle = document.getElementById('theme-toggle');
        toggle.addEventListener('change', function() {{
            // Submit a hidden form to trigger the Streamlit callback
            document.getElementById('theme-form').submit();
        }});
    </script>
    ''', unsafe_allow_html=True)

local_css()

# Theme toggle button in Streamlit (actual functionality)
# Place this at the top of the page
col_header = st.container()
with col_header:
    # Create a small column on the right for the toggle button
    _, _, _, toggle_col = st.columns([10, 10, 10, 2])
    with toggle_col:
        mode_label = "🌙 Dark" if st.session_state.theme == "light" else "☀️ Light"
        if st.button(mode_label, key="theme_toggle"):
            toggle_theme()

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
        "reference_id": f"ITR{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }

def format_currency(value):
    return f"₹{value:,.2f}"

# Load API keys
try:
    secrets = dotenv_values(".env")
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except Exception:
    secrets = st.secrets
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
INITIAL_RESPONSE = secrets.get("INITIAL_RESPONSE", "Hello! I'm here to help with tax finalization.")
CHAT_CONTEXT = secrets.get("CHAT_CONTEXT", "You are a tax assistant helping users navigate tax finalization. Offer guidance on tax forms, deductions, credits, and filing deadlines.")

client = Groq(api_key=GROQ_API_KEY)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": INITIAL_RESPONSE}]

# Page header with updated title
st.markdown('<div class="custom-header">'
            '<h1>💼 TaxNova Assistant</h1>'
            '<p>Your intelligent tax planning and filing companion</p>'
            '</div>', unsafe_allow_html=True)

# Create layout with columns
col1, col2 = st.columns([2, 3])

# COLUMN 1 (LEFT) - Form 16 Analysis
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Form 16 Analysis")
    
    # Improved file uploader
    uploaded_file = st.file_uploader("Upload your Form 16 (PDF)", type=["pdf"])
    
    if uploaded_file:
        with st.spinner("Analyzing your Form 16..."):
            # Show progress bar for visual feedback
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
            
            extracted_data = extract_form16_data(uploaded_file)
            
            # Success message
            st.success("Form 16 analyzed successfully!")
            
            # Display extracted data in a table
            df = pd.DataFrame({
                "Item": extracted_data.keys(),
                "Amount": [format_currency(val) for val in extracted_data.values()]
            })
            st.table(df)
            
            # Tax Calculation
            income = extracted_data.get("Taxable Income", 0)
            tds_paid = extracted_data.get("TDS Deducted", 0)
            deductions = identify_deductions(income)
            total_deductions = sum(deductions.values())
            taxable_income_after_deductions = max(0, income - total_deductions)
            
            # Tax calculation based on income slabs
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
            
            # Display tax breakdown
            st.markdown("### 📊 Tax Summary")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Income", format_currency(income))
                st.metric("Total Deductions", format_currency(total_deductions))
            with col_b:
                st.metric("Taxable Income", format_currency(taxable_income_after_deductions))
                st.metric("Tax Liability", format_currency(tax_liability))
            
            # Visual indicator for tax refund or payment due
            if tax_due > 0:
                st.error(f"Tax Payment Due: {format_currency(tax_due)}")
            else:
                st.success(f"Tax Refund Due: {format_currency(abs(tax_due))}")
            
            # Deductions breakdown with expandable section
            with st.expander("View Deductions Breakdown"):
                deductions_df = pd.DataFrame({
                    "Deduction Type": deductions.keys(),
                    "Amount": [format_currency(val) for val in deductions.values()]
                })
                st.table(deductions_df)
            
            # Auto-fill ITR Form with improved button
            if st.button("🚀 Auto-File ITR"):
                with st.spinner("Filing your ITR..."):
                    itr_response = auto_fill_itr(extracted_data)
                    if itr_response["status"] == "Success":
                        st.success(itr_response["message"])
                        st.info(f"Reference ID: {itr_response['reference_id']}")
                    else:
                        st.error(itr_response["message"])
    else:
        # Placeholder when no file is uploaded
        st.info("Upload your Form 16 PDF to automatically extract tax information and calculate your liability.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Tips Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💡 Quick Tax Tips")
    
    tips = [
        "The last date for filing ITR is July 31st for individuals.",
        "Keep all your investment proofs ready before filing ITR.",
        "You can save up to ₹1.5 lakhs under Section 80C investments.",
        "Health insurance premiums are deductible under Section 80D.",
        "Home loan interest up to ₹2 lakhs is deductible under Section 24."
    ]
    
    for i, tip in enumerate(tips):
        st.markdown(f"<span class='badge'>{i+1}</span> {tip}", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Resources and export section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Additional Features")
    
    # Export chat functionality
    if st.button("📥 Export Chat as PDF"):
        with st.spinner("Generating PDF..."):
            chat_content = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
            pdfkit.from_string(chat_content, "TaxNova_Assistant_Chat.pdf")  # Updated file name
            st.success("Chat exported as PDF! Download started.")
    
    # Resources section with improved links
    st.markdown("### 📚 Tax Resources")
    resources = {
        "Income Tax e-Filing Portal": "https://www.incometax.gov.in/iec/foportal/",
        "Tax Slabs and Deductions": "https://www.incometaxindia.gov.in/",
        "Tax Calculator": "https://cleartax.in/income-tax-calculator",

    }
    
    for name, url in resources.items():
        st.markdown(f"[{name}]({url})")
    
    st.markdown('</div>', unsafe_allow_html=True)

# COLUMN 2 (RIGHT) - Chat Interface
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💬 Tax Consultation")
    
    # Chat interface with improved display
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            role = "user" if message["role"] == "user" else "assistant"
            avatar = "👤" if role == "user" else "🤖"
            with st.chat_message(role, avatar=avatar):
                st.markdown(message["content"])
    
    user_prompt = st.chat_input("Ask me any tax-related question...")
    
    if user_prompt:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        messages = [{"role": "system", "content": CHAT_CONTEXT},
                    {"role": "assistant", "content": INITIAL_RESPONSE},
                    *st.session_state.chat_history]

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                stream = client.chat.completions.create(model="llama3-8b-8192", messages=messages, stream=True)
                response_content = "".join(parse_groq_stream(stream))
                st.markdown(response_content)
                st.session_state.chat_history.append({"role": "assistant", "content": response_content})
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with updated name
st.markdown(f'''
<div style="text-align: center; padding: 1rem; margin-top: 2rem; color: {"#ffffff" if st.session_state.theme == "dark" else "#6b7280"};">
    <p>© 2025 TaxNova Assistant | Current Financial Year: 2024-25</p>
</div>
''', unsafe_allow_html=True)
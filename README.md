# TaxNova-An-AI-Tax-Assistant
## System Architecture:
<img width="376" alt="image" src="https://github.com/user-attachments/assets/d1ef01b5-67c7-4ddc-86c1-7fc422a42b61" />

TaxNova is designed to make tax finalization stress-free and efficient. Using AI, it guides users through tax forms, deductions, credits, and filing requirements. With easy-to-follow answers and personalized tips, the app helps users navigate complex tax processes, ensuring they maximize deductions, avoid errors, and meet deadlines. Perfect for both individuals and small business owners, this app streamlines tax preparation and provides expert assistance, all from one convenient, user-friendly platform.
 Easily upload tax documents for analysis. Get detailed insights on critical areas like deductions, credits, and filing requirements.

## Features
- **AI Chatbot for Tax Guidance**: Get real-time answers to tax-related queries.
- **PDF Processing**: Extract financial details from Form 16/22 using **pdfplumber** and **regex**.
- **ITR Auto-Filing**: Seamlessly file Income Tax Returns.
- **Export Chat Conversations**: Save important discussions in **PDF format** for future reference.

## Tech Stack
- **Frontend**: Streamlit
- **AI Model**: Groq API (for chatbot)
- **PDF Processing**: pdfplumber, regex
- **Backend**: Python, pdfkit
- **Deployment**: Streamlit Cloud / Other Hosting Platforms

## Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Prerna-Nagpal/TaxNova-An-AI-Tax-Assistant.git
   cd TaxNova
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your API key**:
Create a .streamlit/secrets.toml file in the project root
Add your API key:
GROQ_API_KEY=""
LLAMA_CLOUD_API_KEY=""
QDRANT_API_KEY=""
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Project Structure
```
TaxNova/
│── .devcontainer/         # Development container configuration
│── .streamlit/            # Streamlit configuration files
│   ├── secrets.toml       # Secret keys and API credentials
│── .gitignore             # Files to be ignored in Git
│── app.py                 # Main Streamlit app
│── requirements.txt       # Required Python packages
│── README.md              # Project documentation
```

## Future Enhancements
- Integration with **government tax portals** for direct ITR filing.
- Support for **multiple tax regimes and deductions**.
- Advanced AI for **personalized tax planning**.
- Mobile application version.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any queries, reach out via email: **nagpalprerna4@gmail.com**

---
**TaxNova – Making Tax Filing Effortless with AI!** 🚀

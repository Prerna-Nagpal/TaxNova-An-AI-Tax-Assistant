# TaxNova-An-AI-Tax-Assistant

TaxNova is a **Streamlit-based web application** designed to simplify tax filing using **AI-powered chat assistance** and **automated data extraction** from **Form 16/22**. It provides real-time tax guidance, automated tax calculations, and ITR auto-filing, ensuring a hassle-free experience for users.

## 🚀 Features
- **AI Chatbot for Tax Guidance**: Get real-time answers to tax-related queries.
- **PDF Processing**: Extract financial details from Form 16/22 using **pdfplumber** and **regex**.
- **ITR Auto-Filing**: Seamlessly file Income Tax Returns.
- **Export Chat Conversations**: Save important discussions in **PDF format** for future reference.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **AI Model**: Groq API (for chatbot)
- **PDF Processing**: pdfplumber, regex
- **Backend**: Python, pdfkit
- **Deployment**: Streamlit Cloud / Other Hosting Platforms

## 📌 Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Prerna-Nagpal/TaxNova-An-AI-Tax-Assistant.git
   cd TaxNova
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure
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

## 🏆 Future Enhancements
- Integration with **government tax portals** for direct ITR filing.
- Support for **multiple tax regimes and deductions**.
- Advanced AI for **personalized tax planning**.
- Mobile application version.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any queries, reach out via email: **nagpalprerna4@gmail.com**

---
**TaxNova – Making Tax Filing Effortless with AI!** 🚀

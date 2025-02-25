# TaxNova-An-AI-Tax-Assistant
# Problem Statement
Tax filing is often a complex, time-consuming, and expensive process that forces individuals to rely on Chartered Accountants (CAs), adding unnecessary financial strain. Many taxpayers struggle to navigate the ever-changing tax laws, identify eligible deductions, and ensure accurate tax submissions. This lack of clarity results in errors, missed benefits, and costly penalties, making the process overwhelming and stressful. Without expert guidance, individuals are often left uncertain, leading to either overpayment or underpayment of taxes.
Manual tax calculations further complicate the process, increasing the risk of inaccuracies. Traditional tax filing requires multiple steps, document verifications, and a deep understanding of regulations, making it difficult for salaried individuals to file taxes efficiently. The absence of real-time support makes it even harder to make informed financial decisions, leaving taxpayers frustrated and unsure of how to optimize their tax savings.
## Proposed Solution
TaxNova automates tax filing by extracting data, identifying deductions, computing taxes, verifying TDS, and enabling seamless filing. Users start by uploading their Form 16 (for employees) or Form 22 (for business owners), and the system automatically scans the document using PDF parsing and text extraction techniques. It extracts key financial data such as gross salary, taxable income, TDS deducted, and other financial components, eliminating manual data entry and reducing errors.
Once the income details are extracted, TaxNova intelligently identifies applicable deductions under various sections like 80C (investments), 80D (health insurance), and 24 (home loan interest) using predefined tax rules. The AI then applies income tax slabs to compute taxable income, total deductions, and final tax liability, ensuring accurate tax calculations. Additionally, it cross-checks TDS payments and determines whether the user owes additional tax or is eligible for a refund, reducing the risk of miscalculations and penalties.
To further simplify the process, a real-time AI-powered chatbot assists users by answering tax-related queries, offering tax-saving tips, and providing personalized recommendations. The system generates a tax summary with a breakdown of earnings, deductions, and liabilities, ensuring clarity before filing. Finally, with a one-click auto-fill feature, users can directly submit their ITR, making tax filing effortless, accurate, and cost-effective—eliminating the need for a Chartered Accountant.
## System Architecture:
<img width="376" alt="image" src="https://github.com/user-attachments/assets/d1ef01b5-67c7-4ddc-86c1-7fc422a42b61" />
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
   Create a `.streamlit/secrets.toml` file in the project root and add your API keys:
   ```toml
   GROQ_API_KEY=""
   LLAMA_CLOUD_API_KEY=""
   QDRANT_API_KEY=""
   ```
4. **Run the application**:
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
**TaxNova – Making Tax Filing Effortless with AI!** 

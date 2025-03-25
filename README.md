# LLM-Powered Log Analyzer  

🚀 **Overview:**  
This project leverages **Large Language Models (LLMs)** to analyze and summarize system logs, enabling quicker issue detection and troubleshooting. Instead of manually searching logs, the tool provides **automated insights** and highlights potential issues.  

🔒 **Note:**  
- This tool **does not modify logs**—it only analyzes and summarizes them.  
- Users must provide **their own log files** for testing.  

---

## 📌 Installation & Setup  

### 1️⃣ Prerequisites  
Ensure you have the following installed:  
- **Python 3.11**  
- **Hugging Face Transformers** (for LLM processing)  
- **Pandas, Regex, Logging Modules**  

### 2️⃣ Clone the Repository  
git clone https://github.com/adnanhashmi25/llm-log-analyzer.git
cd llm-log-analyzer

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Provide Log Files
Place your system log files inside the /logs folder.
Ensure logs are in text format (.log, .txt).

### 5️⃣ Run the Log Analyzer
python main.py

### 📊 Features
✔ Automated log analysis using LLM
✔ Summarizes errors, warnings, and critical events
✔ Supports various log formats (Linux system logs, application logs, etc.)
✔ Customizable prompts for fine-tuned summaries

### 📜 Detailed Documentation
For a full project breakdown, visit the docs folder.
 - Project Summary

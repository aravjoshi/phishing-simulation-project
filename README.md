# Phishing Simulation Project (Educational)

## Overview
This project demonstrates a phishing attack simulation using **GoPhish** and custom Python scripts in a controlled sandbox environment.  
It simulates sending phishing emails, tracking user interactions, capturing credentials on a fake landing page, and analyzing campaign data through log parsing and reporting.

> ⚠️ **Ethical Use Disclaimer:** This project is for **educational and authorized testing purposes only**.  
> Misuse for unauthorized credential collection is illegal and punishable under law.

---

## ✨ Features
- Realistic phishing email templates with tracking pixels and link redirection
- Fake but trustworthy landing page for credential capture
- Python scripts to parse GoPhish logs and generate CSV reports
- Sample logs to demonstrate realistic campaign results
- Comprehensive PDF documentation summarizing campaign setup and findings

---

## 📂 Project Structure


phishing-simulation-project/
│── README.md # Project overview and instructions
│── config.json # GoPhish campaign configuration (placeholders)
│── phishing-templates/
│ └── phishing_email.html # HTML phishing email template
│── landing-pages/
│ └── index.html # Fake login page HTML
│── code/
│ ├── log_parser.py # Parse GoPhish logs into CSV
│ └── sandbox_server.py # Local credential capture server (safe demo)
│── logs/
│ ├── gophish_logs.json # Sample logs
│ └── phishing_report.csv # CSV generated from logs
│── docs/
│ └── phishing_report.pdf # Final project report
│── images/
│ ├── email_screenshot.png # Screenshot of phishing email
│ └── campaign_chart.png # Chart of campaign results


---

## 🚀 How to Run

1. **Setup GoPhish:**
   - Import `config.json` into GoPhish.
   - Configure SMTP server (use a safe sandbox like Mailtrap).

2. **Upload templates:**
   - Upload `phishing_email.html` to GoPhish email templates.
   - Upload `index.html` to GoPhish landing pages.

3. **Launch campaign** in your sandbox environment.

4. **Parse logs** into CSV report:
   ```bash
  python code/log_parser.py


Review results in the logs/ folder and final report in docs/phishing_report.pdf.

🛡️ Important Notes

All files use fake domains and dummy data.

Strictly for educational and demonstration purposes.

Perform testing only in a controlled lab environment.

📜 License

This project is open-source for educational purposes under the MIT License.

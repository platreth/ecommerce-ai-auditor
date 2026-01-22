# 🕵️‍♂️ E-commerce AI Opportunity Auditor

**"The AI Consultant in a Box"**

> Built by [Hugo Platret](https://www.linkedin.com/in/hugoplatret/) | Senior AI Consultant

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📖 About The Project

The **E-commerce AI Opportunity Auditor** is a sophisticated reconnaissance tool designed to bridge the gap between "Public Data" and "Strategic Automation". 

Instead of generic advice ("You should use AI"), this tool uses **GPT-4o** to analyze a specific storefront's public footprint (JSON-LD Schema, Metadata, Structure) and generate **3 ultra-specific, high-impact automation opportunities** tailored to that business.

**Why?** Because 90% of e-commerce businesses know they *need* AI, but don't know *where* to apply it. This tool answers "Where?" in 30 seconds.

## ✨ Key Features

*   **🛡️ Smart Scraping Engine**: Intelligently extracts structured data (`JSON-LD`) while gracefully handling modern anti-bot "Security Shields".
*   **🧠 Tier-1 Consultant Brain**: A refined AI Agent (GPT-4o) that rejects generic advice and strictly outputs actionable, high-ROI implementation plans.
*   **📊 Strategic Scoring**: Every opportunity is rated on **Project Complexity** (Low/Med/High) and **Potential ROI** (1-10), helping stakeholders prioritize.
*   **💼 Consultant Report Generation**: One-click generation of a professional Markdown strategy report, ready to be sent to clients or internal teams.
*   **🎨 Premium UI**: A custom "Dark Mode" interface designed for decision-makers.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   An OpenAI API Key (GPT-4o recommended)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Start-x-Labs/ecommerce-ai-auditor.git
    cd ecommerce-ai-auditor
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## 🧠 How It Works

1.  **Reconnaissance**: The script scans the target URL, rotating User-Agents to mimic real traffic. It prioritizes schema.org data to understand *what* the business actually sells.
2.  **Analysis**: The extracted data is fed into a specialized GPT-4o system prompt, acting as a "Senior McKinsey Consultant".
3.  **Strategy**: The AI cross-references the store's niche (e.g., "High-ticket Furniture") with known high-value automation patterns (e.g., "Autonomous Returns Agent").
4.  **Delivery**: Results are presented in a dashboard and available as a downloadable report.

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **Core Logic**: Python
*   **AI**: OpenAI GPT-4o
*   **Data Extraction**: BeautifulSoup4 + Requests

---

*This project is part of my "Building in Public" series. Connect with me on [LinkedIn](https://www.linkedin.com/in/hugoplatret/) for more.*

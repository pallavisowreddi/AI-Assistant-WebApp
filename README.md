# Nexus AI: Prompt Engineering & Feedback Assistant

A premium, web-based AI Assistant built with **Flask** and powered by **Google Gemini API** (`gemini-2.5-flash`). This project serves as a practical exploration of **Prompt Engineering** methodologies and dynamic user feedback loop integration.

Created as a major project for the VaultOfCodes Python Developer Internship (AI & Prompt Engineering Track).

---

## 🚀 Key Features

*   **Four Core Cognitive Modules**:
    *   **Question Answering (Q&A)**: Delivers direct factual outputs or elaborate pedagogical explanations.
    *   **Text Summarizer**: Creates concise paragraph overviews, bulleted takeaways, or executive business briefings.
    *   **Content Generator**: Writes vivid poems, fictional stories, or minimalist haikus.
    *   **Study & Career Advisor**: Generates encouraging reviews, weekly study roadmaps, or troubleshooting advice.
*   **12 Engineered System Prompts**: Toggle between 3 distinct stylistic prompts per function to witness changes in response length, tone, structure, and complexity.
*   **Prompt Engineer Inspector**: A collapsible live-terminal component showing the exact prompt payload sent to Gemini, with a **Copy Prompt** utility.
*   **Interactive Analytics Dashboard**: Visual progression charts and table logs detailing total API calls, helpfulness rates, and qualitative comment reviews. 
*   **Export Logs**: Download your entire prompt evaluation history as an Excel-compatible `.csv` file.
*   **Modern Glassmorphic Dark UI**: Fully responsive mobile-optimized layout styled with CSS variables and subtle neon overlays.

---

## 🛠️ Folder Structure

```
AI-Assistant-WebApp/
│
├── app.py                  # Main Flask application & routes (endpoints for generation and feedback)
├── requirements.txt        # Python dependency manifest (essential for Vercel deployment)
├── vercel.json             # Vercel serverless deployment config
├── feedback_data.json      # Flat file JSON database tracking user feedbacks
├── README.md               # Repository documentation and guide
│
├── templates/
│   ├── index.html          # Dynamic dashboard layout and client-side scripts
│   └── static/
│       └── style.css       # Styling backup for asset mapping
│
└── static/
    └── style.css           # Primary CSS styling sheet
```

---

## 💻 Local Setup Instructions

Ensure you have Python installed, then follow these instructions in your terminal:

### 1. Clone or Open Workspace
Open a terminal in the project directory:
```bash
cd C:\Users\palla\OneDrive\Desktop\AI-Assistant-Development
```

### 2. Activate Python Virtual Environment
*   **Windows (PowerShell)**:
    ```powershell
    .\venv\Scripts\activate
    ```
*   **Mac/Linux**:
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies
Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Setup Local Environment File
Create a `.env` file in the root folder and add your Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run Server
Execute the Flask web app:
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your web browser.

---

## 🚀 Deployment to Vercel (100% Free & No Card Required)

This project is fully configured for deployment on Vercel.

1.  Create a free account on [Vercel](https://vercel.com) using your GitHub account.
2.  Click **Add New > Project**.
3.  Connect your GitHub account and import the `AI-Assistant-WebApp` repository.
4.  In the configuration, add an **Environment Variable**:
    *   **Key**: `GEMINI_API_KEY`
    *   **Value**: `your_gemini_api_key`
5.  Click **Deploy**. Vercel will host your app online 24/7!

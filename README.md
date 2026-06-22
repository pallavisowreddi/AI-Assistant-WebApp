# Nexus AI: Prompt Engineering & Feedback Assistant

A premium, web-based AI Assistant built with **Flask** and powered by **Google Gemini API** (`gemini-2.5-flash`). This project serves as a practical exploration of **Prompt Engineering** methodologies and dynamic user feedback loop integration.

Created as a major project for the VaultOfCodes developer internship.

---

## 🚀 Key Features

*   **Four Core Cognitive Modules**:
    *   **Question Answering (Q&A)**: Delivers direct factual outputs or elaborate pedagogical explanations.
    *   **Text Summarizer**: Creates concise paragraph overviews, bulleted takeaways, or executive business briefings.
    *   **Content Generator**: Writes vivid poems, fictional stories, or minimalist haikus.
    *   **Study & Career Advisor**: Generates encouraging reviews, weekly study roadmaps, or troubleshooting advice.
*   **12 Engineered System Prompts**: Toggle between 3 distinct stylistic prompts per function to witness changes in response length, tone, structure, and complexity.
*   **Prompt Engineer Inspector**: A collapsible live-terminal component showing the exact prompt payload sent to Gemini.
*   **Interactive Analytics Dashboard**: Visual progression charts and table logs detailing total API calls, helpfulness rates, and qualitative comment reviews.
*   **Embedded Presentation (PPT Slider)**: An elegant HTML/CSS slide presentation deck built directly into the sidebar to showcase project slides easily.
*   **Modern Glassmorphic Dark UI**: Fully responsive frontend styled with CSS variables and subtle neon overlays.

---

## 🛠️ Folder Structure

```
AI-Assistant-Development/
│
├── app.py                  # Main Flask application & routes (endpoints for generation and feedback)
├── requirements.txt        # Python dependency manifest (essential for Render deployment)
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
cd c:\Users\palla\OneDrive\Desktop\AI-Assistant-Development
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

### 4. Run Server
Execute the Flask web app:
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your web browser.

---

## 🚀 Deployment to Render.com

This project is fully configured for deployment on Render.

1.  Create a free account on [Render](https://render.com).
2.  Click **New +** and choose **Web Service**.
3.  Connect your GitHub repository.
4.  Specify these configurations:
    *   **Language**: `Python`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
5.  Click **Deploy Web Service** and access your live URL!

---

## 🧑‍💻 Prompt Engineering Logic Blueprint

This system utilizes system prompts to wrapper user inputs:

| Function | Style Variant | System wrapper target |
| :--- | :--- | :--- |
| **Q&A** | Factual & Direct | Direct, concise, no conversational fluff (under 2 paragraphs). |
| | Comprehensive Explainer | Pedagogical, deep explanation complete with background and context. |
| | Structured Outline | Ordered outlines highlighting key terminology. |
| **Summarizer** | Short Summary | Paragraph condensation (under 80 words). |
| | Key Takeaways | Action points list (max 5 points). |
| | Executive Brief | Formal brief (Core summary, Key themes, Implications). |
| **Creative** | Poetic & Vivid | Focus on metaphors and imagery. |
| | Narrative Story | Novel-like progression with characters and settings. |
| | Minimalist | Haiku format or one-sentence story. |
| **Advisor** | Empathetic Coach | Encouraging and supportive tips. |
| | Structured Roadmap | Week-by-week program. |
| | Critique & Troubleshoot | Pinpointing common learner pitfalls and resolutions. |

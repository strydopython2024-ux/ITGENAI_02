# Intelligent Information Flow

**Intelligent Information Flow: Leveraging Artificial Intelligence for Real-Time Decision-Making in Business Management Systems**

A student-ready AI-powered decision-support application that accepts a **CSV dataset uploaded at runtime**, automatically understands its structure, performs data analysis and machine-learning tasks, and generates optional AI insights using **Google Gemini 2.5 Flash**.

The system does **not depend on a preloaded student, sales, or business dataset**.

---

## 1. Project Overview

The application converts an uploaded CSV into a usable decision-support workflow.

```text
User
  |
  v
Flask Web Frontend
  |
  v
FastAPI REST Backend
  |
  +---- SQLite Authentication
  |
  +---- CSV Data Processing
  |
  +---- Statistical Analysis
  |
  +---- Categorical Analysis
  |
  +---- Correlation Analysis
  |
  +---- Forecasting
  |
  +---- Segmentation
  |
  +---- Anomaly Detection
  |
  +---- Google Gemini AI
  |
  v
Interactive Results
```

---

## 2. Main Features

### Authentication
- User registration
- User login
- Logout
- Password hashing
- SQLite user database
- Session-based Flask authentication

### Runtime CSV Processing
- Upload CSV from the browser
- Maximum upload size: 25 MB
- UTF-8 and Latin-1 CSV support
- Automatic basic data cleaning
- Automatic column-type detection
- No hardcoded dataset dependency

### Data Analysis
- Dataset overview
- Numeric statistics
- Categorical frequency analysis
- Correlation analysis
- Missing-value information
- Duplicate-row information

### Machine Learning
- Linear regression forecasting
- KMeans segmentation
- Isolation Forest anomaly detection

### AI Decision Support
- Google Gemini API integration
- Model: `gemini-2.5-flash`
- Compact computed dataset summary is sent to Gemini instead of the raw CSV
- AI insights include:
  - Dataset Summary
  - Key Findings
  - Important Patterns
  - Potential Risks
  - Anomalies
  - Recommended Actions
- Clear configuration/error response when Gemini is unavailable

### Visualization
- Interactive web pages
- Plotly-based charts where supported by the frontend
- Professional dashboard layout

---

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Flask, HTML, TailwindCSS, JavaScript |
| Backend | FastAPI |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Plotly |
| AI | Google Gemini 2.5 Flash |
| Default LLM | Llama 3.2 |
| Server | Uvicorn |
| Package Manager | uv |
| Testing | Pytest |

---

## 4. Project Structure

```text
intelligent-information-flow/
|
├── .gitignore
├── .python-version
├── README.md
├── run_script.txt
├── pyproject.toml
├── uv.lock
|
├── CODE/
│   ├── __init__.py
│   |
│   ├── BACKEND/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   |
│   │   └── app/
│   │       ├── database/
│   │       ├── ml/
│   │       ├── models/
│   │       ├── routes/
│   │       ├── services/
│   │       └── utils/
│   |
│   ├── FRONTEND/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── static/
│   │   └── templates/
│   |
│   └── DATA_BASE/
│       ├── data/
│       └── database/
|
└── tests/
```

Runtime files are intentionally ignored by Git.

---

## 5. Requirements

Install the following on Windows:

1. Python 3.11 or newer
2. uv
3. Google Gemini

Set the Gemini API key before starting the application:

```powershell
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

The AI Business Analyst uses `gemini-2.5-flash` and receives only the computed dataset summary.
4. Refresh the browser with:

```text
Ctrl + F5
```

5. Open:

```text
http://127.0.0.1:5000
```

---

## 20. Git Rules

The following should **not** be committed:

```text
.venv/
__pycache__/
*.pyc
.env
*.db
*.sqlite
runtime CSV files
logs
IDE files
temporary files
```

The following should normally be committed:

```text
CODE/
README.md
.gitignore
pyproject.toml
uv.lock
run_script.txt
.python-version
```

---

## 21. First-Time Setup Summary

After cloning the project:

```cmd
cd intelligent-information-flow
pip install uv
uv --version
uv sync
```

Set the Gemini API key before running the AI Business Analyst:

```powershell
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

The AI model is `gemini-2.5-flash`.
```

Start backend:

```cmd
cd CODE\BACKEND
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open another terminal at the project root and start frontend:

```cmd
uv run flask --app CODE/FRONTEND/app.py run --host 127.0.0.1 --port 5000 --debug
```

Open:

```text
http://127.0.0.1:5000
```

---

## 22. Project Status

The project is designed for a **student project demonstration and delivery**.

Core architecture:

```text
CSV Upload
    ↓
Automatic Data Detection
    ↓
Data Cleaning
    ↓
Analytics
    ↓
Machine Learning
    ↓
Decision Support
    ↓
Local AI Insights
```

A Gemini API key is required for the AI Business Analyst.

# README.md

## 🏥 Patient Triage API (FastAPI + HuggingFace)

A small web service that classifies patient messages into triage categories such as `emergency`, `routine`, `follow-up`, or `other` using a HuggingFace transformer model (`facebook/bart-large-mnli`).

This application uses:
- FastAPI for the web framework
- SQLite for local data persistence
- HuggingFace transformers for zero-shot text classification

---

## 📁 Project Folder Structure
```
patient_triage/
├── app/
│   ├── classifier.py     # Loads HuggingFace model and classifies text
│   ├── database.py       # SQLAlchemy DB setup
│   ├── main.py           # FastAPI app, routes, and logic
│   ├── models.py         # SQLAlchemy ORM model
│   ├── schemas.py        # Pydantic request/response models
│   ├── utils.py          # Utility helpers (e.g., validation)
│   └── __pycache__/
├── Dockerfile            # For Docker image build
├── requirements.txt      # Python dependencies
├── patient_data.db       # SQLite DB file (auto-created)
├── README.md             # You are here 📘
```

---

## 🚀 Running the App

### ✅ Option 1: Without Docker


1. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
uvicorn app.main:app
```

> ⚠️ **IMPORTANT: First-Time Model Download Notice**  
> If you're running the app for the first time on your system, please **wait a few minutes** while the model `facebook/bart-large-mnli` (~2GB) is being downloaded in the background.  
> During this time, if you hit the API endpoint, it may appear unresponsive — **this is expected**.  
> Response will work normally **after the model download is complete**.  
> The model is cached locally after the first run, so future startups will be fast.


4. **Access Swagger UI:**
```
http://localhost:8000/docs
```

---

### 🐳 Option 2: With Docker



1. **Build Docker image:**
```bash
docker build -t patient-triage-api .
```

2. **Run Docker container:**
```bash
docker run -d -p 8000:8000 --name triage-app patient-triage-api
```

> ⚠️ **IMPORTANT: First-Time Model Download Notice**  
> If you're running the app for the first time on your system, please **wait a few minutes** while the model `facebook/bart-large-mnli` (~2GB) is being downloaded in the background.  
> During this time, if you hit the API endpoint, it may appear unresponsive — **this is expected**.  
> Response will work normally **after the model download is complete**.  
> The model is cached locally after the first run, so future startups will be fast.


3. **Access Swagger UI:**
```
http://localhost:8000/docs
```

---

## 🔌 API Endpoint

### ➤ `POST /predict`
Classifies a patient message and saves it to the database.

#### 📥 Request Body (JSON):
```json
{
  "name": "John Doe",
  "mobile": "9876543210",
  "message": "I have chest pain and shortness of breath"
}
```

#### ✅ Success Response:
```json
{
  "success": true,
  "data": {
    "current_result": {
      "category": "emergency",
      "confidence": 0.9432
    },
    "history": [
      {
        "message": "I want to consult with doctor",
        "category": "follow-up",
        "confidence": 0.8923
      }
    ]
  },
  "error": null
}
```

#### ❌ Error Response (e.g., validation failure):
```json
{
  "success": false,
  "data": null,
  "error": {
    "field": "mobile",
    "message": "Mobile number must be 10 digits and start with 6 or 7 or 8 or 9."
  }
}
```

#### ❌ Server Error Response (unexpected failure):
```json
{
  "success": false,
  "data": null,
  "error": {
    "message": "Internal server error."
  }
}
```

---

## 🧪 Model Used
- Hugging Face Zero-Shot Classifier:
  - `facebook/bart-large-mnli`

---

## 🧼 Notes
- The SQLite file (`patient_data.db`) is created automatically.
- Data is persisted across sessions.
- Standardized response format is always returned.

---

Made with 💡 using FastAPI & Transformers
# How To Run The Whole Project (Windows)

## 1. Open terminal in project folder
```powershell
cd "c:\Users\DELL\Documents\college work komal\TY Sem2\ML\resume-job-recommendation"
```

## 2. Create virtual environment (recommended)
```powershell
python -m venv .venv
```

## 3. Activate virtual environment
```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Upgrade pip
```powershell
python -m pip install --upgrade pip
```

## 5. Install dependencies
```powershell
python -m pip install -r requirements.txt
```

## 6. Download NLTK data (one-time)
```powershell
python -c "import nltk; nltk.download('stopwords')"
```

## 7. Run the Flask app
```powershell
python app.py
```

## 8. Open in browser
Go to:
- http://127.0.0.1:5000

---

## Important notes
- Do not run `python main.py` in this project (there is no main entrypoint for this app).
- Correct start command is: `python app.py`
- If `spacy` model errors appear, run:
```powershell
python -m spacy download en_core_web_sm
```

## Optional: verify routes quickly
```powershell
python -c "from app import app; c=app.test_client(); print(c.get('/').status_code, c.get('/employee').status_code, c.get('/employeer').status_code)"
```
Expected output:
```text
200 200 200
```

## Troubleshooting (Your Current Logs)
- `HTTP 200` for pages and static files means requests are successful.
- `HTTP 304` for CSS/images is normal browser caching behavior, not an error.
- `WinError 32` means a file is locked by another process.

If you see old lock errors, do this:
1. Stop Flask server (`Ctrl + C`).
2. Close any PDF opened in browser/PDF viewer.
3. Start server again:
```powershell
python app.py
```

Code has been updated to reduce lock issues by:
- Saving uploads with unique names.
- Using a unique folder for employer multi-upload.
- Running Flask with `use_reloader=False`.
- Preferring `pdfplumber/docx2txt` over Tika for parsing.

# ML Model Explanation - Resume Job Recommendation System

## 1. System Overview
This repository now has **two ML tracks**:
1. **Production app track (Flask app)**: recommendation/matching pipeline used by users.
2. **Notebook evaluation track**: supervised multi-class text classification with full metrics.

Files:
- App pipeline: `app.py`, `resume_screening/job.py`, `resume_screening/match.py`, `resume_screening/resparser.py`, `resume_screening/extract_skill.py`
- Evaluation notebook: `ML_PIPELINE_EVALUATION.ipynb`

## 2. App Track (Used in Website)

### A) Input Flows
- **Employee flow** (`/employee_submit`): uploaded resume -> recommended jobs.
- **Employer flow** (`/employeer_submit`): uploaded resumes + job description -> ranked resumes.

### B) Core Processing
- Resume parsing: `resume_screening/resparser.py`, `resume_screening/extract_skill.py`
- Text cleaning: `resume_screening/match.py`
- Similarity ranking: `CountVectorizer` + `cosine_similarity` in `resume_screening/match.py`
- Job data source: `indeed_data.csv`

### C) Scoring
- Match score is cosine similarity percentage.
- This is an **information retrieval / recommendation** setup (not supervised classifier inference in app routes).

## 3. Notebook Track (Updated and Tuned)
The notebook `ML_PIPELINE_EVALUATION.ipynb` contains an improved supervised pipeline for title prediction from job-description text.

### A) Updated Preprocessing
- Cleans text (lowercase, URL removal, punctuation cleanup, whitespace normalization).
- Normalizes noisy title variants into canonical labels (for example `Data Scientist`, `Data Engineer`, `UI/UX Designer`, etc.).
- Filters classes with low support (`min_samples_per_class = 5`) for more stable training.

### B) Updated Models Used
- `RandomForestClassifier` (tuned)
- `LinearSVC` (tuned)
- `LogisticRegression` with `saga` (tuned)
- `SGDClassifier(loss='log_loss')`
- `MultinomialNB`

### C) Feature Engineering
- `TfidfVectorizer` with stronger settings:
   - larger feature space
   - 1-gram to 3-gram where appropriate
   - `sublinear_tf=True` for linear models

### D) Metrics Computed
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-score (weighted)
- Classification report
- Confusion matrix

### E) Best Result (Latest Run)
- Best model: `RandomForest`
- Accuracy: **0.8395** (83.95%)
- Precision: **0.8551**
- Recall: **0.8395**
- F1-score: **0.8351**

### F) Additional Notebook Outputs
- Data distribution visualization (top titles + description length histogram).
- Recommendation sanity checks with sample queries.
- Example query quality summary showed `Hit@5 = 100%` on included sample cases.
- Best model artifact saved as: `best_job_title_classifier.joblib`

## 4. Accuracy Interpretation

### App Track
- App recommendations are similarity-based; classic classifier accuracy is not directly part of route execution.

### Notebook Track
- 83.95% is for the **normalized and support-filtered** supervised setup.
- This improves reliability and is appropriate for evaluation/reporting.

## 5. Libraries Used
- `scikit-learn`: vectorizers, models, metrics, pipeline
- `nltk`: stopword support
- `spaCy`: skill phrase extraction support
- `pdfplumber`, `docx2txt`: resume text extraction
- `matplotlib`, `seaborn`: visualizations

## 6. Practical Guidance By File
- `app.py`: route handling, upload flow
- `resume_screening/job.py`: core ranking workflow and dataframe outputs
- `resume_screening/match.py`: preprocessing + vectorization + cosine similarity
- `resume_screening/extract_skill.py`: skill extraction from resumes
- `resume_screening/resparser.py`: PDF/DOCX parsing utilities
- `ML_PIPELINE_EVALUATION.ipynb`: supervised experimentation, metrics, plots, and model comparison

## 7. Suggested Next Improvements
1. Add cross-validation in notebook for more stable metric estimates.
2. Add ranking metrics (`Precision@K`, `NDCG@K`) for recommendation quality.
3. Add optional embedding-based retriever (for example Sentence-BERT) as a comparison baseline.

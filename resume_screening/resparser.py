import re
import docx2txt
import pdfplumber
# from resume_parser import resumeparse
from . import extract_skill

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')
try:
    from tika import parser as tika_parser
except ModuleNotFoundError:
    tika_parser = None


def skill(resume_file):
    data = extract_skill.read_file(resume_file)
    resume = data['skills']
    skills = []
    skills.append(' '.join(word for word in resume))
    return skills

# def parser(resume_file):
#     data = resumeparse.read_file(resume_file)
#     return data

def convert_docx_to_txt(docx_file):
    text = docx2txt.process(docx_file) or ""
    if not text and tika_parser is not None:
        text = (tika_parser.from_file(docx_file, service='text') or {}).get('content') or ""
    clean_text = re.sub(r'\n+', '\n', text)
    clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
    resume_lines = clean_text.splitlines()  # Split text blob into individual lines
    resume_lines = [re.sub(r'\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
    return resume_lines

def convert_pdf_to_txt(pdf_file):
    pages_text = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                pages_text.append(page.extract_text() or "")
    except Exception:
        pages_text = []

    raw_text = "\n".join(pages_text).strip()
    if not raw_text and tika_parser is not None:
        raw_text = (tika_parser.from_file(pdf_file, service='text') or {}).get('content') or ""

    if not raw_text:
        return []

    full_string = re.sub(r'\n+', '\n', raw_text)
    full_string = full_string.replace("\r", "\n")
    full_string = full_string.replace("\t", " ")

    # Remove awkward LaTeX bullet characters
    full_string = re.sub(r"\uf0b7", " ", full_string)
    full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
    full_string = re.sub(r'• ', " ", full_string)

    # Split text blob into individual lines
    resume_lines = full_string.splitlines(True)

    # Remove empty strings and whitespaces
    resume_lines = [re.sub(r'\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
    return resume_lines
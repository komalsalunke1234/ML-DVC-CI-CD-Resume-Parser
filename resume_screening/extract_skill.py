# !pip install tika
# !pip install docx2txt
# !pip install phonenumbers
# !pip install pyenchant
# !pip install stemming

from __future__ import division
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')

import re
import os
import docx2txt
import pdfplumber
try:
    import spacy
    from spacy.matcher import Matcher
    from spacy.matcher import PhraseMatcher
except ModuleNotFoundError:
    spacy = None
    Matcher = None
    PhraseMatcher = None

try:
    from tika import parser as tika_parser
except ModuleNotFoundError:
    tika_parser = None


# load pre-trained model
base_path = os.path.dirname(__file__)

if spacy is not None:
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        # Fallback keeps app importable when the model is not present yet.
        nlp = spacy.blank('en')

    # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab)

    file = os.path.join(base_path, "LINKEDIN_SKILLS_ORIGINAL.txt")
    file = open(file, "r", encoding='utf-8')
    skill = [line.strip().lower() for line in file]
    skillsmatcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in skill if len(nlp.make_doc(text)) < 10]
    skillsmatcher.add("Job title", None, *patterns)
else:
    nlp = None
    matcher = None
    skillsmatcher = None
skills_header = (
        'credentials',
        'areas of experience',
        'areas of expertise',
        'areas of knowledge',
        'skills',
        "other skills",
        "other abilities",
        'career related skills',
        'professional skills',
        'specialized skills',
        'technical skills',
        'computer skills',
        'personal skills',
        'computer knowledge',        
        'technologies',
        'technical experience',
        'proficiencies',
        'languages',
        'language competencies and skills',
        'programming languages',
        'competencies')

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

def find_segment_indices(string_to_search, resume_segments, resume_indices):
    for i, line in enumerate(string_to_search):
        if line[0].islower():
            continue
        header = line.lower()
        if [s for s in skills_header if header.startswith(s)]:
            try:
                resume_segments['skills'][header]
            except:
                resume_indices.append(i)
                header = [s for s in skills_header if header.startswith(s)][0]
                resume_segments['skills'][header] = i
                
def slice_segments(string_to_search, resume_segments, resume_indices):
    resume_segments['contact_info'] = string_to_search[:resume_indices[0]]
    for section, value in resume_segments.items():
        if section == 'contact_info':
            continue
        for sub_section, start_idx in value.items():
            end_idx = len(string_to_search)
            if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                end_idx = resume_indices[resume_indices.index(start_idx) + 1]
            resume_segments[section][sub_section] = string_to_search[start_idx:end_idx]
            
            
def segment(string_to_search):
    resume_segments = {'skills': {}}
    resume_indices = []
    find_segment_indices(string_to_search, resume_segments, resume_indices)
    if len(resume_indices) != 0:
        slice_segments(string_to_search, resume_segments, resume_indices)
    return resume_segments


def extract_skills(text):
    if nlp is None or skillsmatcher is None:
        return []
    skills = []
    __nlp = nlp(text.lower())
    # Only run nlp.make_doc to speed things up
    matches = skillsmatcher(__nlp)
    for match_id, start, end in matches:
        span = __nlp[start:end]
        skills.append(span.text)
    skills = list(set(skills))
    return skills

def read_file(file):
    file = os.path.join(file)
    if file.endswith('docx') or file.endswith('doc'):
        resume_lines = convert_docx_to_txt(file)
    elif file.endswith('pdf'):
        resume_lines = convert_pdf_to_txt(file)
    else:
        resume_lines = None
    resume_segments = segment(resume_lines)
    full_text = " ".join(resume_lines)
    skills = ""
    if len(resume_segments['skills'].keys()):
        for key , values in resume_segments['skills'].items():
            skills += re.sub(key, '', ",".join(values), flags=re.IGNORECASE)            
        skills = skills.strip().strip(",").split(",")
    if len(skills) == 0:
        skills = extract_skills(full_text)
    skills = list(dict.fromkeys(skills).keys())
    return {
            "skills": skills,
    }
# print(read_file("resume_screening/sample_resumes/sample_resume_1.pdf"))
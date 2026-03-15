# Resume and Job Recommendation System

This project is a Resume and Job Recommendation System that utilizes Python, Flask, NLP (Natural Language Processing), and Web Scraping techniques. The system allows users to scrape resumes and job descriptions from various websites, analyze them using NLP techniques, and provide recommendations based on similarity.

## Features

The Resume and Job Recommendation System includes the following features:

- Web Scraping: The system is capable of scraping resumes and job descriptions from various websites. It utilizes web scraping techniques to extract relevant data for analysis.
- NLP Analysis: The scraped resumes and job descriptions are analyzed using NLP techniques. NLP helps in extracting meaningful information and features from the text data, enabling further processing and comparison.
- Cosine Similarity Algorithm: A cosine similarity algorithm is implemented to rank the resumes and jobs based on their similarity. The algorithm measures the similarity between two vectors by calculating the cosine of the angle between them. This ranking helps in providing accurate recommendations.
- REST API: The system provides a REST API using Flask. The API allows users to interact with the system, perform actions such as uploading resumes or job descriptions, and receive recommendations based on the uploaded data.

## Installation

To install and run the Resume and Job Recommendation System, follow these steps:

1. Clone the repository: `git clone https://github.com/jainiljakasaniya/resume-job-recommendation.git`
2. Navigate to the project directory: `cd resume-job-recommendation`
3. Install the dependencies: `pip install -r requirements.txt`
4. Start the Flask server: `python app.py`
5. Access the system in your browser at `http://localhost:5000`.

## Run with Docker

Use these steps to build and run the project with Docker:

1. Build image:
	- `docker build -t resume-app .`
2. Run container:
	- `docker run --name resume-app -p 5000:5000 resume-app`
3. Open in browser:
	- `http://localhost:5000`
4. Stop container:
	- `docker stop resume-app`
5. Remove container (optional):
	- `docker rm resume-app`

## Run with Docker Compose

1. Start app:
	- `docker compose up --build`
2. Open in browser:
	- `http://localhost:5000`
3. Stop app:
	- `Ctrl + C`
4. Remove containers and network:
	- `docker compose down`

## Usage

The Resume and Job Recommendation System provides a user-friendly web interface for interacting with the system. Here are the main steps to use the system:

1. Open your web browser and go to `http://localhost:8000`.
2. Upload resumes and job descriptions: Use the provided interface to upload resumes and job descriptions for analysis.
3. Analyze and rank: Once the resumes and job descriptions are uploaded, the system will analyze them using NLP techniques and rank them based on similarity using the cosine similarity algorithm.
4. View recommendations: The system will provide recommendations based on the uploaded data. These recommendations will be displayed on the web interface.
5. Explore more features: The system may include additional features such as filtering by keywords, saving preferences, or providing detailed analysis reports.
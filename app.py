import os
import uuid
from flask import Flask,render_template,redirect,request
from resume_screening import job

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')

from nltk.corpus import stopwords
import nltk

try:
    stopw = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    stopw = set(stopwords.words('english'))

# jobs = pd.read_csv(r'indeed_data.csv')
# jobs['test'] = jobs['description'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in (stopw)]))
# df = jobs.drop_duplicates(subset='test').reset_index(drop=True)
# df['clean'] = df['test'].apply(match.preprocessing)
# jobdesc = (df['clean'].values.astype('U'))

app=Flask(__name__)

os.makedirs(os.path.join(app.instance_path, 'resume_files'), exist_ok=True)

ALLOWED_RESUME_EXTENSIONS = {'.pdf', '.doc', '.docx'}


def _is_allowed_resume(filename):
    _, extension = os.path.splitext(filename.lower())
    return extension in ALLOWED_RESUME_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/employee')
def employee():
    return render_template('employee.html')

@app.route('/employeer')
def employeer():
    return render_template('employeer.html')

@app.route("/home")
def home():
    return redirect('/')


@app.route('/employee_submit',methods=['POST'])
def employee_submit_data():
    if request.method != 'POST':
        return render_template('employee.html')

    if 'userfile' not in request.files:
        return render_template('employee.html', error_message='Please choose a resume file first.')

    f = request.files['userfile']
    if not f or not f.filename:
        return render_template('employee.html', error_message='Please choose a resume file first.')

    if not _is_allowed_resume(f.filename):
        return render_template('employee.html', error_message='Only PDF, DOC, and DOCX files are supported.')

    unique_name = f"{uuid.uuid4().hex}_{f.filename}"
    saved_path = os.path.join(app.instance_path, 'resume_files', unique_name)
    f.save(saved_path)

    result_cosine = job.find_sort_job(saved_path)
    return render_template('employee.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
                           link_column="Link", zip=zip)

@app.route('/employeer_submit',methods=['POST'])
def employeer_submit_data():
    if request.method == 'POST':        
        files = request.files.getlist("userfile")
        if not files:
            return render_template('employeer.html', error_message='Please choose at least one resume file.')

        valid_files = [file for file in files if file and file.filename and _is_allowed_resume(file.filename)]
        if not valid_files:
            return render_template('employeer.html', error_message='Only PDF, DOC, and DOCX files are supported.')

        batch_dir = os.path.join(app.instance_path, 'resume_files', f"batch_{uuid.uuid4().hex}")
        os.makedirs(batch_dir, exist_ok=True)

        for file in valid_files:
            unique_name = f"{uuid.uuid4().hex}_{file.filename}"
            file.save(os.path.join(batch_dir, unique_name))

        result_cosine = job.find_sort_resume(f=batch_dir, link='https://in.indeed.com/viewjob?jk=56c808776a6c49db&tk=1gbhet5m92ek1000&from=serp&vjs=3')
        return render_template('employeer.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
                               link_column="link", zip=zip)
    return render_template('employeer.html')
            
    
    # skills = resparser.skill('instance/resume_files/{}'.format(f.filename))
    # skills.append(match.preprocessing(skills[0]))
    # del skills[0]

    # count_matrix = match.vectorizing(skills[0], jobdesc)
    # matchPercentage = match.coSim(count_matrix)
    # matchPercentage = pd.DataFrame(matchPercentage, columns=['Skills Match'])

    # #Job Vacancy Recommendations
    # result_cosine = df[['title','company','link']]
    # result_cosine = result_cosine.join(matchPercentage)
    # result_cosine = result_cosine[['title','company','Skills Match','link']]
    # result_cosine.columns = ['Job Title','Company','Skills Match','Link']
    # result_cosine = result_cosine.sort_values('Skills Match', ascending=False).reset_index(drop=True).head(20)

    # return render_template('employee.html', column_names=result_cosine.columns.values, row_data=list(result_cosine.values.tolist()),
    #                        link_column="Link", zip=zip)

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=False)

    #docker run -p 5000:5000 resume-app


    #if changes in file then use below command to run the app
    #docker build -t resume-app .

    #daily --> docker compose up
    #if changes -->docker compose up --build
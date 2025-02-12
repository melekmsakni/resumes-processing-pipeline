import streamlit as st
from DB.queries import *
import altair as alt
import numpy as np
import pandas as pd
import zipfile
import base64
from streamlit_tags import *
from time import sleep
import shutil
from stqdm import stqdm
import logging
from ollama import Client
logging.basicConfig(level=logging.INFO)
import requests
import ollama

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_processing.log"),  # Log to a file
        logging.StreamHandler()            # Also log to console
    ]
)

logger = logging.getLogger(__name__)

client_server='7869'
model='llama3.1'


def experience_score(cv, job_desc):

    if job_desc["total_years_of_work_experience"] != "":
        experience_required = job_desc["total_years_of_work_experience"]["field"]
    else:
        return 0

    if (
        "total_years_of_work_experience" not in cv
        or cv["total_years_of_work_experience"] is None
    ):
        cv_experience = 0  # or any default value you prefer
    else:
        cv_experience = float(cv["total_years_of_work_experience"])

    if cv_experience >= experience_required:
        experience_score = job_desc["total_years_of_work_experience"]["weight"]
    else:
        experience_score = (
            cv_experience * job_desc["total_years_of_work_experience"]["weight"]
        ) / experience_required
    return experience_score

def skills_score(cv, job_desc):

    if "skills" not in cv or job_desc["skills"] != "":
        job_skills = job_desc["skills"]["field"]
    else:
        return 0

    if len(cv["skills"])==0 :
        return 0
    else:
        cv_skills = cv["skills"]

    cv_skills = [x.lower() for x in cv_skills]
    job_skills = [x.lower() for x in job_skills]

    absent_skills = set(job_skills) - set(cv_skills)

    if len(list(absent_skills)) <= 0:
        skills_score = job_desc["skills"]["weight"]
    else:
        number_prsent_skils = len(job_skills) - len(list(absent_skills))
        skills_score = (number_prsent_skils * job_desc["skills"]["weight"]) / len(
            job_skills
        )

    return skills_score

def education_score(cv, job_desc):
    education_score = 0
    if job_desc["education"] != "":
        job_university = job_desc["education"]["field"]
    else:
        return education_score

    cv_education = cv.get("education", "")
    cv_universities = []
    if len(cv_education)==0:
        return education_score
    
    for i in cv_education:
        if i["degree"] is not None:
            cv_universities.append(i["degree"])

    cv_universities = [x.lower() for x in cv_universities]
    job_university = job_university.lower()

    
    for degree in cv_universities:
        if job_university in degree:
            education_score = job_desc["education"]["weight"]
            break
    return education_score

def languages_score(cv, job_desc):

    if job_desc["languages"] != "":
        job_languages = job_desc["languages"]["field"]
    else:
        return 0

    if "languages" not in cv or len(cv["languages"]) ==0:
        return 0
    else:
        cv_languages = cv["languages"]

    cv_languages = [x.lower() for x in cv_languages]
    job_languages = [x.lower() for x in job_languages]

    languages_found = 0
    for j in job_languages:
        for l in cv_languages:
            if j in l:
                languages_found = languages_found + 1

    if languages_found == len(job_languages):
        languages_score = job_desc["languages"]["weight"]

    else:
        languages_score = (languages_found * job_desc["languages"]["weight"]) / len(
            job_languages
        )

    return languages_score

def gap_years_score(cv, job_desc):

    if job_desc["gap_years"] != "":
        gap_years_job = job_desc["gap_years"]["field"]
    else:
        return 0

    if "gap_years" not in cv or cv["gap_years"] is None:
        gap_years = 0
    else:
        gap_years = float(cv["gap_years"])

    gap_years_score = 0
    if gap_years <= gap_years_job:
        gap_years_score = job_desc["gap_years"]["weight"]

    return gap_years_score

def specific_score_ploting(field,score,job):
    return  score/job[field]["weight"] if job[field]["weight"] !=0 else 0


def upadate_ui_states(state_name, value):
    if state_name == "job_list":
        if state_name in st.session_state:
            st.session_state[state_name].append(value)
        else:
            st.session_state[state_name] = [value]


def calculate_score_job(job_data):
    job, job_id = job_data

    resume_list = fetch_all("resumes")

    
    for resume in resume_list:

        exp_score = experience_score(resume, job)
        skills_score_value = skills_score(resume, job)
        edu_score = education_score(resume, job)
        lang_score = languages_score(resume, job)
        gap_year_score = gap_years_score(resume, job)

        # Calculate total score
        total_score = (
            exp_score + skills_score_value + edu_score + lang_score + gap_year_score
        )

            
        scoring_doc = {
            "job_id": job_id,
            "job_title": job["job_title"]["field"],
            "resume_id": resume["_id"],  # Assuming resume has an "_id" field
            "total_score": total_score * 100,  # Convert to percentage
            "specific_scores": {
                "total_years_of_work_experience": specific_score_ploting("total_years_of_work_experience",exp_score,job),
                "skills": specific_score_ploting("skills",skills_score_value,job),
                "education": specific_score_ploting("education",edu_score,job),
                "languages": specific_score_ploting("languages",lang_score,job),
                "gap_years": specific_score_ploting("gap_years",gap_year_score,job),
            },
        }
        insert_document("scoring", scoring_doc)


def get_top_candidates(job):

    jobs_critiria = []
    job_desc = fetch_one("jobs", {"job_title.field": job})
    if job_desc:
        for key in job_desc:
            if key != "_id" and key != "job_title" and job_desc[key]["score"] != 0 :
                jobs_critiria.append(key)
            
            
    

    resume_scores = fetch_all("scoring", {"job_title": job})
    best_scores = sorted(resume_scores, key=lambda x: x["total_score"], reverse=True)[
        :1000
    ]

    data = {
        "Name": [],
        "Email": [],
        "Phone": [],
        "Title": [],
        "Experience": [],
        "Score": [],
    }

    score_list = []
    resumes_pdf_path=[]

    for score in best_scores:
        resume_info = fetch_one("resumes", {"_id": score["resume_id"]})

        if resume_info is None:
            logging.error(f"Resume with ID {score['resume_id']} not found.")
            continue

        data["Name"].append(resume_info["name"])
        data["Email"].append(resume_info["email"])
        data["Phone"].append(resume_info["phone"])
        data["Title"].append(resume_info["title"])
        data["Experience"].append(resume_info["total_years_of_work_experience"])
        data["Score"].append(score["total_score"])

        score_per_person = [
            score["specific_scores"][key]
            for key in jobs_critiria
            if key in jobs_critiria
        ]

        score_list.append(score_per_person)
        resumes_pdf_path.append(resume_info["pdf_resume"])

    return data, jobs_critiria, score_list ,resumes_pdf_path


def adding_job_form(skills,job_title,main_col):
    skills_score = st.select_slider(
        "Skills Score",
        options=[0, 1, 2, 3, 4, 5],
        key="skills_score",
    )
    
    degree = st.text_input("Required Degree")

    degree_dcore = st.select_slider(
        "degree score ", options=[0, 1, 2, 3, 4, 5], key="degree_score"
    )

    with main_col[1]:
        # Total Years of Work Experience
        experience = st.number_input("Total Years of Work Experience")
        experience_score = st.select_slider(
            "Experience Score", options=[0, 1, 2, 3, 4, 5], key="experience_score"
        )


        # Gap Years
        gap_years = st.number_input("Gap Years")
        gap_years_score = st.select_slider(
            "Gap Years Score", options=[0, 1, 2, 3, 4, 5], key="gap_years_score")

    
        # Languages
        languages = st.multiselect("Languages", ["french", "english", "arabic"])
        languages_score = st.select_slider(
            "Languages Score", options=[0, 1, 2, 3, 4, 5], key="languages_score"
        )

    submit_button = st.form_submit_button(label="ADD JOB", use_container_width=True)

    def get_weights(dic):
        weighted_dic = {}
        total_score = 0
        # get totalscore
        for key in dic:
            if key == "_id":

                continue
            total_score = total_score + dic[key]["score"]
        for key in dic:
            if key == "_id":

                continue
            weight = dic[key]["score"] / total_score if total_score > 0 else 0
            weighted_dic[key] = {"field": dic[key]["field"], "weight": weight,"score":dic[key]["score"]}
        return weighted_dic
    
    if submit_button:
        if  job_title == "":
            st.markdown(
                """
                <p style="color: red; font-weight: bold;">Job's Name is Mandatory!</p>
                """, 
                unsafe_allow_html=True
            )
            return
        elif job_title in st.session_state.job_list :
            st.markdown(
                """
                <p style="color: red; font-weight: bold;">Job's Name Already exists!</p>
                """, 
                unsafe_allow_html=True
            )           
            return
        
        new_job = {
            "job_title": {"field": job_title, "score": 0},
            "education": {
                "field": degree,
                "score": degree_dcore,
            },
            "skills": {
                "field": skills,
                "score": skills_score,
            },
            "total_years_of_work_experience": {
                "field": experience,
                "score": experience_score,
            },
            "gap_years": {
                "field": gap_years,
                "score": gap_years_score,
            },
            "languages": {
                "field": languages,
                "score": languages_score,
            },
        }
        new_job_weight=get_weights(new_job)

        job_id = insert_document("jobs",new_job_weight )

        upadate_ui_states("job_list", job_title)
        st.write("Job added and saved successfully!")

        # calculating score
        job_data = new_job_weight, job_id.inserted_id
        calculate_score_job(job_data)


def post_process_upload_resues_ZIP(uploaded_folder):

    folder_name = uploaded_folder.name.split(".")[0]

    extraction_folder = "unziped_folders"
    resumes_extracted_folder = os.path.join(extraction_folder, folder_name)

    # Save uploaded folder
    with open(uploaded_folder.file_id, "wb") as f:
        f.write(uploaded_folder.read())
    

    # Unzip the folder
    with zipfile.ZipFile(uploaded_folder.file_id, "r") as zip_ref:
        zip_ref.extractall(resumes_extracted_folder)
    
     

    if os.path.exists(uploaded_folder.file_id):
        os.remove(uploaded_folder.file_id)

    unziped_folder=os.listdir(resumes_extracted_folder)[0]

    resumes_extracted_folder_last=os.path.join(resumes_extracted_folder, unziped_folder)


    process_folder_job(resumes_extracted_folder_last)

def check_LLM_model_existing(model,port):
    
    OLLAMA_SERVER=f'http://localhost:7869'
    CLIENT = Client(host=OLLAMA_SERVER)

    try:
        CLIENT.show(model)
        return 'models exist'
    except ollama.ResponseError as e:
        logger.error('Error: could not find the requested model locally')
        if e.status_code == 404:
            logger.info(f'pulling {model} from ollama')
            try:
                CLIENT.pull(model)
                return 'model pulled'
            except Exception as e :
                logger.error("couldn't find the model in ollama try another one ")
                return 
    

def calculate_score_candidate(resume,resume_id):
    job_list = fetch_all("jobs")

    for job in job_list:

        exp_score = experience_score(resume, job)
        skills_score_value = skills_score(resume, job)
        edu_score = education_score(resume, job)
        lang_score = languages_score(resume, job)
        gap_year_score = gap_years_score(resume, job)

        # Calculate total score
        total_score = (
            exp_score + skills_score_value + edu_score + lang_score + gap_year_score
        )

            
        scoring_doc = {
            "job_id": job["_id"],
            "job_title": job["job_title"]["field"],
            "resume_id": resume_id,  
            "total_score": total_score * 100,  
            "specific_scores": {
                "total_years_of_work_experience": specific_score_ploting("total_years_of_work_experience",exp_score,job),
                "skills": specific_score_ploting("skills",skills_score_value,job),
                "education": specific_score_ploting("education",edu_score,job),
                "languages": specific_score_ploting("languages",lang_score,job),
                "gap_years": specific_score_ploting("gap_years",gap_year_score,job),
            },
        }
        insert_document("scoring", scoring_doc)



def process_folder_job(folder_path):
    url = "http://localhost:8004/upload_resume/"



    check=check_LLM_model_existing(model,client_server)

    if check==None :
        st.warning('model dosent exist fix it ', icon="⚠️")
        return

    lm=os.listdir(folder_path)

    
    

    for file in stqdm(lm):
        
        file_path = os.path.join(folder_path, file)
        

        with open(file_path, "rb") as file:
            params = {"file": file,'model':model,'port':client_server}
            resume_json = requests.post(url, files=params)

        if resume_json is None :
            logging.error(f"llama None value returned {file_path}")
            continue
                
        resume_dic=resume_json.json()['json_resume']

        if resume_dic is  None :
            continue

        resume_dic["pdf_resume"] = file_path
        
        id=insert_document('resumes',resume_dic)
        
        calculate_score_candidate(resume_dic,id.inserted_id)
        
            


def get_jobs_list():

    jobs_data = {}

    jobs_list = fetch_all("jobs")
    if len(jobs_list)==0:
        return jobs_data
    keys=jobs_list[0].keys()
    keys=list(keys)[1:]

    
    for job in jobs_list :
        for key in keys:
            if key not in jobs_data :
                jobs_data[key]=[job[key]['field']]
            else :
                jobs_data[key].append(job[key]['field'])

    
            

        

    return jobs_data



def make_donut(input_response, input_text, input_color):
    if input_color == "blue":
        chart_color = ["#29b5e8", "#155F7A"]
    if input_color == "green":
        chart_color = ["#27AE60", "#12783D"]
    if input_color == "orange":
        chart_color = ["#F39C12", "#875A12"]
    if input_color == "red":
        chart_color = ["#E74C3C", "#781F16"]

    source = pd.DataFrame(
        {"Topic": ["", input_text], "% value": [100 - input_response, input_response]}
    )
    source_bg = pd.DataFrame({"Topic": ["", input_text], "% value": [100, 0]})

    plot = (
        alt.Chart(source)
        .mark_arc(innerRadius=45, cornerRadius=25)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(
                    # domain=['A', 'B'],
                    domain=[input_text, ""],
                    # range=['#29b5e8', '#155F7A']),  # 31333F
                    range=chart_color,
                ),
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )

    text = plot.mark_text(
        align="center",
        color="#29b5e8",
        font="Lato",
        fontSize=32,
        fontWeight=700,
        fontStyle="italic",
    ).encode(text=alt.value(f"{input_response} %"))
    plot_bg = (
        alt.Chart(source_bg)
        .mark_arc(innerRadius=45, cornerRadius=20)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(
                    # domain=['A', 'B'],
                    domain=[input_text, ""],
                    range=chart_color,
                ),  # 31333F
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )
    return plot_bg + plot + text


def display_resume_pdf(file):
    from pathlib import Path
    if not Path(file).exists():
        st.write("resume not found ")
        return

    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def initilize_job_list():
    jobs=[]
    job_list = fetch_all("jobs")

    for job in job_list:
        jobs.append(job["job_title"]["field"])

    return jobs


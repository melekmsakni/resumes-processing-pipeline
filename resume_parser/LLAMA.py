from ollama import Client
import json
import logging
import ollama


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("llama.log"),  # Log to a file
        logging.StreamHandler()            # Also log to console
    ]
)

logger = logging.getLogger(__name__)

def check_required_keys(data):
    
    # Define the required keys
  required_keys = [
    'name', 'email', 'location', 'phone', 'title', 'work_experience',
    'total_years_of_work_experience', 'skills', 'languages', 'gap_years', 
    'education', 'certifications'
]


  missing_keys = [key for key in required_keys if key not in data]
  
  if missing_keys:
      return False  
  return True






def LLM_text_to_json(file_path,raw_text,model,port):

    port='11434'
    OLLAMA_SERVER=f'http://ollama:{port}'
    CLIENT = Client(host=OLLAMA_SERVER)
    MODEL=model
    
    prompt = f"""
You will be given a resume in text format in messy and unstructured way in either English or French. Your task is to extract relevant information and structure it in the following exact JSON format without adding any additional text to the output:

Important:

Strictly follow the provided structure and ensure all data fits into the exact format.
Do not add, modify, or guess information outside of what is explicitly provided in the resume.
Ensure all values are returned in the correct format, with lists remaining lists, numbers returned as numbers, and strings returned as strings.
the return must contain only Json without adding any additional text

{{
  "name": null,
  "email": null,
  "location": null,
  "phone": null,
  "title": null,
  "work_experience": [
    {{
      "title": null,
      "duration": null
    }}
  ],
  "total_years_of_work_experience": 0,
  "education": [{{
    "institution": null,
    "degree": null
  }}],
  "skills": [],
  "languages": [],
  "gap_years": 0,
  "certifications": []
}}
Instructions:

Work Experience Durations:

Extract the job title and calculate the job duration in months for each job.
Durations might be given in either months or years. Convert years to months (e.g., 3 years = 36 months).
DO NOT GUESS job durations if information is missing. Return null if no duration is provided.
in the work experience he specifies that he is actually working in that position then use October 2024 as end date

Total Years of Work Experience:

Sum up all job durations (converted to months) and convert the total back to years (e.g., 18 months = 1.5 years ,6 months = 0.5 years ).
DO NOT GUESS. 

Gap Years:

Identify gaps of 3 months or more between jobs from the work experience timeline.
Convert gaps into years (e.g., 3 months = 0.25 years) and sum up all such gaps.
If no gaps are found, return 0.

Skills:

Extract all technical skills from the entire resume (not just from the "Skills" section).
Return all skills in lowercase.
If no skills are found, return an empty list ([]).

Languages:

languages need to be added to the json in English only
example: [french, english, arabic] 
Extract all languages and ensure they are returned in English and lowercase.
If the languages in the text are provided in other languages like French, translate them to English 
example: [francais, anglais, arabe, allemand] needs to be translated to [french, english, arabic, german]
If no languages are mentioned, return an empty list ([]).

Education:

Follow the exact structure for education as outlined in the template.
without adding any extra dictionaries or nesting unnecessary objects.

certifications: 

Follow the exact structure for certifications without adding any extra dictionaries or nesting unnecessary objects.

Stick to the Structure:

DO NOT change the structure of the output.
Ensure that if the template specifies a list, it remains a list.
Ensure all values follow the correct data types (e.g., strings for name, title, institution, numbers for duration, etc.).
Do not add or modify anything outside of the provided template.
the return must contain only Json without adding any additional text

Example Output:

{{
  "name": "Anas Ben Abdallah",
  "email": "benabdallah.anas2000@gmail.com",
  "location": "Tunisie",
  "phone": "+216 95200829",
  "title": "Candidature pour un stage PFE | Ingénieur En Informatique",
  "work_experience": [
    {{
      "title": "Stage d'été : Analyse de logs",
      "duration": 2
    }},
    {{
      "title": "Stage d'été : Site de films",
      "duration": 2
    }}
  ],
  "total_years_of_work_experience": 0.3,
  "skills": ["mongodb", "react", "nodejs", "spring boot", "docker"],
  "languages": ["french", "english", "arabic"],
  "gap_years": 0.25,
  "education": [{{
    "institution": 'higher institut of science',
    "degree": 'bachelor in computer science'
  }}],
  "certifications": [
    "aws cloud practitioner",
    "azure pl900"
  ]
}}

text:

{raw_text}

"""


    response = CLIENT.chat(model=MODEL, messages=[
    {
        'role': 'user',
        'content': prompt ,
    },
    ])
    
    json_string = response['message']['content']

    try :

        json_dict = json.loads(json_string)
        if check_required_keys(json_dict):
            return json_dict
        else:
          logger.error(f"{file_path} - error json data dosent respect format ")
          return

    except Exception as e :
        logger.error(f"{file_path} - error while converting LLM respond to json")
        return 
    
    


    


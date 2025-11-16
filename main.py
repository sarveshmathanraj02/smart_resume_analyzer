import random 
import yt_dlp as ytdlp
import streamlit as st
import pdfplumber
import pymysql
import pandas as pd
import base64
import re
import spacy
from spacy.matcher import PhraseMatcher
from streamlit_tags import st_tags
from courses import ds_course, web_course, android_course, ios_course, uiux_course, software_engineering_courses, resume_videos, interview_videos 
from admin import admin_panel  
from db_connection import connect_to_db, create_table 

nlp = spacy.load("en_core_web_sm")

role_descriptions = {
  "Software Engineer": "A Software Engineer is responsible for designing, developing, and maintaining software applications. They work with various programming languages and frameworks to create efficient and scalable solutions.",
  "Data Scientist": "A Data Scientist analyzes complex data sets to derive insights and inform business decisions. They use statistical methods, machine learning algorithms, and data visualization techniques.",
  "Web Developer": "A Web Developer builds and maintains websites, ensuring they are user-friendly, visually appealing, and functional. They work with HTML, CSS, JavaScript, and backend technologies.",
  "DevOps Engineer": "A DevOps Engineer focuses on the collaboration between development and operations teams, automating processes and improving the deployment pipeline to enhance software delivery.",
  "Machine Learning Engineer": "A Machine Learning Engineer designs and implements machine learning models and algorithms to enable computers to learn from and make predictions based on data.",
  "Cybersecurity Analyst": "A Cybersecurity Analyst protects an organization’s computer systems and networks by monitoring for security breaches, implementing security measures, and conducting risk assessments.",
  "Database Administrator": "A Database Administrator manages databases, ensuring their performance, security, and availability. They handle data storage, backups, and recovery procedures.",
  "Systems Analyst": "A Systems Analyst evaluates and improves IT systems, gathering requirements from users and translating them into technical specifications for development.",
  "Mobile App Developer": "A Mobile App Developer creates applications for mobile devices, focusing on user experience and functionality. They develop for platforms like iOS and Android.",
  "Game Developer": "A Game Developer designs and creates video games across various platforms. They work with graphics, sound, and gameplay mechanics to create engaging experiences.",
  "Cloud Engineer": "A Cloud Engineer manages cloud infrastructure and services, focusing on deployment, management, and security of applications in the cloud.",
  "UI/UX Designer": "A UI/UX Designer focuses on user interface and user experience design, ensuring that applications are intuitive, accessible, and visually appealing."
}

role_skills = {
  "Software Engineer": [
      "Java", "Python", "C++", "Git", "Problem Solving", "OOP",
      "Data Structures", "Algorithms", "Software Development Life Cycle (SDLC)",
      "Agile Methodologies", "RESTful APIs", "Debugging", "Unit Testing",
      "Design Patterns", "Microservices Architecture","Pandas",'Numpy'
  ],
  "Data Scientist": [
      "Python", "Machine Learning", "Data Visualization", "Statistical Analysis",
      "SQL", "R", "Big Data Technologies", "Data Cleaning", "Feature Engineering",
      "Deep Learning", "Natural Language Processing", "A/B Testing",
      "Data Mining", "Predictive Modeling", "Exploratory Data Analysis","Pandas",'Numpy'
  ],
  "Web Developer": [
      "HTML", "CSS", "JavaScript", "React", "Node.js", "Git",
      "Responsive Web Design", "Version Control", "Cross-Browser Compatibility",
      "AJAX", "RESTful Services", "GraphQL", "SEO Principles",
      "Webpack", "Front-End Frameworks"
  ],
  "DevOps Engineer": [
      "CI/CD", "AWS", "Docker", "Kubernetes", "Python", "Monitoring Tools",
      "Infrastructure as Code (IaC)", "Configuration Management",
      "Networking", "Scripting", "Version Control Systems",
      "Cloud Services", "Load Balancing", "Automation Tools"
  ],
  "Machine Learning Engineer": [
      "Python", "Machine Learning", "TensorFlow", "Data Preprocessing",
      "Statistical Analysis", "Deep Learning", "Model Deployment",
      "Hyperparameter Tuning", "Feature Engineering", "Computer Vision",
      "Natural Language Processing", "Data Pipeline Construction","Pandas",'Numpy'
  ],
  "Cybersecurity Analyst": [
      "Network Security", "Risk Assessment", "Incident Response",
      "Ethical Hacking", "Security Auditing", "Threat Intelligence",
      "Malware Analysis", "Firewalls", "Intrusion Detection Systems",
      "Vulnerability Assessment", "Security Information and Event Management (SIEM)"
  ],
  "Database Administrator": [
      "SQL", "Database Design", "Backup and Recovery", "Performance Tuning",
      "Database Migration", "Data Warehousing", "Stored Procedures",
      "Indexing", "Data Security", "NoSQL Databases",
      "Database Monitoring Tools"
  ],
  "Systems Analyst": [
      "Requirements Gathering", "System Design", "Process Improvement",
      "Technical Documentation", "Stakeholder Management", "Agile Methodologies",
      "Business Analysis", "User Acceptance Testing (UAT)",
      "Change Management", "Risk Management", "Database Management"
  ],
  "Mobile App Developer": [
      "Swift", "Kotlin", "API Integration", "UI/UX Design Principles",
      "Cross-Platform Development", "Version Control", "Agile Methodologies",
      "Mobile UI Frameworks", "Database Management for Mobile",
      "App Store Guidelines", "Testing and Debugging"
  ],
  "Game Developer": [
      "Unity", "C#", "3D Modeling", "Problem-Solving", "Game Design Principles",
      "Artificial Intelligence in Games", "Physics Simulation",
      "Shader Programming", "Level Design", "Multiplayer Networking"
  ],
  "Cloud Engineer": [
      "AWS", "Cloud Security", "Networking", "Terraform", "Docker",
      "Kubernetes", "Cloud Services Management", "Microservices Architecture",
      "Serverless Computing", "CI/CD for Cloud", "Data Storage Solutions"
  ],
  "UI/UX Designer": [
      "User Research", "Wireframing", "Visual Design Principles",
      "User Testing", "Prototyping Tools (e.g., Figma, Adobe XD)",
      "Interaction Design", "Information Architecture", "Usability Testing",
      "Responsive Design", "Collaboration with Developers"
  ]
}

def show_pdf(file):
   base64_pdf = base64.b64encode(file.read()).decode('utf-8')
   pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
   st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_reader(file):
   with pdfplumber.open(file) as pdf:
       text = ""
       for page in pdf.pages:
           text += page.extract_text() + '\n'
   return text

def extract_basic_info(text):
  name_pattern = r"(?:(?:Name:\s*)|(?:\b(?:First|Last|Full)?\s*Name:\s*)|(?:[A-Z][a-zA-Z\-' ]{1,}))(?:[ ]?[A-Z][a-zA-Z\-' ]{1,}){1,2}"
  name = re.search(name_pattern, text)
  email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
  email = re.search(email_pattern, text)
  phone_pattern = r"(?:\+?(\d{1,3})[-.\s]?(\(?\d{1,4}?\)?[-.\s]?)(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9}))"
  mobile_number = re.search(phone_pattern, text)
  if name:
      print(f"Extracted Name: {name.group(0).strip()}")
  else:
      print("Name extraction failed.")
  if mobile_number:
      print(f"Extracted Phone Number: {mobile_number.group(0).strip()}")
  else:
      print("Phone Number extraction failed.")
  return {
      "name": name.group(0).strip() if name else "N/A",
      "email": email.group(0) if email else "N/A",
      "mobile_number": mobile_number.group(0).strip() if mobile_number else "N/A",
  }

def calculate_resume_score(basic_info, extracted_skills, total_keywords, total_structure_criteria):
  score = 0
  if basic_info['name'] != "N/A":
      score += 10
  if basic_info['email'] != "N/A":
      score += 5
  score += len(extracted_skills) * 2
  score += (total_keywords / 2)
  score += total_structure_criteria * 5
  max_score = 100
  normalized_score = min(score, max_score)
  return normalized_score

def fetch_yt_thumbnail(link):
  try:
      if "youtube.com/watch?v=" not in link and "youtu.be/" not in link:
          raise ValueError("Invalid YouTube link format.")
      if "youtube.com/watch?v=" in link:
          video_id = link.split("v=")[-1].split("&")[0]  
      elif "youtu.be/" in link:
          video_id = link.split("youtu.be/")[-1].split("?")[0]  
      thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"  
      print(f"Fetching thumbnail for video ID: {video_id} - Thumbnail URL: {thumbnail_url}")  
      return thumbnail_url, link
  except Exception as e:
      print(f"Error fetching thumbnail for link: {link} - {e}")
      return None, None

def course_recommender(extracted_skills, role):
  st.subheader("Courses & Certificates🎓 Recommendations")
  rec_course = []
  required_skills = role_skills.get(role, [])
  missing_skills = [skill for skill in required_skills if skill not in extracted_skills]
  course_set = set()
  for skill in missing_skills:
      if skill in ['Data Analysis', 'Machine Learning', 'Deep Learning']:
          course_set.update(tuple(course) for course in ds_course)
      if skill in ['Web Development', 'JavaScript', 'HTML', 'CSS']:
          course_set.update(tuple(course) for course in web_course)
      if skill in ['Android Development', 'Java']:
          course_set.update(tuple(course) for course in android_course)
      if skill in ['iOS Development', 'Swift']:
          course_set.update(tuple(course) for course in ios_course)
      if skill in ['UI/UX', 'Design']:
          course_set.update(tuple(course) for course in uiux_course)
      for key, courses in software_engineering_courses.items():
          if skill in key:
              course_set.update(tuple(course) for course in courses)
  course_list = list(course_set)
  if not course_list:
      st.warning("No courses found for the missing skills.")
  else:
      no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, min(10, len(course_list)), 4)
      random.shuffle(course_list)
      for i, (c_name, c_link) in enumerate(course_list[:no_of_reco], 1):
          st.markdown(f"({i}) [{c_name}]({c_link})")
          rec_course.append(c_name)
  return rec_course

def extract_skills(resume_text, skills_list):
    resume_text = resume_text.lower()
    skills_list = [skill.lower() for skill in skills_list]
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(skill) for skill in skills_list]
    matcher.add("Skills", patterns)
    resume_text = re.sub(r'[^\w\s+]', ' ', resume_text)  
    doc = nlp(resume_text)
    matches = matcher(doc)
    extracted_skills = list(set([doc[start:end].text.strip() for match_id, start, end in matches]))
    print(f"Extracted skills: {extracted_skills}")
    return extracted_skills

def determine_level(resume_text, extracted_skills):
   experience_level = "Fresher"
   experience_pattern = r'(\d+)\s+years? of experience'
   experience_match = re.search(experience_pattern, resume_text.lower())
   years_of_experience = int(experience_match.group(1)) if experience_match else 0
   skill_count = len(extracted_skills)
   if years_of_experience < 2 or skill_count < 10:
       experience_level = "Fresher"
   elif 2 <= years_of_experience <= 5 or (10 <= skill_count <= 20):
       experience_level = "Intermediate"
   elif years_of_experience > 5 or skill_count > 20:
       experience_level = "Advanced"
   return experience_level

def match_skills_for_role(extracted_skills, role):
    required_skills = role_skills.get(role, [])
    required_skills_normalized = [skill.lower() for skill in required_skills]
    extracted_skills_normalized = [skill.lower() for skill in extracted_skills]
    matched_skills = [skill for skill in extracted_skills_normalized if skill in required_skills_normalized]
    missing_skills = [skill for skill in required_skills_normalized if skill not in extracted_skills_normalized]
    matched_skills_original = [skill.capitalize() for skill in matched_skills]
    missing_skills_original = [skill.capitalize() for skill in missing_skills]
    match_score = (len(matched_skills) / len(required_skills_normalized)) * 100 if required_skills_normalized else 0
    return matched_skills_original, match_score, missing_skills_original

def display_videos():
  st.subheader("Resume Building Tips 📋")
  resume_columns = st.columns(2)  
  for idx, link in enumerate(resume_videos):
      thumbnail_url, video_url = fetch_yt_thumbnail(link)
      if thumbnail_url:
          with resume_columns[idx % 2]:
              st.markdown(
                  f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" width="400"></a>',
                  unsafe_allow_html=True
              )
      else:
          st.warning(f"Thumbnail not found for link: {link}")
  st.subheader("Interview Preparation 🎥")
  interview_columns = st.columns(2)
  for idx, link in enumerate(interview_videos):
      thumbnail_url, video_url = fetch_yt_thumbnail(link)
      if thumbnail_url:
          with interview_columns[idx % 2]:
              st.markdown(
                  f'<a href="{video_url}" target="_blank"><img src="{thumbnail_url}" width="400"></a>',
                  unsafe_allow_html=True
              )
      else:
          st.warning(f"Thumbnail not found for link: {link}")

def is_resume(text):
  resume_keywords = ["experience", "education", "skills", "certifications", "projects", "summary", "contact"]
  return any(keyword in text.lower() for keyword in resume_keywords)

def run():
   st.title("Smart Resume Analyser")
   st.sidebar.markdown("# Choose User")
   activities = ["Normal User", "Admin"]
   choice = st.sidebar.selectbox("Choose among the given options:", activities)
   connection = connect_to_db()
   create_table()
   cursor = connection.cursor()
   try:
       if choice == 'Normal User':
           pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
           if pdf_file:
               show_pdf(pdf_file)
               resume_text = pdf_reader(pdf_file)
               if not is_resume(resume_text):
                   st.error("Uploaded file does not appear to be a resume. Please upload a valid resume.")
                   return
               if resume_text:
                   st.header("Resume Analysis")
                   st.success("Resume successfully read!")
                   st.text_area("Resume Text", value=resume_text, height=300)
                   basic_info = extract_basic_info(resume_text)
                   st.subheader("Basic Info")
                   st.write(f"Name: {basic_info['name']}")
                   st.write(f"Email: {basic_info['email']}")
                   st.write(f"Mobile Number: {basic_info['mobile_number']}")
                   if basic_info['name'] == "N/A":
                       st.warning("Name could not be extracted from the resume.")
                   if basic_info['mobile_number'] == "N/A":
                       st.warning("Mobile number could not be extracted from the resume.")
                   skills_list = [
                       'Python', 'Java', 'C++', 'C#', 'JavaScript', 'HTML', 'CSS', 'SQL', 'Go', 'Ruby',
                       'Swift', 'Kotlin', 'PHP', 'R', 'Perl', 'TypeScript', 'C', 'Rust', 'Scala', 'MATLAB',
                       'Shell Scripting', 'Bash', 'PowerShell', 'VBA', 'Fortran', 'COBOL',
                       'HTML5', 'CSS3', 'Bootstrap', 'React.js', 'Angular.js', 'Vue.js', 'Node.js', 'Express.js',
                       'Django', 'Flask', 'Laravel', 'Spring Boot', 'GraphQL', 'ASP.NET', 'Webpack', 'SASS',
                       'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle Database', 'Firebase', 'Cassandra',
                       'Redis', 'Elasticsearch', 'MariaDB', 'CouchDB', 'DynamoDB', 'Neo4j',
                       'TensorFlow', 'Keras', 'PyTorch', 'scikit-learn', 'OpenCV', 'Pandas', 'NumPy',
                       'Matplotlib', 'Seaborn', 'NLTK', 'Spacy', 'Hugging Face', 'SciPy', 'XGBoost',
                       'LightGBM', 'PyCaret', 'Deep Learning', 'Reinforcement Learning', 'Neural Networks',
                       'Tableau', 'Power BI', 'Excel', 'Google Sheets', 'Looker', 'D3.js', 'Altair',
                       'Plotly', 'Dash', 'Data Wrangling', 'Data Cleaning', 'ETL',
                       'AWS', 'Azure', 'Google Cloud', 'Heroku', 'Docker', 'Kubernetes', 'Jenkins',
                       'Terraform', 'Ansible', 'Chef', 'Puppet', 'Nagios', 'GitHub Actions', 'CI/CD',
                       'CloudFormation', 'Lambda', 'Cloud Functions',
                       'Penetration Testing', 'Ethical Hacking', 'Network Security', 'Cryptography',
                       'Cybersecurity Frameworks', 'Nmap', 'Wireshark', 'Metasploit', 'OWASP',
                       'ISO 27001', 'Firewall Configuration',
                       'Android', 'iOS', 'Flutter', 'React Native', 'SwiftUI', 'Xamarin',
                       'Kotlin Multiplatform', 'Cordova', 'Ionic',
                       'Unity', 'Unreal Engine', 'Game Physics', 'Game AI', 'Cocos2d', 'CryEngine',
                       'Selenium', 'Cypress', 'Appium', 'JUnit', 'Mockito', 'Postman', 'SoapUI',
                       'LoadRunner', 'JMeter', 'QA Automation', 'Manual Testing',
                       'Linux', 'Windows Server', 'Unix', 'MacOS', 'TCP/IP', 'UDP', 'DNS', 'DHCP',
                       'Active Directory', 'VPN', 'SSH', 'FTP', 'Network Protocols',
                       'Team Collaboration', 'Project Management', 'Agile Methodologies', 'Scrum',
                       'Time Management', 'Communication Skills', 'Critical Thinking', 'Problem Solving',
                       'Blockchain', 'Ethereum', 'Solidity', 'Smart Contracts', 'Web3.js',
                       'Internet of Things (IoT)', 'Raspberry Pi', 'Arduino', 'Edge Computing',
                       'Version Control', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'JIRA', 'Confluence',
                       'Agile Development', 'Kanban', 'Design Patterns', 'Object-Oriented Programming',
                       'Functional Programming', 'Data Structures', 'Algorithms'
                   ]
                   extracted_skills = extract_skills(resume_text, skills_list)
                   role = st.selectbox("Select Role for Analysis", list(role_skills.keys()))
                   st.write(role_descriptions[role])
                   matched_skills, match_score, missing_skills = match_skills_for_role(extracted_skills, role)
                   st.subheader("Skills Overview")
                   st.write("Extracted Skills:", ", ".join(extracted_skills) if extracted_skills else "No skills found.")
                   st.write("Matched Skills:", ", ".join(matched_skills))
                   st.write("Missing Skills:", ", ".join(missing_skills))
                   st.write(f"Skill Match Score: {match_score:.2f}%")
                   total_keywords = 20
                   total_structure_criteria = 3
                   resume_score = calculate_resume_score(basic_info, extracted_skills, total_keywords, total_structure_criteria)
                   st.subheader("Resume Score")
                   st.write(f"{resume_score}")
                   experience_level = determine_level(resume_text, extracted_skills)
                   st.subheader("Experience Level")
                   st.write(f"Based on the analysis, you are categorized as: {experience_level}")
                   rec_courses = course_recommender(extracted_skills, role)
                   display_videos()
                   timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                   cursor.execute(
                       "INSERT INTO user_data (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (basic_info['name'], basic_info['email'], resume_score, timestamp, "N/A", role,
                        experience_level,
                        ", ".join(extracted_skills), ", ".join(set(matched_skills)), ", ".join(rec_courses))
                   )
                   connection.commit()
       elif choice == 'Admin':
           admin_panel(cursor)
   finally:
       connection.close()

if __name__ == "__main__":
   run()
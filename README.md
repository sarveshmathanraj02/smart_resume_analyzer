# Smart Resume Analyzer

An AI-powered resume analysis web application built with Python, Streamlit, spaCy, pdfplumber, and MySQL.
The app extracts key information from resumes, evaluates candidate skills, recommends courses, predicts suitable job roles, and provides an admin dashboard with analytics.

---

## 📁 Repository Structure

smart_resume_analyzer/  
├── main.py                   
├── db_connection.py          
├── admin.py                  
├── courses.py                
├── requirements.txt          
├── README.md                  

---

## 🛠 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/sarveshmathanraj02/smart_resume_analyzer.git  
cd smart_resume_analyzer

---

### 2. Setup Environment

Create a virtual environment:  
python -m venv venv

Activate the environment:
Windows:  
venv\Scripts\activate

Mac/Linux:  
source venv/bin/activate

Install dependencies:  
pip install -r requirements.txt

Install spaCy model:  
python -m spacy download en_core_web_sm

---

### Configure MySQL Credentials

Open `db_connection.py` and update:

DB_HOST     = "your-host"  
DB_USER     = "your-username"  
DB_PASSWORD = "your-password"  
DB_NAME     = "your-db-name"  
DB_PORT     = 3306  

---

### ▶ Run the Application

streamlit run main.py

The application will run at:  
👉 http://localhost:8501

---

## 🔍 App Features

### Resume Analysis (User Mode)

- Upload PDF resume  
- Extract Name, Email, Phone  
- NLP-based Skill Extraction  
- Role-based Skill Matching  
- Missing Skill Identification  
- Resume Score Calculation  
- Experience Level Detection  
- Job Role Prediction  
- Course Recommendations  
- Resume & Interview Preparation Videos  

### Admin Dashboard

- View all analyzed resumes  
- Filter by predicted job role  
- Download filtered CSV  
- Resume score distribution graph  
- User activity timeline  

---

## 🔌 Major Functional Components

### User Mode

- Resume PDF Upload  
- Resume Text Extraction  
- Skill Extraction  
- Role Selection  
- Skill Match Percentage  
- Recommended Courses  
- Resume Score  
- Experience Level Detection  

### Admin Mode

- Search resumes by predicted role  
- View complete analysis logs  
- Plotly-based visualizations  
- Download CSV for filtered data  

---

## ✨ Algorithms Implemented

### 1. Resume Parsing  

- Extracts raw text via pdfplumber  

### 2. NLP Skill Matching  

- Uses spaCy PhraseMatcher to match extracted skills with job role–specific skill sets  

### 3. Resume Scoring (Based On)  

- Basic info detection  
- Skill relevance  
- Resume structure  
- Keyword coverage  

### 4. Experience Level Detection 

- Regex-based extraction (“X years of experience”)  
- Skill count analysis  

---

## 🎥 Demo Video



---

## 🧰 Tech Stack Used

- Frontend: Streamlit  
- Backend: Python  
- NLP: spaCy  
- PDF Parsing: pdfplumber  
- Database: MySQL  
- Visualization: Plotly  
- Video Integration: YouTube  
- Skill Matching: PhraseMatcher  

---

## 🧪 How to Contribute / Test

1. Clone the repository  
2. Install dependencies  
3. Run Streamlit  
4. Upload sample resumes  
5. Test Admin Dashboard  
6. Submit issues or pull requests  

---

## 👤 Author

**Sarvesh M**  
📧 Email: sarveshmathanraj2@gmail.com

---

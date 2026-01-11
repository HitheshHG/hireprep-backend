from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import extract_text
from skill_extractor import extract_skills
from openai_service import generate_questions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_resume(resume: UploadFile = File(...)):
    text = extract_text(resume)
    skills = extract_skills(text)
    questions = generate_questions(skills)

    return {
        "skills": skills,
        "questions": questions,
    }

from fastapi import FastAPI, UploadFile, File
import shutil
import os

from rag_pipeline import load_and_index, ask_question
from quiz_generator import generate_mcq, generate_coding_question
from interview_mode import start_interview, next_question
from memory_store import get_weak_topics

app = FastAPI()

os.makedirs("data", exist_ok=True)
os.makedirs("vectorstore", exist_ok=True)
os.makedirs("user_data", exist_ok=True)


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        path = f"data/{file.filename}"

        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        load_and_index(path)

        return {"message": "Indexed successfully"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/ask/")
def ask(query: str):
    try:
        answer = ask_question(query)
        return {"response": answer}

    except Exception as e:
        return {"error": str(e)}


@app.get("/mcq/")
def mcq(topic: str):
    try:
        return {"quiz": generate_mcq(topic)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/coding/")
def coding(topic: str):
    try:
        return {"question": generate_coding_question(topic)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/interview/start")
def interview_start():
    try:
        return {"question": start_interview()}
    except Exception as e:
        return {"error": str(e)}


@app.get("/interview/next")
def interview_next(answer: str):
    try:
        return {"response": next_question(answer)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/weak/")
def weak():
    try:
        return {"weak_topics": get_weak_topics()}
    except Exception as e:
        return {"error": str(e)}
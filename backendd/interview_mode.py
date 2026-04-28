from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def start_interview():
    prompt = "Start a technical interview for a software engineer."

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def next_question(answer):
    prompt = f"""
User answered: {answer}

Evaluate briefly and ask next question.
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
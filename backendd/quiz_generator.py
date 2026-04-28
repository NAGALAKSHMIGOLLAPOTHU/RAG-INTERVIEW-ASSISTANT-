from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def generate_mcq(topic):
    prompt = f"""
Generate 5 MCQ questions on {topic}.
Each should have 4 options and mark correct answer.
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def generate_coding_question(topic):
    prompt = f"""
Generate a coding interview question on {topic}.
Include:
- Problem
- Constraints
- Example
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
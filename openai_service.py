import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


def _generate_batch(skills, batch_no, batch_size=10):
    prompt = f"""
You are a senior technical interviewer.

Generate EXACTLY {batch_size} HIGH-QUALITY multiple-choice interview questions
based on these skills:

{", ".join(skills)}

IMPORTANT RULES:
- Exactly 3 options per question
- Options MUST be clearly different
- Only ONE correct answer
- Wrong options must test misconceptions
- Do NOT reuse the same options
- Mix theory + real-world scenarios
- Difficulty: internship / junior
- Output ONLY valid JSON array
- No explanations
- No markdown

JSON FORMAT:
[
  {{
    "question": "Question text",
    "options": [
      "Correct answer",
      "Plausible but wrong",
      "Clearly incorrect"
    ],
    "answer": "Correct answer",
    "skill": "Skill name"
  }}
]

This is batch #{batch_no}.
"""

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.25,
            "max_tokens": 1200,
        },
        timeout=60,
    )

    data = response.json()

    if "choices" not in data:
        return []

    content = data["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except Exception:
        return []


def generate_questions(skills, target_count=30):
    if not skills:
        return []

    valid = []
    batch_no = 1

    while len(valid) < target_count and batch_no <= 6:
        batch = _generate_batch(skills, batch_no=batch_no, batch_size=10)

        for q in batch:
            if (
                isinstance(q, dict)
                and "question" in q
                and "options" in q
                and "answer" in q
                and "skill" in q
                and len(q["options"]) == 3
                and q["answer"] in q["options"]
            ):
                valid.append(q)

                if len(valid) == target_count:
                    break

        batch_no += 1

    return valid[:target_count]

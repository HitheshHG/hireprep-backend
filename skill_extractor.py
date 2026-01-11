import re

SKILL_PATTERNS = {
    "Python": [r"\bpython\b"],
    "Java": [r"\bjava\b"],
    "C++": [r"\bc\+\+\b"],
    "JavaScript": [r"\bjavascript\b", r"\bjs\b"],
    "React": [r"\breact\b", r"\breactjs\b"],
    "Node.js": [r"\bnode\b", r"\bnode\.js\b"],
    "SQL": [r"\bsql\b", r"\bmysql\b", r"\bpostgres\b"],
    "HTML": [r"\bhtml\b"],
    "CSS": [r"\bcss\b"],
    "Docker": [r"\bdocker\b"]
}

def extract_skills(text: str):
    text = text.lower()
    found_skills = set()

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found_skills.add(skill)
                break

    return sorted(found_skills)

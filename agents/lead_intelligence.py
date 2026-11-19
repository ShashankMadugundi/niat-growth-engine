
import json

from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.6-flash"


def analyze_lead(student_data):

    with open("prompts/lead_analysis.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    prompt = f"""
    {system_prompt}

    STUDENT REGISTRATION DETAILS:

    {json.dumps(student_data, indent=4)}

    Analyse this student and return the required JSON.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    result = json.loads(response.text)

    # Validate AI output
    score = result["lead_score"]

    if not isinstance(score, int) or not 0 <= score <= 100:
        raise ValueError("Invalid lead score")

    expected_priority = (
        "High" if score >= 70
        else "Medium" if score >= 40
        else "Low"
    )

    if result["priority"] != expected_priority:
        raise ValueError("Priority does not match lead score")

    return result

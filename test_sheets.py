
from services.google_sheets import save_lead

student = {
    "name": "Rahul",
    "phone": "9999999999",
    "city": "Hyderabad",
    "coaching_centre": "ABC Academy",
    "exam": "JEE Main",
    "exam_status": "Did not get expected rank",
    "technology_interest": "AI and Software Engineering",
    "primary_concern": "Getting into a good college",
    "parent_involvement": "Wants parents to understand",
    "counselling_interest": "Yes"
}

analysis = {
    "lead_score": 85,
    "priority": "High",
    "primary_concern": "College admission",
    "admission_intent": "High",
    "student_interests": ["AI", "Software Engineering"],
    "recommended_action": "Arrange counselling",
    "whatsapp_message": "Hi Rahul! Let's discuss your career options.",
    "reasoning": "Strong interest and counselling readiness."
}

result = save_lead(student, analysis)

print("Lead saved successfully:", result)

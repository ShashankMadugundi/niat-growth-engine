
from agents.lead_intelligence import analyze_lead

student = {
    "name": "Rahul",
    "city": "Hyderabad",
    "coaching_centre": "ABC Academy",
    "exam": "JEE Main",
    "exam_status": "Did not get expected rank",
    "technology_interest": "AI and Software Engineering",
    "primary_concern": "Getting into a good college",
    "parent_involvement": "Wants parents to understand the program",
    "counselling_interest": "Yes"
}

result = analyze_lead(student)

print("\nAI LEAD ANALYSIS")
print("=" * 40)

for key, value in result.items():
    print(f"{key}: {value}")

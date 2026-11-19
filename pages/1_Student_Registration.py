
import streamlit as st

from agents.lead_intelligence import analyze_lead
from services.google_sheets import save_lead

st.set_page_config(
    page_title="NIAT Student Registration",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 NIAT Career Awareness Session")
st.subheader("Student Registration")

st.write(
    "Register to explore opportunities in AI, "
    "software engineering and technology careers."
)

with st.form("student_registration"):

    st.subheader("Personal Information")

    name = st.text_input("Full Name")
    phone = st.text_input("WhatsApp Number (10 digits)")
    city = st.text_input("City")

    st.subheader("Coaching Centre Information")

    coaching_centre = st.text_input("Coaching Centre Name")

    st.subheader("Academic Information")

    exam = st.selectbox(
        "Which examination did you take?",
        ["JEE Main", "JEE Advanced", "Intermediate", "Other"]
    )

    exam_status = st.selectbox(
        "What is your current examination status?",
        [
            "Got my expected rank",
            "Did not get expected rank",
            "Waiting for results",
            "Preparing for examination",
            "Other"
        ]
    )

    technology_interest = st.multiselect(
        "Which technology areas interest you?",
        [
            "Artificial Intelligence",
            "Machine Learning",
            "Software Engineering",
            "Web Development",
            "Data Science",
            "Not sure yet"
        ]
    )

    primary_concern = st.selectbox(
        "What is your biggest concern right now?",
        [
            "Getting into a good college",
            "Choosing the right degree",
            "Understanding career opportunities",
            "College fees",
            "Getting industry-ready skills",
            "Convincing my parents",
            "Other"
        ]
    )

    st.subheader("Counselling Preferences")

    parent_involvement = st.radio(
        "Would you like your parents involved in counselling?",
        ["Yes", "No", "Maybe"]
    )

    parent_phone = st.text_input(
        "Parent's WhatsApp Number (optional, 10 digits)"
    )

    counselling_interest = st.radio(
        "Would you like a personalized counselling session?",
        ["Yes", "No", "Maybe"]
    )

    consent = st.checkbox(
        "I agree to be contacted regarding NIAT counselling "
        "and understand that my information will be used "
        "for this purpose."
    )

    submitted = st.form_submit_button(
        "Register & Submit",
        use_container_width=True
    )


if submitted:

    if not all([name.strip(), phone.strip(), city.strip(),
                coaching_centre.strip()]):
        st.error("Please complete all mandatory fields.")

    elif not phone.isdigit() or len(phone) != 10:
        st.error("Enter a valid 10-digit WhatsApp number.")

    elif parent_phone and (
        not parent_phone.isdigit() or len(parent_phone) != 10
    ):
        st.error("Enter a valid parent phone number.")

    elif not technology_interest:
        st.error("Please select at least one technology interest.")

    elif not consent:
        st.error("Please provide consent before registering.")

    else:

        student_data = {
            "name": name.strip(),
            "phone": phone,
            "parent_phone": parent_phone,
            "city": city.strip(),
            "coaching_centre": coaching_centre.strip(),
            "exam": exam,
            "exam_status": exam_status,
            "technology_interest": ", ".join(technology_interest),
            "primary_concern": primary_concern,
            "parent_involvement": parent_involvement,
            "counselling_interest": counselling_interest,
            "consent": consent
        }

        try:
            with st.spinner(
                "AI agent is analysing your registration..."
            ):

                ai_result = analyze_lead(student_data)

                save_lead(student_data, ai_result)

            st.success("Registration completed successfully!")

            st.subheader("Your Registration Summary")

            st.write(f"**Name:** {name}")
            st.write(f"**Coaching Centre:** {coaching_centre}")
            st.write(f"**Interests:** {', '.join(technology_interest)}")

            st.info(
                "Thank you for registering! "
                "Our counselling team can follow up with you."
            )

        except Exception as e:
            st.error(f"Registration failed: {e}")

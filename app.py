
import streamlit as st
import pandas as pd
from services.google_sheets import get_all_leads
from services.google_sheets import update_followup_status
from urllib.parse import quote

st.set_page_config(
    page_title="NIAT Growth Engine",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 NIAT Growth Engine")
st.caption("AI-powered Coaching Centre Lead Intelligence")

# Fetch CRM records
try:
    leads = get_all_leads()
except Exception as e:
    st.error(f"Unable to load CRM: {e}")
    st.stop()

if not leads:
    st.info("No student registrations found yet.")
    st.stop()

df = pd.DataFrame(leads)

# Sidebar filters
st.sidebar.header("Lead Filters")

priority_options = ["All", "High", "Medium", "Low"]

selected_priority = st.sidebar.selectbox(
    "Filter by Priority",
    priority_options
)

if selected_priority != "All":
    df = df[df["Priority"] == selected_priority]

# Dashboard metrics
st.subheader("Lead Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", len(leads))
col2.metric("High Priority", 
            sum(x["Priority"] == "High" for x in leads))
col3.metric("Medium Priority",
            sum(x["Priority"] == "Medium" for x in leads))
col4.metric("Low Priority",
            sum(x["Priority"] == "Low" for x in leads))

st.divider()

# Lead table
st.subheader("Student Lead Management")

display_columns = [
    "Student Name",
    "City",
    "Coaching Centre",
    "Lead Score",
    "Priority",
    "Counselling Interest",
    "Follow-up Status"
]

st.dataframe(
    df[display_columns],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Individual lead details

# Individual lead details
st.divider()
st.subheader("AI Lead Intelligence & Follow-up")

if not df.empty:

    # Use phone number as the unique identifier
    student_options = {
        f"{row['Student Name']} | {row['Phone']}": row
        for _, row in df.iterrows()
    }

    selected_student = st.selectbox(
        "Select a student",
        list(student_options.keys())
    )

    lead = student_options[selected_student]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {lead['Student Name']}")

        st.write("Phone:", lead["Phone"])
        st.write("City:", lead["City"])
        st.write("Coaching Centre:", lead["Coaching Centre"])

        st.metric(
            "Lead Score",
            lead["Lead Score"]
        )

        st.write("Priority:", lead["Priority"])
        st.write("Primary Concern:", lead["Primary Concern (AI)"])
        st.write("Admission Intent:", lead["Admission Intent"])

    with col2:

        st.markdown("### Recommended Action")

        st.info(lead["Recommended Action"])

        st.markdown("### AI Reasoning")
        st.write(lead["AI Reasoning"])

    st.divider()

    st.markdown("### Personalized WhatsApp Outreach")

    message = lead["WhatsApp Message"]

    st.text_area(
        "Review message",
        value=message,
        height=130
    )

    phone = str(lead["Phone"]).strip()

    # Indian mobile numbers
    if len(phone) == 10 and phone.isdigit():
        whatsapp_phone = "91" + phone
    else:
        whatsapp_phone = phone

    whatsapp_url = (
        f"https://wa.me/{whatsapp_phone}"
        f"?text={quote(message)}"
    )

    st.link_button(
        "Open WhatsApp",
        whatsapp_url
    )

    st.divider()

    st.markdown("### Update Follow-up Status")

    statuses = [
        "Pending",
        "Contacted",
        "Counselling Scheduled",
        "Applied",
        "Not Interested"
    ]

    current_status = str(lead["Follow-up Status"])

    if current_status not in statuses:
        current_status = "Pending"

    new_status = st.selectbox(
        "Current status",
        statuses,
        index=statuses.index(current_status)
    )

    if st.button("Update Lead Status"):

        try:
            update_followup_status(
                phone,
                new_status
            )

            st.success("Follow-up status updated successfully!")

            st.rerun()

        except Exception as e:
            st.error(f"Unable to update status: {e}")

else:
    st.warning("No leads match the selected filter.")

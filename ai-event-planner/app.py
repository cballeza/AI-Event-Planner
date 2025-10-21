import os
import streamlit as st
from dotenv import load_dotenv
import google.genai as genai
from prompts import build_system_prompt, build_few_shot_examples, format_user_brief

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="AI Event Planner", layout="centered")
st.title("AI Event Planner Assistant")
st.write("Plan structured, budget-conscious events with AI assistance.")

# ----------------------
# Load environment & configure Gemini
# ----------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    st.error("GEMINI_API_KEY not found. Please create a `.env` file with your API key.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_NAME = "models/gemini-2.5-flash"

# ----------------------
# Initialize session state
# ----------------------
if "plan_text" not in st.session_state:
    st.session_state.plan_text = ""

# ----------------------
# Event Input Form
# ----------------------
st.subheader("Event Details")
with st.form("event_form"):
    col1, col2 = st.columns(2)
    with col1:
        event_type = st.text_input("Event Type", placeholder="e.g., Pool Party, Picnic, Conference")
        guest_count = st.number_input("Guest Count", min_value=1, step=1, value=20)
        budget = st.number_input("Budget (USD)", min_value=0, step=50, value=500)
    with col2:
        theme = st.text_input("Theme/Style", placeholder="e.g., Cottagecore, Formal, Festival")
        duration = st.text_input("Duration", placeholder="e.g., 4 hours")
        special = st.text_area("Special Considerations", placeholder="e.g., Outdoors, Dietary needs, Accessibility")
    submitted = st.form_submit_button("Generate Event Plan")

# ----------------------
# Build Prompt
# ----------------------
def build_full_prompt(brief: dict) -> str:
    system_prompt = build_system_prompt()
    shots = build_few_shot_examples()
    user_brief = format_user_brief(brief)
    shots_text = "\n\n".join([s["parts"][0] for s in shots if "parts" in s])
    return f"{system_prompt}\n\n{shots_text}\n\n{user_brief}"

# ----------------------
# Generate Plan
# ----------------------
def generate_event_plan(brief: dict) -> str:
    prompt = build_full_prompt(brief)
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=[prompt])
    except Exception as e:
        return f"API request failed: {e}"

    if response and response.candidates:
        return response.candidates[0].content.parts[0].text
    return "No response from model. Please try again."

# ----------------------
# Main App Logic
# ----------------------
if submitted:
    brief = {
        "event_type": event_type.strip(),
        "guest_count": int(guest_count),
        "budget": float(budget),
        "theme": theme.strip(),
        "duration": duration.strip(),
        "special_considerations": special.strip(),
    }

    if not all(brief.values()):
        st.error("Please fill in all fields before generating a plan.")
        st.stop()

    with st.spinner("Generating your event plan..."):
        plan_text = generate_event_plan(brief)

    if "Error" in plan_text:
        st.error(plan_text)
    else:
        st.success("Event plan generated successfully!")
        st.session_state.plan_text = plan_text
        st.markdown(plan_text)

# ----------------------
# Refinement Tools
# ----------------------
if st.session_state.plan_text:
    st.divider()
    st.subheader("Refine Your Plan")

    colA, colB, colC = st.columns(3)

    # ---- Make it Cheaper ----
    if colA.button("Make It Cheaper"):
        refine_prompt = st.session_state.plan_text + "\n\nRefine this plan to reduce total cost by ~20% without lowering quality."
        refined = client.models.generate_content(model=MODEL_NAME, contents=[refine_prompt])
        st.markdown(refined.candidates[0].content.parts[0].text)

    # ---- Generate Interactive Checklist ----
    if colB.button("Generate Event Checklist"):
        refine_prompt = st.session_state.plan_text + """
\n\nConvert this event plan into a clear, organized checklist.
Include categories like:
- Pre-event planning tasks (with recommended timelines)
- Booking and logistics tasks
- Food and drinks prep/shopping list
- Setup and decoration tasks
- Activities checklist
- Post-event cleanup/reminder list

Make sure the checklist is easy to follow and sequential.
Return only a numbered list of tasks.
"""
        with st.spinner("Generating your event checklist..."):
            refined = client.models.generate_content(model=MODEL_NAME, contents=[refine_prompt])
            checklist_text = refined.candidates[0].content.parts[0].text

        # Turn checklist text into a Python list
        checklist_items = [
            item.strip("- ").strip()
            for item in checklist_text.split("\n")
            if item.strip() and not item.lower().startswith("###")
        ]

        # Save to session state
        st.session_state.checklist = checklist_items

    # ---- Make Kid-Friendly ----
    if colC.button("Make Kid-Friendly"):
        refine_prompt = st.session_state.plan_text + "\n\nAdapt this plan to be family- and kid-friendly, including safe activities and menu changes."
        refined = client.models.generate_content(model=MODEL_NAME, contents=[refine_prompt])
        st.markdown(refined.candidates[0].content.parts[0].text)

    # Show interactive checklist if available
if "checklist" in st.session_state and st.session_state.checklist:
    st.subheader("Event Planning Checklist")
    st.write("Mark tasks as complete as you go:")

    for i, task in enumerate(st.session_state.checklist):
        st.checkbox(task, key=f"task_{i}")

    # Show progress
    total_tasks = len(st.session_state.checklist)
    completed = sum(1 for i in range(total_tasks) if st.session_state.get(f"task_{i}", False))
    st.progress(completed / total_tasks)
    st.caption(f"{completed}/{total_tasks} tasks completed")


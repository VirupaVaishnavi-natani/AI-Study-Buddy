import streamlit as st
import os
from datetime import datetime
#Importing modules
from utils.pdf_handler import extract_text
from utils.ai_logic import get_study_response, solve_questions, generate_smart_schedule
from utils.quiz_manager import generate_dynamic_quiz

hf_token = st.secrets["Hf_Token"]
schedule_placeholder = st.empty()
st.set_page_config(page_title="AI Study Buddy", layout="wide", page_icon="🎓")
#state initialization
if "active_tab_index" not in st.session_state:
    st.session_state.active_tab_index = 0
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "user_choices" not in st.session_state:
    st.session_state.user_choices = {}
#custom ui styling
st.markdown("""
<style>
button[kind="primary"] {
    position: sticky;
    bottom: 20px;
    z-index: 100;
}
</style>
""", unsafe_allow_html=True)
#title
st.title("🎓 AI Study Buddy and Smart Scheduler")
st.caption("Simplified Learning, Accurate Summaries, Interactive Quizzes and Scheduler")
#sidebar
with st.sidebar:
    st.header("📂 Study Material")
    source_type = st.radio("Input Method:", ["PDF Upload", "Direct Text"])
    context_text = ""
    if source_type == "PDF Upload":
        upload_file = st.file_uploader("Upload Notes (PDF)", type="pdf")
        if upload_file:
            with st.spinner("Extracting text..."):
                context_text = extract_text(upload_file)
            st.success("✅ PDF Content Loaded!")
    else:
        context_text = st.text_area("Paste your notes here:", height=200)
    with st.expander("🕒 Smart Scheduler", expanded=True):
        home_time = st.time_input(
            "What time do you reach home?",
            value=None
        )
        work_input = st.text_input(
            "Tasks (comma separated):",
            placeholder="e.g. Science, Maths, Dance"
        )
        if st.button("📅 Plan My Evening"):
            if not home_time:
                st.warning("Please select arrival time!")
            elif not work_input:
                st.warning("Please enter your tasks!")
            else:
                tasks = [t.strip() for t in work_input.split(",")]
                formatted_home = home_time.strftime("%I:%M %p")
                with st.spinner("Assigning tasks..."):
                    raw_schedule = generate_smart_schedule(
                        hf_token, formatted_home, tasks
                    )
                    schedule = raw_schedule.split("\n\n")[0]
                    st.session_state.custom_schedule = schedule
                    schedule_placeholder.success("🗓️ Your Evening Schedule")
                    schedule_placeholder.markdown(schedule)
#interface logic
tab_list = ["🧠 Explainer", "📄 Summarizer", "🧩 Quizzer", "📅 My Schedule"]
# Use active_tab_index to control which tab is open
tab = st.tabs(tab_list)
#tab1:explainer section-from Ai tools or from pdf or text
with tab[0]:
    st.subheader("Concept Explainer & Solver")
    user_input = st.text_area("Enter a concept to explain or a question to solve:",
                              placeholder="e.g., What is Data Cleaning?")
    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox("Action:", ["Explain Concept", "Solve Question"])
    with col2:
        marks = st.number_input("Target Marks (1-5):", min_value=1, max_value=5, value=3)
    if st.button("Get Answer"):
        if user_input:
            with st.spinner("Processing..."):
                query = f"{mode}: {user_input}"
                response = solve_questions(hf_token, query, context_text, marks=marks)
                st.markdown(response)
        else:
            st.warning("Please enter a concept or question first!")
    #To display whether it is currently generating from web or through material
    if context_text:
        st.caption("✅ Currently explaining using your uploaded material.")
    else:
        st.caption("🌐 No document uploaded. Using AI general knowledge in simple terms.")
#Tab2:Summarizer
with tab[1]:
    st.subheader("Note Summarizer")
    if context_text:
        sum_style = st.selectbox("Summary Style:", ["Executive Summary", "Key Bullet Points", "Concept Map"])
        if st.button("Create Summary"):
            with st.spinner("Condensing..."):
                prompt = f"Style: {sum_style}\n\nText: {context_text[:10000]}"
                response = get_study_response(prompt, task_type="summarize")
                st.success(response)
#tab3:Quizzer
with tab[2]:
    st.subheader("🧩 Interactive Knowledge Check")
    if context_text:
        # Update the button logic to request 10 questions
        if st.button("✨ Generate New Quiz"):
            with st.spinner("Creating your quiz with 10 questions..."):
                # Explicitly pass 10 here
                new_q = generate_dynamic_quiz(hf_token, context_text, num_questions=10)
                if new_q:
                    st.session_state.quiz_questions = new_q
                    st.session_state.quiz_submitted = False
                    st.session_state.user_choices = {}
                    st.rerun()

        if st.session_state.quiz_questions:
            with st.form("quiz_form"):
                for i, q in enumerate(st.session_state.quiz_questions):
                    st.markdown(f"**Q{i + 1}: {q['question']}**")
                    #to make sure exactly 4 options are used
                    current_options = q['options'][:4]
                    st.radio(
                        "Select an answer:",
                        options=current_options,
                        index=None,
                        key=f"q_{i}",
                        disabled=st.session_state.quiz_submitted,
                        label_visibility="collapsed"
                    )
                    #display res only after submission
                    if st.session_state.quiz_submitted:
                        user_ans = st.session_state.get(f"q_{i}")
                        is_corr = (user_ans == q['answer'])
                        if is_corr:
                            st.success("✅ Correct!")
                        else:
                            # Matches your screenshot error style
                            st.error(f"❌ Incorrect. The correct answer was: **{q['answer']}**")
                        with st.expander("📖 Explanation", expanded=True):
                            st.write(q['reasoning'])
                    st.write("---")
                submit_btn = st.form_submit_button("Submit Quiz")
                if submit_btn:
                    st.session_state.quiz_submitted = True
                    st.rerun()
            #final score display-at the end
            if st.session_state.quiz_submitted:
                correct_count = sum(1 for i, q in enumerate(st.session_state.quiz_questions)
                                    if st.session_state.get(f"q_{i}") == q['answer'])
                st.metric("Total Score", f"{correct_count} / {len(st.session_state.quiz_questions)}")
                if st.button("🔄 Restart Quiz"):
                    st.session_state.quiz_questions = None
                    st.session_state.quiz_submitted = False
                    st.rerun()
    else:
        st.info("👋 Upload material to start a quiz.")
#tab4:Scheduler
with tab[3]:
    st.subheader("🗓️ Personalized Daily Plan")
    if "custom_schedule" in st.session_state:
        st.markdown(st.session_state.custom_schedule)
    else:
        st.info("Plan your evening in the sidebar to see your schedule here!")
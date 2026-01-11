import streamlit as st
from huggingface_hub import InferenceClient

HF_TOKEN = st.secrets["Hf_Token"]
MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
client = InferenceClient(token=HF_TOKEN)

def solve_questions(hf_token, user_query, context="", marks=3):
    from huggingface_hub import InferenceClient
    client = InferenceClient(token=hf_token)
    MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
    depth_guide = {
        1: "Provide a concise definition and important key points (2-3 lines total).",
        2: "Provide a brief explanation with 2 bullet points (4-6 lines total).",
        3: "Provide a balanced explanation with definition and examples (7-9 lines total).",
        4: "Provide a comprehensive response (approx. 10-12 lines) with structured headings.",
        5: "Provide a full academic breakdown (13+ lines) with Introduction, Detailed Explanation, and Conclusion."
    }

    if context.strip():
        instruction = "Answer the question STRICTLY based on the provided CONTEXT. Use simple terms."
        context_part = f"CONTEXT:\n{context[:8000]}"
    else:
        instruction = "You are an expert tutor. Explain the concept in simple, easy-to-understand terms using your general knowledge."
        context_part = "CONTEXT: No document uploaded. Use general knowledge."

    system_message = (
        f"{instruction} "
        f"Format your response for a {marks}-mark question. "
        f"Strictly follow this length: {depth_guide.get(marks)}"
    )

    user_prompt = f"""
    {context_part}

    QUESTION:
    {user_query}
    """
    try:
        response = client.chat_completion(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🚨 AI Error: {e}"


def generate_smart_schedule(hf_token, home_time, tasks_list):
    """
    Generates a task-based schedule in a tabular format with
    clear Start/End times and a focus on 9 hours of sleep.
    """
    client = InferenceClient(token=hf_token)
    tasks_str = ", ".join(tasks_list)

    prompt = f"""
    Create a professional study timetable for a student.
    - Arrival Time: {home_time}
    - Tasks: {tasks_str}

    CRITICAL RULES:
    1. Output MUST be a Markdown Table: | Time Block | Activity | Description |
    2. Every row must have a specific [Start Time] - [End Time].
    3. Include 10-minute 'Short Breaks' between tasks.
    4. SLEEP GOAL: The student must be in bed by 10:00 PM for a 7:00 AM wake-up (9 Hours Sleep).
    5. No school work should be scheduled after 9:00 PM.
    6. Include a 'Wind-down' hour (9 PM - 10 PM) with no electronics.
    """
    try:
        response = client.chat_completion(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🚨 Error creating schedule: {e}"

def get_study_response(prompt: str, task_type="summarize"):
    """Summarizer tab compatibility."""
    try:
        response = client.chat_completion(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are an expert at summarizing."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🚨 AI Error: {e}"
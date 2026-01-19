# 🎓 AI Study Buddy and Smart Scheduler

### 🔗 [Live Demo - View App on Streamlit Cloud](https://virupavaishnavi-natani-xzsknnlewubucabq7npjlk.streamlit.app/)

AI Study Buddy is a Streamlit-based educational platform designed to help students transform static notes into interactive learning tools. It leverages Large Language Models (LLMs) to provide customized study assistance and evening planning.

## 🛠️ Tools and Technologies Used

### **Tools**
* **Python**: Core programming language.
* **Streamlit**: Web application framework for the user interface.
* **Hugging Face API**: Used for AI model inference.
* **Meta Llama 3.2-3B-Instruct**: The LLM used for Natural Language Processing (NLP) tasks.
* **PyPDF2**: Library for extracting text from PDF documents.

### **Techniques**
| Technique | Description |
| :--- | :--- |
| **Natural Language Processing (NLP)** | Used to understand, analyze, and generate human-like responses from study material. |
| **Prompt Engineering** | Carefully designed prompts to control AI responses for explanations, summaries, and quizzes. |
| **Dynamic Quiz Generation** | AI automatically creates multiple-choice questions with answers and explanations from provided material. |
| **Session State Management** | Used in Streamlit to preserve quiz progress, user inputs, and results across interactions. |
| **Modular Programming** | The application is structured into separate modules to improve readability and maintenance. |

---

## 🚀 Key Features

* **🧠 Concept Explainer**: Get custom explanations based on your material, tailored to specific mark values (1-5 marks).
* **📄 Note Summarizer**: Quickly generate Executive Summaries, Bullet Points, or Concept Maps from your notes.
* **🧩 Interactive Quizzer**: Automatically generates 10-question multiple-choice quizzes from uploaded PDFs with detailed reasoning for each answer.
* **📅 Smart Scheduler**: Creates a personalized evening timetable in a tabular format, ensuring a 9-hour sleep goal.

## 📋 Setup and Installation

1.  **Install dependencies**:
    ```bash
    pip install streamlit huggingface-hub PyPDF2
    ```

2.  **Configure Secrets**:
    In your project root, create a `.streamlit/secrets.toml` file and add your Hugging Face token:
    ```toml
    Hf_Token = "your_huggingface_api_token_here"
    ```

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 📁 Project Structure

* `app.py`: Main Streamlit interface and session management.
* `utils/ai_logic.py`: Logic for AI responses, scheduling, and mark-specific depth guides.
* `utils/quiz_manager.py`: Handles dynamic quiz generation and JSON parsing.
* `utils/pdf_handler.py`: Manages text extraction from uploaded PDF files.
## 📖 How to Use

Follow these steps to get the most out of the AI Study Buddy:

1.  **Upload Your Material**: In the sidebar, choose "PDF Upload" to upload your notes or "Direct Text" to paste content manually.
2.  **Set Your Schedule**: Enter the time you reach home and list your tasks (e.g., "Maths, Science, Coding"). Click **Plan My Evening** to generate a routine in the **My Schedule** tab.
3.  **Explain Concepts**: Go to the **Explainer** tab, enter a topic, and choose the target marks (1-5). The AI will provide an answer based on your uploaded notes.
4.  **Summarize Notes**: Use the **Summarizer** tab to quickly create bullet points or an executive summary of your document.
5.  **Take a Quiz**: Navigate to the **Quizzer** tab and click **Generate New Quiz**. Answer 10 multiple-choice questions and check the explanations for each.

---

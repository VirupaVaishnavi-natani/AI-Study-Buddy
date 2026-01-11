import json
import re
from huggingface_hub import InferenceClient

class QuizManager:
    def __init__(self, hf_token):
        self.client = InferenceClient(token=hf_token)
        self.model = "meta-llama/Llama-3.2-3B-Instruct"
    def _extract_json(self, text: str) -> str:
        """
        Extract JSON safely from LLM output.
        """
        match = re.search(
            r"@@@JSON_START@@@(.*?)@@@JSON_END@@@",
            text,
            re.DOTALL
        )
        if match:
            return match.group(1).strip()
        start = text.find("[")
        end = text.rfind("]") + 1
        if start != -1 and end > start:
            return text[start:end]
        raise ValueError("No JSON found")

    def generate_quiz(self, context: str, num_questions: int = 5):
        if not context or len(context.strip()) < 300:
            return []

        system_prompt = (
            "You are an educational quiz generator.\n"
            "You MUST return valid JSON only.\n"
            "No explanations outside JSON."
        )

        user_prompt = f"""
        Create {num_questions} multiple-choice questions from the text below.

        STRICT FORMATTING RULES:
        1. You MUST provide EXACTLY 4 options for every question.
        2. If the text lacks enough distractors, use "Data integration", "Data reduction", or "None of the above" to fill the 4th slot.
        3. The "answer" must exactly match one of the strings in the "options" list.
        4. The "reasoning" field should be a clear, educational explanation of why the answer is correct.

        OUTPUT JSON FORMAT:
        @@@JSON_START@@@
        [
          {{
            "question": "Question text here?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "answer": "Option 1",
            "reasoning": "Data cleaning is the primary task in data preprocessing..."
          }}
        ]
        @@@JSON_END@@@

        TEXT:
        {context[:4000]}
        """
        try:
            response = self.client.chat_completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.2
            )

            raw_output = response.choices[0].message.content
            json_text = self._extract_json(raw_output)
            quiz = json.loads(json_text)

            # Final validation
            validated = []
            for q in quiz:
                if all(k in q for k in ("question", "options", "answer", "reasoning")):
                    validated.append(q)
            return validated
        except Exception as e:
            print("Quiz Generation Error:", e)
            return []

def generate_dynamic_quiz(hf_token, context, num_questions=10):
    return QuizManager(hf_token).generate_quiz(context, num_questions=num_questions)

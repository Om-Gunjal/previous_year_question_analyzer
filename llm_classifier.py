
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_questions(questions):
    if not questions:
        return []

    all_results = []
    batch_size = 2

    # Process questions in small batches
    for start in range(0, len(questions), batch_size):

        batch = questions[start:start + batch_size]

        question_text = "\n".join(
            [f"{i+1}. {q}" for i, q in enumerate(batch)]
        )

        prompt = f"""
You are an expert exam question analyzer.

Identify the main academic topic of each question.
Use short, consistent topic names.

Return ONLY a valid JSON object in this format:
{{
    "questions": [
        {{
            "question": "original question",
            "topic": "identified topic"
        }}
    ]
}}

Include every input question exactly once.
Do not add explanations or Markdown.

Input questions:
{question_text}
"""

        print(
            f"Classifying questions "
            f"{start + 1} to {start + len(batch)}..."
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_completion_tokens=4096
        )

        result = response.choices[0].message.content

        try:
            data = json.loads(result)
            batch_results = data["questions"]

            if len(batch_results) != len(batch):
                raise ValueError(
                    "AI returned an incorrect number of questions."
                )

            all_results.extend(batch_results)

        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print("Invalid response for this batch:")
            print(result)
            raise ValueError(
                f"Could not classify batch starting at question "
                f"{start + 1}. Please try again. Details: {e}"
            )

    return all_results

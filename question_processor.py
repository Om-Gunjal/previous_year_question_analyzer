
import re

def extract_questions(text):

    # Split text into lines
    lines = text.split("\n")

    questions = []

    current_question = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Detect question numbers such as Q1, Q.1, 1.
        if re.match(
            r"^(Q\s*\.?\s*\d+|Question\s*\d+|\d+\s*[\.\)])",
            line,
            re.IGNORECASE
        ):

            # Save previous question
            if current_question:
                questions.append(current_question.strip())

            # Start new question
            current_question = line

        else:

            # Continue previous question
            if current_question:
                current_question += " " + line

    # Save last question
    if current_question:
        questions.append(current_question.strip())

    return questions

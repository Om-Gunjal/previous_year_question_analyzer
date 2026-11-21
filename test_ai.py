
from llm_classifier import classify_questions

sample_questions = [
    "Explain Stack and its operations.",
    "What is database normalization?",
    "Explain process scheduling in an operating system.",
    "What is TCP/IP?"
]

results = classify_questions(sample_questions)

print("\nAI CLASSIFICATION RESULTS:\n")

for item in results:
    print("Question:", item["question"])
    print("Topic:", item["topic"])
    print("-------------------------")

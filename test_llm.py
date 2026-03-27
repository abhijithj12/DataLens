from llm import ask_gemini

# Example dataset columns
columns = [
    "date",
    "sales",
    "profit",
    "region",
    "product"
]

# Test questions
questions = [
    "What is the total sales?",
    "What is the average profit?",
    "Show total sales by region",
    "Create a line chart of sales over date"
]

for q in questions:
    print("\nQuestion:", q)

    result = ask_gemini(q, columns)

    print("LLM Output:")
    print(result)
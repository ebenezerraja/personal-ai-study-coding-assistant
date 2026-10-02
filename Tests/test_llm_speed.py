import time
from config import LLM_MODEL
from ollama import chat


question = "/no_think Explain binary search in simple terms."


start = time.time()

response = chat(
    model=LLM_MODEL,
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    options={
        "temperature": 0,
        "num_predict": 800
    }
)

elapsed = time.time() - start


print(f"LLM response time: {elapsed:.2f} seconds")
print()
print("Answer:")
print(response.message.content)
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Step(BaseModel):
    explanation: int
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {
            "role": "user",
            "content": "how can I solve 8x + 7 = -23"
        },
    ],
    text_format=MathReasoning,
)

math_reasoning = response.output_parsed

print("Final Answer:", math_reasoning.final_answer)
for step in math_reasoning.steps:
    print(f"Step: {step.explanation} | Output: {step.output}")
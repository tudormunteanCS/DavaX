from textwrap import dedent
from openai import OpenAI

client = OpenAI()

MODEL = "gpt-4o-2024-08-06"

math_tutor_prompt = '''
    You are a helpful math tutor. You will be provided with a math problem,
    and your goal will be to output a step by step solution, along with a final answer.
    For each step, just provide the output as an equation use the explanation field to detail the reasoning.
'''

def get_math_solution(question):
    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": dedent(math_tutor_prompt)
        },
        {
            "role": "user",
            "content": question
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "math_reasoning",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "number"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps",  "final_answer"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

    return response.choices[0].message

# Testing with an example question
question = "how can I solve 8x + 7 = -23"

result = get_math_solution(question)

print(result.content)

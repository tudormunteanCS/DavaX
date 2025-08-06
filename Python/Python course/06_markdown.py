import os
from openai import OpenAI

client = OpenAI()

markdown_prompt = """
You are a helpful assistant. Please answer the user's question using Markdown formatting.
Include headings, bullet points, and code blocks where appropriate.
"""

def get_markdown_response(question):
    response = client.chat.completions.create(
        model='gpt-4o-2024-08-06',
        messages=[
            {"role": "system", "content": markdown_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Example usage
question = "Show me how to write a Python function that adds two numbers."
markdown_response = get_markdown_response(question)
print(markdown_response)
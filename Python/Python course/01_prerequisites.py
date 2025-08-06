# Run this cell if you need to set your OpenAI API key for this session
import os
import getpass
from openai import OpenAI
client = OpenAI()

if not os.getenv('OPENAI_API_KEY'):
    api_key = getpass.getpass('Enter your OpenAI API key: ')
    os.environ['OPENAI_API_KEY'] = api_key
else:
    print('OPENAI_API_KEY is already set in the environment.')

response = client.responses.create(
        model="gpt-4o-2024-08-06",
        input="Write a one-sentence bedtime story about a unicorn."
    )
print(response.output_text)
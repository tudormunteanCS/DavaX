import os

import openai
import requests
from openai import OpenAI
import json

api_key = os.getenv('OPEN_AI_API_KEY')

client = OpenAI(api_key=api_key)  # Ensure you have set your OpenAI API key in the environment variable

# Step 0: Define prerequisites: get_weather function,  tool and input messages

def get_weather(latitude, longitude):
    """Get the current temperature from Open-Meteo API for given coordinates"""
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']


tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
}]

input_messages = [{"role": "user", "content": "What's the weather like in Bucharest today?"}]

# Step 1: Call model with get_weather tool defined

response = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools,
)

# Step 2: Model decides to call function(s) – model returns the name and input arguments. Like:
                                                                                                # [{
                                                                                                #     "type": "function_call",
                                                                                                #     "id": "fc_12345xyz",
                                                                                                #     "call_id": "call_12345xyz",
                                                                                                #     "name": "get_weather",
                                                                                                #     "arguments": "{\"latitude\":48.8566,\"longitude\":2.3522}"
                                                                                                # }]
print(response.output)

# tool_call = response.output[0]
# args = json.loads(tool_call.arguments)
#
# # Step 3: Execute get_weather function: receive some like a number, e.g. 20.5
# result = get_weather(args["latitude"], args["longitude"])
#
# print(result)
#
# # Step 4: Supply result and call model again
#
# input_messages.append(tool_call)  # append model's function call message
# input_messages.append({           # append result message
#     "type": "function_call_output",
#     "call_id": tool_call.call_id,
#     "output": str(result)
# })
#
# response_2 = client.responses.create(
#     model="gpt-4.1",
#     input=input_messages,
#     tools=tools,
# )
# # Step 5: Model returns final output in a natural language format: 'The current temperature in Bucharest today is approximately 25.5°C.'
# print(response_2.output_text)
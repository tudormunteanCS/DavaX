from openai import OpenAI
from pydantic import BaseModel, Field
import os
import requests
import json


class Query(BaseModel):
    amount: float = Field(..., description="Amount of money to convert")
    from_currency: str = Field(..., description="Currency to convert from")
    to_currency: str = Field(..., description="Currency to convert to")
    date: str = Field(None, description="Date in YYYY-MM-DD format, optional for historical conversion")


EXCHANGE_HOST_API_URL = "https://api.exchangerate.host"


def currency_converter(query: Query) -> float:
    if query.date:
        params = {
            "access_key": os.getenv("EXCHANGE_HOST_API_KEY"),
            "date": query.date,
            "source": query.from_currency
        }
        response = requests.get(f"{EXCHANGE_HOST_API_URL}/historical", params=params)
        data = response.json()
        if not data.get("success"):
            raise ValueError("Historical conversion failed: " + data.get("error", {}).get("info", "Unknown error"))
        to_currency = query.to_currency
        conversion_rate_source_to_destination = data.get("quotes").get(f"{query.from_currency}{to_currency}")
        return query.amount * conversion_rate_source_to_destination
    else:
        params = {
            "from": query.from_currency,
            "to": query.to_currency,
            "amount": query.amount,
            "access_key": os.getenv("EXCHANGE_HOST_API_KEY")
        }
        response = requests.get(f"{EXCHANGE_HOST_API_URL}/convert", params=params)
        data = response.json()
        if not data.get("success"):
            raise (ValueError("Conversion failed: " + data.get("error", {}).get("info", "Unknown error")))
        result = data.get("result")
        return result


if __name__ == "__main__":
    prompt = "How many RON were 1 EURO at 2023-11-26?"
    api_key = os.getenv("OPEN_AI_API_KEY")
    # used for chat.completions.create not documented yet in openAI
    # functions = [
    #     {
    #         "type": "function",
    #         "function":{
    #             "name": "currency_converter",
    #             "description": "Convert an amount of money from one currency to another.",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "amount": {
    #                         "type": "number",
    #                         "description": "Amount of money to convert"
    #                     },
    #                     "from_currency": {
    #                         "type": "string",
    #                         "description": "Currency to convert from, e.g. 'RON'"
    #                     },
    #                     "to_currency": {
    #                         "type": "string",
    #                         "description": "Currency to convert to, e.g. 'EUR'"
    #                     }
    #                 },
    #                 "required": ["amount", "from_currency", "to_currency"],
    #                 "additionalProperties": False
    #             }
    #         },
    #         "strict": True
    #     }
    # ]

    tools = [{
        "type": "function",
        "name": "currency_converter",
        "description": "Convert an amount of money from one currency to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "Amount of money to convert"},
                "from_currency": {"type": "string", "description": "Currency to convert from, e.g. 'RON'"},
                "to_currency": {"type": "string", "description": "Currency to convert to, e.g. 'EUR'"},
                "date": {"type": "string", "format": "date",
                         "description": "Date in YYYY-MM-DD format, optional for historical conversion"}
            },
            "required": ["amount", "from_currency", "to_currency", "date"],
            "additionalProperties": False
        },
        "strict": True
    }
    ]

    client = OpenAI(api_key=api_key)

    input_messages = [{
        "role": "user",
        "content": prompt
    }]

    response = client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools,
    )

    tool_call = response.output[0]
    args = json.loads(tool_call.arguments)
    result = currency_converter(Query(**args))
    input_messages.append(tool_call)  # append model's function call message
    input_messages.append({  # append result message
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(result)
    })

    response_2 = client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools,
    )
    print(response_2.output_text)

import os
import textwrap

from flask import Flask, request, jsonify
from flask_cors import CORS
from vector_store import embedd_texts
from openai import OpenAI
from qdrant_client import QdrantClient
import json

# from guardrails import Guard, OnFailAction
# from guardrails.hub import ToxicLanguage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
collection_name = "book_recommendations"

openai_api_key = os.getenv("OPENAI_Lawgentic_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

local_host_url = "http://localhost:31333/"
qdrant_client = QdrantClient(
    url=local_host_url,
    check_compatibility=False,
)


@app.route("/")
def home():
    return "Hello, World!"


def retrieve_top_k_points(embedded_question, k=3):
    # retrieve top k vectors from Qdrant
    results = qdrant_client.query_points(
        collection_name=collection_name,
        query=embedded_question,
        with_payload=True,
        limit=k,
    )
    return results.points


def extract_relevant_words_from_question(question):
    """
    pass the question to an LLM to extract genre/topic related words from the question
    :param question: string
    :return: string, relevant words extracted from the question
    """
    system_msg = (
        "You are a helpful assistant that extracts genre/topic related words from a prompt."
        "Example 1: Recommend me a book about bravery and courage"
        "The answer should be: bravery and courage"
        "Example 2: Give me a book recommendation about romance"
        "The answer should be: romance"
    )
    instructiuni = textwrap.dedent(f"""
    {system_msg}
    Question: {question}
    """)
    response = openai_client.responses.create(
        model="gpt-5-nano",
        input=instructiuni
    )
    return response.output_text


def get_book_resume(title):
    """
    Function to get a resume of the book based on its title.
    :param title: string
    :return: string - resume
    """
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
        for book in books:
            if book["title"] == title:
                return book.get("resume", "No resume available for this book.")


def tool_calling_with_openai(title):
    """
    Call OpenAI to get a resume of the book based on its title using function calling
    :param title: string, the title of the book
    :return: the resume of the book retrievd by the function called by the model
    """
    tools = [{
        "type": "function",
        "name": "get_book_resume",
        "description": "Get a resume of the book based on its title.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the book to get a resume for."
                }
            },
            "required": ["title"]
        }
    }]

    input_messages = [{
        "role": "user",
        "content": f"Can you give me a resume of the book titled '{title}'?"
    }]
    response = openai_client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools
    )
    function_call = None
    function_call_arguments = None
    for item in response.output:
        if item.type == "function_call":
            function_call = item
            function_call_arguments = json.loads(item.arguments)

    # Call the function to get the book resume
    book_resume = get_book_resume(title=function_call_arguments["title"])
    input_messages.append(function_call)
    input_messages.append({  # append result message
        "type": "function_call_output",
        "call_id": function_call.call_id,
        "output": str(book_resume)
    })

    instructions = textwrap.dedent(f"""
    The answer should look like this: 
    if the title would be : 1984 and the resume would be: A dystopian political fiction, the novel portrays Winston Smith living under the oppressive rule of Big Brother in a society where surveillance and propaganda crush freedom. His quiet rebellion raises timeless questions about truth, privacy, and individuality.
    Answer: Based on your request, I would recommend the book titled '1984'. Here is a brief resume of the book: A dystopian political fiction, the novel portrays Winston Smith living under the oppressive rule of Big Brother in a society where surveillance and propaganda crush freedom. His quiet rebellion raises timeless questions about truth, privacy, and individuality.
    USE STRICTLY THE FORMAT ABOVE, DO NOT ADD ANYTHING ELSE.
    DO NOT BY ANY MEANS INVENT A RESUME, USE THE RESUME YOU OBTAINED FROM THE FUNCTION CALL.
    """)
    response_2 = openai_client.responses.create(
        model="gpt-4o",
        input=input_messages,
        instructions=instructions,
        tools=tools,
    )
    return response_2.output_text


def process(question):
    """
    Process the question to get recommendations based on semantic retrieval from Qdrant Vector DB
    :param question: string, the question asked by the user
    :return: Recommended book + a resume of the book retrieved by tool calling with OpenAI
    """
    # relevant_question = extract_relevant_words_from_question(question)
    embedded_question = embedd_texts(question, openai_api_key, dimensions=1536)
    top_k_points = retrieve_top_k_points(embedded_question)
    best_points_payload = [x.payload for x in top_k_points]
    title = best_points_payload[0]["title"]
    answer = tool_calling_with_openai(title)
    return answer


def validate_with_guardrails(question):
    """
    Validate the question using guardrails to ensure it does not have any toxic content
    :param question: string, the question asked by the user
    :return:
    :exception: Raises an exception if the question is toxic or violates guardrails
    """
    # guard = Guard().use_many()(
    #      ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION)
    # )
    try:
        # guard.validate(question)
        pass
    except Exception as e:
        raise Exception(
            "Your question contains toxic content or violates our guidelines. Please rephrase your question.")


@app.route("/recommendation", methods=["POST"])
def get_recommendations():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    try:
        validate_with_guardrails(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    answer = process(question)
    return jsonify({"question": question, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True, port=5050)

import os

from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant
import json
import uuid
from openai import OpenAI


def create_collection(client, collection_name, dimensions):
    if not client.collection_exists(collection_name):
        print(f"Collection {collection_name} does not exist. Creating it...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant.VectorParams(
                size=dimensions,
                distance=qdrant.Distance.COSINE
            )
        )
        print(f"Collection {collection_name} created successfully.")
    else:
        print("Collection " + collection_name + " already exists.")


def embedd_texts(texts, openai_api_key, dimensions):
    client = OpenAI(
        api_key=openai_api_key
    )
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
        dimensions=dimensions,
        encoding_format="float"
    ).data[0].embedding
    return resp


def insert_to_qdrant(client, collection_name, file_path, dimensions, openai_api_key):
    # open json file for reading
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        ids, payloads, vectors = [], [], []
        for book in data:
            ids.append(str(uuid.uuid4()))
            resume = book["resume"]
            payloads.append({
                "title": book["title"],
                "resume": resume
            })
            vectors.append(embedd_texts(resume, openai_api_key, dimensions))

        # insert data into Qdrant
        client.upsert(
            collection_name=collection_name,
            points=qdrant.Batch(
                ids=ids,
                payloads=payloads,
                vectors=vectors
            )
        )


if __name__ == "__main__":
    file_path = "books.json"
    local_host_url = "http://localhost:31333/"
    dimensions = 1536
    collection_name = "book_recommendations"
    client = QdrantClient(
        url=local_host_url,
        check_compatibility=False,
    )
    create_collection(client, collection_name, dimensions)
    openai_api_key = os.getenv("OPENAI_Lawgentic_API_KEY")
    insert_to_qdrant(client, collection_name, file_path, dimensions, openai_api_key)

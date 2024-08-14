import os

import jsonlines
from dotenv import load_dotenv
from mistralai import Mistral
from upstash_vector import Index

load_dotenv()
mistral_client = Mistral(os.getenv("MISTRAL_API_KEY"))
upstash_index = Index.from_env()

query = "Theo thống kê, các lĩnh vực nào có số công bố nhiều nhất?"
print(f"Query: {query}")

query_embedding = (
    mistral_client.embeddings.create(model="mistral-embed", inputs=[query])
    .data[0]
    .embedding
)
query_result = upstash_index.query(query_embedding, top_k=1, include_metadata=True)
source_metadata = query_result[0].metadata

with jsonlines.open("data/articles.jsonl") as reader:
    for article_id, i in enumerate(reader):
        if article_id == source_metadata["article_id"]:
            print(f"Link: {i['link']}")
            print(f"Title: {i['title']}")
            paragraph = i["content"][source_metadata["paragraph_id"]]
            print(f"Paragraph: {paragraph}")

instruction = f"""Answer the following question based on the context below.

Question:
{query}

Context:
{paragraph}
"""
chat_response = mistral_client.chat.complete(
    model="open-mistral-nemo",
    messages=[
        {
            "role": "user",
            "content": instruction,
        }
    ],
)
print(f"Response: {chat_response.choices[0].message.content}")

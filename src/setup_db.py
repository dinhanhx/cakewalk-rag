import os
import time

import jsonlines
from dotenv import load_dotenv
from mistralai import Mistral
from tqdm import tqdm
from upstash_vector import Index

load_dotenv()
mistral_client = Mistral(os.getenv("MISTRAL_API_KEY"))
upstash_index = Index.from_env()

with jsonlines.open("data/articles.jsonl") as reader:
    for article_id, i in enumerate(tqdm(reader)):
        embedding_batch_response = mistral_client.embeddings.create(
            model="mistral-embed", inputs=i["content"]
        )
        vectors = []
        for paragraph_id, j in enumerate(embedding_batch_response.data):
            vectors.append(
                (
                    f"id-{article_id}-{paragraph_id}",
                    j.embedding,
                    {"article_id": article_id, "paragraph_id": paragraph_id},
                )
            )
        upstash_index.upsert(vectors=vectors)
        time.sleep(60)

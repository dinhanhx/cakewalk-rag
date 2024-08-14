# A very simple RAG implementation

This project is a simple RAG tool for asking questions related to some vnexpress articles.

This project is to demonstrate how RAG can be easily implemented without buzzy frameworks such as LangChain or LLamaIndex. Therefor, people can integrate RAG into their own system/project. 

This projects uses:
- Scrapy for getting plain text of articles from [vnexpress giao duc tin tuc](https://vnexpress.net/giao-duc/tin-tuc)
- [Mistral Platform](https://mistral.ai/) for both embedding and language models. They are `mistral-embed` and `open-mistral-nemo`
- [Upstash Vector](https://upstash.com/docs/vector/overall/getstarted) for vector database

## Setup

Python 3.10

Install required packages, please see `requirements.txt` for extra information
```bash
pip install -r requirements.txt
```

Mistral API key and Upstash API key are stored at `.env`

```bash
MISTRAL_API_KEY=<key_here>
UPSTASH_VECTOR_REST_URL=<key_here>
UPSTASH_VECTOR_REST_TOKEN=<key_here>
```

## Run

It is strongly advised to reach each .py file before running any command. By doing so, you get to understand the project more.

### Scrap the data

At root project
```bash
scrapy runspider --set FEED_EXPORT_ENCODING=utf-8 src/vnexpress_spider.py -o data/articles.jsonl
```

Scrapy won't overwrite `data/articles.jsonl` if it already exists. If you want new data, you have to delete the file.

### Setup the database

At root project
```bash
python src/setup_db.py
```

If a vector database already exists and `data/articles.jsonl` changes, you should delete the database.

### Run the tool

You should definitely edit `query` variable in `src/rag.py`.

At root project
```bash
python src/rag.py
```

## Great researcher/developer-friendly RAG frameworks

- [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)
- [neuml/txtai](https://github.com/neuml/txtai)
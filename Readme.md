# FastAPI NLP Tasks API

This repository contains a FastAPI application that provides various Natural Language Processing (NLP) tasks through a RESTful API. The application supports summarization, translation, sentiment analysis, question answering, and text generation.

## Features

- **Summarization**: Generates a concise summary of the input text.
- **Translation**: Translates text to a specified target language.
- **Sentiment Analysis**: Analyzes the sentiment of the input text.
- **Question Answering**: Answers questions based on a given context.
- **Text Generation**: Generates new text based on an input prompt.

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn (for running the server)
- Required NLP libraries (transformers, torch, etc.)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/fastapi-nlp-tasks.git
   cd fastapi-nlp-tasks
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`.

3. You can access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

### POST /summarizer
Generates a summary of the input text.

### POST /translator
Translates the input text to the specified target language.

### POST /sentiment_analizer
Analyzes the sentiment of the input text.

### POST /question_answerer
Answers a question based on the provided context.

### POST /text_generation
Generates new text based on an input prompt.

## Request Bodies

Each endpoint expects a JSON request body with specific fields. Here are the models for each task:

- Summarization: `{"text": "string"}`
- Translation: `{"text": "string", "language_to": "string"}`
- Classification (Sentiment Analysis): `{"text": "string"}`
- QuestionAnswering: `{"text": "string", "context": "string"}`
- TextGeneration: `{"text": "string"}`

## Models Used

- Summarization: `google/pegasus-xsum`
- Translation: `t5-small`
- Sentiment Analysis: `distilbert-base-uncased-finetuned-sst-2-english`
- Question Answering: `deepset/roberta-base-squad2`
- Text Generation: `distilgpt2`

## Error Handling

The API includes basic error handling. If an unsupported language is provided for translation, it will return an error message.

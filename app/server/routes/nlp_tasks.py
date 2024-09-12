import json
import logging
from multiprocessing.sharedctypes import Value
from fastapi import APIRouter, Body, Depends, Request
from fastapi.encoders import jsonable_encoder

from ..models.nlp_tasks import Summarization, Translation, Classification, QuestionAnswering, TextGeneration
from ..models.main import ResponseModel, ErrorResponseModel

from ..utils.summarization import Summarizer
from ..utils.translation import Translator
from ..utils.sentiment_classification import SentimentClassifier
from ..utils.question_answering import QuestionAnswerer
from ..utils.text_generation import TextGenerator

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post('/summarizer')
def summarize(task: Summarization):
    task = jsonable_encoder(task)
    summarizer = Summarizer('google/pegasus-xsum')
    output = summarizer(task.get('text'))
    return ResponseModel(output, "Summarization complete")

@router.post('/translator')
def translate(task: Translation):
    task = jsonable_encoder(task)
    try:
        translator = Translator('t5-small', language_to= task.get('language_to'))
    except ValueError as err:
        print(f'Please enter a supported Language and try again.')
        return ErrorResponseModel(err, 400 , 'Please enter a supported language and try again.')
    output = translator(task.get('text'))
    return ResponseModel(output, "Summarization complete")

@router.post('/sentiment_analizer')
def analyse_sentiment(task: Classification):
    task = jsonable_encoder(task)
    classifier = SentimentClassifier('distilbert-base-uncased-finetuned-sst-2-english')
    output = classifier(task.get('text'))
    return ResponseModel(output, "Sentiment Analysation complete")

@router.post('/question_answerer')
def answer_question(task: QuestionAnswering):
    task = jsonable_encoder(task)
    answerer = QuestionAnswerer('deepset/roberta-base-squad2')
    output = answerer(task.get('text'), task.get('context'))
    return ResponseModel(output, 'Question Answered complete')

@router.post('/text_generation')
def generate_text(task: TextGeneration):
    task = jsonable_encoder(task)
    answerer = TextGenerator('distilgpt2')
    output = answerer(task.get('text'))
    return ResponseModel(output, 'Text Generation complete')

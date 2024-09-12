from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routes.user import router as userRouter
from .routes.nlp_tasks import router as nlpRouter
from .utils.middlewares import ChangeResponseMiddleware
from .utils.main import html_home

import logging

format = "%(levelname)s:%(funcName)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=format)

app = FastAPI()
app.include_router(userRouter, tags=["user"], prefix="/huggingai/v1/user")
app.include_router(nlpRouter, tags=["nlp_tasks"], prefix="/huggingai/v1/nlp_tasks")
app.add_middleware(ChangeResponseMiddleware)

# controller routes
@app.get("/")
def get():
    return HTMLResponse(html_home)


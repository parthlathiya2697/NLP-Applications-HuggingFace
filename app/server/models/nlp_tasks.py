from pydantic import BaseModel, validator


class Summarization(BaseModel):
    text: str
    @validator('text')
    def check_string(cls, v, **kwargs):
        if not len(v.split(" ")) >= 10:
            raise ValueError("Please enter text longer than 10 words atleast.")
        return v

class Translation(BaseModel):
    text: str
    language_to: str

class Classification(BaseModel):
    text: str

class QuestionAnswering(BaseModel):
    text: str
    context: str

class TextGeneration(BaseModel):
    text: str
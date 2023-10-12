from datetime import datetime
from pydantic import BaseModel, Field


class Question(BaseModel):
    id: int  # noqa A003
    question: str
    answer: str
    created_at: datetime | None

    class Config:
        orm_mode = True
        extra = "ignore"


class QuestionQuantityRequest(BaseModel):
    questions_num: int = Field(gt=0)

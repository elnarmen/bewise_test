from fastapi import FastAPI

import schemas
from jservice_client import fetch_random_questions
from db.crud import get_existing_question_ids, get_last_db_question, add_questions_to_db

app = FastAPI()
MAX_RETRIES = 20


@app.post('/questions')
def main(response: schemas.QuestionQuantityRequest) -> schemas.Question | None:
    retry_count = 0
    questions_num = response.questions_num
    last_db_question = get_last_db_question()
    while questions_num:
        questions = fetch_random_questions(questions_num)
        existing_question_ids = get_existing_question_ids(questions)
        if existing_question_ids:
            questions = [
                question for question in questions if question.id not in existing_question_ids
            ]
        add_questions_to_db(questions)
        questions_num = len(existing_question_ids)
        if retry_count == MAX_RETRIES:  # выходит из цикла, если jservice перестал выдавать новые вопросы
            break
    return schemas.Question.from_orm(last_db_question) if last_db_question else None

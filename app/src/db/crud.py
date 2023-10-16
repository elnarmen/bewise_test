from db import models
import schemas
from db.database import Session


def get_existing_question_ids(questions: list[schemas.Question]) -> list[int]:
    with Session() as session:
        question_ids = [question.id for question in questions]
        db_questions_by_ids = session.query(models.Question.id).filter(models.Question.id.in_(question_ids)).all()
    db_question_ids = [item[0] for item in db_questions_by_ids]
    return db_question_ids


def add_questions_to_db(questions: list[schemas.Question]) -> None:
    with Session() as session:
        db_questions = [
            models.Question(
                id=question.id,
                question=question.question,
                answer=question.answer,
                created_at=question.created_at,
            ) for question in questions
        ]
        session.add_all(db_questions)
        session.commit()


def get_last_db_question() -> models.Question:
    with Session() as session:
        last_added_question = session.query(models.Question).order_by(models.Question.auto_id.desc()).first()
    return last_added_question

import httpx

from schemas import Question


def fetch_random_questions(question_count: int) -> list[Question]:
    url = 'https://jservice.io/api/random'

    with httpx.Client() as client:
        response = client.get(url, params={'count': question_count})
        response.raise_for_status()

    questions = [Question.parse_obj(question) for question in response.json()]
    return questions

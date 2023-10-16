from sqlalchemy import Column, Integer, String, DateTime

from db.database import Base


class Question(Base):
    __tablename__ = "questions"

    auto_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, index=True)  # noqa A003
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True))

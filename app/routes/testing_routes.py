from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.connector.postgres_conn import SessionLocal
from app.schema import models

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/questions")
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions

@router.post("/questions")
def create_question(question_text: str, db: Session = Depends(get_db)):
    new_question = models.Question(question_text=question_text)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.post("/choices")
def create_choice(choice_text: str, question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    new_choice = models.Choice(choice_text=choice_text, question_id=question_id)
    db.add(new_choice)
    db.commit()
    db.refresh(new_choice)
    return new_choice

from fastapi import APIRouter, Depends,Path, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todos
from starlette import status



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.to_dict())

    db.add(todo_model)
    db.commit()


from fastapi import FastAPI,Depends
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from database import sessionLocal, engine
from models import Todo


app = FastAPI()

# Create DB Tables
import models
models.Base.metadata.create_all(bind=engine)

#Dependency for DB Session
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

#post - create todo
@app.post("/todos",response_model=TodoSchema)
def create(todo:TodoCreate,db: Session = Depends(get_db)):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#get - all Todos
@app.get("/todos",response_model=list[TodoSchema])
def read_todos(db:Session = Depends(get_db)):
    return db.query(Todo).all()

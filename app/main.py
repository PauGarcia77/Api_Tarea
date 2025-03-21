from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from crud import get_tasks, create_tasks, update_tasks, delete_tasks
from schemas import TaskCreate, TaskUpdate, TaskResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/tasks", response_model=list[TaskResponse])
def read_taks(db: Session = Depends(get_db)):
    return get_tasks(db)


@app.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_tasks(db, task)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def modify_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    updated_tasks = update_tasks(db, task_id, task_update)
    if not updated_tasks:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    return updated_tasks


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_tasks(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    return {"message": "Tasca eliminada"}

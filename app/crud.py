from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    """
    Input:
        db: database session
    Output:
        List all tasks
    """
    # TODO: El vostre codi va aqui
    return db.query(Task).all()


def create_tasks(db: Session, task: TaskCreate):
    """
    Input:
        db: database session
    Output:
        Return the new task
    """
    # TODO: El vostre codi va aqui
    # import ipdb; ipdb.set_trace()
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task  # 🔹 Ahora devuelve la tarea creada


def update_tasks(db: Session, task_id: int, task_update: TaskUpdate):
    # import ipdb; ipdb.set_trace()

    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None  # Opcional: podrías lanzar un HTTPException aquí

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task  # 🔹 Devuelve la tarea actualizada


def delete_tasks(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None  # Opcional: podrías lanzar un HTTPException aquí

    db.delete(db_task)
    db.commit()
    return db_task  # 🔹 Devuelve la tarea eliminada

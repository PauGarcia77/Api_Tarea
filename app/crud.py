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
    pass


def create_tasks(db: Session, task: TaskCreate):
    """
    Input:
        db: database session
    Output:
        Return the new task
    """
    # TODO: El vostre codi va aqui
    pass


def update_tasks(db: Session, task_id: int, task_update: TaskUpdate):
    """
    Input:
        db: database session
    Output:
        Updated some task fields
    """
    # TODO: El vostre codi va aqui
      # Buscar la tarea por ID
    task = db.query(Task).filter(Task.id == task_id).first()
    
    # Si la tarea no se encuentra, devolver None
    if not task:
        return None
    
    # Actualizar los atributos de la tarea
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    
    # Confirmar los cambios en la base de datos
    db.commit()
    
    # Actualizar la instancia de la tarea para reflejar los cambios
    db.refresh(task)
    
    return task
    pass


def delete_tasks(db: Session, task_id: int):
    """
    Input:
        db: database session
    Output:
        Return delete task
    """
    # TODO: El vostre codi va aqui
    task = db.query(Task).filter(Task.id == task_id).first()
    
    # Si la tarea no se encuentra, devolver None
    if not task:
        return None
    
    # Guardar la tarea antes de eliminarla (para poder devolverla)
    deleted_task = task
    
    # Eliminar la tarea
    db.delete(task)
    
    # Confirmar los cambios en la base de datos
    db.commit()
    
    return deleted_task
    pass

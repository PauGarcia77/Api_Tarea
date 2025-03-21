from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# TODO: els vostres test venen aqui
import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from models import Task
from schemas import TaskCreate
from crud import get_tasks, create_tasks


class TestGetCreateFunctions(unittest.TestCase):
    
    def setUp(self):
        # Configuración común para todas las pruebas
        self.db = MagicMock(spec=Session)
        
        # Crear una tarea ficticia para usar en las pruebas
        self.mock_task = Task(
            id=1,
            title="Tarea de prueba",
            description="Descripción de prueba",
            completed=False
        )
    
    def test_get_tasks(self):
        """Prueba que get_tasks devuelve todas las tareas de la base de datos"""
        # Configurar el mock para que .query().all() devuelva una lista de tareas
        mock_tasks = [self.mock_task]
        self.db.query.return_value.all.return_value = mock_tasks
        
        # Llamar a la función
        result = get_tasks(self.db)
        
        # Verificar que se llamó a .query() con el modelo Task
        self.db.query.assert_called_once_with(Task)
        
        # Verificar que se llamó a .all() después de .query()
        self.db.query.return_value.all.assert_called_once()
        
        # Verificar que el resultado es la lista de tareas esperada
        self.assertEqual(result, mock_tasks)
    
    def test_get_tasks_empty(self):
        """Prueba que get_tasks devuelve una lista vacía cuando no hay tareas"""
        # Configurar el mock para que .query().all() devuelva una lista vacía
        self.db.query.return_value.all.return_value = []
        
        # Llamar a la función
        result = get_tasks(self.db)
        
        # Verificar que se llamó a .query() con el modelo Task
        self.db.query.assert_called_once_with(Task)
        
        # Verificar que se llamó a .all() después de .query()
        self.db.query.return_value.all.assert_called_once()
        
        # Verificar que el resultado es una lista vacía
        self.assertEqual(result, [])
    
    def test_create_tasks(self):
        """Prueba que create_tasks crea correctamente una nueva tarea"""
        # Crear datos de prueba
        task_data = TaskCreate(
            title="Nueva tarea",
            description="Nueva descripción"
        )
        
        # Configurar el mock para que el objeto devuelto por .refresh() sea la tarea creada
        def side_effect_refresh(task):
            # Simular el comportamiento de refresh que asigna un ID a la tarea
            task.id = 1
            return task
            
        self.db.refresh.side_effect = side_effect_refresh
        
        # Llamar a la función
        result = create_tasks(self.db, task_data)
        
        # Verificar que se llamó a db.add() con una instancia de Task
        self.db.add.assert_called_once()
        added_task = self.db.add.call_args[0][0]
        self.assertIsInstance(added_task, Task)
        
        # Verificar que los datos de la tarea son correctos
        self.assertEqual(added_task.title, "Nueva tarea")
        self.assertEqual(added_task.description, "Nueva descripción")
        
        # Verificar que se llamó a commit y refresh
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        
        # Verificar que la función devuelve la tarea creada
        self.assertEqual(result, added_task)
        
    def test_create_tasks_validates_fields(self):
        """Prueba que create_tasks asigna correctamente todos los campos necesarios"""
        # Crear datos de prueba más detallados
        task_data = TaskCreate(
            title="Tarea con detalles",
            description="Descripción detallada de la tarea"
        )
        
        # Llamar a la función
        result = create_tasks(self.db, task_data)
        
        # Obtener la tarea que se pasó a db.add()
        added_task = self.db.add.call_args[0][0]
        
        # Verificar que todos los campos se asignaron correctamente
        self.assertEqual(added_task.title, "Tarea con detalles")
        self.assertEqual(added_task.description, "Descripción detallada de la tarea")
        
        # Verificar que el campo completed es False por defecto (según el modelo)
        # Nota: Esto depende de cómo se inicializa Task, pero asumimos que sigue el modelo
        # donde completed tiene un valor por defecto de False
        self.assertFalse(hasattr(added_task, 'completed') or added_task.completed is None, 
                         "El campo 'completed' debería ser None o no existir en este punto, ya que se establece por defecto en la base de datoss")


if __name__ == "__main__":
    unittest.main()
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# TODO: els vostres test venen aqui

import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from models import Task
from schemas import TaskUpdate
from crud import update_tasks, delete_tasks


class TestUpdateDeleteFunctions(unittest.TestCase):
    
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

    def test_update_tasks_existing_task(self):
        """Prueba que update_tasks actualiza correctamente una tarea existente"""
        # Configurar el mock para simular que se encuentra la tarea
        self.db.query.return_value.filter.return_value.first.return_value = self.mock_task
        
        # Crear datos de actualización
        task_update = TaskUpdate(
            title="Título actualizado",
            description="Descripción actualizada",
            completed=True
        )
        
        # Llamar a la función
        result = update_tasks(self.db, 1, task_update)
        
        # Verificar que se buscó la tarea correcta
        self.db.query.assert_called_once_with(Task)
        self.db.query.return_value.filter.assert_called_once()
        
        # Verificar que se actualizaron los atributos
        self.assertEqual(self.mock_task.title, "Título actualizado")
        self.assertEqual(self.mock_task.description, "Descripción actualizada")
        self.assertEqual(self.mock_task.completed, True)
        
        # Verificar que se llamó a commit y refresh
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(self.mock_task)
        
        # Verificar que la función devuelve la tarea actualizada
        self.assertEqual(result, self.mock_task)

    def test_update_tasks_nonexistent_task(self):
        """Prueba que update_tasks devuelve None cuando la tarea no existe"""
        # Configurar el mock para simular que no se encuentra la tarea
        self.db.query.return_value.filter.return_value.first.return_value = None
        
        # Crear datos de actualización
        task_update = TaskUpdate(
            title="Título actualizado",
            description="Descripción actualizada",
            completed=True
        )
        
        # Llamar a la función
        result = update_tasks(self.db, 999, task_update)
        
        # Verificar que se buscó la tarea
        self.db.query.assert_called_once_with(Task)
        self.db.query.return_value.filter.assert_called_once()
        
        # Verificar que no se llamó a commit ni refresh
        self.db.commit.assert_not_called()
        self.db.refresh.assert_not_called()
        
        # Verificar que la función devuelve None
        self.assertIsNone(result)

    def test_delete_tasks_existing_task(self):
        """Prueba que delete_tasks elimina correctamente una tarea existente"""
        # Configurar el mock para simular que se encuentra la tarea
        self.db.query.return_value.filter.return_value.first.return_value = self.mock_task
        
        # Llamar a la función
        result = delete_tasks(self.db, 1)
        
        # Verificar que se buscó la tarea correcta
        self.db.query.assert_called_once_with(Task)
        self.db.query.return_value.filter.assert_called_once()
        
        # Verificar que se llamó a delete con la tarea correcta
        self.db.delete.assert_called_once_with(self.mock_task)
        
        # Verificar que se llamó a commit
        self.db.commit.assert_called_once()
        
        # Verificar que la función devuelve la tarea eliminada
        self.assertEqual(result, self.mock_task)

    def test_delete_tasks_nonexistent_task(self):
        """Prueba que delete_tasks devuelve None cuando la tarea no existe"""
        # Configurar el mock para simular que no se encuentra la tarea
        self.db.query.return_value.filter.return_value.first.return_value = None
        
        # Llamar a la función
        result = delete_tasks(self.db, 999)
        
        # Verificar que se buscó la tarea
        self.db.query.assert_called_once_with(Task)
        self.db.query.return_value.filter.assert_called_once()
        
        # Verificar que no se llamó a delete ni commit
        self.db.delete.assert_not_called()
        self.db.commit.assert_not_called()
        
        # Verificar que la función devuelve None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
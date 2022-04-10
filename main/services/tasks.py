from typing import List, Optional

from fastapi.params import Depends

from main.core.logging import logger
from main.db.repositories.tasks import TasksRepository, get_tasks_repository
from main.db.tables import Task
from main.schemas.tasks import TaskInCreate, TaskInUpdate


class TasksService:
    """
    Service for manipulation with tasks.
    """

    def __init__(self, db: TasksRepository = Depends(get_tasks_repository)) -> None:
        self.db = db

    def insert_task(self, task: TaskInCreate, owner_id: int) -> Task:
        """
        Insert task to the database.
        """
        logger.info(f"Creating task: title {task.title}, owner_id {owner_id}")
        return self.db.create_with_owner(obj_create=task, owner_id=owner_id)

    def get_all_owner_tasks(self, owner_id: int, skip: int, limit: int) -> List[Task]:
        """
        Return all tasks from the database.
        """
        logger.info(f"Retrieving all tasks for user with owner_id: {owner_id}")
        return self.db.get_all_by_owner(owner_id=owner_id, skip=skip, limit=limit)

    def delete_task(self, task: Task) -> Optional[Task]:
        """
        Delete task with specific `task_id`.
        """
        logger.info(f"Deleting task with id: {task.id}")
        return self.db.delete(obj_id=task.id)

    def update_task(self, task: Task, task_update: TaskInUpdate) -> Task:
        """
        Update task with specific `task_id` field.
        """
        logger.info(f"Updating task with id: {task.id}")
        return self.db.update(obj=task, obj_update=task_update)

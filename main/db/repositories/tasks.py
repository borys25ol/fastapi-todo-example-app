from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from main.core.config import get_app_settings
from main.db.repositories.base import BaseRepository
from main.db.session import get_db
from main.models.task import Task
from main.schemas.tasks import TaskInCreate, TaskInUpdate

settings = get_app_settings()


class TasksRepository(BaseRepository[Task, TaskInCreate, TaskInUpdate]):
    """
    Repository to manipulate with the task.
    """

    def get_all_by_owner(
        self, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        Get all tasks created by specific user with id `owner_id`.
        """
        return (
            self.db.query(self.model)
            .filter(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(self, *, obj_create: TaskInCreate, owner_id: int) -> Task:
        """
        Create new task by specific user with id `owner_id`.
        """
        obj = self.model(**obj_create.dict(), owner_id=owner_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_many_by_owner(self, obj_ids: List[int], owner_id: int) -> List[int]:
        """
        Bulk delete objects.
        """
        query = (
            self.db.query(self.model)
            .filter(Task.owner_id == owner_id)
            .filter(self.model.id.in_(obj_ids))
        )
        query.delete(synchronize_session=False)
        self.db.commit()
        return obj_ids


def get_tasks_repository(session: Session = Depends(get_db)) -> TasksRepository:
    return TasksRepository(db=session, model=Task)

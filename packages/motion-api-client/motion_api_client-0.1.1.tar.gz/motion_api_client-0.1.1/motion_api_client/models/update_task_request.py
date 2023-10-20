from datetime import datetime
from typing import List

from motion_api_client.models.create_task_request import AutoScheduled

class UpdateTaskRequest:
    def __init__(self, name: str = None, dueDate: datetime = None, duration: str = None, status: str = None,
                 autoScheduled: AutoScheduled = None, projectId: str = None, description: str = None,
                 priority: str = None, labels: List[str] = None, assigneeId: str = None):
        self.name = name
        self.dueDate = dueDate
        self.duration = duration
        self.status = status
        self.autoScheduled = autoScheduled
        self.projectId = projectId
        self.description = description
        self.priority = priority
        self.labels = labels
        self.assigneeId = assigneeId

    def to_dict(self):
        return vars(self)
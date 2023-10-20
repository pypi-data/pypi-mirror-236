import json
from datetime import datetime
from typing import List, overload


class AutoScheduled:
    def __init__(self, startDate: datetime, deadlineType: str, schedule: str):
        self.startDate = startDate
        self.deadlineType = deadlineType
        self.schedule = schedule


class CreateTaskRequest:



    def __init__(self, name: str, workspaceId: str, dueDate: datetime = None, duration: str = 30, status: str = "",
                 autoScheduled: AutoScheduled = None,
                 projectId: str = "", description: str = "", priority: str = "", labels: List[str] = None,
                 assigneeId: str = ""):
        self.dueDate = dueDate
        self.duration = duration
        self.status = status
        self.autoScheduled = autoScheduled
        self.name = name
        self.projectId = projectId
        self.workspaceId = workspaceId
        self.description = description
        self.priority = priority
        self.labels = labels
        self.assigneeId = assigneeId

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        return vars(self)

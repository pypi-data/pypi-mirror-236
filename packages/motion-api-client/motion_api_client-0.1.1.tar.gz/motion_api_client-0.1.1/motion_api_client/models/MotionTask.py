import datetime
from typing import List


class Creator:
    id: str
    name: str
    email: str

    def __init__(self, id: str, name: str, email: str) -> None:
        self.id = id
        self.name = name
        self.email = email


class Label:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class Project:
    id: str
    name: str
    description: str
    workspace_id: str

    def __init__(self, id: str, name: str, description: str, workspaceId: str) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.workspace_id = workspaceId


class Status:
    name: str
    is_default_status: bool
    is_resolved_status: bool

    def __init__(self, name: str, isDefaultStatus: bool, isResolvedStatus: bool) -> None:
        self.name = name
        self.is_default_status = isDefaultStatus
        self.is_resolved_status = isResolvedStatus


class Workspace:
    id: str
    name: str
    team_id: str
    statuses: List[Status]
    labels: List[Label]
    type: str

    def __init__(self, id: str, name: str, teamId: str, statuses: List[Status], labels: List[Label], type: str) -> None:
        self.id = id
        self.name = name
        self.team_id = teamId
        self.statuses = statuses
        self.labels = labels
        self.type = type


class MotionTask:
    duration: str
    workspace: Workspace
    id: str
    name: str
    description: str
    due_date: datetime
    deadline_type: str
    parent_recurring_task_id: str
    completed: bool
    creator: Creator
    project: Project
    status: Status
    priority: str
    labels: List[Label]
    assignees: List[Creator]
    scheduled_start: datetime
    created_time: datetime
    scheduled_end: datetime
    scheduling_issue: bool

    def __init__(self, duration: str, workspace: Workspace, id: str, name: str, description: str, dueDate: datetime,
                 deadlineType: str, parentRecurringTaskId: str, completed: bool, creator: Creator, project: Project,
                 status: Status, priority: str, labels: List[Label], assignees: List[Creator], scheduledStart: datetime,
                 createdTime: datetime, scheduledEnd: datetime, schedulingIssue: bool) -> None:
        self.duration = duration
        self.workspace = workspace
        self.id = id
        self.name = name
        self.description = description
        self.due_date = dueDate
        self.deadline_type = deadlineType
        self.parent_recurring_task_id = parentRecurringTaskId
        self.completed = completed
        self.creator = creator
        self.project = project
        self.status = status
        self.priority = priority
        self.labels = labels
        self.assignees = assignees
        self.scheduled_start = scheduledStart
        self.created_time = createdTime
        self.scheduled_end = scheduledEnd
        self.scheduling_issue = schedulingIssue

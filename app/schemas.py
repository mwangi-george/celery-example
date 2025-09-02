import enum
from typing import Any

from pydantic import BaseModel


class TaskStatus(str, enum.Enum):
    """Valid task statuses"""
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ResponseModel(BaseModel):
    """
    pydantic model to validate task response

    fields:
        - task_id (str | None)
        - status (TaskStatus | None)
        - result (Any | None)
        - cache_key (str | None)
    """
    task_id: str | None = None
    status: TaskStatus | None = None
    result: Any | None = None
    cache_key: str | None = None

    # documentation for openapi docs
    model_config = {
        "json_schema_extra": {
            "task_id": "<Task ID>",
            "status": TaskStatus.PROCESSING,
            "result": "Task result",
            "cache_key": "<Task cache key>",
        }
    }


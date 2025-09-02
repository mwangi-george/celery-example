from loguru import logger
from fastapi import FastAPI, status
from celery.result import AsyncResult

from app.celery_worker import heavy_task
from app.schemas import ResponseModel, TaskStatus
from app.utils import make_cache_key, add_result_to_cache, get_cached_result



app = FastAPI(
    title="FastAPI + Celery + Flower + Redis Demo",
    description="A simple fastapi application implementing long-running tasks with Celery with Redis",
    version="0.1.0",
)


@app.post("/start-task", response_model=ResponseModel, status_code=status.HTTP_202_ACCEPTED)
async def start_task(n: int, sleep_time_seconds: int = 30) -> ResponseModel:
    """
    Start a heavy task with input `n`. If already cached, return cached result.
    Otherwise, queue the task in celery
    """
    cached_key = make_cache_key(f"{n}_{sleep_time_seconds}")
    cached_result, cached_task_id = get_cached_result(cached_key)
    if cached_result:
        return ResponseModel(
            task_id=cached_task_id,
            status=TaskStatus.COMPLETED,
            result=cached_result,
            cache_key=cached_key
        )

    # offload task to celery
    task = heavy_task.delay(n, sleep_time_seconds)
    return ResponseModel(task_id=task.id, status=TaskStatus.PROCESSING, cache_key=cached_key)


@app.get("/task-status/{task_id}/", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_task_status(task_id: str, cache_key: str) -> ResponseModel:
    """Check the status of a task. If finished, also return result and store in cache"""
    task_result = AsyncResult(task_id)
    logger.info(f"Status for task {task_id} is {task_result.status}")

    if task_result.ready():
        result = task_result.result

        add_result_to_cache(cache_key, result, task_id)
        return ResponseModel(task_id=task_id, status=TaskStatus.COMPLETED, result=result, cache_key=cache_key)

    return ResponseModel(task_id=task_id, status=TaskStatus.PROCESSING, cache_key=cache_key)

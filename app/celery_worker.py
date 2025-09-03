from celery import Celery, current_task
import time

from app.utils import add_result_to_cache, make_cache_key
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from app.tasks import generate_excel_workbook


# Celery app configuration (using redis as the broker and backend)
celery_app = Celery(
    main="celery_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


# define a task -> simulating a long-running and heavy computation taks
@celery_app.task(name="heavy_task")
def heavy_task(n: int, sleep_time_seconds: int = 10) -> int:
    redis_key = make_cache_key(f"{n}_{sleep_time_seconds}")

    time.sleep(sleep_time_seconds)  # simulate long computation
    result = n * n

    add_result_to_cache(redis_key, result, current_task.request.id)
    return result



@celery_app.task(name="generate_excel_file")
def generate_excel_file(title: str, rows: list[list[str]], cache_key: str):

    # generate workbook
    wb = generate_excel_workbook(title, rows)

    # cache result
    add_result_to_cache(cache_key, wb, current_task.request.id)
    return wb



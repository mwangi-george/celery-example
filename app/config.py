import os
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL=os.getenv('REDIS_URL')
CELERY_RESULT_BACKEND=os.getenv('REDIS_URL')
REDIS_URL=os.getenv('REDIS_URL')
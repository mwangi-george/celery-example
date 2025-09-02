FastAPI + Celery + Redis + Flower

This project provides a production-ready setup for running a FastAPI application with Celery for background task processing, Redis as the message broker and result backend, and Flower for monitoring tasks.

🚀 Features

FastAPI – Modern, fast web framework for building APIs.

Celery – Handles background and asynchronous tasks.

Redis – Used as both a message broker and result backend for Celery.

Flower – Provides a web dashboard for monitoring Celery tasks.

Dockerized – Easily deployable with docker-compose.

📦 Services

fastapi: Runs the FastAPI application (exposed on port 8000).

worker: Celery worker that processes background tasks.

flower: Task monitoring UI (available on port 5555).

redis: Message broker & result store (exposed on port 6379).

🛠 Setup & Run 1. Clone the repository git clone https://github.com/your-username/your-repo-name.git cd your-repo-name

2.  Create a .env file

Provide your environment variables (e.g., database URL, API keys). Example:

REDIS_URL=redis://redis:6379/0

3.  Build and start services docker-compose up --build

4.  Access the services

FastAPI API: http://localhost:8000

Flower Monitoring UI: http://localhost:5555

📌 Example Usage

Send a request to an endpoint in the FastAPI app that triggers a Celery task.

The task is queued in Redis and processed by the Celery worker.

Monitor task execution in the Flower dashboard.

🗂 Project Structure . ├── app/ │ ├── main.py \# FastAPI app entry point │ ├── celery_worker.py \# Celery app configuration │ └── tasks/ \# Celery tasks ├── Dockerfile \# FastAPI app container build ├── docker-compose.yml \# Orchestrates all services ├── .dockerignore └── README.md

🔍 Monitoring

Use Flower to track:

Active workers

Queued tasks

Task execution history

Failures & retries

📝 License

This project is licensed under the MIT License – see the LICENSE file for details.
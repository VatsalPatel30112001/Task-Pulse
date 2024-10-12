# Task Pulse

## Description

**Task Pulse** is a Django project with Celery for task scheduling, Redis as a message broker, and Daphne for ASGI server support. It features role-based access control and periodic updates for machine data.

## Features

- **Periodic task updates** with Celery Beat
- **Role-based access control**
- **Redis** for Celery message broking
- **Daphne** for ASGI server support

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Celery
- Redis
- Daphne
- PostgreSQL or other database

### Installation

1. **Clone the repo:**
    ```
        git clone https://github.com/VatsalPatel30112001/Task-Pulse
    ```

2. **Set up environment**
    ```
        python3 -m venv venv
        venv/bin/activate
    ```

3. **Install dependencies**
    ```
        pip install -r requirements.txt
    ```

4. **Install Redis and Daphne**
    ```
        Redis: Follow installation instructions from Redis documentation.
        Daphne: Typically installed via pip and managed as part of requirements.txt.
    ```

5. **Configure database in settings.py**

6. **Apply migrations**
    ```
        python manage.py migrate
    ```

## Usage

1. **Start Redis server**
    ```
        redis-server
    ```

2. **Start Django server**
    ```
        python manage.py runserver
    ```

3. **Start Celery worker**
    ```
        celery -A machines worker --pool=eventlet --concurrency=20 -l info
    ```

4. **Start Celery Beat**
    ```
        celery -A machines beat -l info
    ```

4. **Start Daphne server**
    ```
        daphne -p 8008 machines.asgi:application
    ```

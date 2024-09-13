#Intoduction
This project is a multi-user application designed for buying grocery items. Users can purchase multiple products from one or multiple sections/categories. The admin can manage categories and products. The application supports Role-Based Access Control (RBAC) and includes backend job scheduling for various tasks.

#Features
User authentication and authorization with three roles.
Admin can add, delete, and edit categories and products.
Users can purchase products from multiple categories.
Asynchronous jobs for exporting product details as CSV files.


# Project Setup and Running Guide
This guide will help you set up and run both the backend and frontend of the project, along with the task scheduler using Celery and Redis.

## Prerequisites

Ensure you have the following installed:
- Python (with `pip`)
- Node.js (with `npm`)
- Redis server

## Backend Setup
1. **Install backend dependencies**:
    Navigate to the backend folder and install the required dependencies listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run Flask backend**:
    Start the backend server using Flask:
    ```bash
    python main.py
    ```

## Frontend Setup
1. **Install frontend dependencies**:
    Navigate to the frontend folder and install the required packages using `npm`:
    ```bash
    npm install
    ```

2. **Run the frontend**:
    Start the frontend development server:
    ```bash
    npm run serve
    ```

## Running Celery and Celery Beat
1. **Start Celery worker**:
    Run the following command to start Celery workers with thread support:
    ```bash
    celery -A main.celery worker -l info -P threads
    ```

2. **Start Celery beat**:
    Run Celery beat to schedule tasks:
    ```bash
    celery -A main.celery beat -l info
    ```

## Running Redis
To support Celery, you need to start the Redis server. Run the following command:
```bash
redis-server


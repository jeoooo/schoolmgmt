# School Management System

This is a Django-based School Management System project. It is part of a training arc to learn how to set up database relationships and structure JSON generated through API requests.

## Project Structure

The project is organized into the following main directories:

- `colleges/`: Contains models, views, serializers, and URLs related to colleges.
- `courses/`: Contains models, views, serializers, and URLs related to courses.
- `departments/`: Contains models, views, serializers, and URLs related to departments.
- `schoolmgmt/`: Contains the main project settings and configurations.

## Features

- **Colleges**: Manage colleges with CRUD operations.
- **Departments**: Manage departments within colleges with CRUD operations.
- **Courses**: Manage courses within departments with CRUD operations.
- **API Documentation**: Swagger UI for API documentation.

---

## Setup

### Without Docker

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd schoolmgmt
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

6. **Access the application**:
    Open your browser and go to `http://127.0.0.1:8000/`.

---

### With Docker

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd schoolmgmt
    ```

2. **Build the Docker image**:
    ```sh
    docker-compose build
    ```

3. **Start the Docker containers**:
    ```sh
    docker-compose up
    ```

4. **Apply migrations**:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

5. **Access the application**:
    Open your browser and go to `http://localhost:8000/`.

---

## API Endpoints

- **Colleges**:
    - `GET /api/v1/colleges/`: List all colleges.
    - `POST /api/v1/colleges/`: Create a new college.
    - `GET /api/v1/colleges/<id>/`: Retrieve a college by ID.
    - `PUT /api/v1/colleges/<id>/`: Update a college by ID.
    - `DELETE /api/v1/colleges/<id>/`: Delete a college by ID.

- **Departments**:
    - `GET /api/v1/departments/`: List all departments.
    - `POST /api/v1/departments/`: Create a new department.
    - `GET /api/v1/departments/<id>/`: Retrieve a department by ID.
    - `PUT /api/v1/departments/<id>/`: Update a department by ID.
    - `DELETE /api/v1/departments/<id>/`: Delete a department by ID.

- **Courses**:
    - `GET /api/v1/courses/`: List all courses.
    - `POST /api/v1/courses/`: Create a new course.
    - `GET /api/v1/courses/<id>/`: Retrieve a course by ID.
    - `PUT /api/v1/courses/<id>/`: Update a course by ID.
    - `DELETE /api/v1/courses/<id>/`: Delete a course by ID.

---

## API Documentation

The API documentation is available at:

- Without Docker: `http://127.0.0.1:8000/api/v1/docs/`
- With Docker: `http://localhost:8000/api/v1/docs/`
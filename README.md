# School Management System

This is a Django-based School Management System project. It is part of a training arc to learn how to set up database relationships and structure JSON generated through API requests.

## Project Structure

The project is organized into the following main directories:

- `colleges/`: Contains models, views, serializers, and URLs related to colleges.
- `courses/`: Contains models, views, serializers, and URLs related to courses.
- `departments/`: Contains models, views, serializers, and URLs related to departments.
- `conf/`: Contains the main project settings and configurations.

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
    cd conf
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

7. **Access Swagger API Documentation**:
    Open your browser and go to `http://127.0.0.1:8000/api/v1/docs/` for interactive API documentation.

---

## Commands & Cheat Sheet

### Database Management

**Create and apply migrations**:
```sh
python manage.py makemigrations
python manage.py migrate
```

**Reset database (SQLite)**:
```sh
# Delete the database file
rm db.sqlite3  # On Windows: del db.sqlite3
# Re-run migrations
python manage.py migrate
```

**Create superuser**:
```sh
python manage.py createsuperuser
```

### Testing

**Run all tests**:
```sh
python manage.py test
```

**Run tests with verbose output**:
```sh
python manage.py test --verbosity=2
```

**Run specific app tests**:
```sh
python manage.py test colleges
python manage.py test departments
python manage.py test courses
python manage.py test students
python manage.py test professors
python manage.py test subjects
```

**Run integration tests**:
```sh
python manage.py test tests
```

**Run specific test methods**:
```sh
python manage.py test colleges.tests.CollegeModelTest.test_college_creation
python manage.py test tests.test_integration.SchoolManagementIntegrationTest
```

### Development Server

**Start development server**:
```sh
python manage.py runserver
```

**Start on specific port**:
```sh
python manage.py runserver 8080
```

**Start on all interfaces**:
```sh
python manage.py runserver 0.0.0.0:8000
```

### Django Shell

**Open Django shell**:
```sh
python manage.py shell
```

**Example shell commands**:
```python
# Import models
from colleges.models import College
from departments.models import Department

# Create objects
college = College.objects.create(name="Test College", address="123 Main St")
department = Department.objects.create(college=college, name="CS Department")

# Query objects
College.objects.all()
Department.objects.filter(college=college)
```

### Utility Commands

**Check for issues**:
```sh
python manage.py check
```

**Show migrations**:
```sh
python manage.py showmigrations
```

**Collect static files** (for production):
```sh
python manage.py collectstatic
```

---

### With Docker

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd conf
    ```

2. **Build the Docker image**:
    ```sh
    docker-compose build
    ```

3. **Start the Docker containers**:
    ```sh
    docker-compose up
    ```

4. **Apply migrations** (recommended to do locally):
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Access the application**:
    Open your browser and go to `http://localhost:8000/`.

6. **Access Swagger API Documentation**:
    Open your browser and go to `http://localhost:8000/api/v1/docs/` for interactive API documentation.

---

## Docker Commands

### Database Management

**Apply migrations locally** (recommended):
```sh
python manage.py makemigrations
python manage.py migrate
```

**Apply migrations inside Docker** (alternative):
```sh
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

**Create superuser**:
```sh
docker-compose exec web python manage.py createsuperuser
```

### Testing

**Run all tests**:
```sh
docker-compose exec web python manage.py test
```

**Run tests with verbose output**:
```sh
docker-compose exec web python manage.py test --verbosity=2
```

**Run specific app tests**:
```sh
docker-compose exec web python manage.py test colleges
docker-compose exec web python manage.py test departments
```

### Container Management

**Start containers**:
```sh
docker-compose up
```

**Start in background**:
```sh
docker-compose up -d
```

**Stop containers**:
```sh
docker-compose down
```

**Rebuild containers**:
```sh
docker-compose build
docker-compose up --build
```

**View logs**:
```sh
docker-compose logs web
```

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
# School Management System

This is a Django-based School Management System project. It is part of a training arc to learn how to set up database relationships and structure JSON generated through API requests.

## Project Structure

The project is organized into the following main directories:

- `colleges/`: Contains models, views, serializers, and URLs related to colleges.
- `courses/`: Contains models, views, serializers, and URLs related to courses.
- `departments/`: Contains models, views, serializers, and URLs related to departments.
- `students/`: Contains models, views, serializers, and URLs related to students.
- `professors/`: Contains models, views, serializers, and URLs related to professors.
- `subjects/`: Contains models, views, serializers, and URLs related to subjects.
- `enrollments/`: Contains models, views, serializers, and URLs related to course enrollments.
- `users/`: Contains custom user model and authentication-related functionality.
- `conf/`: Contains the main project settings and configurations.

## Features

- **Colleges**: Manage colleges with CRUD operations.
- **Departments**: Manage departments within colleges with CRUD operations.
- **Courses**: Manage courses within departments with CRUD operations.
- **Students**: Manage student information and academic records.
- **Professors**: Manage professor profiles and assignments.
- **Subjects**: Manage academic subjects and curriculum.
- **Enrollments**: Manage student course enrollments with status tracking (enrolled, completed, dropped, withdrawn) and grade management.
- **User Management**: Custom user model with role-based access control.
- **Test Data Generation**: Management command to populate realistic test data using Faker library.
- **API Documentation**: Swagger UI for API documentation.

---

## Setup

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

### Test Data Generation

**Populate realistic test data using Faker**:
```sh
python manage.py populate_enrollment_data
```

**Clear existing data and populate with custom parameters**:
```sh
python manage.py populate_enrollment_data --clear --students 50 --colleges 3
```

**Available options**:
- `--clear`: Clear all existing data before populating
- `--students NUMBER`: Number of students to create (default: 100)
- `--colleges NUMBER`: Number of colleges to create (default: 5)  
- `--departments-per-college NUMBER`: Number of departments per college (default: 4)
- `--courses-per-department NUMBER`: Number of courses per department (default: 6)

**Example with all options**:
```sh
python manage.py populate_enrollment_data --clear --students 200 --colleges 5 --departments-per-college 6 --courses-per-department 8
```

This command creates realistic test data using the Faker library including:
- Colleges with realistic names and addresses
- Departments with academic discipline names
- Courses with appropriate codes and descriptions
- Students with student IDs and academic information
- Course enrollments with various statuses (enrolled, completed, dropped, withdrawn) and grades

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

- **Students**:
    - `GET /api/v1/students/`: List all students.
    - `POST /api/v1/students/`: Create a new student.
    - `GET /api/v1/students/<id>/`: Retrieve a student by ID.
    - `PUT /api/v1/students/<id>/`: Update a student by ID.
    - `DELETE /api/v1/students/<id>/`: Delete a student by ID.

- **Professors**:
    - `GET /api/v1/professors/`: List all professors.
    - `POST /api/v1/professors/`: Create a new professor.
    - `GET /api/v1/professors/<id>/`: Retrieve a professor by ID.
    - `PUT /api/v1/professors/<id>/`: Update a professor by ID.
    - `DELETE /api/v1/professors/<id>/`: Delete a professor by ID.

- **Subjects**:
    - `GET /api/v1/subjects/`: List all subjects.
    - `POST /api/v1/subjects/`: Create a new subject.
    - `GET /api/v1/subjects/<id>/`: Retrieve a subject by ID.
    - `PUT /api/v1/subjects/<id>/`: Update a subject by ID.
    - `DELETE /api/v1/subjects/<id>/`: Delete a subject by ID.

- **Enrollments**:
    - `GET /api/v1/enrollments/`: List all enrollments with filtering support.
    - `POST /api/v1/enrollments/`: Create a new enrollment.
    - `GET /api/v1/enrollments/<id>/`: Retrieve an enrollment by ID.
    - `PUT /api/v1/enrollments/<id>/`: Update an enrollment by ID.
    - `DELETE /api/v1/enrollments/<id>/`: Delete an enrollment by ID.
    - `POST /api/v1/enrollments/<id>/complete/`: Mark enrollment as completed with grade.
    - `POST /api/v1/enrollments/<id>/drop/`: Drop a student from enrollment.
    - `POST /api/v1/enrollments/<id>/withdraw/`: Withdraw a student from enrollment.

**Query Parameters for Enrollments**:
- `student_id`: Filter by student ID
- `course_id`: Filter by course ID
- `status`: Filter by enrollment status (enrolled, completed, dropped, withdrawn)
- `semester`: Filter by semester
- `year`: Filter by academic year

---

## API Documentation

The API documentation is available at:

- Without Docker: `http://127.0.0.1:8000/api/v1/docs/`
- With Docker: `http://localhost:8000/api/v1/docs/`
from django.test import TestCase
from django.db import transaction
from colleges.models import College
from departments.models import Department
from courses.models import Course
from subjects.models import Subject
from students.models import Student
from professors.models import Professor


class SchoolManagementIntegrationTest(TestCase):
    """Integration tests for the entire school management system"""
    
    def setUp(self):
        """Set up test data with complete hierarchy"""
        # Create College
        self.college = College.objects.create(
            name="University of Technology",
            address="123 University Avenue",
            contact_number="555-0100"
        )
        
        # Create Department
        self.department = Department.objects.create(
            college=self.college,
            name="Computer Science and Engineering",
            description="Department focusing on computer science and software engineering"
        )
        
        # Create Course
        self.course = Course.objects.create(
            department=self.department,
            name="Bachelor of Science in Computer Science",
            code="BSCS",
            description="4-year undergraduate program in computer science"
        )
        
        # Create Subject
        self.subject = Subject.objects.create(
            course=self.course,
            name="Data Structures and Algorithms",
            code="CS301",
            description="Advanced study of data structures and algorithmic thinking"
        )
        
        # Create Student
        self.student = Student.objects.create(
            department=self.department,
            first_name="Alice",
            last_name="Johnson",
            student_id="2024001",
            email="alice.johnson@university.edu",
            contact_number="555-0101"
        )
        
        # Create Professor
        self.professor = Professor.objects.create(
            department=self.department,
            first_name="Dr. John",
            last_name="Smith",
            specialization="Machine Learning and Data Science",
            contact_number="555-0102"
        )
    
    def test_complete_hierarchy_creation(self):
        """Test that all models are created correctly with proper relationships"""
        # Verify College
        self.assertEqual(College.objects.count(), 1)
        self.assertEqual(self.college.name, "University of Technology")
        
        # Verify Department and its relationship to College
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(self.department.college, self.college)
        
        # Verify Course and its relationship to Department
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.department, self.department)
        
        # Verify Subject and its relationship to Course
        self.assertEqual(Subject.objects.count(), 1)
        self.assertEqual(self.subject.course, self.course)
        
        # Verify Student and its relationship to Department
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(self.student.department, self.department)
        
        # Verify Professor and its relationship to Department
        self.assertEqual(Professor.objects.count(), 1)
        self.assertEqual(self.professor.department, self.department)
    
    def test_cascade_delete_from_college(self):
        """Test that deleting college cascades to all related models"""
        college_id = self.college.id
        department_id = self.department.id
        course_id = self.course.id
        subject_id = self.subject.id
        student_id = self.student.id
        professor_id = self.professor.id
        
        # Delete college
        self.college.delete()
        
        # Verify all related objects are deleted
        with self.assertRaises(College.DoesNotExist):
            College.objects.get(id=college_id)
        
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(id=department_id)
        
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)
        
        with self.assertRaises(Subject.DoesNotExist):
            Subject.objects.get(id=subject_id)
        
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=student_id)
        
        with self.assertRaises(Professor.DoesNotExist):
            Professor.objects.get(id=professor_id)
    
    def test_cascade_delete_from_department(self):
        """Test that deleting department cascades to students, professors, and courses"""
        department_id = self.department.id
        course_id = self.course.id
        subject_id = self.subject.id
        student_id = self.student.id
        professor_id = self.professor.id
        
        # Delete department
        self.department.delete()
        
        # College should still exist
        self.assertTrue(College.objects.filter(id=self.college.id).exists())
        
        # Department and all related objects should be deleted
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(id=department_id)
        
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)
        
        with self.assertRaises(Subject.DoesNotExist):
            Subject.objects.get(id=subject_id)
        
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=student_id)
        
        with self.assertRaises(Professor.DoesNotExist):
            Professor.objects.get(id=professor_id)
    
    def test_cascade_delete_from_course(self):
        """Test that deleting course cascades only to subjects"""
        course_id = self.course.id
        subject_id = self.subject.id
        
        # Delete course
        self.course.delete()
        
        # College, Department, Student, and Professor should still exist
        self.assertTrue(College.objects.filter(id=self.college.id).exists())
        self.assertTrue(Department.objects.filter(id=self.department.id).exists())
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())
        self.assertTrue(Professor.objects.filter(id=self.professor.id).exists())
        
        # Course and Subject should be deleted
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)
        
        with self.assertRaises(Subject.DoesNotExist):
            Subject.objects.get(id=subject_id)
    
    def test_reverse_relationships(self):
        """Test reverse relationships work correctly"""
        # Test College -> Departments
        departments = self.college.department_set.all()
        self.assertEqual(len(departments), 1)
        self.assertEqual(departments[0], self.department)
        
        # Test Department -> Courses
        courses = self.department.courses.all()
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course)
        
        # Test Department -> Students
        students = self.department.students.all()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0], self.student)
        
        # Test Department -> Professors
        professors = self.department.professors.all()
        self.assertEqual(len(professors), 1)
        self.assertEqual(professors[0], self.professor)
        
        # Test Course -> Subjects
        subjects = self.course.subjects.all()
        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0], self.subject)
    
    def test_multiple_entities_per_parent(self):
        """Test creating multiple entities under the same parent"""
        # Create second department
        department2 = Department.objects.create(
            college=self.college,
            name="Electrical Engineering",
            description="Department of Electrical Engineering"
        )
        
        # Create second course under same department
        course2 = Course.objects.create(
            department=self.department,
            name="Master of Science in Computer Science",
            code="MSCS",
            description="Graduate program in computer science"
        )
        
        # Create second student under same department
        student2 = Student.objects.create(
            department=self.department,
            first_name="Bob",
            last_name="Wilson",
            student_id="2024002",
            email="bob.wilson@university.edu",
            contact_number="555-0103"
        )
        
        # Verify counts
        self.assertEqual(self.college.department_set.count(), 2)
        self.assertEqual(self.department.courses.count(), 2)
        self.assertEqual(self.department.students.count(), 2)
        
        # Verify specific relationships
        self.assertIn(department2, self.college.department_set.all())
        self.assertIn(course2, self.department.courses.all())
        self.assertIn(student2, self.department.students.all())
    
    def test_string_representations(self):
        """Test string representations of all models"""
        self.assertEqual(str(self.college), "University of Technology")
        self.assertEqual(str(self.department), "Computer Science and Engineering")
        self.assertEqual(str(self.course), "Bachelor of Science in Computer Science")
        self.assertEqual(str(self.subject), "Data Structures and Algorithms")
        self.assertEqual(str(self.student), "Alice Johnson")
        self.assertEqual(str(self.professor), "Dr. John Smith")


class SchoolManagementValidationTest(TestCase):
    """Test data validation across the system"""
    
    def setUp(self):
        self.college = College.objects.create(
            name="Test College",
            address="Test Address"
        )
        self.department = Department.objects.create(
            college=self.college,
            name="Test Department"
        )
    
    from django.db import IntegrityError

    def test_course_unique_code(self):
        course1 = Course.objects.create(
            department=self.department,
            name="Course 1",
            code="C001"
        )
        with self.assertRaises(self.IntegrityError):
            Course.objects.create(
                department=self.department,
                name="Course 2",
                code="C001"
            )

    def test_subject_unique_code(self):
        course1 = Course.objects.create(
            department=self.department,
            name="Course 1",
            code="C002"
        )
        subject1 = Subject.objects.create(
            course=course1,
            name="Subject 1",
            code="S001",
            description="Test subject"
        )
        with self.assertRaises(self.IntegrityError):
            Subject.objects.create(
                course=course1,
                name="Subject 2",
                code="S001",
                description="Another test subject"
            )

    def test_student_unique_id(self):
        student1 = Student.objects.create(
            department=self.department,
            first_name="John",
            last_name="Doe",
            student_id="ST001",
            email="john.doe@test.edu",
            contact_number="123-456-7890"
        )
        with self.assertRaises(self.IntegrityError):
            Student.objects.create(
                department=self.department,
                first_name="Jane",
                last_name="Smith",
                student_id="ST001",
                email="jane.smith@test.edu",
                contact_number="098-765-4321"
            )

    def test_college_name_required(self):
        from django.core.exceptions import ValidationError
        college = College(address="Test Address")
        with self.assertRaises(ValidationError):
            college.full_clean()

    def test_department_name_required(self):
        from django.core.exceptions import ValidationError
        department = Department(college=self.college)
        with self.assertRaises(ValidationError):
            department.full_clean()

    def test_department_college_required(self):
        with self.assertRaises(self.IntegrityError):
            Department.objects.create(name="Test Department")

    def test_course_name_required(self):
        from django.core.exceptions import ValidationError
        course = Course(department=self.department)
        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_course_department_required(self):
        with self.assertRaises(self.IntegrityError):
            Course.objects.create(name="Test Course")

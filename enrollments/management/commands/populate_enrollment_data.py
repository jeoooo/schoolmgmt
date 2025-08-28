from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from colleges.models import College
from departments.models import Department
from courses.models import Course
from students.models import Student
from enrollments.models import Enrollment
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with realistic sample enrollment data using Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )
        parser.add_argument(
            '--colleges',
            type=int,
            default=3,
            help='Number of colleges to create (default: 3)',
        )
        parser.add_argument(
            '--departments-per-college',
            type=int,
            default=4,
            help='Number of departments per college (default: 4)',
        )
        parser.add_argument(
            '--courses-per-department',
            type=int,
            default=6,
            help='Number of courses per department (default: 6)',
        )
        parser.add_argument(
            '--students',
            type=int,
            default=50,
            help='Number of students to create (default: 50)',
        )
        parser.add_argument(
            '--max-enrollments-per-student',
            type=int,
            default=5,
            help='Maximum enrollments per student (default: 5)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Enrollment.objects.all().delete()
            Student.objects.all().delete()
            Course.objects.all().delete()
            Department.objects.all().delete()
            College.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Create colleges
        colleges = []
        for i in range(options['colleges']):
            college = College.objects.create(
                name=fake.company() + " " + random.choice(['University', 'College', 'Institute']),
                address=fake.address(),
                contact_number=fake.phone_number()
            )
            colleges.append(college)
            self.stdout.write(f'Created college: {college.name}')

        # Create departments
        departments = []
        department_names = [
            'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology',
            'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
            'Business Administration', 'Economics', 'Psychology', 'Sociology',
            'English Literature', 'History', 'Philosophy', 'Art & Design',
            'Music', 'Theater Arts', 'Political Science', 'Environmental Science'
        ]
        
        for college in colleges:
            college_departments = random.sample(department_names, options['departments_per_college'])
            for dept_name in college_departments:
                department = Department.objects.create(
                    name=dept_name,
                    college=college,
                    description=fake.text(max_nb_chars=200)
                )
                departments.append(department)
                self.stdout.write(f'Created department: {dept_name} at {college.name}')

        # Create courses
        courses = []
        course_prefixes = {
            'Computer Science': ['CS', 'CSCI', 'COMP'],
            'Mathematics': ['MATH', 'MTH', 'CALC'],
            'Physics': ['PHYS', 'PHY'],
            'Chemistry': ['CHEM', 'CHM'],
            'Biology': ['BIO', 'BIOL'],
            'Electrical Engineering': ['EE', 'ECE', 'ELEC'],
            'Mechanical Engineering': ['ME', 'MECH'],
            'Civil Engineering': ['CE', 'CIVL'],
            'Business Administration': ['BUS', 'MGMT', 'ADMIN'],
            'Economics': ['ECON', 'ECN'],
            'Psychology': ['PSY', 'PSYC'],
            'Sociology': ['SOC', 'SOCL'],
            'English Literature': ['ENG', 'ENGL', 'LIT'],
            'History': ['HIST', 'HIS'],
            'Philosophy': ['PHIL', 'PHI'],
            'Art & Design': ['ART', 'ARTS', 'DSGN'],
            'Music': ['MUS', 'MUSC'],
            'Theater Arts': ['THEA', 'DRMA'],
            'Political Science': ['POLS', 'GOVT'],
            'Environmental Science': ['ENV', 'ENVS']
        }

        # Create courses
        courses = []
        used_course_codes = set()
        
        for department in departments:
            prefix = random.choice(course_prefixes.get(department.name, ['GEN']))
            for i in range(options['courses_per_department']):
                # Generate unique course code
                max_attempts = 100
                for attempt in range(max_attempts):
                    course_number = random.randint(100, 499)
                    course_code = f"{prefix}{course_number}"
                    if course_code not in used_course_codes:
                        used_course_codes.add(course_code)
                        break
                else:
                    # Fallback: use sequential numbering
                    course_code = f"{prefix}{100 + len(used_course_codes)}"
                    used_course_codes.add(course_code)
                
                course = Course.objects.create(
                    name=fake.catch_phrase(),
                    code=course_code,
                    description=fake.text(max_nb_chars=300),
                    department=department
                )
                courses.append(course)
                self.stdout.write(f'Created course: {course.code} - {course.name}')

        # Create students
        students = []
        used_student_ids = set()
        
        for i in range(options['students']):
            # Generate unique student ID
            while True:
                dept_code = random.choice(departments).name[:3].upper()
                year = random.choice([2021, 2022, 2023, 2024])
                number = random.randint(1, 999)
                student_id = f"{dept_code}{year}{number:03d}"
                if student_id not in used_student_ids:
                    used_student_ids.add(student_id)
                    break
            
            student = Student.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                student_id=student_id,
                email=fake.email(),
                contact_number=fake.phone_number(),
                department=random.choice(departments)
            )
            students.append(student)
            self.stdout.write(f'Created student: {student.student_id} - {student.first_name} {student.last_name}')

        # Create enrollments
        enrollment_count = 0
        statuses = ['enrolled', 'completed', 'dropped', 'withdrawn']
        status_weights = [0.6, 0.25, 0.1, 0.05]  # More enrolled students
        grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        grade_weights = [0.05, 0.15, 0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05, 0.03, 0.01, 0.01]

        for student in students:
            # Each student enrolls in random number of courses
            num_enrollments = random.randint(1, options['max_enrollments_per_student'])
            
            # Prefer courses from student's department and related departments
            dept_courses = [c for c in courses if c.department == student.department]
            other_courses = [c for c in courses if c.department != student.department]
            
            # 70% chance to pick from own department, 30% from others
            available_courses = []
            for _ in range(num_enrollments * 2):  # Get more than needed to have options
                if random.random() < 0.7 and dept_courses:
                    available_courses.append(random.choice(dept_courses))
                elif other_courses:
                    available_courses.append(random.choice(other_courses))
            
            # Remove duplicates and limit to requested number
            selected_courses = list(set(available_courses))[:num_enrollments]
            
            for course in selected_courses:
                # Check if enrollment already exists
                if not Enrollment.objects.filter(student=student, course=course).exists():
                    status = random.choices(statuses, weights=status_weights)[0]
                    grade = None
                    notes = fake.sentence() if random.random() < 0.3 else ""  # 30% chance of notes
                    
                    if status == 'completed':
                        grade = random.choices(grades, weights=grade_weights)[0]
                    
                    enrollment = Enrollment.objects.create(
                        student=student,
                        course=course,
                        status=status,
                        grade=grade,
                        notes=notes
                    )
                    enrollment_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {enrollment_count} enrollments for {len(students)} students in {len(courses)} courses'
            )
        )

        # Print detailed summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('ENROLLMENT SYSTEM DATA SUMMARY'))
        self.stdout.write('='*50)
        self.stdout.write(f'📚 Colleges: {College.objects.count()}')
        self.stdout.write(f'🏢 Departments: {Department.objects.count()}')
        self.stdout.write(f'📖 Courses: {Course.objects.count()}')
        self.stdout.write(f'👨‍🎓 Students: {Student.objects.count()}')
        self.stdout.write(f'📝 Total Enrollments: {Enrollment.objects.count()}')
        
        self.stdout.write('\n📊 Enrollment Status Breakdown:')
        for status, _ in Enrollment.ENROLLMENT_STATUS_CHOICES:
            count = Enrollment.objects.filter(status=status).count()
            percentage = (count / Enrollment.objects.count() * 100) if Enrollment.objects.count() > 0 else 0
            self.stdout.write(f'  {status.capitalize()}: {count} ({percentage:.1f}%)')
        
        completed_with_grades = Enrollment.objects.filter(status='completed').exclude(grade__isnull=True).count()
        self.stdout.write(f'\n🎓 Completed courses with grades: {completed_with_grades}')
        
        self.stdout.write('\n✅ Sample data population completed successfully!')
        self.stdout.write('You can now test the enrollment system with realistic data.')

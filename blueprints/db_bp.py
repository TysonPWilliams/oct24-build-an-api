from flask import Blueprint
from init import db
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables Created')

@db_bp.cli.command('seed')
def seed_tables():
    teachers = [
        Teacher(
            name = 'Stephen Hawking',
            department = 'STEM',
            address = 'Brisbane'
        ),
        Teacher(
            name = 'Mary Shelley',
            department = 'English',
            address = 'London'
        )
    ]

    db.session.add_all(teachers)
    db.session.commit()

    students = [
        Student(
            name ='Mary Jones',
            email='mary.jones@gmail.com',
            address='Sydney'
        ),
        Student(
            name='John Smith',
            email='john.smith@gmail.com'
        )
    ]

    db.session.add_all(students)
    db.session.commit()

    courses = [
        Course(
            name = "Diploma of Web Development",
            duration = "12 Months",
            teacher_id = 1
        ),
        Course(
            name = "Bachelor of Arts",
            duration = "36 Months",
            teacher_id = 2
        )
        
    ]
    
    db.session.add_all(courses)
    db.session.commit()

    enrolments = [
        Enrolment(
            student_id=1,
            course_id=1,
            date_enrolment="2025-01-15"
        ),
        Enrolment(
            student_id=2,
            course_id=1,
            date_enrolment="2025-10-24"
        )
    ]
    
    db.session.add_all(enrolments)
    db.session.commit()
    print('Tables seeded')


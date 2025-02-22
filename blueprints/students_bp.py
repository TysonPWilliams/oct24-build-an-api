from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.student import Student, many_students, one_student, StudentSchema, student_without_id
import re

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student).order_by(Student.name)
    students = db.session.scalars(stmt)
    return many_students.dump(students)

# Read one - GET /students/<int:student_id>
@students_bp.route('/students/<int:student_id>')
def get_one_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        return one_student.dump(student)
    else:
        return {"error": f"Student with id {student_id} not found!"}, 404
    
# Create - POST /students
@students_bp.route('/students', methods=['POST'])
def create_student():
    try:
        # Parse the incoming JSON body
        data = student_without_id.load(request.json) #Tried to use one_student as defined in student.py, had to import StudentSchema and then run

        # Create a new instance
        new_student = Student(
            name = data.get('name'),
            email = data.get('email'),
            address = data.get('address')
        )
        # Add to the DB session
        db.session.add(new_student)
        # Commit to the DB
        db.session.commit()
        # Return the new product
        return one_student.dump(new_student), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: #unique violation
            return {"error": "Email address already in use"}, 409
        # elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        #     # return {"error": "Field is required"}, 400
        #     db.session.rollback()  # Rollback the transaction to prevent corruption
        #     error_message = str(err.orig)  # Extract the original error message
        #     return {f"Integrity Error": f"{error_message}"}
        else:
            # return {"error": err._message.orig.diag.message_detail}, 400
            db.session.rollback()  # Rollback the transaction to prevent corruption
            error_message = str(err.orig)  # Extract the original error message
            return {f"Error": f"{error_message}"}
    
# Update - PUT /students/<int:id>
@students_bp.route('/students/<int:student_id>', methods=['PUT', 'PATCH'])
def update_student(student_id):
    try:
        # Get the requested student from the db
        stmt = db.select(Student).filter_by(id=student_id)
        student = db.session.scalar(stmt)

        if student:
            # Load and parse the incoming JSON body
            data = student_without_id.load(request.json)
            # Update the attributes of the student with the incoming data using "short circuit boolean"
            student.name = data.get('name') or student.name
            student.email = data.get('email') or student.email
            student.address = data.get('address', student.address)

         # Commit changes
            db.session.commit()  
            # Return the updated student
            return one_student.dump(student), 200
        else:
            return {"error": f"Student with id {student_id} not found"}, 404  
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409 # Conflict

# Delete - DELETE /students/<int:id>
@students_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {}, 204
    else:
        return {"error": f"Student with id {student_id} not found"}, 404



# Possible extra routes:
# Enrol - POST /students/<int:student_id>/<int:course_id>
# Unenrol - DELETE /students/<int:student_id>/<int:course_id>
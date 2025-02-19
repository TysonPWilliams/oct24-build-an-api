from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.student import Student, many_students, one_student, StudentSchema

students_bp = Blueprint('students', __name__)

# Read all - GET /students
@students_bp.route('/students')
def get_all_students():
    stmt = db.select(Student)
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
        data = StudentSchema(exclude=['id']).load(request.json) #Tried to use one_student as defined in student.py, had to import StudentSchema and then run

        # Create a new instance
        new_student = Student(
            name = data['name'],
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
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": "Field is required"}, 400
        else:
            return {"error": err}, 400
    
    

# Update - PUT /students/<int:id>
@students_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # Load and parse the incoming JSON body
    data = StudentSchema(exclude=['id']).load(request.json)
    # Get the requested student from the db
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)

    if student:
        student.name = data['name'],
        student.email = data['email'],
        student.address = data.get('address')
        # Commit changes
        db.session.commit()  
        # Return the updated student
        return StudentSchema().dump(student), 200
    else:
        return {"error": f"Student with id {student_id} not found"}, 404  

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
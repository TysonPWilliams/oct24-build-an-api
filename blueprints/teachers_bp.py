from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.teacher import Teacher, many_teachers, one_teacher, TeacherSchema, teacher_without_id
import re

teachers_bp = Blueprint('teachers', __name__)

# Read all - GET /teachers
@teachers_bp.route('/teachers')
def get_all_teachers():
    stmt = db.select(Teacher).order_by(Teacher.name)
    teachers = db.session.scalars(stmt)
    return many_teachers.dump(teachers)

# Read one - GET /teachers/<int:teacher_id>
@teachers_bp.route('/teachers/<int:teacher_id>')
def get_one_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return one_teacher.dump(teacher)
    else:
        return {"error": f"Teacher with id {teacher_id} not found!"}, 404
    
# Create - POST /teachers
@teachers_bp.route('/teachers', methods=['POST'])
def create_teacher():
    try:
        # Parse the incoming JSON body
        data = teacher_without_id.load(request.json) #Tried to use one_teacher as defined in teacher.py, had to import TeacherSchema and then run

        # Create a new instance
        new_teacher = Teacher(
            name = data.get('name'),
            department = data.get('department'),
            address = data.get('address')
        )
        # Add to the DB session
        db.session.add(new_teacher)
        # Commit to the DB
        db.session.commit()
        # Return the new product
        return one_teacher.dump(new_teacher), 201
    
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
            return {"Error": f"{error_message}"}
    
# Update - PUT /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['PUT', 'PATCH'])
def update_teacher(teacher_id):
    try:
        # Get the requested teacher from the db
        stmt = db.select(Teacher).filter_by(id=teacher_id)
        teacher = db.session.scalar(stmt)

        if teacher:
            # Load and parse the incoming JSON body
            data = teacher_without_id.load(request.json)
            # Update the attributes of the teacher with the incoming data using "short circuit boolean"
            teacher.name = data.get('name') or teacher.name
            teacher.department = data.get('department') or teacher.department
            teacher.address = data.get('address', teacher.address)

         # Commit changes
            db.session.commit()  
            # Return the updated teacher
            return one_teacher.dump(teacher), 200
        else:
            return {"error": f"Teacher with id {teacher_id} not found"}, 404  
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409 # Conflict

# Delete - DELETE /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204
    else:
        return {"error": f"Teacher with id {teacher_id} not found"}, 404



# Possible extra routes:
# Enrol - POST /teachers/<int:teacher_id>/<int:course_id>
# Unenrol - DELETE /teachers/<int:teacher_id>/<int:course_id>
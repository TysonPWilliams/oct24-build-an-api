from flask import Blueprint, request
from init import db
from models.teacher import Teacher, many_teachers, one_teacher, TeacherSchema, teacher_without_id

teachers_bp = Blueprint('teachers', __name__)

# Read all - GET /teachers
@teachers_bp.route('/teachers')
def get_all_teachers():
    stmt = db.select(Teacher)
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
    # Parse the incoming JSON body
    data = teacher_without_id.load(request.json) 

    # Create a new instance
    new_teacher = Teacher(
        name = data['name'],
        department = data['department'],
        address = data.get('address')
    )
    # Add to the DB session
    db.session.add(new_teacher)
    # Commit to the DB
    db.session.commit()
    # Return the new product
    return one_teacher.dump(new_teacher), 201

# Update - PUT /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    # Load and parse the incoming JSON body
    data = teacher_without_id.load(request.json)
    # Get the requested teacher from the db
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)

    if teacher:
        teacher.name = data['name'],
        teacher.department = data['department'],
        teacher.address = data.get('address')
        # Commit changes
        db.session.commit()  
        # Return the updated teacher
        return one_teacher().dump(teacher), 200
    else:
        return {"error": f"Teacher with id {teacher_id} not found"}, 404  

# Delete - DELETE /teachers/<int:id>
@teachers_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    # Create a statement and filter for teacher id
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    # Create a teacher instance and scalar the statement
    teacher = db.session.scalar(stmt)
    # If teacher exists, delete the teacher and return nothing
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204
    else:
        return {"error" : f"Teacher with id {teacher_id} not found"}, 404
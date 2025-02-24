from flask import Blueprint, request
from init import db
from models.course import Course, many_courses, one_course, course_without_id

courses_bp = Blueprint('courses', __name__)

# Read all - GET /courses
@courses_bp.route('/courses')
def get_all_courses():
    stmt = db.select(Course).order_by(Course.name)
    courses = db.session.scalars(stmt)
    return many_courses.dump(courses)

# Read one - GET /courses/<int:course_id>
@courses_bp.route('/courses/<int:course_id>')
def get_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        return one_course.dump(course)
    else:
        return {"error": f"Course with id {course_id} not found"}, 404

# Create one - POST /courses
@courses_bp.route('/courses', methods=['POST'])
def create_course():
    try:
        #  Parse incoming JSON body
        data = course_without_id.load(request.json)

        # Create a new instance
        new_course = Course(
            name = data.get('name'),
            start_date = data.get('start_date'),
            end_date = data.get('end_date'),
            teacher_id = data.get('teacher_id')
        )

        db.session.add(new_course)
        db.session.commit()
        return one_course.dump(new_course), 201
    
    except Exception as err:
        return {f"Error": str(err.orig)}, 400

# Delete one - DELETE /courses/<int:id>
@courses_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    stmt = db.Select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)

    if course:
        db.session.delete(course)
        db.session.commit()
        return {}, 204
    else:
        return {"error": f"Course with with id {course_id} not found"}, 404

# Update one - PUT /courses/<int:course_id>
@courses_bp.route('/courses/<int:course_id>', methods=['PUT', 'PATCH'])
def update_course(course_id):
    try:
        stmt = db.Select(Course).filter_by(id=course_id)
        course = db.session.scalar(stmt)

        if course:
            data = course_without_id.load(request.json)

            course.name = data.get('name') or course.name
            course.start_date = data.get('start_date') or course.start_date
            course.end_date = data.get('end_date') or course.end_date
            course.teacher_id = data.get('teacher_id') or course.teacher_id

            db.session.commit()
            return one_course.dump(course), 200
        
        else:
            return {"error", f"Course with id {course_id} not found"}, 404
    except Exception as err:
        db.session.rollback()
        return {"error": str(err.orig)}
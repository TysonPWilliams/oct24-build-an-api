from flask import Blueprint, request
from init import db
from models.course import Course, many_courses, one_course, CourseSchema

courses_bp = Blueprint('courses', __name__)

# Read all - GET /courses
@courses_bp.route('/courses')
def get_all_courses():
    stmt = db.select(Course)
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
    # Parse incoming JSON body
    data = CourseSchema(exclude=['id']).load(request.json)

    # Create a new instance
    new_course = Course(
        name = data['name'],
        duration = data['duration'],
        teacher_id = data['teacher_id']
    )

    db.session.add(new_course)
    db.session.commit()
    return one_course.dump(new_course), 201

# Delete one - DELETE /courses/<int:id>
# Update one - PUT /courses/<int:id>
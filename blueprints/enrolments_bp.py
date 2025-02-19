from flask import Blueprint, request
from init import db
from models.enrolment import Enrolment, many_enrolments, one_enrolment, EnrolmentSchema

enrolments_bp = Blueprint('enrolments', __name__)

# Read all - GET /enrolments
@enrolments_bp.route('/enrolments')
def get_enrolments():
    stmt = db.Select(Enrolment)
    enrolments = db.session.scalars(stmt)
    return many_enrolments.dump(enrolments)

# Read one - GET /enrolments/<int:enrolment_id>
@enrolments_bp.route('/enrolments/<int:enrolment_id>')
def get_one_enrolment(enrolment_id):
    stmt = db.Select(Enrolment).filter_by(id=enrolment_id)
    enrolment = db.session.scalar(stmt)
    if enrolment:
        return one_enrolment.dump(enrolment)
    else:
        return {"error": f"Enrolment with enrolment ID {enrolment_id} not found"}, 404

# Create one - POST /enrolments
@enrolments_bp.route('/enrolments', methods=['POST'])
def create_enrolment():
    data = EnrolmentSchema(exclude=['id']).load(request.json)

    new_enrolment = Enrolment(
        student_id = data.get('student_id'),
        course_id = data.get('course_id'),
        date_enrolment = data.get('date_enrolment')
    )
    db.session.add(new_enrolment)
    db.session.commit()
    return one_enrolment.dump(new_enrolment), 201

# Delete one - DELETE /enrolments/<int:enrolment_id>

# Update one - PUT /enrolments/<int:enrolment_id>
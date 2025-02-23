from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.enrolment import Enrolment, many_enrolments, one_enrolment, enrolment_without_id

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
    data = enrolment_without_id.load(request.json)

    new_enrolment = Enrolment(
        student_id = data.get('student_id'),
        course_id = data.get('course_id'),
        date_enrolment = data.get('date_enrolment')
    )
    db.session.add(new_enrolment)
    db.session.commit()
    return one_enrolment.dump(new_enrolment), 201

# Delete one - DELETE /enrolments/<int:enrolment_id>
@enrolments_bp.route('/enrolments/<int:enrolment_id>', methods=['DELETE'])
def delete_enrolment(enrolment_id):
    stmt = db.Select(Enrolment).filter_by(id=enrolment_id)
    enrolment = db.session.scalar(stmt)

    if enrolment:
        db.session.delete(enrolment)
        db.session.commit()
        return {}, 204
    else:
        return {"error": f"Enrolment with id {enrolment_id} not found"}, 404

# Update one - PUT /enrolments/<int:enrolment_id>
@enrolments_bp.route('/enrolments/<int:enrolment_id>', methods=['PUT', 'PATCH'])
def update_enrolment(enrolment_id):
    try:
        stmt = db.Select(Enrolment).filter_by(id=enrolment_id)
        enrolment = db.session.scalar(stmt)

        if enrolment:
            data = enrolment_without_id.load(request.json)

            enrolment.student_id = data.get('student_id') or enrolment.student_id
            enrolment.course_id = data.get('course_id') or enrolment.course_id
            enrolment.date_enrolment = data.get('date_enrolment') or enrolment.date_enrolment
            
            db.session.commit()
            return one_enrolment.dump(enrolment)
        else:
            return {"error": f"Enrolment with id {enrolment_id} not found"}, 404
        
    except IntegrityError as err:
        db.session.rollback()
        error_message = str(err.orig)
        return {"error": f"{error_message}"}

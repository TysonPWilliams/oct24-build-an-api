from init import db, ma
from marshmallow_sqlalchemy import fields
from models.student import Student


class Enrolment(db.Model):
    __tablename__ = 'enrolments'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete='cascade'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete='cascade'), nullable=False)
    date_enrolment = db.Column(db.Date)

    student = db.relationship('Student', back_populates='enrolments')
    course = db.relationship('Course', back_populates='enrolments')

Student.enrolments = db.relationship('Enrolment', back_populates='student')


class EnrolmentSchema(ma.Schema):
    student = fields.Nested('StudentSchema', exclude=['id'])
    course = fields.Nested('CourseSchema', exclude=['id'])

    class Meta:
        fields = ('id', 'student_id', 'course_id', 'date_enrolment', 'student', 'course')

one_enrolment = EnrolmentSchema()
many_enrolments = EnrolmentSchema(many=True)
enrolment_without_id = EnrolmentSchema(exclude=['id'])

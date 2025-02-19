from init import db, ma

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(200), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete='cascade'), nullable=False)

    enrolments = db.relationship('Enrolment', back_populates='course')

class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'duration', 'teacher_id')


one_course = CourseSchema()
many_courses = CourseSchema(many=True)
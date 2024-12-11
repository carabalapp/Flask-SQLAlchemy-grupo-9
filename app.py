import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@database-1-instance-1.c1ysiwq8g2mz.us-east-2.rds.amazonaws.com:5432/AWSGrupo9')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref='student_course', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'major': self.major,
            'course_id': self.course_id,
            'course': self.course.to_dict()
        }

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', backref='courses', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
# Crear tabla
with app.app_context():
    db.create_all()

    # Verificar la conexion a la base de datos
    try:
        db.session.execute(text('SELECT 1'))
        print('Conexion exitosa a la base de datos')
    except Exception as e:
        print(f'Error al conectar a la base de datos: {str(e)}')
        
@app.route('/estudiantes', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(name=data['name'], age=data['age'], major=data['major'], course_id=data['course_id'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({
        'message': 'Estudiante creado exitosamente',
        'data': new_student.to_dict()
    })
    
@app.route('/estudiantes', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify({
        'data': [student.to_dict() for student in students]
    })
    
@app.route('/estudiantes/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    # student = Student.query.get_or_404(student_id)
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({
            'message': 'Estudiante no encontrado'
        }), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({
        'message': 'Estudiante eliminado exitosamente'
    })

@app.route('/estudiantes/<int:student_id>', methods=['PATCH'])
def update_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({
            'message': 'Estudiante no encontrado'
        }), 404
    student.name = data['name']
    student.age = data['age']
    student.major = data['major']
    student.course_id = data['course_id']
    db.session.commit()
    return jsonify({
        'message': 'Estudiante actualizado exitosamente',
        'data': student.to_dict()
    })
    
@app.route('/cursos', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify({
        'data': [course.to_dict() for course in courses]
    })
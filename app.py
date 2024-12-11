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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'major': self.major
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
    new_student = Student(name=data['name'], age=data['age'], major=data['major'])
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
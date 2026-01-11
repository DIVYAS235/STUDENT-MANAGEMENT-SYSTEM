import json
import os

class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        """Converts object data to a dictionary for JSON saving."""
        return {"id": self.student_id, "name": self.name, "grade": self.grade}

class ManagementSystem:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return [Student(**data) for data in json.load(f)]
        return []

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def add_student(self, student_id, name, grade):
        new_student = Student(student_id, name, grade)
        self.students.append(new_student)
        self.save_data()

    def remove_student(self, student_id):
        self.students = [s for s in self.students if s.student_id != student_id]
        self.save_data()

    def get_all(self):
        return [s.to_dict() for s in self.students]

# --- Flask Integration ---
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
system = ManagementSystem()

@app.route('/')
def index():
    return render_template('students.html')

@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'POST':
        data = request.json
        system.add_student(data['id'], data['name'], data['grade'])
        return jsonify({"status": "success"})
    return jsonify(system.get_all())

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    system.remove_student(student_id)
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
import urllib.parse

app = Flask(__name__)



username = urllib.parse.quote_plus("susantkumarsks96")
password = urllib.parse.quote_plus("Susant@123456")  # This encodes '@'

mongo_uri = f"mongodb+srv://{username}:{password}@student01.6laap.mongodb.net/?retryWrites=true&w=majority&appName=student01"


client = MongoClient("mongo_uri")


# Database Setup
db = client["college"]
collection = db["students"]



# Home Route - Display Students (GET Method)
@app.route('/', methods=['GET'])
def index():
    students = list(collection.find())
    for student in students:
        student['_id'] = str(student['_id'])  # Convert ObjectId to string
    return render_template('index.html', students=students)


# API Route to Get All Students (GET Method)
@app.route('/api/students', methods=['GET'])
def get_students():
    students = list(collection.find())
    for student in students:
        student['_id'] = str(student['_id'])
    return jsonify(students)


# Add Student Route (POST Method)
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_number = request.form['roll_number']
    department = request.form['department']
    email = request.form['email']


    student = {"name": name, "roll_number": roll_number, "department": department, "email": email}
    collection.insert_one(student)
    return redirect(url_for('index'))


# API Route to Add Student (POST Method)
@app.route('/api/students', methods=['POST'])
def api_add_student():
    data = request.get_json()
    student = {"name": data['name'], "roll_number": data['roll_number'], "department": data['department'], "email": data['email']}
    result = collection.insert_one(student)
    return jsonify({"_id": str(result.inserted_id), "message": "Student added successfully"}), 201


# Delete Student Route (GET Method)
@app.route('/delete/<string:id>', methods=['GET'])
def delete_student(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# API Route to Delete Student (DELETE Method)
@app.route('/api/students/<string:id>', methods=['DELETE'])
def api_delete_student(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully"})
    else:
        return jsonify({"error": "Student not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)





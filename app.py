from flask import Flask, request, jsonify
import os

app = Flask(__name__)

courses = [
    {'id': 1, 'name': 'Python Programming', 'details': 'Learn Python from scratch.', 'enrolled_students': []},
    {'id': 2, 'name': 'Data Science', 'details': 'Learn how to process and visualize data.', 'enrolled_students': []},
    {'id': 3, 'name': 'Web Development', 'details': 'Learn to build websites with HTML, CSS, JavaScript, and Flask.', 'enrolled_students': []}
]

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify({'courses': courses}), 200

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    course = next((course for course in courses if course['id'] == course_id), None)
    if course:
        return jsonify(course), 200
    else:
        return jsonify({'message': 'Course not found'}), 404

@app.route('/courses/enroll', methods=['POST'])
def enroll_in_course():
    if not request.json or not 'course_id' in request.json or not 'student_name' in request.json:
        return jsonify({'message': 'Invalid request'}), 400
    course_id = request.json['course_id']
    student_name = request.json['student_name']
    course = next((course for course in courses if course['id'] == course_id), None)

    if course:
        if student_name not in course['enrolled_students']:
            course['enrolled_students'].append(student_name)
            return jsonify({'message': f"{student_name} successfully enrolled in {course['name']}"}), 200
        else:
            return jsonify({'message': 'Student already enrolled in this course'}), 409
    else:
        return jsonify({'message': 'Course not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
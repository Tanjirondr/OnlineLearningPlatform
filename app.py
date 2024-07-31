from flask import Flask, request, jsonify
import os

app = Flask(__name__)

ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

courses = [
    {'id': 1, 'name': 'Python Programming', 'details': 'Learn Python from scratch.', 'enrolled_students': []},
    {'id': 2, 'name': 'Data Science', 'details': 'Learn how to process and visualize data.', 'enrolled_students': []},
    {'id': 3, 'name': 'Web Development', 'details': 'Learn to build websites with HTML, CSS, JavaScript, and Flask.', 'enrolled_students': []}
]

def authenticate(username, password):
    """Simple authentication function."""
    return username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']

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

@app.route('/courses/create', methods=['POST'])
def create_course():
    auth = request.authorization
    if not auth or not authenticate(auth.username, auth.password):
        return jsonify({'message': 'Authentication required'}), 401

    request_data = request.json
    if not request_data or 'name' not in request_data or 'details' not in request_data:
        return jsonify({'message': 'Invalid request'}), 400

    new_course = {
        'id': courses[-1]['id'] + 1 if courses else 1,
        'name': request_data['name'],
        'details': request_data['details'],
        'enrolled_students': []
    }
    courses.append(new_course)
    return jsonify(new_course), 201

if __name__ == '__main__':
    app.run(debug=True)
import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv('API_BASE_URL')
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {getenv('API_KEY')}"
}

def create_course(course_data):
    response = requests.post(f"{BASE_URL}/courses", json=course_data, headers=HEADERS)
    return response.json()

def get_course(course_id):
    response = requests.get(f"{BASE_URL}/courses/{course_id}", headers=HEADERS)
    return response.json()

def update_course(course_id, update_data):
    response = requests.put(f"{BASE_URL}/courses/{course_id}", json=update_data, headers=HEADERS)
    return response.json()

def delete_course(course_id):
    response = requests.delete(f"{BASE_URL}/courses/{course_id}", headers=HEADERS)
    return response.status_code

def register_user(user_data):
    response = requests.post(f"{BASE_URL}/users/register", json=user_data, headers=HEADERS)
    return response.json()

def login_user(credentials):
    response = requests.post(f"{BASE_URL}/users/login", json=credentials, headers=HEADERS)
    return response.json()

def enroll_user(course_id, user_id):
    enrollment_data = {'user_id': user_id, 'course_id': course_id}
    response = requests.post(f"{BASE_URL}/enrollments", json=enrollment_data, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }
    course_data = {
        "title": "Introduction to Python",
        "description": "A course for beginners."
    }
    credentials = {
        "email": "john.doe@example.com",
        "password": "password123"
    }

    print(register_user(user_data))
    user_response = login_user(credentials)
    print(user_response)

    course_response = create_course(course_data)
    print(course_response)
    course_id = course_response.get('id')
    print(get_course(course_id))
    print(update_course(course_id, {"title": "Python for All"}))
    print(delete_course(course_id))
    
    user_id = user_response.get('user', {}).get('id')
    print(enroll_user(course_id, user_id))
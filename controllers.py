import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = getenv('API_BASE_URL')
API_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {getenv('API_KEY')}"
}

def create_new_course(course_details):
    response = requests.post(f"{API_BASE_URL}/courses", json=course_details, headers=API_HEADERS)
    return response.json()

def retrieve_course_details(course_identifier):
    response = requests.get(f"{API_BASE_URL}/courses/{course_identifier}", headers=API_HEADERS)
    return response.json()

def modify_course_details(course_identifier, new_details):
    response = requests.put(f"{API_BASE_URL}/courses/{course_identifier}", json=new_details, headers=API_HEADERS)
    return response.json()

def remove_course(course_identifier):
    response = requests.delete(f"{API_BASE_URL}/courses/{course_identifier}", headers=API_HEADERS)
    return response.status_code

def register_new_user(user_details):
    response = requests.post(f"{API_BASE_URL}/users/register", json=user_details, headers=API_HEADERS)
    return response.json()

def authenticate_user(login_credentials):
    response = requests.post(f"{API_BASE_URL}/users/login", json=login_credentials, headers=API_HEADERS)
    return response.json()

def enroll_user_in_course(course_identifier, user_identifier):
    enrollment_details = {'user_id': user_identifier, 'course_id': course_identifier}
    response = requests.post(f"{API_BASE_URL}/enrollments", json=enrollment_details, headers=API_HEADERS)
    return response.json()

if __name__ == "__main__":
    user_details = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }
    course_details = {
        "title": "Introduction to Python",
        "description": "A course for beginners."
    }
    login_credentials = {
        "email": "john.doe@example.com",
        "password": "password123"
    }

    print(register_new_user(user_details))
    user_login_response = authenticate_user(login_credentials)
    print(user_login_response)

    course_creation_response = create_new_course(course_details)
    print(course_creation_response)
    created_course_id = course_creation_response.get('id')
    print(retrieve_course_details(created_course_id))
    print(modify_course_details(created_course_id, {"title": "Python for All"}))
    print(remove_course(created_course_id))
    
    logged_user_id = user_login_response.get('user', {}).get('id')
    print(enroll_user_in_course(created_course_id, logged_user_id))
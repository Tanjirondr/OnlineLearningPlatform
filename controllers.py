import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = getenv('API_BASE_URL')
API_KEY = getenv('API_KEY')

def get_headers():
    return {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {API_KEY}"
    }

def send_request(method, endpoint, payload=None):
    url = f"{API_BASE_URL}/{endpoint}"
    headers = get_headers()

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=payload, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=payload, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError("Unsupported HTTP method")

    return response

def create_new_course(course_details):
    response = send_request("POST", "courses", course_details)
    return response.json()

def retrieve_course_details(course_identifier):
    response = send_request("GET", f"courses/{course_identifier}")
    return response.json()

def modify_course_details(course_identifier, new_details):
    response = send_request("PUT", f"courses/{course_identifier}", new_details)
    return response.json()

def remove_course(course_identifier):
    response = send_request("DELETE", f"courses/{course_identifier}")
    return response.status_code

def register_new_user(user_details):
    response = send_request("POST", "users/register", user_details)
    return response.json()

def authenticate_user(login_credentials):
    response = send_request("POST", "users/login", login_credentials)
    return response.json()

def enroll_user_in_course(course_identifier, user_identifier):
    enrollment_details = {'user_id': user_identifier, 'course_id': course_identifier}
    response = send_request("POST", "enrollments", enrollment_details)
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
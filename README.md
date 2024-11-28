 # Join API

Join API is a Django RESTful API designed to manage tasks, contacts, categories, and subtasks. The application supports user authentication and provides endpoints for creating, updating, and managing tasks and related entities. This API is intended to be the backend of a task management application.


## Features
- User registration and authentication
- Task management (CRUD operations)
- Contact management (CRUD operations)
- Category and subtask management
- API endpoints secured with token-based authentication
- Detailed error handling and validation


## Getting Started

### Prerequisites
- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL (or another database of your choice)


## API Documentation

### User Endpoints
- `POST /api/signup/`: Register a new user.
- `POST /api/login/`: Authenticate a user and return a token.

### Task Endpoints
- `GET /api/tasks/`: Retrieve a list of tasks.
- `POST /api/tasks/`: Create a new task.
- `GET /api/tasks/{id}/`: Retrieve a specific task by ID.
- `PUT /api/tasks/{id}/`: Update a task by ID.
- `DELETE /api/tasks/{id}/`: Delete a task by ID.

### Contact Endpoints
- `GET /api/contacts/`: Retrieve a list of contacts.
- `POST /api/contacts/`: Create a new contact.
- `GET /api/contacts/{id}/`: Retrieve a specific contact by ID.
- `PUT /api/contacts/{id}/`: Update a contact by ID.
- `DELETE /api/contacts/{id}/`: Delete a contact by ID.


## The API can be accessed at http://localhost:8000/api/.


## Running Tests

To run the tests, use the following command:

```bash
python manage.py test


## Project Structure

join-api/
├── join_backend/            # Main application folder
│   ├── migrations/          # Database migrations
│   ├── models.py            # Database models
│   ├── serializers.py       # Serializers for API data
│   ├── views.py             # API views
│   ├── urls.py              # URL routing for the API
├── tests/                   # Test cases
├── docs/                    # Sphinx documentation
├── manage.py                # Django management script
└── README.md                # Project README file

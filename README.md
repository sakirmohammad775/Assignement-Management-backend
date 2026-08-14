# Assignment Management System — Backend

Live Link: [https://assignement-management-backend.onrender.com/api/](https://assignement-management-backend.onrender.com/api/)

Swagger Link: [https://assignement-management-backend.onrender.com/swagger](https://assignement-management-backend.onrender.com/swagger)


Django REST API backend for the Assignment Management System.

The backend provides authentication, role-based access control, assignment management, submission management, and database-backed APIs for the frontend application.

---

## 1. Overview

The Assignment Management System is a role-based academic platform designed for:

* **Administrators**
* **Teachers**
* **Students**

The backend is built with **Django** and **Django REST Framework** and uses **PostgreSQL** as the primary database.

The API uses JWT-based authentication to protect authenticated endpoints.

---

## 2. Main Features

### Authentication

* User login
* JWT access and refresh tokens
* Role-based users
* Secure password hashing
* Authenticated API access

### User Roles

The system supports three primary roles:

| Role    | Main Responsibilities                      |
| ------- | ------------------------------------------ |
| ADMIN   | Manage and monitor the entire system       |
| TEACHER | Create and manage assignments              |
| STUDENT | View published assignments and submit work |

### Assignment Management

Teachers can:

* Create assignments
* Update assignments
* Delete assignments
* Save assignments as drafts
* Publish assignments
* Set deadlines
* Set maximum marks
* Assign subjects
* Assign classes

Students can:

* View assignments available for their class
* View published assignments
* View assignment details
* Submit answers

Administrators can access assignment data according to the backend permission rules.

### Submission Management

Students can:

* Submit an assignment
* View their submissions
* Track submission status

Teachers can:

* View student submissions
* Review submitted work
* Grade submissions

The backend validates submission and assignment rules.

---

## 3. Technology Stack

### Backend

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Psycopg

### Development Tools

* Git
* GitHub
* Virtual Environment
* Postman / API client

---

## 4. Project Structure

```text
assignment-management-backend/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── assignments/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── submissions/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 5. Prerequisites

Before running the backend, install:

* Python 3.11+
* PostgreSQL
* Git

Verify Python:

```bash
python --version
```

Verify PostgreSQL:

```bash
psql --version
```

---

## 6. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the backend directory:

```bash
cd assignment-management-backend
```

---

## 7. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 8. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 9. Environment Configuration

Create a `.env` file in the backend root directory.

Use `.env.example` as the template.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_NAME=assignment_management
DATABASE_USER=postgres
DATABASE_PASSWORD=your-postgres-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

ALLOWED_HOSTS=localhost,127.0.0.1

CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Important

Never commit the real `.env` file.

Only commit:

```text
.env.example
```

Do not put real passwords, API keys, database credentials, or Django secret keys in GitHub.

---

## 10. Database Setup

The project uses PostgreSQL.

Create a PostgreSQL database:

```sql
CREATE DATABASE assignment_management;
```

Configure the database credentials in `.env`.

Then apply Django migrations:

```bash
python manage.py migrate
```

Django migrations automatically create the required database tables.

You do **not** need to manually create application tables.

---

## 11. Create Administrator

Create a Django superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts.

Example:

```text
Username: admin
Email: admin@example.com
Password: ********
```

If your custom User model contains a `role` field, make sure the administrator account has:

```text
role = ADMIN
is_staff = True
is_superuser = True
```

You can verify users through the Django shell:

```bash
python manage.py shell
```

Then:

```python
from accounts.models import User

User.objects.all().values(
    "username",
    "email",
    "role",
    "is_superuser"
)
```

---

## 12. Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

## 13. API Authentication

The application uses JWT authentication.

Users first authenticate through the login endpoint.

Example:

```http
POST /auth/login/
```

Request:

```json
{
  "username": "student",
  "password": "password"
}
```

The API returns access and refresh tokens.

The frontend uses the access token for authenticated requests.

Example:

```http
Authorization: Bearer <access_token>
```

---

## 14. Main API Endpoints

### Authentication

```text
POST /auth/login/
```

Login and receive JWT tokens.

---

### Assignments

```text
GET    /assignments/
POST   /assignments/
GET    /assignments/<id>/
PATCH  /assignments/<id>/
DELETE /assignments/<id>/
```

Assignment visibility and modification are controlled by backend authentication and permissions.

---

### Submissions

```text
GET    /submissions/
POST   /submissions/
GET    /submissions/<id>/
PATCH  /submissions/<id>/
```

Submission access is restricted according to the authenticated user's role and ownership.

---

## 15. Role-Based Access Control

Role-based access control is enforced by the backend API.

### Admin

Administrators have system-level access.

Typical capabilities:

* Manage users
* View assignments
* Manage academic data
* View submissions
* Access Django Admin

### Teacher

Teachers can:

* Create assignments
* Update their assignments
* Delete their assignments
* Publish assignments
* View relevant submissions
* Grade student submissions

Teachers should not be able to modify another teacher's assignments unless explicitly permitted by the backend.

### Student

Students can:

* View assignments available to their class
* View published assignments
* Submit assignments
* View their own submissions

Students cannot:

* Create assignments
* Edit assignments
* Delete assignments
* Publish assignments
* Access another student's submission

Frontend restrictions are only for user experience. Security-sensitive permissions are enforced by the backend API.

---

## 16. Assignment Business Rules

The backend implements the following business rules:

1. Teachers can create assignments.
2. Assignments belong to a specific class and subject.
3. Assignments can have `DRAFT` or `PUBLISHED` status.
4. Students should only receive published assignments.
5. Students should only receive assignments applicable to their class.
6. Students can submit answers for available assignments.
7. Assignment ownership is validated for teacher operations.
8. Authentication is required for protected endpoints.

---

## 17. Submission Business Rules

The submission system follows these rules:

1. A student must be authenticated to submit.
2. A submission belongs to a specific assignment.
3. A student cannot submit on behalf of another student.
4. Students should only submit assignments available to them.
5. Assignment and student relationships are validated by the backend.
6. Submission access is restricted according to user role.
7. Teachers can review relevant student submissions.

---

## 18. Database Migrations

Whenever models are changed, create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Check whether migrations are pending:

```bash
python manage.py makemigrations --check
```

For evaluation, the repository includes the Django migration files required to recreate the database schema.

---

## 19. Testing

Run the Django test suite:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test accounts
```

```bash
python manage.py test assignments
```

```bash
python manage.py test submissions
```

Tests should cover important functionality such as:

* Authentication
* Role permissions
* Assignment creation
* Assignment visibility
* Student submissions
* Submission permissions
* Assignment ownership
* Business-rule validation

---

## 20. Backend Validation

Before submitting the project, run:

```bash
python manage.py check
```

Check migrations:

```bash
python manage.py makemigrations --check
```

Run tests:

```bash
python manage.py test
```

All commands should complete successfully before submission.

---

## 21. Demo Accounts

The evaluator should use the following demo accounts.

### Admin

```text
Email: <ADMIN_EMAIL>
Password: <ADMIN_PASSWORD>
```

### Teacher

```text
Email: <TEACHER_EMAIL>
Password: <TEACHER_PASSWORD>
```

### Student

```text
Email: <STUDENT_EMAIL>
Password: <STUDENT_PASSWORD>
```

Use dedicated evaluation credentials rather than personal accounts.

---

## 22. Sample Evaluation Flow

### Admin

```text
Login
  ↓
Access administrative features
  ↓
View/manage system data
```

### Teacher

```text
Login
  ↓
Open Assignments
  ↓
Create Assignment
  ↓
Select Class + Subject
  ↓
Save / Publish
  ↓
View Assignment
  ↓
Review Student Submissions
```

### Student

```text
Login
  ↓
Open Assignments
  ↓
View published assignments for their class
  ↓
Open Assignment
  ↓
Write Answer
  ↓
Submit Assignment
  ↓
View Submission
```

---

## 23. Frontend Integration

The frontend is a Next.js application that communicates with this Django REST API.

For local development, configure the frontend API URL to point to:

```text
http://127.0.0.1:8000
```

Example frontend environment variable:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Start the frontend separately:

```bash
npm install
npm run dev
```

The frontend normally runs at:

```text
http://localhost:3000
```

---

## 24. Production

The backend can be deployed to a production hosting service supporting Django and PostgreSQL.

Production configuration should use:

```env
DEBUG=False
```

and secure production values for:

* `SECRET_KEY`
* Database credentials
* Allowed hosts
* CORS configuration

Never expose production secrets in the repository.

---

## 25. Known Limitations

The current version may have the following limitations depending on the deployed configuration:

* File attachments are not currently part of the core assignment submission workflow.
* Email notifications are not implemented.
* Advanced grading/rubric functionality may be limited.
* Real-time notifications are not implemented.
* Production deployment configuration may differ from local development.

---

## 26. Security Notes

The backend follows these security practices:

* Passwords are handled through Django's authentication system.
* JWT authentication protects API endpoints.
* Role-based permissions are enforced server-side.
* Sensitive environment variables are stored outside the repository.
* `.env` files containing real credentials must not be committed.
* Database credentials must not be hardcoded in source code.

---

## 27. Quick Start

For a fresh local installation:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd assignment-management-backend

python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure `.env`.

Create the PostgreSQL database:

```sql
CREATE DATABASE assignment_management;
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin:

```bash
python manage.py createsuperuser
```

Run tests:

```bash
python manage.py test
```

Start the server:

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

---


---

## License

This project was developed as an academic/technical assessment project.

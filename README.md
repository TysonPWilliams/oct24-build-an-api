# 🎓 LMS API – Learning Management System (Python REST API)

A simple yet functional **Learning Management System (LMS)** API built with **Python** and **Flask**, designed to manage courses, users, and their enrollment status. This project was developed as part of a backend web development learning module.

---

## 🚀 Features

- 📚 **Course Management** – Add, update, delete, and view available courses.
- 👤 **User Profiles** – Register users and manage basic profile information.
- 🔗 **Enrollments** – Enroll users in courses and manage their course lists.
- 🔍 **RESTful Endpoints** – Built using Python's Flask framework and follows REST conventions.
- ✅ **Validation & Error Handling** – Ensures smooth request/response flow with basic error responses.

---

## 🧰 Tech Stack

- **Language:** Python 3.11+
- **Framework:** Flask
- **Data Format:** JSON
- **Storage:** In-memory data structures (ideal for learning/testing)
- **Development Tools:** Postman, VS Code

---

## 📂 Project Structure

```
oct24-build-an-api/
├── app.py                # Main application file
├── models/               # Data models (e.g. User, Course, Enrollment)
├── routes/               # Flask route handlers
├── utils/                # Helper functions and validations
└── README.md             # Project documentation
```

---

## 📡 API Endpoints

### 📚 Courses
| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| GET    | `/courses`           | List all courses          |
| POST   | `/courses`           | Create a new course       |
| GET    | `/courses/<id>`      | Get course details        |
| PUT    | `/courses/<id>`      | Update a course           |
| DELETE | `/courses/<id>`      | Delete a course           |

### 👤 Users
| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| GET    | `/users`             | List all users            |
| POST   | `/users`             | Register a new user       |
| GET    | `/users/<id>`        | Get user details          |

### 📌 Enrollments
| Method | Endpoint                    | Description                          |
|--------|-----------------------------|--------------------------------------|
| POST   | `/enrollments`              | Enroll a user in a course            |
| GET    | `/users/<id>/courses`       | List a user’s enrolled courses       |

---

## 🚀 Getting Started

### 🔧 Prerequisites
- Python 3.11+
- `pip` (Python package manager)

### 📦 Installation

```bash
git clone https://github.com/TysonPWilliams/oct24-build-an-api.git
cd oct24-build-an-api
pip install -r requirements.txt
```

### ▶️ Running the App

```bash
python app.py
```

The API will be live at `http://localhost:5000/`

---

## 🧪 Testing the API

Use [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to test various endpoints:

```bash
curl http://localhost:5000/courses
```

You can also add seed data in `app.py` or build a simple UI or CLI tool to interact with the API.

---

## 🛠️ Future Improvements

- Persistent storage using SQLite or PostgreSQL
- Authentication (JWT or session-based)
- Unit tests with PyTest or unittest
- Swagger/OpenAPI docs for better developer experience

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

Built by [Tyson P Williams](https://github.com/TysonPWilliams) during the October 2024 Backend API module at Coder Academy.

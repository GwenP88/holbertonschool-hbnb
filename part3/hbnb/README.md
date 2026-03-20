![HBnB Banner](assets/banner.png)

# HBnB

HBnB is a RESTful API built with Flask, inspired by AirBnB. It allows users to manage places, reviews, amenities, and authentication through a clean layered architecture using SQLAlchemy and JWT.

This project was built during the first year at [Holberton School](https://www.holbertonschool.com/).

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Database](#database)
  - [Schema](#schema)
  - [Initial Data](#initial-data)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Users](#users)
  - [Amenities](#amenities)
  - [Places](#places)
  - [Reviews](#reviews)
- [Testing](#testing)
  - [CRUD Tests](#crud-tests)
  - [Swagger Tests](#swagger-tests)
- [Authors](#authors)

---

## Features

- User registration and authentication with JWT
- Role-based access control (admin vs regular user)
- Full CRUD for users, places, amenities, and reviews
- Many-to-many relationship between places and amenities
- Password hashing with bcrypt
- Input validation at model level
- SQLite database with SQLAlchemy ORM
- Interactive API documentation via Swagger UI

---

## Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3.x | Main language |
| Flask | Web framework |
| Flask-RESTX | REST API + Swagger UI |
| Flask-JWT-Extended | JWT authentication |
| Flask-SQLAlchemy | ORM |
| Flask-Bcrypt | Password hashing |
| SQLite | Database |

---

## Project Structure

```
part3/hbnb/
├── app/
│   ├── __init__.py               <- Flask app factory
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py           <- Authentication endpoints
│   │       ├── users.py          <- User endpoints
│   │       ├── amenities.py      <- Amenity endpoints
│   │       ├── places.py         <- Place endpoints
│   │       └── reviews.py        <- Review endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── basemodel.py          <- Base model (id, timestamps)
│   │   ├── user.py               <- User model
│   │   ├── place.py              <- Place model
│   │   ├── amenity.py            <- Amenity model
│   │   └── review.py             <- Review model
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── repository.py         <- Repository base classes
│   │   ├── user_repository.py    <- User repository
│   │   ├── place_repository.py   <- Place repository
│   │   ├── amenity_repository.py <- Amenity repository
│   │   └── review_repository.py  <- Review repository
│   └── services/
│       ├── __init__.py           <- Facade instance
│       └── facade.py             <- HBnBFacade (business logic)
├── sql/
│   ├── schema.sql                <- Table creation scripts
│   ├── seed.sql                  <- Initial data (admin + amenities)
│   └── test_crud.sql             <- Raw SQL CRUD tests
├── tests/
│   ├── assets/
│   ├── tests_auth.py             <- Unit tests — Auth
│   ├── tests_users.py            <- Unit tests — Users
│   ├── tests_amenities.py        <- Unit tests — Amenities
│   ├── tests_places.py           <- Unit tests — Places
│   ├── tests_reviews.py          <- Unit tests — Reviews
│   └── tests_swagger.md          <- Swagger manual test documentation
├── instance/
│   └── development.db            <- SQLite database (auto-generated)
├── config.py                     <- App configuration
├── run.py                        <- Application entry point
└── requirements.txt              <- Python dependencies
```

---

## Architecture

HBnB follows a **3-layer architecture**:

```
┌─────────────────────────────────┐
│         API Layer               │
│  Flask-RESTX Namespaces         │
│  auth / users / places /        │
│  amenities / reviews            │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│       Service Layer             │
│       HBnBFacade                │
│  Business logic & validation    │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│     Persistence Layer           │
│  SQLAlchemy Repositories        │
│  UserRepository / PlaceRepo     │
│  ReviewRepo / AmenityRepo       │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│          Database               │
│       SQLite (dev)              │
└─────────────────────────────────┘
```

**Key design pattern — Facade:** all business logic is centralized in `HBnBFacade`. The API layer never accesses the database directly.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/<your-username>/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3/hbnb
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv Python_env
source Python_env/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set environment variables:**
```bash
export SECRET_KEY="your_secret_key_here"
```

### Running the Application

```bash
python3 run.py
```

The application will start at:
```
http://127.0.0.1:5000
```

The Swagger UI is available at:
```
http://127.0.0.1:5000/api/v1/
```

---

## Database

### Schema

The database contains 5 tables:

| Table | Description |
|-------|-------------|
| `users` | Registered users with hashed passwords and admin flag |
| `places` | Places listed by users |
| `amenities` | Available amenities (WiFi, pool, etc.) |
| `place_amenity` | Many-to-many join table between places and amenities |
| `reviews` | User reviews for places (one review per user per place) |

To create the schema manually:
```bash
sqlite3 instance/development.db < sql/schema.sql
```

### Initial Data

The database is pre-populated with:

- 1 administrator account
- 2 users
- 5 default amenities
- 2 places
- 2 reviews

To insert initial data manually:
```bash
sqlite3 instance/development.db < sql/seed.sql
```

**Default admin credentials:**

| Field | Value |
|-------|-------|
| Email | `admin@hbnb.io` |
| Password | `admin1234` |
| is_admin | `True` |

---

## API Documentation

The full interactive documentation is available via Swagger UI at `http://127.0.0.1:5000/api/v1/`.

### Authentication

All protected endpoints require a Bearer JWT token in the `Authorization` header.

To obtain a token:

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Use the token in subsequent requests:
```
Authorization: Bearer <access_token>
```

---

### Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/users/` | No | Create a new user |
| GET | `/api/v1/users/` | No | List all users |
| GET | `/api/v1/users/<id>` | No | Get user by ID |
| PUT | `/api/v1/users/<id>` | Yes (owner/admin) | Update first/last name only |
| PUT | `/api/v1/users/<id>/email` | Yes (owner/admin) | Update email |
| PUT | `/api/v1/users/<id>/password` | Yes (owner/admin) | Update password |
| DELETE | `/api/v1/users/<id>` | Yes (owner/admin) | Delete user account |

**Create user example:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "johndoe@email.com",
  "password": "string123"
}
```

**Validation rules:**
- `first_name` and `last_name`: required, max 50 characters
- `email`: must be unique and valid format (with `@` and domain dot)
- `password`: min 8 characters
- `email` and `password` cannot be modified via `PUT /users/<id>` — use dedicated endpoints
- `is_admin` cannot be set or modified via the API

---

### Amenities

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/amenities/` | Yes (admin only) | Create a new amenity |
| GET | `/api/v1/amenities/` | No | List all amenities |
| GET | `/api/v1/amenities/<id>` | No | Get amenity by ID |
| PUT | `/api/v1/amenities/<id>` | Yes (admin only) | Update amenity |
| DELETE | `/api/v1/amenities/<id>` | Yes (admin only) | Delete amenity |

**Create amenity example (with description):**
```json
{
  "name": "Rooftop Terrace",
  "description": "A spacious rooftop terrace with panoramic city views."
}
```

**Create amenity example (without description):**
```json
{
  "name": "Hot Tub"
}
```

**Validation rules:**
- `name`: required, max 50 characters, stored in lowercase, must be unique
- `description`: optional, max 255 characters

---

### Places

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/places/` | Yes | Create a new place |
| GET | `/api/v1/places/` | No | List all places |
| GET | `/api/v1/places/<id>` | No | Get place by ID (with owner, amenities, reviews) |
| PUT | `/api/v1/places/<id>` | Yes (owner/admin) | Update place |
| DELETE | `/api/v1/places/<id>` | Yes (owner/admin) | Delete place |
| POST | `/api/v1/places/<id>/amenities/<amenity_id>` | Yes (owner/admin) | Add amenity to place |
| DELETE | `/api/v1/places/<id>/amenities/<amenity_id>` | Yes (owner/admin) | Remove amenity from place |
| GET | `/api/v1/places/<id>/reviews` | No | Get all reviews for a place |

**Create place example:**
```json
{
  "title": "Sunny Loft in the City Center",
  "description": "A bright and modern loft in the heart of the city.",
  "price": 95.00,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "amenities": ["c5fcec1a-08f8-40ba-beae-fc5717d8f60e"]
}
```

**Validation rules:**
- `title`: required
- `price`: must be greater than 0
- `latitude`: must be between -90 and 90
- `longitude`: must be between -180 and 180
- `amenities`: list of existing amenity IDs (can be empty)
- Deleting a place also deletes its reviews and amenity links

---

### Reviews

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/reviews/` | Yes | Create a new review |
| GET | `/api/v1/reviews/` | No | List all reviews |
| GET | `/api/v1/reviews/<id>` | No | Get review by ID |
| PUT | `/api/v1/reviews/<id>` | Yes (author/admin) | Update review |
| DELETE | `/api/v1/reviews/<id>` | Yes (author/admin) | Delete review |

**Create review example:**
```json
{
  "comment": "Absolutely loved the loft! The location was unbeatable.",
  "rating": 5,
  "place_id": "ef448d99-36e6-4aa6-880a-59bab9bbe439"
}
```

**Business rules:**
- A user cannot review their own place
- A user can only leave one review per place
- `rating`: must be between 1 and 5

---

## Testing

### Unittest

---

### Swagger Tests

54 manual tests are documented for the Swagger UI, covering all endpoints and edge cases (invalid data, unauthorized actions, duplicate entries, etc.).

See [SWAGGER_TESTS.md](SWAGGER_TESTS.md) for the full test list.

---

## Author

**Gwenaelle PICHOT**  
Student at Holberton School  
Track: Project HBnB
# Holberton School – Full Stack Development Program - HBNB Project

![HBnB Banner](assets/banner.png)

## HBnB – Part 1: UML

### 1. Introduction

HBnB Evolution is a simplified AirBnB-like application designed to manage users, places, reviews, and amenities.

This first phase focuses on producing technical documentation that defines the system architecture, business logic design, and interaction flow between components. The documentation created in this part serves as a blueprint for the implementation phases in the following parts of the project.

---

### 2. Project Scope

The application supports four core domains:

#### User Management
- Users can register, update their profiles, and be deleted.
- Each user has a first name, last name, email, password, and an administrator flag.
- Each user is uniquely identified by an ID.

#### Place Management
- Users can create, update, delete, and list places.
- A place includes a title, description, price, latitude, and longitude.
- Each place is associated with an owner (user).
- Places can have multiple amenities.

#### Review Management
- Users can create, update, delete, and list reviews.
- Each review is linked to a user and a place.
- A review includes a rating and a comment.

#### Amenity Management
- Amenities have a name and description.
- Amenities can be created, updated, deleted, and listed.
- Amenities can be associated with multiple places.

---

### 3. General Requirements

- Every entity must have a unique identifier (ID).
- Creation and update timestamps must be stored for audit purposes.
- The system must respect the defined business rules and entity relationships.

---

### 4. Architecture Overview

The application follows a three-layer architecture:

#### Presentation Layer
Handles API endpoints, request validation, and HTTP responses.

#### Business Logic Layer
Contains domain models and enforces business rules.

#### Persistence Layer
Manages data storage and retrieval from the database (to be implemented in Part 3).

The layers communicate in a structured manner to ensure separation of concerns and maintainability.

---

### 5. Deliverables for Part 1

This part includes:

- A High-Level Package Diagram illustrating the layered architecture.
- A Detailed Class Diagram for the Business Logic layer.
- Sequence Diagrams for key API calls:
  - User registration
  - Place creation
  - Review submission
  - Fetching places
- A consolidated technical documentation file.

---

### 6. Objective of This Documentation

This documentation provides:

- A clear architectural foundation.
- A structured representation of domain entities.
- Defined interaction flows between layers.
- A reference guide for future implementation phases.

The diagrams and explanations included in this part ensure consistency and clarity as the project evolves in Parts 2, 3, and 4.

---

## HBnB – Part 2: Business Logic and API

### Overview

Implementation of the core business logic and exposure of a RESTful API using **Flask** and **Flask-RESTX**. Data is stored in-memory (no database yet). This part establishes the foundational architecture that is carried through Parts 3 and 4.

### Key Elements

- Full CRUD API for `User`, `Place`, `Review`, and `Amenity`
- **Facade pattern** centralizing all business logic
- Input validation and error handling on all endpoints
- Auto-generated Swagger UI documentation at `/api/v1/`

### Architecture

```
API Layer (Flask-RESTX namespaces)
        ↓
HBnBFacade (single entry point for business logic)
        ↓
In-Memory Repositories
        ↓
Domain Models (User, Place, Review, Amenity)
```

### API Endpoints

| Method | Endpoint                      | Description              |
|--------|-------------------------------|--------------------------|
| POST   | `/api/v1/users`               | Create a user            |
| GET    | `/api/v1/users`               | List all users           |
| GET    | `/api/v1/users/<id>`          | Get user by ID           |
| PUT    | `/api/v1/users/<id>`          | Update a user            |
| POST   | `/api/v1/places`              | Create a place           |
| GET    | `/api/v1/places`              | List all places          |
| GET    | `/api/v1/places/<id>`         | Get place details        |
| PUT    | `/api/v1/places/<id>`         | Update a place           |
| POST   | `/api/v1/reviews`             | Create a review          |
| GET    | `/api/v1/reviews/<id>`        | Get review by ID         |
| PUT    | `/api/v1/reviews/<id>`        | Update a review          |
| DELETE | `/api/v1/reviews/<id>`        | Delete a review          |
| POST   | `/api/v1/amenities`           | Create an amenity        |
| GET    | `/api/v1/amenities`           | List all amenities       |
| PUT    | `/api/v1/amenities/<id>`      | Update an amenity        |

---

## HBnB – Part 3: Authentication and Database

### Overview

Extension of Part 2 with **SQLite** database persistence via **SQLAlchemy**, and introduction of **JWT-based authentication** and role-based access control. Passwords are hashed using **bcrypt**.

### Key Elements

- SQLAlchemy ORM models replacing in-memory storage
- Repository pattern for clean data access abstraction
- JWT authentication with `flask-jwt-extended`
- Password hashing with `flask-bcrypt`
- Admin vs. regular user access control via JWT claims
- SQL seed file for reproducible initial data
- Protected endpoints requiring valid token or admin role

### New/Updated Endpoints

| Method | Endpoint                          | Auth Required | Description                  |
|--------|-----------------------------------|---------------|------------------------------|
| POST   | `/api/v1/auth/login`              | No            | Authenticate and get token   |
| GET    | `/api/v1/users/me`                | Yes           | Get current user data        |
| DELETE | `/api/v1/places/<id>`             | Yes (owner)   | Delete a place               |
| DELETE | `/api/v1/reviews/<id>`            | Yes (author)  | Delete a review              |
| POST   | `/api/v1/places/<id>/amenities/<amenity_id>` | Yes (owner) | Add amenity to place |

### Database Models

```
User ──< Place ──< Review
          │
          └──< PlaceAmenity >── Amenity
```

---

## HBnB – Part 4: Simple Web Client

### Overview

Development of a dynamic front-end client connecting to the Part 3 API. Built with **HTML5**, **CSS3**, and **vanilla JavaScript ES6** — no front-end framework. The Flask application also serves the HTML pages via Jinja2 templates.

### Pages

| Route              | Description                                      |
|--------------------|--------------------------------------------------|
| `/`                | List of all places with client-side filters      |
| `/login`           | Login form with JWT authentication               |
| `/places/<id>`     | Detailed view of a place + review submission     |
| `/user`            | Authenticated user's owned places and reviews    |

### Key Features

- JWT token stored in cookie, included in all API requests
- Dynamic place listing loaded from the API
- Three client-side filters: city, maximum price, minimum rating
- Place detail page with owner info, amenities, average rating, and reviews
- Review submission via Bootstrap modal (authenticated users only)
- User account page showing owned places and all reviews received on them
- Navbar adapts based on authentication state (Login ↔ Logout, My Account visibility)

### JavaScript Architecture (`scripts.js`)

Organized into 6 sections:

1. **Initialization** — `DOMContentLoaded`, page detection
2. **Authentication** — `loginUser`, `getCookie`, `getCurrentUser`
3. **Index page** — `fetchPlaces`, `displayPlaces`, `filterPlaces`
4. **User page** — `loadUserPage`, `displayUserPlaces`, `loadUserReviews`
5. **Place details** — `fetchPlaceDetails`, `displayPlaceDetails`
6. **Add review** — `submitReview`

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Git

### Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/GwenP88/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4/hbnb
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv Python_env
source Python_env/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Initialize the database with seed data**

```bash
mkdir -p instance
sqlite3 instance/development.db < sql/seed.sql
```

**5. Start the application**

```bash
python3 run.py
```

- Front-end: `http://localhost:5000`
- API documentation (Swagger): `http://localhost:5000/api/v1/`

---

## Seed Data

| Entity    | Count | Details                                          |
|-----------|-------|--------------------------------------------------|
| Users     | 4     | 1 admin + 3 regular users                        |
| Amenities | 5     | WiFi, Pool, AC, Rooftop Terrace, Private Parking |
| Places    | 6     | 2 in Lyon, 2 in Annecy, 2 in Genève             |
| Reviews   | 12    | 2 per place                                      |

### Test Credentials

| User       | Email                  | Password    |
|------------|------------------------|-------------|
| John Doe   | johndoe@email.com      | `admin1234` |
| Jane Doe   | janedoe@email.com      | `string123` |
| Jean Peplu | jeanpeplu@email.com    | `string123` |
| Admin      | admin@hbnb.io          | `string123` |

---

## Author

**Gwenaelle PICHOT**  
Student at Holberton School  
Project: Holberton - HBNB
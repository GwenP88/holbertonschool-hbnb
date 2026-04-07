# HBnB - Web Client

## Overview

HBnB is a full-stack web application inspired by AirBnB, built as part of the Holberton School curriculum. This repository contains the **front-end client** (Part 4), which connects to a RESTful back-end API built with Flask and SQLAlchemy.

The client is built with **HTML5**, **CSS3**, and **vanilla JavaScript (ES6)**. It communicates with the API using the **Fetch API** and manages user sessions through **JWT tokens stored in cookies**.

---

## Features

### Authentication
- Login form with email and password
- JWT token stored in a cookie (valid for 1 hour)
- Logout button clears the token and redirects to home
- "My Account" button visible only when authenticated

### Index Page (`/`)
- Displays all available places as cards
- Dynamically loaded from the API
- **Three client-side filters** (no page reload):
  - Filter by city (Lyon, Annecy, Genève)
  - Filter by maximum price
  - Filter by minimum rating
- Login link visible only when not authenticated

### Place Details (`/places/<place_id>`)
- Full place information: title, description, owner, price, city, amenities, average rating
- Customer reviews with author names and star ratings
- "Add a Review" button visible only when authenticated
- Review submission via a Bootstrap modal form

### User Account (`/user`)
- Displays the authenticated user's own places
- Lists all reviews received on those places, organized by place
- Redirects to login if not authenticated

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Markup     | HTML5 (Jinja2 templates via Flask)  |
| Styling    | CSS3 + Bootstrap 5.3                |
| Icons      | Font Awesome 6.5                    |
| Fonts      | Google Fonts (Fraunces, DM Sans)    |
| Scripting  | JavaScript ES6 (vanilla)            |
| HTTP       | Fetch API (AJAX)                    |
| Auth       | JWT via cookies                     |

---

## Project Structure

```
/
├── static/
│   ├── styles.css          # Main stylesheet
│   ├── scripts.js          # All client-side JavaScript
│   └── images/
│       ├── logo/           # Logo assets
│       ├── hero/           # Hero background images
│       └── places/         # Place images
├── templates/
│   ├── header.html         # Shared navigation header (Jinja2 include)
│   ├── footer.html         # Shared footer (Jinja2 include)
│   ├── index.html          # List of places
│   ├── login.html          # Login form
│   ├── place.html          # Place details + review modal
│   └── user.html           # User account page
└── routes.py               # Flask route definitions
```

---

## Pages

| Route              | Template       | Description                        |
|--------------------|----------------|------------------------------------|
| `/`                | index.html     | List of all places with filters    |
| `/login`           | login.html     | Login form                         |
| `/places/<id>`     | place.html     | Detailed view of a specific place  |
| `/user`            | user.html      | Authenticated user's account       |

---

## JavaScript Architecture (`scripts.js`)

The script is organized into 6 sections:

1. **Initialization** — `DOMContentLoaded` listener, routes to the right functions based on the active page
2. **Authentication** — `loginUser`, `getCookie`, `getCurrentUser`
3. **Index page** — `checkAuthentication`, `fetchPlaces`, `displayPlaces`, `filterPlaces`, filter setup
4. **User page** — `loadUserPage`, `loadUserPlaces`, `displayUserPlaces`, `loadUserReviews`
5. **Place details** — `getPlaceIdFromURL`, `loadPlacePage`, `fetchPlaceDetails`, `displayPlaceDetails`
6. **Add review** — `submitReview`

---

## API Endpoints Used

| Method | Endpoint                          | Description                  |
|--------|-----------------------------------|------------------------------|
| POST   | `/api/v1/auth/login`              | Authenticate and get token   |
| GET    | `/api/v1/users/me`                | Get current user data        |
| GET    | `/api/v1/users/<id>`              | Get user by ID               |
| GET    | `/api/v1/places`                  | List all places              |
| GET    | `/api/v1/places/<id>`             | Get place details            |
| GET    | `/api/v1/places/<id>/reviews`     | Get reviews for a place      |
| POST   | `/api/v1/reviews/`                | Submit a new review          |

---

## Authentication Flow

```
User fills login form
        ↓
POST /api/v1/auth/login
        ↓
API returns JWT token
        ↓
Token saved in cookie (max-age: 3600s)
        ↓
User redirected to /user
        ↓
On each page load: getCookie('token') checks auth state
        ↓
Token included in Authorization header for protected requests
```

---

## Design Choices

- **Color palette** based on natural tones (beige, teal, warm white) to match a travel/accommodation theme
- **Fraunces** serif font for titles, **DM Sans** for body text
- **Bootstrap 5** grid for responsive place cards
- Place images mapped by fixed IDs (seed data), with a default fallback image
- City resolved from GPS coordinates server-side using a coordinate-to-city mapping utility

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

**4. Initialize the database**

The application uses SQLite. On first run, the database is created automatically. To populate it with seed data, run the SQL seed file:

```bash
sqlite3 instance/development.db < sql/seed.sql
```

> Make sure the `instance/` directory exists before running this command:
> ```bash
> mkdir -p instance
> ```

**5. Start the application**

```bash
python3 run.py
```

The application will be available at `http://localhost:5000`.

---

### Project Layout (from root)

```
hbnb/
├── app/
│   ├── api/            # Flask-RESTX API namespaces (places, users, reviews, auth)
│   ├── models/         # SQLAlchemy models (User, Place, Review, Amenity)
│   ├── persistence/    # Repository pattern (SQLAlchemy implementations)
│   ├── services/       # Facade coordinating business logic
│   ├── static/         # CSS, JS, images
│   ├── templates/      # Jinja2 HTML templates
│   ├── utils/          # Helpers (city resolution, image mapping)
│   ├── __init__.py     # App factory
│   └── routes.py       # Flask page routes
├── sql/
│   └── seed.sql        # Initial seed data (users, places, reviews, amenities)
├── instance/
│   └── development.db  # SQLite database (auto-generated)
├── config.py           # App configuration
├── requirements.txt    # Python dependencies
└── run.py              # Application entry point
```

---

## Running the Application

Once set up, start the server with:

```bash
python3 run.py
```

The client will be available at `http://localhost:5000`.

The API documentation (Swagger UI) is available at `http://localhost:5000/api/v1/`.

> **Note on CORS:** If you encounter CORS errors, ensure `flask-cors` is configured in your Flask application to allow requests from the client's origin.

---

## Seed Data

The application comes with pre-loaded seed data including:

- 4 users (1 admin, 3 regular users)
- 5 amenities (WiFi, Swimming Pool, Air Conditioning, Rooftop Terrace, Private Parking)
- 6 places across 3 cities (Lyon, Annecy, Genève)
- 12 reviews distributed across all places

Default user credentials for testing:

| User       | Email                  | Password    |
|------------|------------------------|-------------|
| John Doe   | johndoe@email.com      | `string123` |
| Jane Doe   | janedoe@email.com      | `string123` |
| Jean Peplu | jeanpeplu@email.com    | `string123` |
| Admin      | admin@hbnb.io          | `admin1234` |

---

## Authors

**Gwenaelle PICHOT**  
Student at Holberton School   
Project: Holberton - HBNB

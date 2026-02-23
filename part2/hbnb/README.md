![HBnB Banner](assets/banner.png)

# HBnB – Part 2: Project Setup and Package Initialization

## Overview

This project sets up the initial architecture of the HBnB application.  
The goal of this phase is to create a clean, modular, and scalable structure following best practices for Python applications.

The application is organized into three main layers:

- **Presentation Layer** (API)
- **Business Logic Layer** (Models)
- **Persistence Layer** (In-memory repository)

This structure prepares the project for future integration of database-backed persistence (Part 3 using SQLAlchemy).

---

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

---

## Architecture Explanation

### Presentation Layer (`app/api/`)

Handles API endpoints using **Flask-RESTX**.  
Routes are organized by version (`v1/`).

The `v1/` directory contains:

- `users.py` – User-related endpoints
- `places.py` – Place-related endpoints
- `reviews.py` – Review-related endpoints
- `amenities.py` – Amenity-related endpoints

This layer communicates only with the **Facade**, not directly with models or repositories.

---

### Business Logic Layer (`app/models/`)
Contains the core domain models:

- `User`
- `Place`
- `Review`
- `Amenity`

This layer manages business rules and application logic.

---

### Persistence Layer (`app/persistence/`)
Implements the **Repository pattern**.

- `Repository` (abstract base class)
- `InMemoryRepository` (temporary storage using a dictionary)

This in-memory repository will be replaced by a database-backed implementation in Part 3.

---

### Services Layer (`app/services/`)
Implements the **Facade pattern**.

`HBnBFacade` centralizes communication between:

- API layer
- Business logic
- Persistence layer

A singleton instance of the facade is created to ensure a single access point across the application.

---

## How to Run the Application

### Clone the repository

```
git clone https://github.com/GwenP88/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2/hbnb
```

---

### Install dependencies

```
pip install -r requirements.txt
```

---

### Run the server

```
python run.py
```

You should see:

```
* Running on http://127.0.0.1:5000
```

The application will start successfully, even though no endpoints are fully implemented yet.

---

## ⚙️ Configuration

The `config.py` file defines environment-specific settings such as:

- `SECRET_KEY`
- `DEBUG` mode

This configuration system will be extended in later parts of the project to support additional environments and database integration.

---

## 🎯 Expected Outcome

By the end of this setup:

- The project structure is modular and scalable.
- The application runs successfully with Flask.
- The Repository and Facade patterns are implemented.
- The system is ready for API endpoint implementation.
- The persistence layer is designed to be easily replaced by a database-backed solution.

---

## 📚 Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-RESTX Documentation: https://flask-restx.readthedocs.io/
- Python Project Structure Best Practices: https://docs.python-guide.org/writing/structure/
- Facade Design Pattern: https://refactoring.guru/design-patterns/facade

---

**Author:** **Gwenaelle PICHOT** - Student at Holberton School  
**Repository:** holbertonschool-hbnb  
**Directory:** part2/hbnb

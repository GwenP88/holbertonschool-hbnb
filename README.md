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

## HBnB – Part 2: BL and API

Further implementation details will be provided in the upcoming project phases.

---

## HBnB – Part 3: Auth abnd DB

Further implementation details will be provided in the upcoming project phases.

---

## HBnB – Part 4: Simple Web Client

Further implementation details will be provided in the upcoming project phases.

---

## Author

**Gwenaelle PICHOT**  
Student at Holberton School   
Project: Holberton - HBNB

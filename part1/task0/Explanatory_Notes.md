```
---
config:
  layout: dagre
---
flowchart TB
    PL["<b>Presentation Layer</b><br>
    <hr>
    API Endpoints<br> 
    Controllers
    (UserController, PlaceController, ReviewController, AmenityController...)"]
    -. via Facade Pattern .-> BL["<b>Business Logic Layer</b><br>
    <hr>
    Facade (entry point)<br>
    Validation<br>
    Models (user, place, review, amenity)<br>
    Use cases (RegisterUser, CreatePlace, SubmitReview, SearchPlaces...)"]
    BL -. Database Operations .-> DAL["<b>Persistence Layer</b><br>
    <hr>
    Repositories (UserRepo, PlaceRepo, ReviewRepo, AmenityRepo...)<br>
    Database Access Object"]

    style PL fill:#f0f8ff,stroke:#4682b4
    style BL fill:#fff8e7,stroke:#ffa500
    style DAL fill:#ffe4e1,stroke:#dc143c
```

# High-Level Package Diagram – Explanatory Notes

## Overview

The system is structured into three distinct architectural layers:

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

This separation ensures clear responsibility boundaries, better maintainability, improved scalability, and easier testing.

---

# Presentation Layer

## Components

- API Endpoints  
- Controllers:
  - UserController  
  - PlaceController  
  - ReviewController  
  - AmenityController  

## Responsibilities

The Presentation Layer is responsible for handling all external interactions with clients (e.g., web browsers, REST clients).

Its main responsibilities include:

- Receiving HTTP requests  
- Validating and parsing incoming data  
- Calling the appropriate business operation through the Facade  
- Formatting and returning HTTP responses (JSON, status codes, error messages)  

This layer **does not implement business rules**. It only coordinates communication between the client and the Business Logic layer.

---

# Business Logic Layer

## Components

- Models:
  - User  
  - Place  
  - Review  
  - Amenity  

- Use Cases:
  - RegisterUser  
  - CreatePlace  
  - SubmitReview  
  - SearchPlaces  

## Responsibilities

The Business Logic Layer contains the core rules and behaviors of the application.

Its main responsibilities include:

- Implementing business rules  
- Enforcing validation and constraints  
- Managing relationships between entities  
- Orchestrating workflows (e.g., creating a place and linking it to a user)  

This layer is independent of HTTP and database technologies.  
It focuses purely on domain logic.

---

# Persistence Layer

## Components

- Repositories:
  - UserRepo  
  - PlaceRepo  
  - ReviewRepo  
  - AmenityRepo  

- Database Access Object (DAO)

## Responsibilities

The Persistence Layer is responsible for data storage and retrieval.

Its main responsibilities include:

- Executing database operations (CRUD)  
- Managing database connections  
- Translating domain objects into database records  
- Isolating database-specific logic from the rest of the system  

This layer ensures that changes in the database technology do not affect the Business Logic or Presentation layers.

---

# Communication Between Layers

## Layer Interaction Flow

1. The client sends an HTTP request to the Presentation Layer.
2. A Controller forwards the request to the Business Logic Layer through the Facade.
3. The Business Logic Layer processes the request.
4. If data storage or retrieval is required, it communicates with the Persistence Layer.
5. The result is returned back through the same path to the client.

---

# Facade Pattern Explanation

The **Facade Pattern** acts as a simplified interface between the Presentation Layer and the Business Logic Layer.

## Why Use a Facade?

Without a facade:
- Controllers would directly interact with multiple models and services.
- The Presentation Layer would become tightly coupled to internal logic.

With a facade:
- Controllers call a single unified interface.
- Internal complexity remains hidden.
- Business logic changes do not impact controllers.
- The system becomes easier to maintain and extend.

## Benefits of the Facade Pattern

- Reduces coupling between layers  
- Improves code organization  
- Simplifies controller implementation  
- Provides a centralized entry point to business operations  
- Enhances testability  

---

# Architectural Benefits

This layered architecture combined with the Facade Pattern provides:

- Clear separation of concerns  
- Improved maintainability  
- Easier scalability  
- Better test isolation  
- Cleaner dependency management  

Each layer has a well-defined role, ensuring that responsibilities are not mixed across the system. 

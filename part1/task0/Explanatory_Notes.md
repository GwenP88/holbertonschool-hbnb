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

# Explanatory Notes

## 1. Overall Architecture

The **HBnB application** follows a three-layered architecture.  
This structure ensures clear separation of responsibilities, reduced coupling, and improved maintainability and scalability.

The three main layers are:

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

Each layer has a clearly defined responsibility and communicates only with the adjacent layer.

---

## 2. Presentation Layer

The **Presentation Layer** serves as the entry point of the application.  
It handles user interaction through API endpoints.

### Responsibilities

- Receiving HTTP requests  
- Validating input format  
- Managing HTTP response codes  
- Forwarding requests to the Business Logic layer  

This layer does not contain business rules.  
It does not access the database directly nor manipulate domain models.

Its purpose is strictly to expose services and manage communication between the client and the system.

---

## 3. Business Logic Layer

The **Business Logic Layer** represents the core of the application.

### It contains:

- Domain models (`User`, `Place`, `Review`, `Amenity`)  
- Business validation rules  
- Use cases (`RegisterUser`, `CreatePlace`, `SubmitReview`, etc.)  
- The Facade (internal entry point)  

### Responsibilities

- Applying business rules  
- Ensuring data consistency  
- Orchestrating operations  
- Coordinating between models and persistence  

It remains independent from the Presentation Layer and does not depend on database implementation details.

Centralizing business logic in this layer ensures system consistency and avoids duplication of rules.

---

## 4. Persistence Layer

The **Persistence Layer** is responsible for data storage and retrieval.

### It includes:

- Repositories (`UserRepository`, `PlaceRepository`, etc.)  
- Database access mechanisms (SQL, ORM, DAO)  

### Responsibilities

- Executing CRUD operations  
- Managing SQL queries  
- Handling communication with the database  
- Encapsulating storage-related technical details  

This isolation allows the Business Logic to remain independent of database technology.

As a result, the storage solution can be changed without affecting business logic.

---

## 5. Role of the Facade Pattern

The **Facade Pattern** simplifies communication between the Presentation and Business Logic layers.

### The facade:

- Provides a single entry point  
- Exposes high-level methods  
- Hides internal complexity  
- Reduces coupling between layers  

Without the facade, the Presentation Layer would need to directly interact with multiple models or services, increasing complexity and dependency.

By using a facade:

- The Presentation Layer interacts with one unified interface  
- The internal organization of the Business Layer remains protected  
- Internal changes do not affect the API layer  

This improves maintainability, readability, and architectural robustness.

---

## 6. Layer Communication Flow

The communication flow is strictly unidirectional:

Presentation → Business Logic (via Facade)
Business Logic → Persistence (via Repositories)


No layer directly accesses a non-adjacent layer.

This structure ensures:

- High cohesion  
- Low coupling  
- Scalability  
- Better testability  

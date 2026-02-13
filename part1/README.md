![HBnB Banner](assets/banner.png)

# HBnB Technical Documentation

## 1. Introduction

### 1.1 Project Overview

HBnB is a layered web application designed to manage users, places, reviews, and amenities. The system follows a structured architectural approach to ensure scalability, maintainability, and clear separation of responsibilities.

The application is built around a domain-driven design where core entities encapsulate business behavior, and API endpoints orchestrate user interactions through clearly defined layers.

---

### 1.2 Purpose of This Document

This document serves as a comprehensive technical blueprint for the HBnB project.

Its objectives are to:

- Present the overall system architecture.
- Describe the Business Logic domain model.
- Explain API interaction flows.
- Clarify architectural decisions and design rationale.
- Provide a reference for future implementation phases.

This document consolidates all diagrams and explanatory notes produced during the design phase.

---

# 2. High-Level Architecture

## 2.1 Layered Architecture Overview

The HBnB system is structured using a three-layer architecture:

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

Each layer has a clearly defined responsibility and communicates only with adjacent layers.

The layered design promotes modularity, testability, and maintainability.

```
flowchart LR
    PL["<b>Presentation Layer</b><br>
    <hr>
    API Endpoints<br> 
    Controllers
    (UserController, PlaceController, ReviewController, AmenityController)"] -. Facade Pattern .-> BL["<b>Business Logic Layer</b><br>
    <hr>
    Models (user, place, review, amenity)<br>
    Use cases (RegisterUser, CreatePlace, SubmitReview, SearchPlaces)"]
    BL -. Database Operations .-> DAL["<b>Persistence Layer</b><br>
    <hr>
    Repositories (UserRepo, PlaceRepo, ReviewRepo, AmenityRepo)<br>
    Database Access Object"]
```

---

## 2.2 Architectural Pattern: Facade

The system uses the **Facade Pattern** between the Presentation Layer and the Business Logic Layer.

The facade provides a simplified interface to the domain logic, preventing controllers from directly interacting with multiple internal components or domain entities.

### Design Rationale

The use of the Facade pattern:

- Reduces coupling between layers  
- Centralizes business operations  
- Improves maintainability  
- Simplifies controller responsibilities  
- Ensures clear separation between request handling and domain logic  

Controllers delegate operations to a unified entry point instead of directly manipulating domain models.

---

# 3. Business Logic Layer

## 3.1 Overview

The Business Logic Layer contains the core domain entities and business rules of the system.

It is responsible for:

- Defining domain behavior  
- Enforcing business constraints  
- Managing entity relationships  
- Orchestrating domain workflows  

This layer is independent of HTTP concerns and database implementation details.

```
classDiagram
direction TB
    class BaseModel {
        <<abstract>>
	    #id: UUID4
	    #created_at: DateTime
	    #updated_at: DateTime
        +save() void
        +update_time() void
    }

    class User {
	    -first_name: str
	    -last_name: str
	    -email: str
	    -password: str
	    -is_admin: bool
	    +create_user(data: dict) User
	    +get_profile() dict
	    +update_user(data: dict) void
	    +set_password(password: str) void
	    +delete() void
    }

    class Place {
	    -title: str
	    -description: str
	    -price: float
	    -latitude: float
	    -longitude: float
	    -amenities: list[Amenity]
	    -owner_id: UUID4
	    +create_place(data: dict, owner_id: UUID4) Place
	    +get_details(): dict
		+to_list_item(): dict
	    +update_details(data: dict) void
	    +delete() void
	    +add_amenity(amenity: Amenity) void
        +remove_amenity(amenity: Amenity) void
    }

    class Review {
	    -rating: int
	    -comment: str
	    -author_id: UUID4
	    -place_id: UUID4
	    +create_review(data: dict, author_id: UUID4, place_id: UUID4) Review
	    +get_details() dict
	    +update_review(data: dict) void
	    +delete() void
    }

    class Amenity {
	    -name: str
	    -description: str
	    +create_amenity(data: dict) Amenity
	    +get_details() dict
	    +update_amenity(data: dict) void
	    +delete() void
    }
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    User "1" --> "0..*" Review
    User "1" --> "0..*" Place
    Place "1" *-- "0..*" Review
    Place "0..*" o-- "0..*" Amenity
```

---

## 3.2 Entity Descriptions

### BaseModel

`BaseModel` is an abstract class that provides shared attributes and behaviors for all domain entities.

It defines:

- A unique identifier (UUID4)
- Creation timestamp
- Update timestamp
- Core persistence-related methods

This abstraction ensures consistency across entities and avoids duplication.

---

### User

The `User` entity represents a registered user of the system.

A user can:

- Create and manage place listings  
- Submit reviews  
- Update profile information  

The `is_admin` attribute allows role differentiation within the system.

---

### Place

The `Place` entity represents a property listing.

Each place:

- Is owned by a user (referenced via `owner_id`)
- Can have multiple reviews
- Can include multiple amenities

The entity provides methods to:

- Create and update listing details
- Manage associated amenities
- Return formatted representations for detailed and list views

---

### Review

The `Review` entity represents user feedback on a specific place.

Each review:

- Is associated with one user (`author_id`)
- Is linked to one place (`place_id`)
- Contains a rating and comment

The entity enforces business constraints before persistence.

---

### Amenity

The `Amenity` entity represents reusable features such as WiFi or parking.

Amenities:

- Can be associated with multiple places
- Exist independently of specific listings

This supports a many-to-many relationship between places and amenities.

---

# 4. API Interaction Flow

This section describes how the system processes API requests through the layered architecture.

Each sequence diagram illustrates:

- The normal execution flow  
- Error handling at each architectural layer  
- Communication between Presentation, Business Logic, and Persistence  

The interaction pattern is consistent across all use cases:

1. The USER sends an HTTP request.
2. The API validates and forwards the request.
3. The Business Logic applies domain rules.
4. The Database performs data retrieval or persistence.
5. The response propagates back to the USER.

---

## 4.1 User Registration – `POST /users`

### Purpose

Creates a new user account.

### Flow Summary

1. The API validates the request input.
2. The Business Logic checks email uniqueness.
3. The Database stores the new user.
4. The API returns the appropriate HTTP response.

### Error Handling

- **400** – Invalid input  
- **409** – Email already exists  
- **500** – Database failure  

```
sequenceDiagram
    autonumber
    participant USER as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    USER->>API: POST /users (registration data)
    API->>BL: validateRegistration(data)

    alt Invalid input (Presentation/API validation)
        BL-->>API: ValidationError
        API-->>USER: 400 Bad Request
    else Input valid
        BL->>DB: check_email(email)
        DB-->>BL: emailExists true/false

        alt Email already exists
            BL-->>API: EmailAlreadyExists
            API-->>USER: 409 Conflict
        else Email available
            BL->>DB: save_new_user(user)
            alt Database failure
                DB-->>BL: DatabaseError
                BL-->>API: PersistenceError
                API-->>USER: 500 Internal Server Error
            else Saved successfully
                DB-->>BL: UserSaved
                BL-->>API: UserCreated(user)
                API-->>USER: 201 Created
            end
        end
    end
```

---

## 4.2 Place Creation – `POST /places`

### Purpose

Creates a new place listing.

### Flow Summary

1. The API validates the input data.
2. The Business Logic verifies that the owner exists.
3. The Database saves the new place.
4. The API returns `201 Created`.

### Error Handling

- **400** – Invalid input  
- **404** – Owner not found  
- **500** – Database failure  

```
sequenceDiagram
    autonumber
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: POST /places (place data)
    API->>BL: validatePlace(data)

    alt Invalid data
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid data
        BL->>DB: check_owner(owner_id)
        DB-->>BL: ownerExists=true/false

        alt Owner not found
            BL-->>API: OwnerNotFound
            API-->>U: 404 Not Found
        else Owner exists
            BL->>DB: save_new_place(place)

            alt Database failur
                DB-->>BL: DatabaseError
                BL-->>API: PersistenceError
                API-->>U: 500 Internal Server Error
            else Saved successfully
                DB-->>BL: savedPlace
                BL-->>API: PlaceCreated(place)
                API-->>U: 201 Created
            end
        end
    end
```

---

## 4.3 Review Submission – `POST /places/{place_id}/reviews`

### Purpose

Allows a user to submit a review for a place.

### Flow Summary

1. The API validates the input.
2. The Business Logic verifies:
   - The user exists  
   - The place exists  
   - Permission rules are satisfied (e.g., booking requirement)  
3. The Database stores the review.
4. The API returns `201 Created`.

### Error Handling

- **400** – Invalid input  
- **404** – User or place not found  
- **403** – Permission denied  
- **500** – Database failure  

```
sequenceDiagram
    autonumber
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: POST /places/{place_id}/reviews (review data)
    API->>BL: validateReview(data)

    alt Invalid data
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid data
        BL->>DB: check_user(author_id)
        DB-->>BL: userExists=true/false

        alt User not found
            BL-->>API: UserNotFound
            API-->>U: 404 Not Found
        else User exists
            BL->>DB: check_place(place_id)
            DB-->>BL: placeExists=true/false

            alt Place not found
                BL-->>API: PlaceNotFound
                API-->>U: 404 Not Found
            else Place exists
                BL->>DB: check_permission(author_id, place_id)
                DB-->>BL: permission=true/false

                alt Permission denied
                    BL-->>API: PermissionDenied
                    API-->>U: 403 Forbidden
                else Allowed
                    BL->>DB: save_new_review(review)

                    alt Database failure
                        DB-->>BL: DatabaseError
                        BL-->>API: PersistenceError
                        API-->>U: 500 Internal Server Error
                    else Saved successfully
                        DB-->>BL: savedReview
                        BL-->>API: ReviewCreated(savedReview)
                        API-->>U: 201 Created
                    end
                end
            end
        end
    end
```

---

## 4.4 Fetching Places – `GET /places`

### Purpose

Retrieves a filtered list of places based on search criteria.

### Flow Summary

1. The API validates query parameters.
2. The Business Logic builds and validates search criteria.
3. The Database executes the search query.
4. The API returns `200 OK` with the result list.

### Error Handling

- **400** – Invalid filters  
- **422** – Business rule violation  
- **500** – Database failure  

```
sequenceDiagram
    autonumber  
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: GET /places?lat=&lon=&max_price=&amenity=
    API->>BL: validateFilters(filters)

    alt Invalid filters
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid filters
        BL->>BL: buildSearchCriteria(filters)

        opt lat & lon provided
            BL->>BL: computeGeoArea(lat, lon)
        end

        opt max_price provided
            BL->>BL: setMaxPrice(max_price)
        end

        opt amenity provided
            BL->>BL: addAmenityFilter(amenity)
        end

        BL->>BL: validateSearchCriteria(criteria)

        alt Business rule violation
            BL-->>API: InvalidSearchCriteria
            API-->>U: 422 Unprocessable Entity
        else Criteria accepted
            BL->>DB: search_places(criteria)

            alt Database failure
                DB-->>BL: DatabaseError
                BL-->>API: PersistenceError
                API-->>U: 500 Internal Server Error
            else Query success
                DB-->>BL: places[]
                BL-->>API: places[]
                API-->>U: 200 OK (places[])
            end
        end
    end
```

---

# 5. Overall Design Considerations

## 5.1 Separation of Concerns

Each layer has a clearly defined responsibility:

- The **Presentation Layer** handles HTTP communication.
- The **Business Logic Layer** enforces domain rules.
- The **Persistence Layer** manages data storage and retrieval.

This separation improves modularity and system clarity.

---

## 5.2 Error Handling Strategy

Each layer can fail independently:

- Input validation errors  
- Business rule violations  
- Database errors  

Handling failures at the appropriate layer ensures robust and predictable system behavior.

---

## 5.3 Scalability and Maintainability

The layered architecture and facade pattern:

- Reduce coupling  
- Improve modularity  
- Simplify testing  
- Support future extensions  

The design allows the system to evolve without compromising structural integrity.

---

# Conclusion

This technical documentation provides a structured blueprint for the HBnB system.

It defines:

- The high-level architecture  
- The domain model  
- The interaction flow between layers  

The document serves as a reference guide throughout the implementation phases of the HBnB project and ensures consistency in architectural decisions.

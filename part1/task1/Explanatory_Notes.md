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

# Detailed Class Diagram – Explanatory Notes

## Overview

The system is modeled using a domain-driven approach centered around four main entities:

- `User`
- `Place`
- `Review`
- `Amenity`

All entities inherit from an abstract base class `BaseModel`, which provides shared attributes and behaviors.

The diagram uses standard UML notation to represent:
- Generalization (inheritance)
- Associations
- Composition
- Multiplicities

---

# 1. BaseModel (Abstract)

## Role

`BaseModel` is an abstract class that provides common attributes and behaviors shared by all domain entities.

## Key Attributes

- `id: UUID4` — Unique identifier for each entity instance.
- `created_at: DateTime` — Timestamp indicating when the entity was created.
- `updated_at: DateTime` — Timestamp indicating the last update.

## Key Methods

- `save(): void` — Persists the entity.
- `update_time(): void` — Updates the `updated_at` timestamp.

## Purpose

This abstraction ensures:
- Consistent identity management.
- Centralized lifecycle handling.
- Reduced duplication across entities.

All domain entities (`User`, `Place`, `Review`, `Amenity`) inherit from `BaseModel`.

---

# 2. User

## Role

Represents a system user. A user can own places and write reviews.

## Key Attributes

- `first_name: str`
- `last_name: str`
- `email: str`
- `password: str`
- `is_admin: bool`

## Key Methods

- `create_user(data: dict): User`
- `get_profile(): dict`
- `update_user(data: dict): void`
- `set_password(password: str): void`
- `delete(): void`

## Business Responsibility

- Manages user identity and profile information.
- Can own multiple places.
- Can write multiple reviews.

---

# 3. Place

## Role

Represents a property listed in the system.

## Key Attributes

- `title: str`
- `description: str`
- `price: float`
- `latitude: float`
- `longitude: float`
- `amenities: list[Amenity]`
- `owner_id: UUID4` — References the user who owns the place.

## Key Methods

- `create_place(data: dict, owner_id: UUID4): Place`
- `get_details(): dict` — Returns full detailed representation of the place.
- `to_list_item(): dict` — Returns summarized representation for list views.
- `update_details(data: dict): void`
- `delete(): void`
- `add_amenity(amenity: Amenity): void`
- `remove_amenity(amenity: Amenity): void`

## Business Responsibility

- Encapsulates all data related to a listing.
- Maintains association with its owner via `owner_id`.
- Manages relationships with amenities.
- Provides different data representations for detailed and list views.

---

# 4. Review

## Role

Represents a review written by a user for a specific place.

## Key Attributes

- `rating: int`
- `comment: str`
- `author_id: UUID4`
- `place_id: UUID4`

## Key Methods

- `create_review(data: dict, author_id: UUID4, place_id: UUID4): Review`
- `get_details(): dict`
- `update_review(data: dict): void`
- `delete(): void`

## Business Responsibility

- Links a user to a place through feedback.
- Stores evaluation data (rating and comment).
- Maintains referential integrity through `author_id` and `place_id`.

---

# 5. Amenity

## Role

Represents a feature or facility available at a place (e.g., Wi-Fi, parking).

## Key Attributes

- `name: str`
- `description: str`

## Key Methods

- `create_amenity(data: dict): Amenity`
- `get_details(): dict`
- `update_amenity(data: dict): void`
- `delete(): void`

## Business Responsibility

- Defines reusable features.
- Can be associated with multiple places.

---

# Relationships Between Entities

## 1. Generalization (Inheritance)

All entities inherit from `BaseModel`:

- `BaseModel <|-- User`
- `BaseModel <|-- Place`
- `BaseModel <|-- Review`
- `BaseModel <|-- Amenity`

This ensures shared identity and lifecycle management.

---

## 2. User – Place (One-to-Many)

- A `User` can own multiple `Place` entities.
- Each `Place` is associated with exactly one owner via `owner_id`.

Multiplicity:
- `User "1" --> "0..*" Place`

This models the ownership relationship in the system.

---

## 3. User – Review (One-to-Many)

- A `User` can write multiple `Review` entities.
- Each `Review` is authored by one user via `author_id`.

Multiplicity:
- `User "1" --> "0..*" Review`

This represents authorship of reviews.

---

## 4. Place – Review (Composition, One-to-Many)

- A `Place` can have multiple reviews.
- Each `Review` is associated with exactly one place via `place_id`.

Multiplicity:
- `Place "1" *-- "0..*" Review`

Composition indicates strong ownership:
If a `Place` is removed, its associated reviews are also logically removed.

---

## 5. Place – Amenity (Many-to-Many)

- A `Place` can have multiple amenities.
- An `Amenity` can be shared across multiple places.

Multiplicity:
- `Place "0..*" o-- "0..*" Amenity`

Aggregation reflects a reusable relationship where amenities exist independently of places.

---

# Contribution to Overall Business Logic

The domain model supports the core system workflows:

- Users create and manage places.
- Users search and view places using different representations (`get_details`, `to_list_item`).
- Users write reviews for places.
- Places aggregate reviews and amenities.
- Amenities are reusable domain features.

The use of UUID-based references (`owner_id`, `author_id`, `place_id`) ensures:
- Clear separation between domain identity and object references.
- Compatibility with persistence layers.
- Reduced coupling between entities.

This structured domain model provides a solid foundation for implementing business rules, enforcing constraints, and supporting API operations while maintaining clear separation of responsibilities.

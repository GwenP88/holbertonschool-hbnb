```
classDiagram
direction TB
    class BaseModel {
	    #id: UUID4
	    #created_at: DateTime
	    #updated_at: DateTime
        +save() void
        +update_time() void
        +update(data: dict) void
    }

    class User {
	    -first_name: str
	    -last_name: str
	    -email: str
	    -password: str
	    -is_admin: bool
        +set_password(password: str) void
	    +create_user(data: dict) User
	    +get_profile() dict
        +update(data: dict) void
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
        +add_amenity(amenity_id: UUID4) void
        +remove_amenity(amenity_id: UUID4) void
	    +delete() void
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
        +update(data: dict) void
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

The system follows a domain-driven design centered around four main entities:

- `User`
- `Place`
- `Review`
- `Amenity`

All entities inherit from `BaseModel`, which provides identity management and lifecycle handling.

The UML diagram represents:

- Inheritance (Generalization)
- Associations
- Composition
- Aggregation
- Multiplicities

---

# 1. BaseModel (Abstract)

## Role

`BaseModel` provides shared identity and lifecycle behavior for all domain entities.

## Attributes

- `id: UUID4` — Unique identifier for each entity instance.
- `created_at: DateTime` — Timestamp when the entity was created.
- `updated_at: DateTime` — Timestamp of the last update.

## Methods

- `save(): void` — Persists the entity.
- `update_time(): void` — Updates the `updated_at` timestamp.
- `update(data: dict): void` — Generic update method for modifying entity attributes.

## Responsibility

- Centralized identity management.
- Consistent timestamp handling.
- Shared update mechanism across entities.
- Reduction of duplicated logic.

All domain entities inherit from `BaseModel`.

---

# 2. User

## Role

Represents a system user. A user can own places and write reviews.

## Attributes

- `first_name: str`
- `last_name: str`
- `email: str`
- `password: str`
- `is_admin: bool`

## Methods

- `set_password(password: str): void`
- `create_user(data: dict): User`
- `get_profile(): dict`
- `update(data: dict): void`
- `delete(): void`

## Business Responsibility

- Manages identity and authentication data.
- Owns multiple places.
- Writes multiple reviews.
- Encapsulates profile representation logic.

---

# 3. Place

## Role

Represents a property listing in the system.

## Attributes

- `title: str`
- `description: str`
- `price: float`
- `latitude: float`
- `longitude: float`
- `amenities: list[Amenity]`
- `owner_id: UUID4`

## Methods

- `create_place(data: dict, owner_id: UUID4): Place`
- `get_details(): dict`
- `to_list_item(): dict`
- `update_details(data: dict): void`
- `add_amenity(amenity_id: UUID4): void`
- `remove_amenity(amenity_id: UUID4): void`
- `delete(): void`

## Business Responsibility

- Encapsulates listing information.
- Maintains association with its owner through `owner_id`.
- Manages amenity relationships.
- Provides multiple data representations (detailed and summary views).

---

# 4. Review

## Role

Represents feedback written by a user for a specific place.

## Attributes

- `rating: int`
- `comment: str`
- `author_id: UUID4`
- `place_id: UUID4`

## Methods

- `create_review(data: dict, author_id: UUID4, place_id: UUID4): Review`
- `get_details(): dict`
- `update_review(data: dict): void`
- `delete(): void`

## Business Responsibility

- Connects a user to a place through evaluation.
- Stores rating and comment data.
- Maintains referential integrity via UUID references.

---

# 5. Amenity

## Role

Represents a reusable feature available at a place (e.g., Wi-Fi, parking).

## Attributes

- `name: str`
- `description: str`

## Methods

- `create_amenity(data: dict): Amenity`
- `get_details(): dict`
- `update(data: dict): void`
- `delete(): void`

## Business Responsibility

- Defines reusable listing features.
- Exists independently of places.
- Can be associated with multiple places.

---

# Relationships Between Entities

## 1. Inheritance

All entities inherit from `BaseModel`:

- `BaseModel <|-- User`
- `BaseModel <|-- Place`
- `BaseModel <|-- Review`
- `BaseModel <|-- Amenity`

This ensures shared lifecycle and identity logic.

---

## 2. User – Place (One-to-Many)

- A `User` can own multiple `Place` entities.
- Each `Place` is associated with exactly one owner via `owner_id`.

Multiplicity:

- `User "1" --> "0..*" Place`

Ownership is modeled using a UUID reference.

---

## 3. User – Review (One-to-Many)

- A `User` can write multiple `Review` entities.
- Each `Review` is authored by exactly one user via `author_id`.

Multiplicity:

- `User "1" --> "0..*" Review`

This models review authorship.

---

## 4. Place – Review (Composition, One-to-Many)

- A `Place` can contain multiple reviews.
- Each `Review` belongs to exactly one place via `place_id`.

Multiplicity:

- `Place "1" *-- "0..*" Review`

Composition indicates strong ownership:  
If a `Place` is removed, its associated reviews are logically removed as well.

---

## 5. Place – Amenity (Many-to-Many, Aggregation)

- A `Place` can have multiple amenities.
- An `Amenity` can be shared across multiple places.

Multiplicity:

- `Place "0..*" o-- "0..*" Amenity`

Aggregation reflects that amenities exist independently and are reusable.

---

# Contribution to Overall Business Logic

The domain model supports the system’s core workflows:

- Users create and manage places.
- Users retrieve place data in different formats.
- Users write reviews for places.
- Places aggregate reviews and amenities.
- Amenities are reusable domain features.

The use of UUID-based references (`owner_id`, `author_id`, `place_id`) ensures:

- Decoupling between entities.
- Clear identity management.
- Compatibility with repository and persistence layers.
- Clean separation of responsibilities.

This structured domain model provides a solid foundation for implementing business rules, enforcing constraints, and supporting API operations while maintaining maintainable and scalable architecture.
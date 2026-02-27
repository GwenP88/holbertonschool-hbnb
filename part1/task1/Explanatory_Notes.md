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
	    -is_admin: bool
        -password: str
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
        +get_details() dict
		+to_list_item() dict
        +get_all_places() list[dict]
        +update(data: dict) void
        +add_amenity(amenity: Amenity) void
        +remove_amenity(amenity: Amenity) void
	    +delete() void
    }

    class Review {
        -comment: str
	    -rating: int
	    -author_id: UUID4
	    -place_id: UUID4
	    +create_review(data: dict, author_id: UUID4, place_id: UUID4) Review
	    +get_details() dict
	    +update(data: dict) void
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

# Detailed Class Diagram – Explanatory Notes (Aligned with Current Implementation)

## Overview

The system is built around four core domain entities:

- `User`
- `Place`
- `Review`
- `Amenity`

All entities inherit from `BaseModel`, which centralizes identity and lifecycle behavior.

This documentation strictly reflects the current implementation and architectural choices.

---

# 1. BaseModel (Abstract)

## Role

Provides shared identity and lifecycle handling for all domain entities.

## Attributes

- `id: UUID4` — Unique identifier for each entity instance.
- `created_at: DateTime` — Creation timestamp.
- `updated_at: DateTime` — Last update timestamp.

## Methods

- `save(): void` — Persists or registers the entity in storage.
- `update_time(): void` — Refreshes `updated_at` timestamp.
- `update(data: dict): void` — Applies field updates from a dictionary (delegated to child classes when overridden).

---

# 2. User

## Role

Represents a system user who can own places and write reviews.

## Attributes

- `first_name: str`
- `last_name: str`
- `email: str` (unique)
- `password: str` (stored securely)
- `is_admin: bool`

## Methods

- `set_password(password: str): void` — Sets and hashes the password.
- `create_user(data: dict): User` — Factory method to create a new user.
- `get_profile(): dict` — Returns a public profile representation.
- `update(data: dict): void` — Updates editable fields.
- `delete(): void` — Removes the user from storage.

---

# 3. Place

## Role

Represents a property listing owned by a user.

## Attributes

- `title: str`
- `description: str`
- `price: float`
- `latitude: float`
- `longitude: float`
- `amenities: list[Amenity]` *(conceptually)*  
- `owner_id: UUID4`

### Important Implementation Note

In the current implementation:

- `amenities` are internally stored as a list of amenity IDs (not full Amenity objects).
- `owner_id` is stored as an identifier and resolved through the repository layer.
- The class does not directly access storage; it delegates listing responsibilities.

## Methods

- `create_place(data: dict, owner_id: UUID4): Place`  
  Factory method creating a new place linked to an owner.

- `get_details(): dict`  
  Returns a complete dictionary representation of the place.

- `to_list_item(): dict`  
  Returns a lightweight summary representation (used for listings).

- `get_all_places(): list[dict]`  
  Class-level method returning all places as dictionaries.  
  This method delegates retrieval to a repository/service layer instead of managing storage internally.  
  It exists to satisfy UML requirements while preserving architectural separation of concerns.

- `update(data: dict): void`  
  Updates editable fields with validation.

- `add_amenity(amenity: Amenity): void`  
  Links an amenity to the place (internally stored by ID).

- `remove_amenity(amenity: Amenity): void`  
  Removes the association with an amenity.

- `delete(): void`  
  Removes the place from storage.

---

# 4. Review

## Role

Represents a user review for a specific place.

## Attributes

- `comment: str`
- `rating: int`
- `author_id: UUID4`
- `place_id: UUID4`

## Methods

- `create_review(data: dict, author_id: UUID4, place_id: UUID4): Review`  
  Factory method creating a review linked to a user and a place.

- `get_details(): dict`  
  Returns review details as a dictionary.

- `update(data: dict): void`  
  Updates rating and/or comment.

- `delete(): void`  
  Removes the review.

---

# 5. Amenity

## Role

Represents a reusable feature (e.g., Wi-Fi, parking).

## Attributes

- `name: str`
- `description: str`

## Methods

- `create_amenity(data: dict): Amenity`  
  Factory method creating a new amenity.

- `get_details(): dict`  
  Returns amenity details.

- `update(data: dict): void`  
  Updates amenity fields.

- `delete(): void`  
  Removes the amenity.

---

# Relationships Between Entities

## Inheritance

All domain entities inherit from `BaseModel`.

## User → Place (1 to many)

A user can own multiple places.  
Each place references exactly one owner via `owner_id`.

## User → Review (1 to many)

A user can write multiple reviews.  
Each review references exactly one author via `author_id`.

## Place *-- Review (Composition)

A place logically owns its reviews.  
If a place is deleted, its associated reviews should also be removed.

## Place o-- Amenity (Aggregation – Many-to-Many)

Amenities exist independently and may be shared across multiple places.  
The relationship is managed through identifiers rather than embedded objects.

---

# Architectural Clarification

Although `get_all_places()` appears in the `Place` class for UML completeness, actual storage and retrieval logic is handled through repository and service layers. This preserves separation of concerns while remaining compliant with diagram expectations.

Identifiers (`owner_id`, `author_id`, `place_id`) ensure loose coupling between entities and persistence layers.

---

## Author

Gwenaelle PICHOT  
Holberton School – HBNB Project
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
        +get_details() dict
		+to_list_item() dict
        +get_all_places() list[dict]
        +update_details(data: dict) void
        +add_amenity(amenity: Amenity) void
        +remove_amenity(amenity: Amenity) void
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

# Detailed Class Diagram – Explanatory Notes (with Method Summaries)

## Overview

The system is built around four core entities:

- `User`
- `Place`
- `Review`
- `Amenity`

All entities inherit from `BaseModel`, which centralizes identity and lifecycle behavior.

The UML diagram covers inheritance, associations, composition, aggregation, and multiplicities.

---

# 1. BaseModel (Abstract)

## Role

Provides shared identity and lifecycle handling for all domain entities.

## Attributes

- `id: UUID4` — Unique identifier for each entity instance.
- `created_at: DateTime` — Creation timestamp.
- `updated_at: DateTime` — Last update timestamp.

## Methods (What they do)

- `save(): void` — Persists the entity to storage.
- `update_time(): void` — Refreshes `updated_at` to current time.
- `update(data: dict): void` — Applies generic field updates from a dictionary.

---

# 2. User

## Role

Represents a user who can own places and write reviews.

## Attributes

- `first_name: str` — User first name.
- `last_name: str` — User last name.
- `email: str` — Unique email address.
- `password: str` — User password (stored securely).
- `is_admin: bool` — Admin privilege flag.

## Methods (What they do)

- `set_password(password: str): void` — Sets (and hashes) the user password.
- `create_user(data: dict): User` — Creates a new user from provided data.
- `get_profile(): dict` — Returns a public profile representation.
- `update(data: dict): void` — Updates user fields (excluding sensitive rules if needed).
- `delete(): void` — Removes the user from the system.

---

# 3. Place

## Role

Represents a property listing owned by a user.

## Attributes

- `title: str` — Listing title.
- `description: str` — Listing description.
- `price: float` — Price per unit (e.g., per night).
- `latitude: float` — Geographic latitude.
- `longitude: float` — Geographic longitude.
- `amenities: list[Amenity]` — Amenities linked to the place.
- `owner_id: UUID4` — ID of the owner user.

## Methods (What they do)

- `create_place(data: dict, owner_id: UUID4): Place` — Creates a place linked to an owner.
- `get_details(): dict` — Returns full place details.
- `to_list_item(): dict` — Returns a lighter summary for listings.
- `get_all_places(): list[dict]` — Returns a list of all places (as dictionaries).
- `update_details(data: dict): void` — Updates editable place fields.
- `add_amenity(amenity: Amenity): void` — Links an amenity to the place.
- `remove_amenity(amenity: Amenity): void` — Unlinks an amenity from the place.
- `delete(): void` — Removes the place (and its owned reviews logically).

---

# 4. Review

## Role

Represents a user review for a specific place.

## Attributes

- `rating: int` — Numeric score between 1 and 5.
- `comment: str` — Review text.
- `author_id: UUID4` — ID of the review author.
- `place_id: UUID4` — ID of the reviewed place.

## Methods (What they do)

- `create_review(data: dict, author_id: UUID4, place_id: UUID4): Review` — Creates a review linked to author + place.
- `get_details(): dict` — Returns review content/details.
- `update_review(data: dict): void` — Updates rating/comment fields.
- `delete(): void` — Removes the review.

---

# 5. Amenity

## Role

Represents a reusable feature (e.g., Wi-Fi, parking).

## Attributes

- `name: str` — Amenity name.
- `description: str` — Amenity description.

## Methods (What they do)

- `create_amenity(data: dict): Amenity` — Creates a new amenity.
- `get_details(): dict` — Returns amenity details.
- `update(data: dict): void` — Updates amenity fields.
- `delete(): void` — Removes the amenity from the system.

---

# Relationships Between Entities

## Inheritance

All entities inherit from `BaseModel`.

## User → Place (1 to many)

A user can own multiple places; each place has one owner via `owner_id`.

## User → Review (1 to many)

A user can write multiple reviews; each review has one author via `author_id`.

## Place *-- Review (composition)

A place owns its reviews logically: deleting a place implies deleting its reviews.

## Place o-- Amenity (aggregation, many-to-many)

Amenities exist independently and can be reused across multiple places.

---

# Architectural Impact

UUID references (`owner_id`, `author_id`, `place_id`) keep the domain loosely coupled, repository-friendly, and compatible with persistence layers while preserving clear responsibility boundaries.

---

## Author

**Gwenaelle PICHOT**  
Student at Holberton School   
Project: Holberton - HBNB
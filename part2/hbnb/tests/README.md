![Banner](assets/banner.png)

# HBnB API — Testing & Validation Documentation
_Task 6 — Implement Testing and Validation of the Endpoints_

---

# 1. Overview

This document describes the full testing process implemented for the HBnB API.

The objective of this task was to:

- Implement validation logic at the business/model layer
- Perform manual black-box testing using Swagger UI
- Implement automated unit tests using Python `unittest`
- Verify correct behavior for:
  - Valid input
  - Invalid input
  - Boundary conditions
  - Relationship integrity
  - Resource not found (404)
  - Business logic constraints

---

# 2. Environment

- Python version: 3.x
- Framework: Flask
- API Documentation: Flask-RESTx (Swagger)
- Storage: In-memory repository
- Base URL: `http://127.0.0.1:5000`
- Swagger UI: `http://127.0.0.1:5000/api/v1/`

---

# 3. How to Run the API

From the project root directory:

```bash
export FLASK_APP=app
flask run
```

The API will be available at:

```
http://127.0.0.1:5000
```

Swagger documentation:

```
http://127.0.0.1:5000/api/v1/
```

---

# 4. How to Run Automated Tests

From the project root directory:

```bash
python -m unittest discover tests
```

Expected result:

```
Ran 22 tests
OK
```

---

# 5. Business Logic Validation Implemented

Validation is performed at the business layer (Facade / Models), not only at the API level.

## 5.1 Users

Validation rules:

- `first_name` must be a non-empty string
- `last_name` must be a non-empty string
- `email` must:
  - contain exactly one "@"
  - be normalized to lowercase
  - be unique
- `password`:
  - required at creation
  - minimum 8 characters
- `is_admin`:
  - cannot be set or modified by regular user
- Unknown fields are rejected

---

## 5.2 Amenities

Validation rules:

- `name`:
  - required
  - non-empty
  - max 50 characters
  - unique
  - normalized to lowercase
- `description`:
  - optional
  - max 255 characters
- Unknown fields rejected
- `id` cannot be modified

---

## 5.3 Places

Validation rules:

- `title` required and non-empty
- `price` must be > 0
- `latitude` must be between -90 and 90
- `longitude` must be between -180 and 180
- `owner_id`:
  - required
  - must reference an existing user
- `amenities`:
  - required
  - must be a list
  - all IDs must exist
- Owner cannot be modified after creation
- Amenities must be modified via dedicated methods

---

## 5.4 Reviews

Validation rules:

- `author_id` required
- `place_id` required
- Both must reference existing entities
- `comment` required
- `rating`:
  - required
  - must be between 1 and 5
- One review per (user, place)
- `author_id` and `place_id` cannot be modified

---

# 6. Manual Testing (Swagger)

Manual black-box testing was performed through Swagger UI.

## 6.1 Users — Covered Cases

✔ Create user (valid)  
✔ Create user duplicate email  
✔ Create user invalid fields  
✔ Create user invalid email  
✔ Update name  
✔ Update email (normalized)  
✔ Update password  
✔ Update duplicate email  
✔ Update forbidden `is_admin`  
✔ Update unknown field  
✔ Password too short  
✔ Get user by ID  
✔ Get user not found  
✔ List users  

---

## 6.2 Amenities — Covered Cases

✔ Create amenity  
✔ Create without description  
✔ Duplicate name  
✔ Empty name  
✔ Name spaces only  
✔ Name > 50 chars  
✔ Description > 255 chars  
✔ Update name  
✔ Update duplicate name  
✔ Unknown field update  
✔ Modify ID forbidden  
✔ Get by ID  
✔ Get not found  
✔ List all  

---

## 6.3 Places — Covered Cases

✔ Create place with empty amenities  
✔ Create place with valid amenity  
✔ Invalid amenity ID  
✔ Invalid latitude  
✔ Invalid owner  
✔ GET all places  
✔ GET place by ID  

---

## 6.4 Reviews — Covered Cases

✔ Create review  
✔ Duplicate review  
✔ Invalid rating (>5)  
✔ Update review  
✔ Delete review  
✔ GET deleted review (404)  

---

# 7. Automated Unit Tests

The `tests/` directory contains:

```
tests/
 ├── test_users.py
 ├── test_amenities.py
 ├── test_places.py
 ├── test_reviews.py
```

Total: **22 unit tests**

Each test file:

- Uses Flask test client
- Resets in-memory repositories before each test
- Ensures test isolation

Repositories are cleared in `setUp()`:

- user_repo
- amenity_repo
- place_repo
- review_repo

---

# 8. What the Unit Tests Cover

## Success Cases

- Valid user creation
- Valid amenity creation
- Valid place creation
- Valid review creation
- Valid updates
- Valid delete operations

---

## Invalid Input Cases

- Missing required fields
- Invalid email
- Duplicate email
- Duplicate amenity
- Invalid owner
- Invalid amenity ID
- Invalid rating
- Password too short
- Forbidden field modification
- Unknown fields

---

## Boundary Testing

- Latitude out of range
- Rating out of range
- Name length > limit
- Description length > limit

---

## Error Handling (404)

- Get non-existent user
- Get non-existent amenity
- Get non-existent place
- Get non-existent review
- Get deleted review

---

# 9. Test Isolation Strategy

The API uses an in-memory repository.

To ensure reliable tests:

- The global facade repositories are cleared before each test
- No test depends on data created by another test
- Each test creates its own required dependencies (user, place, amenity)

This guarantees deterministic and reproducible test execution.

---

# 10. Final Status

All validation rules, business constraints, boundary checks, and relationship integrity checks behave correctly.

Automated tests:

```
Ran 22 tests
OK
```

Manual tests through Swagger confirm consistent behavior.

The API satisfies:

- Input validation requirements
- Proper status code handling
- Business logic integrity
- Relationship consistency
- Error handling requirements

---

# Conclusion

Task 6 — Testing and Validation of the Endpoints — is fully implemented:

✔ Business layer validation  
✔ Manual Swagger testing  
✔ Automated unit tests  
✔ Boundary testing  
✔ Error handling verification  
✔ Proper documentation  

The implementation meets all stated objectives.

**Author:** **Gwenaelle PICHOT** - Student at Holberton School  
**Repository:** holbertonschool-hbnb  
**Directory:** part2/hbnb
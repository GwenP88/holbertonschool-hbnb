# HBnB Database Manual Testing Report (SQLite3)

## Project
**HBnB - Part 3**

| Field | Details |
|---|---|
| **File Tested** | `instance/development.db` |
| **Testing Type** | Manual database testing performed directly with `sqlite3` |
| **Tool Used** | `sqlite3` |
| **SQLite Version** | `3.45.1` |
| **Test Date** | `2026-03-13` |

**Objective:** This document records all manual tests executed directly in SQLite3 to validate the database schema, constraints, relationships, updates, deletions, and data integrity for the HBnB project.

---

## Table of Contents

1. [Test Environment](#1-test-environment)
2. [Tested Schema](#2-tested-schema)
3. [Foreign Key Activation](#3-foreign-key-activation)
4. [Table Creation and Schema Verification](#4-table-creation-and-schema-verification)
5. [Users Table Tests](#5-users-table-tests)
6. [Amenities Table Tests](#6-amenities-table-tests)
7. [Places Table Tests](#7-places-table-tests)
8. [place_amenity Association Table Tests](#8-place_amenity-association-table-tests)
9. [Reviews Table Tests](#9-reviews-table-tests)
10. [Relationship Query Tests](#10-relationship-query-tests)
11. [Integrity and Orphan Data Checks](#11-integrity-and-orphan-data-checks)
12. [Summary of Validated Behavior](#12-summary-of-validated-behavior)
13. [Final Database State](#13-final-database-state)
14. [Conclusion](#14-conclusion)

---

## 1. Test Environment

### Command used to open the database
```bash
sqlite3 instance/development.db
```

---

## 2. Tested Schema

The following tables were created and verified:

- `users`
- `amenities`
- `places`
- `place_amenity`
- `reviews`

### Expected Constraints

#### `users`
- `id` is the primary key
- `first_name` is required
- `last_name` is required
- `email` is required and unique
- `password` is required
- `is_admin` is required with default `FALSE`

#### `amenities`
- `id` is the primary key
- `name` is required and unique
- `description` is optional

#### `places`
- `id` is the primary key
- `title` is required
- `description` is required
- `price` must be greater than 0
- `latitude` must be between -90 and 90
- `longitude` must be between -180 and 180
- `owner_id` is required and references `users(id)`

#### `place_amenity`
- Composite primary key: `(place_id, amenity_id)`
- `place_id` references `places(id)`
- `amenity_id` references `amenities(id)`

#### `reviews`
- `id` is the primary key
- `comment` is required
- `rating` must be between 1 and 5
- `author_id` references `users(id)`
- `place_id` references `places(id)`
- Unique constraint on `(author_id, place_id)` to prevent duplicate reviews by the same user on the same place

---

## 3. Foreign Key Activation

### Test DB-001 — Check foreign key enforcement status

| | |
|---|---|
| **Command** | `PRAGMA foreign_keys;` |
| **Expected** | Foreign keys may be disabled by default in SQLite. |
| **Actual** | `0` |
| **Status** | ✅ Passed |

---

### Test DB-002 — Enable foreign key enforcement

```sql
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;
```

| | |
|---|---|
| **Expected** | Foreign key enforcement should be enabled. |
| **Actual** | `1` |
| **Status** | ✅ Passed |

---

## 4. Table Creation and Schema Verification

### Test DB-003 — Verify created tables

| | |
|---|---|
| **Command** | `.tables` |
| **Expected** | The five expected tables should exist. |
| **Actual** | `amenities   place_amenity   places   reviews   users` |
| **Status** | ✅ Passed |

---

### Test DB-004 — Verify schema definitions

```sql
.schema amenities
.schema places
.schema place_amenity
.schema reviews
.schema users
```

| | |
|---|---|
| **Expected** | Each table schema should match the project requirements and include all expected constraints. |
| **Actual** | All schemas matched the expected structure: primary keys present, unique constraints present, foreign keys present, check constraints present where required. |
| **Status** | ✅ Passed |

---

## 5. Users Table Tests

### Test US-001 — Insert valid admin user

```sql
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    TRUE
);
```

**Verification:**
```sql
SELECT id, first_name, last_name, email, is_admin FROM users;
```

| | |
|---|---|
| **Expected** | The admin user should be inserted successfully. |
| **Actual** | `36c9050e-ddd3-4c3b-9731-9f487208bbc1\|Admin\|HBnB\|admin@hbnb.io\|1` |
| **Status** | ✅ Passed |

---

### Test US-002 — Verify hashed password storage

```sql
SELECT password FROM users WHERE email = 'admin@hbnb.io';
```

| | |
|---|---|
| **Expected** | The password should be stored as a hash, not plain text. |
| **Actual** | `$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq` |
| **Status** | ✅ Passed |

---

### Test US-003 — Insert valid standard user

```sql
INSERT INTO users (
    id, created_at, updated_at, first_name, last_name, email, password, is_admin
) VALUES (
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'John',
    'Doe',
    'john@example.com',
    '$2b$12$abcdefghijklmnopqrstuv12345678901234567890123456789012',
    FALSE
);
```

**Verification:**
```sql
SELECT id, first_name, last_name, email, is_admin FROM users ORDER BY email;
```

| | |
|---|---|
| **Actual** | `36c9050e...\|Admin\|HBnB\|admin@hbnb.io\|1` and `11111111...\|John\|Doe\|john@example.com\|0` |
| **Status** | ✅ Passed |

---

### Test US-004 — Reject duplicate email

```sql
INSERT INTO users (
    id, created_at, updated_at, first_name, last_name, email, password, is_admin
) VALUES (
    '22222222-2222-2222-2222-222222222222',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Jane', 'Doe', 'john@example.com',
    '$2b$12$abcdefghijklmnopqrstuv12345678901234567890123456789012',
    FALSE
);
```

| | |
|---|---|
| **Expected** | Insertion should fail because email must be unique. |
| **Actual** | `Runtime error: UNIQUE constraint failed: users.email (19)` |
| **Status** | ✅ Passed |

---

### Test US-005 — Insert second valid standard user

```sql
INSERT INTO users (
    id, created_at, updated_at, first_name, last_name, email, password, is_admin
) VALUES (
    '99990000-0000-0000-0000-000000000000',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Alice', 'Smith', 'alice@example.com',
    '$2b$12$abcdefghijklmnopqrstuv12345678901234567890123456789012',
    FALSE
);
```

| | |
|---|---|
| **Status** | ✅ Passed |

---

### Test US-006 — Update first name

```sql
UPDATE users
SET first_name = 'Johnny', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';
```

| | |
|---|---|
| **Actual** | `Johnny\|2026-03-13 14:51:12` |
| **Status** | ✅ Passed |

---

### Test US-007 — Update email with valid new value

```sql
UPDATE users
SET email = 'johnny@example.com', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';
```

| | |
|---|---|
| **Actual** | `johnny@example.com` |
| **Status** | ✅ Passed |

---

### Test US-008 — Reject email update to existing email

```sql
UPDATE users
SET email = 'alice@example.com', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';
```

| | |
|---|---|
| **Expected** | Update should fail because email must remain unique. |
| **Actual** | `Runtime error: UNIQUE constraint failed: users.email (19)` |
| **Status** | ✅ Passed |

---

### Test US-009 — Prevent deletion of user referenced by a place

```sql
DELETE FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
```

| | |
|---|---|
| **Expected** | Deletion should fail because the user is referenced by `places.owner_id`. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test US-010 — Verify admin user still exists

```sql
SELECT email, is_admin FROM users WHERE email = 'admin@hbnb.io';
```

| | |
|---|---|
| **Actual** | `admin@hbnb.io\|1` |
| **Status** | ✅ Passed |

---

## 6. Amenities Table Tests

### Test AM-001 — Insert valid amenity: wifi

```sql
INSERT INTO amenities (id, created_at, updated_at, name, description)
VALUES (
    'c7a66c94-5a7e-4746-8c30-308f7695a36c',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'wifi',
    'High-speed wireless internet access available throughout the property.'
);
```

| | |
|---|---|
| **Status** | ✅ Passed |

---

### Test AM-002 — Reject duplicate amenity name

```sql
INSERT INTO amenities (id, created_at, updated_at, name, description)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'wifi', 'Duplicate wifi test'
);
```

| | |
|---|---|
| **Expected** | Insertion should fail because name must be unique. |
| **Actual** | `Runtime error: UNIQUE constraint failed: amenities.name (19)` |
| **Status** | ✅ Passed |

---

### Test AM-003 — Insert second valid amenity

```sql
INSERT INTO amenities (id, created_at, updated_at, name, description)
VALUES (
    '984fc2e7-bb3b-49ff-9c93-6fe57119ba53',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'swimming pool',
    'Private or shared swimming pool available for guests.'
);
```

| | |
|---|---|
| **Status** | ✅ Passed |

---

### Test AM-004 — Insert valid amenity with NULL description

```sql
INSERT INTO amenities (id, created_at, updated_at, name, description)
VALUES (
    '68615b51-bb01-4d8f-8222-a445efdf23b6',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'air conditioning', NULL
);
```

| | |
|---|---|
| **Expected** | NULL description should be accepted (optional field). |
| **Status** | ✅ Passed |

---

### Test AM-005 — Reject amenity without required name

```sql
INSERT INTO amenities (id, created_at, updated_at, description)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Missing name test'
);
```

| | |
|---|---|
| **Expected** | Insertion should fail because name is required. |
| **Actual** | `Runtime error: NOT NULL constraint failed: amenities.name (19)` |
| **Status** | ✅ Passed |

---

### Test AM-006 — Update amenity description

```sql
UPDATE amenities
SET description = 'Fast wireless internet in all rooms.', updated_at = CURRENT_TIMESTAMP
WHERE name = 'wifi';
```

| | |
|---|---|
| **Actual** | `wifi\|Fast wireless internet in all rooms.` |
| **Status** | ✅ Passed |

---

### Test AM-007 — Prevent deletion of amenity linked in place_amenity

```sql
DELETE FROM amenities WHERE id = 'c7a66c94-5a7e-4746-8c30-308f7695a36c';
```

| | |
|---|---|
| **Expected** | Deletion should fail because the amenity is referenced in `place_amenity`. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test AM-008 — Verify final amenity data

```sql
SELECT name, description
FROM amenities
WHERE id IN (
    'c7a66c94-5a7e-4746-8c30-308f7695a36c',
    '984fc2e7-bb3b-49ff-9c93-6fe57119ba53',
    '68615b51-bb01-4d8f-8222-a445efdf23b6'
)
ORDER BY name;
```

| Name | Description |
|---|---|
| air conditioning | *(null)* |
| swimming pool | Private or shared swimming pool available for guests. |
| wifi | Fast wireless internet in all rooms. |

**Status:** ✅ Passed

---

## 7. Places Table Tests

### Test PL-001 — Insert valid place

```sql
INSERT INTO places (
    id, created_at, updated_at, title, description, price, latitude, longitude, owner_id
) VALUES (
    '44444444-4444-4444-4444-444444444444',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Lake House', 'Beautiful house near the lake',
    120.50, 45.9000, 6.1300,
    '11111111-1111-1111-1111-111111111111'
);
```

| | |
|---|---|
| **Actual** | `44444444...\|Lake House\|120.5\|45.9\|6.13\|11111111...` |
| **Status** | ✅ Passed |

---

### Test PL-002 — Reject place with unknown owner

```sql
INSERT INTO places (
    id, created_at, updated_at, title, description, price, latitude, longitude, owner_id
) VALUES (
    '55555555-5555-5555-5555-555555555555',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Ghost House', 'Owner does not exist',
    100.00, 45.0, 5.0,
    '99999999-9999-9999-9999-999999999999'
);
```

| | |
|---|---|
| **Expected** | Insertion should fail because `owner_id` does not reference an existing user. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test PL-003 — Reject place with negative price

```sql
INSERT INTO places (...) VALUES (..., -10.00, ...);
```

| | |
|---|---|
| **Expected** | Insertion should fail because `price > 0`. |
| **Actual** | `Runtime error: CHECK constraint failed: price > 0 (19)` |
| **Status** | ✅ Passed |

---

### Test PL-004 — Reject place with invalid latitude

```sql
INSERT INTO places (...) VALUES (..., 100.0, 5.0, ...);
```

| | |
|---|---|
| **Expected** | Insertion should fail because latitude must be between -90 and 90. |
| **Actual** | `Runtime error: CHECK constraint failed: latitude BETWEEN -90 AND 90 (19)` |
| **Status** | ✅ Passed |

---

### Test PL-005 — Reject place with invalid longitude

```sql
INSERT INTO places (...) VALUES (..., 45.0, 190.0, ...);
```

| | |
|---|---|
| **Expected** | Insertion should fail because longitude must be between -180 and 180. |
| **Actual** | `Runtime error: CHECK constraint failed: longitude BETWEEN -180 AND 180 (19)` |
| **Status** | ✅ Passed |

---

### Test PL-006 — Update place price with valid value

```sql
UPDATE places
SET price = 150.00, updated_at = CURRENT_TIMESTAMP
WHERE id = '44444444-4444-4444-4444-444444444444';
```

| | |
|---|---|
| **Actual** | `Lake House\|150` |
| **Status** | ✅ Passed |

---

### Test PL-007 — Reject update with invalid price

```sql
UPDATE places
SET price = 0, updated_at = CURRENT_TIMESTAMP
WHERE id = '44444444-4444-4444-4444-444444444444';
```

| | |
|---|---|
| **Expected** | Update should fail because `price > 0`. |
| **Actual** | `Runtime error: CHECK constraint failed: price > 0 (19)` |
| **Status** | ✅ Passed |

---

### Test PL-008 — Prevent deletion of place referenced by place_amenity

```sql
DELETE FROM places WHERE id = '44444444-4444-4444-4444-444444444444';
```

| | |
|---|---|
| **Expected** | Deletion should fail because the place is referenced in `place_amenity`. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

## 8. place_amenity Association Table Tests

### Test PA-001 — Insert valid place/amenity association

```sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    'c7a66c94-5a7e-4746-8c30-308f7695a36c'
);
```

| | |
|---|---|
| **Actual** | `44444444...\|c7a66c94...` |
| **Status** | ✅ Passed |

---

### Test PA-002 — Reject duplicate place/amenity association

```sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    'c7a66c94-5a7e-4746-8c30-308f7695a36c'
);
```

| | |
|---|---|
| **Expected** | Insertion should fail because the composite primary key must be unique. |
| **Actual** | `Runtime error: UNIQUE constraint failed: place_amenity.place_id, place_amenity.amenity_id (19)` |
| **Status** | ✅ Passed |

---

### Test PA-003 — Reject association with unknown place

```sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('99999999-9999-9999-9999-999999999999', 'c7a66c94-5a7e-4746-8c30-308f7695a36c');
```

| | |
|---|---|
| **Expected** | Insertion should fail because `place_id` does not exist. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test PA-004 — Reject association with unknown amenity

```sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('44444444-4444-4444-4444-444444444444', '99999999-9999-9999-9999-999999999999');
```

| | |
|---|---|
| **Expected** | Insertion should fail because `amenity_id` does not exist. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test PA-005 — Delete existing association

```sql
DELETE FROM place_amenity
WHERE place_id = '44444444-4444-4444-4444-444444444444'
  AND amenity_id = 'c7a66c94-5a7e-4746-8c30-308f7695a36c';
```

| | |
|---|---|
| **Expected** | The existing association should be removed. |
| **Actual** | No error returned. |
| **Status** | ✅ Passed |

---

### Test PA-006 — Delete non-existing association

```sql
DELETE FROM place_amenity
WHERE place_id = '44444444-4444-4444-4444-444444444444'
  AND amenity_id = 'c7a66c94-5a7e-4746-8c30-308f7695a36c';
```

| | |
|---|---|
| **Expected** | No error should occur, but no row should be deleted. |
| **Actual** | No error returned. |
| **Status** | ✅ Passed |

---

### Test PA-007 — Reinsert association after deletion

```sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    'c7a66c94-5a7e-4746-8c30-308f7695a36c'
);
```

| | |
|---|---|
| **Expected** | The association should be inserted again successfully. |
| **Actual** | No error returned. |
| **Status** | ✅ Passed |

---

### Test PA-008 — Verify final association state

```sql
SELECT * FROM place_amenity
WHERE place_id = '44444444-4444-4444-4444-444444444444';
```

| | |
|---|---|
| **Actual** | One row confirmed after reinsertion. |
| **Status** | ✅ Passed |

---

## 9. Reviews Table Tests

### Test RV-001 — Insert valid review

```sql
INSERT INTO reviews (
    id, created_at, updated_at, comment, rating, author_id, place_id
) VALUES (
    'abcdabcd-abcd-abcd-abcd-abcdabcdabcd',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Very nice place', 5,
    '99990000-0000-0000-0000-000000000000',
    '44444444-4444-4444-4444-444444444444'
);
```

| | |
|---|---|
| **Actual** | `abcdabcd...\|Very nice place\|5\|99990000...\|44444444...` |
| **Status** | ✅ Passed |

---

### Test RV-002 — Reject review with rating above allowed range

```sql
INSERT INTO reviews (...) VALUES (..., 6, ...);
```

| | |
|---|---|
| **Expected** | Insertion should fail because rating must be between 1 and 5. |
| **Actual** | `Runtime error: CHECK constraint failed: rating BETWEEN 1 AND 5 (19)` |
| **Status** | ✅ Passed |

---

### Test RV-003 — Reject review with unknown author

```sql
INSERT INTO reviews (...) VALUES (..., '12121212-1212-1212-1212-121212121212', ...);
```

| | |
|---|---|
| **Expected** | Insertion should fail because `author_id` does not exist. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test RV-004 — Reject review with unknown place

```sql
INSERT INTO reviews (...) VALUES (..., '34343434-3434-3434-3434-343434343434');
```

| | |
|---|---|
| **Expected** | Insertion should fail because `place_id` does not exist. |
| **Actual** | `Runtime error: FOREIGN KEY constraint failed (19)` |
| **Status** | ✅ Passed |

---

### Test RV-005 — Reject duplicate review for same author/place pair

```sql
INSERT INTO reviews (
    id, created_at, updated_at, comment, rating, author_id, place_id
) VALUES (
    '13131313-1313-1313-1313-131313131313',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
    'Second review should fail', 3,
    '99990000-0000-0000-0000-000000000000',
    '44444444-4444-4444-4444-444444444444'
);
```

| | |
|---|---|
| **Expected** | Insertion should fail because `(author_id, place_id)` must be unique. |
| **Actual** | `Runtime error: UNIQUE constraint failed: reviews.author_id, reviews.place_id (19)` |
| **Status** | ✅ Passed |

---

### Test RV-006 — Update review comment and rating

```sql
UPDATE reviews
SET comment = 'Excellent stay', rating = 4, updated_at = CURRENT_TIMESTAMP
WHERE id = 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd';
```

| | |
|---|---|
| **Actual** | `Excellent stay\|4` |
| **Status** | ✅ Passed |

---

### Test RV-007 — Reject invalid review rating on update

```sql
UPDATE reviews
SET rating = 0, updated_at = CURRENT_TIMESTAMP
WHERE id = 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd';
```

| | |
|---|---|
| **Expected** | Update should fail because rating must remain between 1 and 5. |
| **Actual** | `Runtime error: CHECK constraint failed: rating BETWEEN 1 AND 5 (19)` |
| **Status** | ✅ Passed |

---

### Test RV-008 — Delete review

```sql
DELETE FROM reviews WHERE id = 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd';
```

| | |
|---|---|
| **Expected** | The review should be removed. |
| **Actual** | No row returned after verification. |
| **Status** | ✅ Passed |

---

## 10. Relationship Query Tests

### Test REL-001 — Verify place owner relationship

```sql
SELECT 
    p.id AS place_id,
    p.title,
    u.email AS owner_email
FROM places p
JOIN users u ON p.owner_id = u.id;
```

| | |
|---|---|
| **Expected** | The place should correctly resolve its owner. |
| **Actual** | `44444444...\|Lake House\|john@example.com` |
| **Status** | ✅ Passed |

---

### Test REL-002 — Verify place/amenity relationship

```sql
SELECT 
    p.title,
    a.name AS amenity_name
FROM place_amenity pa
JOIN places p ON pa.place_id = p.id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = '44444444-4444-4444-4444-444444444444';
```

| | |
|---|---|
| **Expected** | The selected place should return its linked amenity. |
| **Actual** | `Lake House\|wifi` |
| **Status** | ✅ Passed |

---

### Test REL-003 — Verify review joins with user and place

```sql
SELECT 
    r.id AS review_id,
    r.comment,
    r.rating,
    u.email AS author_email,
    p.title AS place_title
FROM reviews r
JOIN users u ON r.author_id = u.id
JOIN places p ON r.place_id = p.id;
```

| | |
|---|---|
| **Expected** | The review should correctly join to both author and place. |
| **Actual** | `abcdabcd...\|Very nice place\|5\|alice@example.com\|Lake House` |
| **Status** | ✅ Passed |

---

## 11. Integrity and Orphan Data Checks

### Test INT-001 — Verify final row counts

```sql
SELECT 'users' AS table_name, COUNT(*) AS total FROM users
UNION ALL
SELECT 'amenities', COUNT(*) FROM amenities
UNION ALL
SELECT 'places', COUNT(*) FROM places
UNION ALL
SELECT 'place_amenity', COUNT(*) FROM place_amenity
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews;
```

| Table | Count |
|---|---|
| users | 3 |
| amenities | 3 |
| places | 1 |
| place_amenity | 1 |
| reviews | 0 |

**Status:** ✅ Passed

---

### Test INT-002 — Check for places with missing owners

```sql
SELECT p.*
FROM places p
LEFT JOIN users u ON p.owner_id = u.id
WHERE u.id IS NULL;
```

| | |
|---|---|
| **Actual** | No row returned. |
| **Status** | ✅ Passed |

---

### Test INT-003 — Check for reviews with missing authors

```sql
SELECT r.*
FROM reviews r
LEFT JOIN users u ON r.author_id = u.id
WHERE u.id IS NULL;
```

| | |
|---|---|
| **Actual** | No row returned. |
| **Status** | ✅ Passed |

---

### Test INT-004 — Check for reviews with missing places

```sql
SELECT r.*
FROM reviews r
LEFT JOIN places p ON r.place_id = p.id
WHERE p.id IS NULL;
```

| | |
|---|---|
| **Actual** | No row returned. |
| **Status** | ✅ Passed |

---

### Test INT-005 — Check for place_amenity rows with missing places

```sql
SELECT pa.*
FROM place_amenity pa
LEFT JOIN places p ON pa.place_id = p.id
WHERE p.id IS NULL;
```

| | |
|---|---|
| **Actual** | No row returned. |
| **Status** | ✅ Passed |

---

### Test INT-006 — Check for place_amenity rows with missing amenities

```sql
SELECT pa.*
FROM place_amenity pa
LEFT JOIN amenities a ON pa.amenity_id = a.id
WHERE a.id IS NULL;
```

| | |
|---|---|
| **Actual** | No row returned. |
| **Status** | ✅ Passed |

---

## 12. Summary of Validated Behavior

The manual SQLite3 tests confirmed that:

| Category | Result |
|---|---|
| All expected tables created | ✅ |
| All schemas matched designed structure | ✅ |
| Foreign key enforcement (when enabled) | ✅ |
| Primary key constraints | ✅ |
| Unique constraint: `users.email` | ✅ |
| Unique constraint: `amenities.name` | ✅ |
| Unique constraint: `reviews(author_id, place_id)` | ✅ |
| Unique constraint: `place_amenity(place_id, amenity_id)` | ✅ |
| NOT NULL constraints | ✅ |
| CHECK constraint: `places.price` | ✅ |
| CHECK constraint: `places.latitude` | ✅ |
| CHECK constraint: `places.longitude` | ✅ |
| CHECK constraint: `reviews.rating` | ✅ |
| Foreign key: prevents invalid inserts | ✅ |
| Foreign key: prevents invalid deletes | ✅ |
| Update operations succeed on valid values | ✅ |
| Update operations fail on constraint violations | ✅ |
| Relationship JOINs return expected data | ✅ |
| No orphaned rows detected | ✅ |

---

## 13. Final Database State

At the end of testing, the database contained:

| Table | Rows |
|---|---|
| users | 3 |
| amenities | 3 |
| places | 1 |
| place_amenity | 1 |
| reviews | 0 |

---

## 14. Conclusion

The SQLite3 manual tests validate that the HBnB database schema behaves as expected for:

- **Entity creation** — all valid inserts succeed
- **Relationship enforcement** — foreign keys correctly link tables
- **Uniqueness rules** — duplicate values are rejected
- **Required field validation** — NOT NULL constraints enforced
- **Value range validation** — CHECK constraints enforced
- **Update safety** — valid updates succeed, invalid updates are rejected
- **Deletion protection** — referenced rows cannot be deleted
- **Referential integrity** — no orphaned rows present

> The current database structure is consistent with the project requirements and successfully enforces the main business rules at the SQL level.
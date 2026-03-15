# CRUD Tests — HBnB Project

This document explains the CRUD tests for the HBnB project, how to run them, and how to read the results.

---

## Prerequisites

- Python 3.x installed
- The application launched at least once to create the database
- Be at the root of the project `part3/hbnb/`

If the database does not exist yet:

```bash
python3 run.py
```

---

## Running the Tests

### Python Script (recommended)

Displays a clear summary with a checkmark or cross for each test:

```bash
python3 run_tests.py
```

### Raw SQL Script

Displays SQL results directly in the terminal:

```bash
sqlite3 -column -header instance/development.db < sql/test_crud.sql
```

> Note: With the raw SQL script, expected errors appear as `Runtime error` — this is normal and means the constraint is working correctly.

---

## Test Structure

The tests are organized into 6 sections:

### Section 0 — Initial Data
Verifies that the data inserted by `seed.sql` is present before starting.

| Test | Description |
|------|-------------|
| 0.1 | Admin exists with `is_admin = TRUE` |
| 0.2 | The 3 initial amenities are present (WiFi, Swimming Pool, Air Conditioning) |

---

### Section 1 — Valid Insertions
Verifies that correct insertions work without errors.

| Test | Description |
|------|-------------|
| 1.1 | Insert a valid user (John) |
| 1.2 | Insert a second valid user (Jane) |
| 1.3 | Insert a valid place (Test Place) |
| 1.4 | Insert a valid review (rating 5, by admin) |
| 1.5 | Insert a second valid review (rating 3, by Jane) |
| 1.6 | Link 2 amenities to the place (WiFi + Swimming Pool) |

---

### Section 2 — Constraints (must fail)
Verifies that database constraints correctly reject invalid data.

| Test | Description | Constraint tested |
|------|-------------|-------------------|
| 2.1 | Duplicate user email | `UNIQUE` on `users.email` |
| 2.2 | Duplicate amenity name | `UNIQUE` on `amenities.name` |
| 2.3 | Place with non-existent `owner_id` | `FOREIGN KEY` to `users` |
| 2.4 | Review with non-existent `author_id` | `FOREIGN KEY` to `users` |
| 2.5 | Review with non-existent `place_id` | `FOREIGN KEY` to `places` |
| 2.6 | Duplicate review same author/place | `UNIQUE` on `(author_id, place_id)` |
| 2.7 | Duplicate in `place_amenity` | Composite `PRIMARY KEY` |
| 2.8 | Negative price | `CHECK (price > 0)` |
| 2.9 | Latitude out of range | `CHECK (latitude BETWEEN -90 AND 90)` |
| 2.10 | Longitude out of range | `CHECK (longitude BETWEEN -180 AND 180)` |
| 2.11 | Rating out of range | `CHECK (rating BETWEEN 1 AND 5)` |

---

### Section 3 — Read (SELECT)
Verifies that data is correctly readable using joins.

| Test | Description |
|------|-------------|
| 3.1 | Read all users (3 expected) |
| 3.2 | Read places with their owner name |
| 3.3 | Read reviews with author and place |
| 3.4 | Read amenities of a place |
| 3.5 | Read places of a specific user |
| 3.6 | Read reviews of a specific place |

---

### Section 4 — Update
Verifies valid and invalid updates.

| Test | Description |
|------|-------------|
| 4.1 | Update a user's first name to `Johnny` |
| 4.2 | Update a place's price to `149.99` |
| 4.3 | Update a review's comment |
| 4.4 | Update a rating with an invalid value (must fail) |
| 4.5 | Update a price with a negative value (must fail) |

---

### Section 5 — Delete
Verifies valid and invalid deletions, and the correct deletion order.

| Test | Description |
|------|-------------|
| 5.1 | Delete a review |
| 5.2 | Delete a place that still has reviews (must fail) |
| 5.3 | Delete a user that still has places (must fail) |
| 5.4 | Delete in the correct order (reviews -> place_amenity -> places -> users) |

---

### Final Verification

| Test | Description |
|------|-------------|
| F.1 | Only the admin remains in `users` |
| F.2 | The 3 initial amenities are intact |
| F.3 | 0 places remaining |
| F.4 | 0 reviews remaining |

---

## Reading the Results

### With `run_tests.py`

```
============================================================
   CRUD TEST RESULTS -- HBnB
============================================================

  SECTION 0 -- Initial Data
  --------------------------------------------------
  [OK] [0.1] Admin exists with is_admin = TRUE
  [OK] [0.2] 3 initial amenities present

  SECTION 1 -- Valid Insertions
  --------------------------------------------------
  [OK] [1.1] Insert valid user (John)
  [OK] [1.2] Insert second valid user (Jane)
  [OK] [1.3] Insert valid place (Test Place)
  [OK] [1.4] Insert valid review (rating 5, by admin)
  [OK] [1.5] Insert second valid review (rating 3, by Jane)
  [OK] [1.6] Link 2 amenities to place (wifi + swimming pool)

  SECTION 2 -- Constraints (must fail)
  --------------------------------------------------
  [OK] [2.1] Duplicate user email (must fail)
  [OK] [2.2] Duplicate amenity name (must fail)
  [OK] [2.3] Place with non-existent owner (must fail)
  [OK] [2.4] Review with non-existent author (must fail)
  [OK] [2.5] Review with non-existent place (must fail)
  [OK] [2.6] Duplicate review same author/place (must fail)
  [OK] [2.7] Duplicate place_amenity (must fail)
  [OK] [2.8] Negative price (must fail)
  [OK] [2.9] Latitude out of range (must fail)
  [OK] [2.10] Longitude out of range (must fail)
  [OK] [2.11] Rating out of range (must fail)

  SECTION 3 -- Read
  --------------------------------------------------
  [OK] [3.1] Read all users (3 expected)
  [OK] [3.2] Read all places with their owner (1 expected)
  [OK] [3.3] Read all reviews with author and place (2 expected)
  [OK] [3.4] Read amenities of the test place (2 expected)
  [OK] [3.5] Read places of John (1 expected)
  [OK] [3.6] Read reviews of the test place (2 expected)

  SECTION 4 -- Update
  --------------------------------------------------
  [OK] [4.1] Update user first name -> Johnny
  [OK] [4.2] Update place price -> 149.99
  [OK] [4.3] Update review comment -> Updated comment!
  [OK] [4.4] Update rating with invalid value (must fail)
  [OK] [4.5] Update price with negative value (must fail)

  SECTION 5 -- Delete
  --------------------------------------------------
  [OK] [5.1] Delete a review
  [OK] [5.2] Delete place with existing reviews (must fail)
  [OK] [5.3] Delete user with existing places (must fail)
  [OK] [5.4] Delete in the correct order

  FINAL VERIFICATION
  --------------------------------------------------
  [OK] [F.1] Final check: only admin remains in users
  [OK] [F.2] Final check: 3 initial amenities intact
  [OK] [F.3] Final check: 0 places remaining
  [OK] [F.4] Final check: 0 reviews remaining

============================================================
  RESULTS: 31/31 tests passed -- ALL TESTS PASSED!
============================================================
```

### Understanding the symbols

| Symbol | Meaning |
|--------|---------|
| OK | Test passed -- the result matches what was expected |
| FAIL | Test failed -- the result does not match what was expected |

> A "must fail" test is marked OK when the database correctly rejects the invalid operation. If it shows FAIL, the constraint is not working.

---

## File Structure

```
part3/hbnb/
├── run_tests.py          <- Python test script (readable summary)
├── sql/
│   ├── schema.sql        <- table creation
│   ├── seed.sql          <- initial data (admin + amenities)
│   └── test_crud.sql     <- raw SQL tests
└── instance/
    └── development.db    <- SQLite database
```

---

## Important Notes

- The `run_tests.py` script automatically cleans the database before running the tests to avoid conflicts with existing data. The initial data (admin + amenities) is never deleted.
- SQLite foreign keys are disabled by default. Both the Python script and the SQL file automatically enable `PRAGMA foreign_keys = ON`.
- The tests are idempotent: you can run them as many times as you want and always get the same result.
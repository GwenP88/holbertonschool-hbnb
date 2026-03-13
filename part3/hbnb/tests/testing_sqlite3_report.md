# HBnB — Manual SQLite3 Testing Report

## Objective

This document summarizes the manual tests performed directly with `sqlite3` on `instance/development.db` to validate the HBnB database schema, constraints, relationships, and data integrity.

---

## Test Environment

| Property | Value |
|---|---|
| Tool | `sqlite3` |
| Database | `instance/development.db` |
| SQLite version | `3.45.1` |

Foreign keys were manually enabled before all tests:

```sql
PRAGMA foreign_keys = ON;
```

---

## 1. Schema Validation

The following tables were created and verified successfully:

- `users`
- `amenities`
- `places`
- `place_amenity`
- `reviews`

The `.schema` commands confirmed the presence of:

- Primary keys on all main entities
- Unique constraints on `users.email`, `amenities.name`, and `reviews(author_id, place_id)`
- Foreign keys between related tables
- Check constraints on `places.price`, `places.latitude`, `places.longitude`, and `reviews.rating`

---

## 2. Users Table

### Valid Inserts

| User | Email | Role |
|---|---|---|
| Admin | `admin@hbnb.io` | `is_admin = TRUE` |
| Regular user | `john@example.com` | Standard |
| Regular user | `alice@example.com` | Standard |

### Constraint Checks

| Test | Expected Error | Result |
|---|---|---|
| Duplicate email | `UNIQUE constraint failed: users.email` | ✅ Rejected |

### Password Verification

The `password` field was verified to contain a **hashed value**, not plain text.

### Update Tests

| Operation | Result |
|---|---|
| `first_name`: `John` → `Johnny` | ✅ Success |
| `email`: `john@example.com` → `johnny@example.com` | ✅ Success |
| `email`: `johnny@example.com` → `alice@example.com` (duplicate) | ❌ `UNIQUE constraint failed: users.email` |

### Delete Protection

Deleting the owner of an existing place was rejected:

```
FOREIGN KEY constraint failed
```

---

## 3. Amenities Table

### Valid Inserts

| Name | Description |
|---|---|
| `wifi` | — |
| `swimming pool` | — |
| `air conditioning` | `NULL` (optional field confirmed) |

### Constraint Checks

| Test | Expected Error | Result |
|---|---|---|
| Duplicate name | `UNIQUE constraint failed: amenities.name` | ✅ Rejected |
| Missing name | `NOT NULL constraint failed: amenities.name` | ✅ Rejected |

### Update Tests

| Operation | Result |
|---|---|
| `wifi` description → `Fast wireless internet in all rooms.` | ✅ Success |

### Delete Protection

Deleting an amenity linked in `place_amenity` was rejected:

```
FOREIGN KEY constraint failed
```

---

## 4. Places Table

### Valid Insert

A valid place was inserted successfully:

- **Name:** Lake House
- Valid `price`, `latitude`, `longitude`, and `owner_id`

### Constraint Checks

| Test | Expected Error | Result |
|---|---|---|
| Unknown `owner_id` | `FOREIGN KEY constraint failed` | ✅ Rejected |
| Negative price | `CHECK constraint failed: price > 0` | ✅ Rejected |
| Invalid latitude | `CHECK constraint failed: latitude BETWEEN -90 AND 90` | ✅ Rejected |
| Invalid longitude | `CHECK constraint failed: longitude BETWEEN -180 AND 180` | ✅ Rejected |

### Update Tests

| Operation | Result |
|---|---|
| `price`: `120.50` → `150.00` | ✅ Success |
| `price` → `0` | ❌ `CHECK constraint failed: price > 0` |

### Delete Protection

Deleting the place while still referenced in `place_amenity` was rejected:

```
FOREIGN KEY constraint failed
```

---

## 5. place_amenity Association Table

### Valid Insert

A valid association between **Lake House** and **wifi** was inserted successfully.

### Constraint Checks

| Test | Expected Error | Result |
|---|---|---|
| Duplicate association | `UNIQUE constraint failed: place_amenity.place_id, place_amenity.amenity_id` | ✅ Rejected |
| Unknown `place_id` | `FOREIGN KEY constraint failed` | ✅ Rejected |
| Unknown `amenity_id` | `FOREIGN KEY constraint failed` | ✅ Rejected |

### Delete Tests

| Operation | Result |
|---|---|
| Delete existing association | ✅ Success |
| Delete same association again | ✅ No error (safe) |
| Reinsert association after deletion | ✅ Success |

---

## 6. Reviews Table

### Valid Insert

A valid review was inserted successfully:

- **Author:** `alice@example.com`
- **Place:** Lake House
- **Rating:** 5

### Constraint Checks

| Test | Expected Error | Result |
|---|---|---|
| Rating above range | `CHECK constraint failed: rating BETWEEN 1 AND 5` | ✅ Rejected |
| Unknown `author_id` | `FOREIGN KEY constraint failed` | ✅ Rejected |
| Unknown `place_id` | `FOREIGN KEY constraint failed` | ✅ Rejected |
| Duplicate review (same author + place) | `UNIQUE constraint failed: reviews.author_id, reviews.place_id` | ✅ Rejected |

### Update Tests

| Operation | Result |
|---|---|
| Comment → `Excellent stay` | ✅ Success |
| `rating`: `5` → `4` | ✅ Success |
| `rating` → `0` | ❌ `CHECK constraint failed: rating BETWEEN 1 AND 5` |

### Delete Tests

| Operation | Result |
|---|---|
| Delete the review | ✅ Success |
| Verify row no longer exists | ✅ Confirmed |

---

## 7. Relationship Verification

The following join queries were executed successfully:

### Place → Owner

```
Lake House belongs to john@example.com
```

### Place → Amenities

```
Lake House is linked to wifi
```

### Review → Author → Place

The inserted review was correctly linked to both its author and its place.

---

## 8. Referential Integrity Checks

Final integrity queries confirmed **no orphan records** in the database:

| Check | Result |
|---|---|
| Places without existing owners | ✅ None |
| Reviews without existing authors | ✅ None |
| Reviews without existing places | ✅ None |
| `place_amenity` rows without existing places | ✅ None |
| `place_amenity` rows without existing amenities | ✅ None |

---

## 9. Final Database State

| Table | Row Count |
|---|---|
| `users` | 3 |
| `amenities` | 3 |
| `places` | 1 |
| `place_amenity` | 1 |
| `reviews` | 0 |

---

## Conclusion

The manual tests performed with SQLite3 confirmed that the HBnB database schema behaves correctly across all validated dimensions:

- ✅ Table creation and schema correctness
- ✅ Foreign key enforcement
- ✅ Unique constraints
- ✅ NOT NULL constraints
- ✅ Check constraints
- ✅ Insert, update, and delete validation
- ✅ Delete protection on referenced rows
- ✅ Relationship consistency
- ✅ Final referential integrity

The database structure correctly enforces the main business rules expected for the project.
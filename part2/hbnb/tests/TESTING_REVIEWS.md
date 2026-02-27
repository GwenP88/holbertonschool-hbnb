![Banner](assets/banner.png.png)

# HBnB API — Manual Testing Report (Swagger UI)
_Date: 27 Feb 2026_  
_Base URL: `http://127.0.0.1:5000`_  
_Swagger UI: `http://127.0.0.1:5000/api/v1/`_

> This report logs **all tests performed so far** during the session, including **valid + invalid** cases.  
> When a request/response wasn’t fully captured in the screenshots, I mark it as **(not captured)** rather than inventing values.

---

## Setup / Access

### TEST S0 — Root URL
- **Method/Endpoint:** `GET /`
- **Result:** `404 Not Found` (expected: app has no route on `/`)
- **Notes:** Normal. Swagger configured on `/api/v1/`.

### TEST S1 — Swagger UI
- **Method/Endpoint:** `GET /api/v1/`
- **Result:** Swagger UI loads with namespaces: `users`, `amenities`, `places`, `reviews` ✅

---

# REVIEWS — Full Test Set

## REVIEWS — Known Test Data (created/used during tests)

### Author (User B — primary test user)
- **id:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **email:** `new.email@example.com`
- **first_name/last_name:** `Updated User`
- **Note:** Used as `author_id` for review creation.

### Place used for reviews
- **Place P2 — Studio with wifi**
  - **id:** `8764f01f-654e-40ef-81cf-1f7752cdcc4a`
  - **title:** `Studio with wifi (updated)`
  - **owner_id:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`

### Secondary place (used for invalid rating test)
- **Place P1 — Cozy studio**
  - **id:** `e08851ce-589c-47e8-b967-8bd964cd902b`
  - **title:** `Cozy studio`

### Review created during tests

#### Review R1 — Valid Review
- **id:** `b2b4f7a0-88ec-4682-bc3a-53066850a66d`
- **author_id:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **place_id:** `8764f01f-654e-40ef-81cf-1f7752cdcc4a`
- **comment:** `Very nice place.`
- **rating:** `5`

---

## ✅ REVIEWS — Valid Cases

### TEST R1 — Create Review
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**

```
{
  "author_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "place_id": "8764f01f-654e-40ef-81cf-1f7752cdcc4a",
  "comment": "Very nice place.",
  "rating": 5
}
```

- **Status:** 201
- **Response body:**

```
{
  "id": "b2b4f7a0-88ec-4682-bc3a-53066850a66d",
  "comment": "Very nice place.",
  "rating": 5,
  "author_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "place_id": "8764f01f-654e-40ef-81cf-1f7752cdcc4a"
}
```

- **Note:** Review successfully created with rating inside valid bounds (1–5).

---

### TEST R2 — Update Review comment
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Path param:** `6b2b4f7a0-88ec-4682-bc3a-53066850a66d`
- **Request body:**

```
{
  "comment": "Updated comment: still a very nice place."
}
```

- **Status:** 200
- **Response body:**

```
{
  "id": "b2b4f7a0-88ec-4682-bc3a-53066850a66d",
  "comment": "Updated comment: still a very nice place.",
  "rating": 5
}
```

- **Note:** Comment updated successfully. Rating remained unchanged.

### TEST R3 — Delete Review
- **Method/Endpoint:** `DELETE /api/v1/reviews/`
- **Path param:** `b2b4f7a0-88ec-4682-bc3a-53066850a66d`
- **Status:** 200
- **Response body:**

```
{
  "message": "Review deleted successfully."
}
```

- **Note:** Review removed from storage.

---

### TEST R4 — GET Deleted Review (expected failure after delete)
- **Method/Endpoint:** `GET /api/v1/reviews/`
- **Path param:** `b2b4f7a0-88ec-4682-bc3a-53066850a66d`
- **Status:** 404
- **Response body:**

```
{
  "error": "Review not found"
}
```

- **Note:** Confirms deletion was effective.

---

## ❌ REVIEWS — Invalid / Error Cases

### TEST R5 — Duplicate Review (same author + same place)
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**

```
{
  "author_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "place_id": "8764f01f-654e-40ef-81cf-1f7752cdcc4a",
  "comment": "Very nice place.",
  "rating": 5
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Review already exists for this user and place."
}
```

- **Note:** Business rule enforced — one review per user per place.

---

### TEST R6 — Invalid Rating (> 5)
- **Method/Endpoint:** `POST /api/v1/reviews/`
- **Request body:**

```
{
  "author_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "place_id": "e08851ce-589c-47e8-b967-8bd964cd902b",
  "comment": "Bad rating test",
  "rating": 6
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Rating must be between 1 and 5."
}
```

- **Note:** Rating validation enforces bounds 1 ≤ rating ≤ 5.

---

## Notes / Observations

- A user can create only one review per place.
- Rating must be within 1 to 5 inclusive.
- Updating a review allows modifying the comment (rating remained unchanged in tested scenario).
- After deletion, attempting to fetch the review correctly returns 404.
- Business logic constraints and referential integrity (user + place) are enforced.

---

**Author:** **Gwenaelle PICHOT** - Student at Holberton School  
**Repository:** holbertonschool-hbnb  
**Directory:** part2/hbnb

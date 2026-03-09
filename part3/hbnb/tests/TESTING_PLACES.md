![Banner](assets/banner.png)

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
- **Result:** Swagger UI loads with namespaces: `users`, `amenities`, `places`, `reviews`

---

# PLACES — Full Test Set

## PLACES — Known Test Data (created/used during tests)

### Owner (User B — primary test user)
- **id:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **email initially:** `jay.p@example.com`
- **email later:** `new.email@example.com`
- **first_name/last_name later:** `Updated User`
- **Note:** Used as `owner_id` for all valid place creation attempts in this test suite.

### Amenity reference used in places
- **Amenity A — wifi**
  - **id:** `6b39efae-fbae-4ac9-b18c-7e3cb2008fce`
  - **name:** `wifi`
  - **description:** `High speed internet`
  - **Note:** Used as an element in the `amenities` list when creating a place with amenities.

### Places created during tests

#### Place P1 — Cozy studio (empty amenities list)
- **id:** `e08851ce-589c-47e8-b967-8bd964cd902b`
- **title:** `Cozy studio`
- **amenities:** `[]`
- **reviews:** `[]`

#### Place P2 — Studio with wifi (with amenity)
- **id:** `8764f01f-654e-40ef-81cf-1f7752cdcc4a`
- **title (later observed in GET/list):** `Studio with wifi (updated)`
- **price:** `60`
- **amenities:** contains `wifi` (`6b39efae-fbae-4ac9-b18c-7e3cb2008fce`)
- **reviews:** `[]` at time of GET place by ID

---

## ✅ PLACES — Valid Cases

### TEST P1 — Create Place WITH empty amenities
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**

```
{
  "title": "Cozy studio",
  "description": "Small but well located",
  "price": 45.5,
  "latitude": 45.923,
  "longitude": 6.869,
  "owner_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "amenities": []
}
```

- **Status:** 201
- **Response body:**

```
{
  "id": "e08851ce-589c-47e8-b967-8bd964cd902b",
  "title": "Cozy studio",
  "amenities": [],
  "reviews": []
}
```

- **Note:** Place created successfully with an empty amenities list.

---

### TEST P2 — Create Place WITH valid amenity
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**

```
{
  "title": "Studio with wifi",
  "description": "With internet",
  "price": 60,
  "latitude": 45.923,
  "longitude": 6.869,
  "owner_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "amenities": ["6b39efae-fbae-4ac9-b18c-7e3cb2008fce"]
}
```

- **Status:** 201
- **Response body:**

```
{
  "id": "8764f01f-654e-40ef-81cf-1f7752cdcc4a",
  "amenities": [
    {
      "id": "6b39efae-fbae-4ac9-b18c-7e3cb2008fce",
      "name": "wifi"
    }
  ]
}
```

- **Note:** Amenities appear expanded to objects (id + name) in captured response excerpt.

---

### TEST P3 — GET All Places
- **Method/Endpoint:** `GET /api/v1/places/`
- **Status:** 200
- **Response body:**

```
[
  {
    "id": "8764f01f-654e-40ef-81cf-1f7752cdcc4a",
    "title": "Studio with wifi (updated)",
    "price": 60
  }
]
```

---

### TEST P4 — GET Place by ID
- **Method/Endpoint:** `GET /api/v1/places/`
- **Path param:** `8764f01f-654e-40ef-81cf-1f7752cdcc4a`
- **Status:** 200
- **Response body:**

```
{
  "id": "8764f01f-654e-40ef-81cf-1f7752cdcc4a",
  "title": "Studio with wifi (updated)",
  "reviews": []
}
```

---

## ❌ PLACES — Invalid / Error Cases

### TEST P5 — Create Place WITHOUT amenities field
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**

```
{
  "title": "Cozy studio",
  "description": "Small but well located",
  "price": 45.5,
  "latitude": 45.923,
  "longitude": 6.869,
  "owner_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Amenities must be a list."
}
```

- **Note:** API requires amenities to exist and be a list (even if empty).

---

### TEST P6 — Create Place with INVALID amenity ID
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**

```
{
  "title": "Broken place",
  "description": "Invalid amenity",
  "price": 60,
  "latitude": 45.923,
  "longitude": 6.869,
  "owner_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "amenities": ["00000000-0000-0000-0000-000000000000"]
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Invalid amenity ID."
}
```

- **Note:** API requires amenities to exist and be a list (even if empty).

---

### TEST P7 — Create Place with INVALID latitude
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**

```
{
  "title": "Invalid lat",
  "description": "bad latitude",
  "price": 50,
  "latitude": 200,
  "longitude": 6.869,
  "owner_id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "amenities": []
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Latitude must be between -90 and 90."
}
```

---

### TEST P8 — Create Place with INVALID owner_id (owner not found)
- **Method/Endpoint:** `POST /api/v1/places/`
- **Request body:**

```
{
  "title": "Invalid owner",
  "description": "bad owner id",
  "price": 50,
  "latitude": 45.923,
  "longitude": 6.869,
  "owner_id": "00000000-0000-0000-0000-000000000000",
  "amenities": []
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Owner not found."
}
```

---

## Notes / Observations

- Creating a place fails if amenities is not provided at all, with error: "Amenities must be a list."
- Creating a place succeeds when amenities is provided as an empty list.
- Creating a place with amenities: ["<valid_amenity_id>"] succeeds and returns amenities expanded (in captured excerpt).

## Validations confirmed

- Invalid amenity IDs → ```Invalid amenity ID.```
- Latitude bounds → ```Latitude must be between -90 and 90.```
- Owner existence → ```Owner not found.```

---

**Author:** **Gwenaelle PICHOT** - Student at Holberton School  
**Repository:** holbertonschool-hbnb  
**Directory:** part2/hbnb

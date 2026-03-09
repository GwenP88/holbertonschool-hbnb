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

# AMENITIES — Full Test Set

## AMENITIES — Known Test Data

### Amenity A — wifi
- **id:** `6b39efae-fbae-4ac9-b18c-7e3cb2008fce`
- **name:** `wifi`
- **description:** `High speed internet`

### Amenity B — parking → renamed to garden
- **id:** `0301365b-5935-460d-8e14-dcaf160a09ae`
- **name:** `parking` then updated to `garden`
- **description:** `null`

### Amenity C — machine à café 
- **id:** `fc581dd5-dc4e-4532-8149-6fb2a5a9ca95`
- **name:** `machine à café`
- **description:** `Nespresso`

### Amenity D — serviettes 
- **id:** `b0d0506c-1df2-499d-a856-948eaa2cf369`
- **name:** `serviettes`
- **description:** `""`

---

## ✅ AMENITIES — Valid Cases

### TEST A1 — Create Amenity
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**

```
{
  "name": "WiFi",
  "description": "High speed internet"
}
```

- **Status:** 201
- **Response body:**

```
{
  "id": "6b39efae-fbae-4ac9-b18c-7e3cb2008fce",
  "name": "WiFi",
  "description": "High speed internet"
}
```

- **Note**: name appeared as "WiFi" in this response, but later GET returns "wifi" (Normalization is present at model level; response inconsistency might come from where the response is built.)

---

### TEST A2 — Create Amenity without description
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**

```
{
  "name": "Parking"
}
```

- **Response body:**
- **Status:** 200

```
{
  "id": "0301365b-5935-460d-8e14-dcaf160a09ae",
  "name": "parking",
  "description": null
}
```

---

### TEST A3 — Get Amenity by ID
- **Method/Endpoint:** `GET /api/v1/amenities/{amenity_id}`
- **Path param:** `6b39efae-fbae-4ac9-b18c-7e3cb2008fce`
- **Status:** 200
- **Response body:**

```
{
  "id": "6b39efae-fbae-4ac9-b18c-7e3cb2008fce",
  "name": "wifi",
  "description": "High speed internet"
}
```

---

### TEST A4 — List Amenities
- **Method/Endpoint:** `GET /api/v1/amenities/`
- **Status:** 200
- **Response body:**

```
[
  {
    "id": "6b39efae-fbae-4ac9-b18c-7e3cb2008fce",
    "name": "wifi",
    "description": "High speed internet"
  },
  {
    "id": "0301365b-5935-460d-8e14-dcaf160a09ae",
    "name": "parking",
    "description": null
  },
  {
    "id": "fc581dd5-dc4e-4532-8149-6fb2a5a9ca95",
    "name": "machine à café",
    "description": "Nespresso"
  },
  {
    "id": "b0d0506c-1df2-499d-a856-948eaa2cf369",
    "name": "serviettes",
    "description": ""
  }
]
```

- **Notes**: UTF-8 strings accepted

---

### TEST A5 — Update Amenity name
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `0301365b-5935-460d-8e14-dcaf160a09ae`
- **Request body:**

```
{
  "name": "Garden"
}
```

- **Status:** 200
- **Response body:**

```
{
  "id": "0301365b-5935-460d-8e14-dcaf160a09ae",
  "name": "garden",
  "description": null
}
```

- **Notes**: Normalized to lowercase on update

---

## ❌ AMENITIES — Invalid / Error Cases

### TEST A6 — Create Amenity with empty name
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**

```
{
  "name": "",
  "description": "test"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name is required."
}
```

- **Notes**: Here error comes from facade-level early check

---

### TEST A7 — Create Amenity with spaces-only name
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**

```
{
  "name": "",
  "description": "test"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name is required and must be a non-empty string."
}
```

- **Notes**: Here error comes from facade-level early check

---

### TEST A8 — Create Amenity name > 50 chars
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body (51 chars):**

```
{
  "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "description": "test"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name must not exceed 50 characters."
}
```

---

### TEST A9 — Create Amenity description > 255 chars
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body (description length 256):**

```
{
  "name": "pool",
  "description": "(256 characters string)"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Description must not exceed 255 characters."
}
```

---

### TEST A10 — Create Amenity duplicate name
- **Method/Endpoint:** `POST /api/v1/amenities/`
- **Request body:**

```
{
  "name": "wifi",
  "description": "another one"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name already exists."
}
```

---

### TEST A11 — Get Amenity not found
- **Method/Endpoint:** `GET /api/v1/amenities/{amenity_id}`
- **Path param:** `11111111-1111-1111-1111-111111111111`
- **Status:** 404
- **Response body:**

```
{
  "error": "Amenity not found"
}
```

---

### TEST A12 — Update Amenity to duplicate name
- **Method/Endpoint:** `GET /api/v1/amenities/{amenity_id}`
- **Path param:** `0301365b-5935-460d-8e14-dcaf160a09ae`

```
{
  "name": "wifi"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name already exists."
}
```

---

### TEST A13 — Update Amenity unknown field
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `0301365b-5935-460d-8e14-dcaf160a09ae`
- **Request body:**

```
{
  "color": "green"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "color is not a valid field."
}
```

---

### TEST A14 — Update Amenity modify id
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `0301365b-5935-460d-8e14-dcaf160a09ae`
- **Request body:**

```
{
  "id": "123"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "id cannot be modified."
}
```

---

### TEST A15 — Update Amenity empty name
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `0301365b-5935-460d-8e14-dcaf160a09ae`
- **Request body:**

```
{
  "name": ""
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name is required and must be a non-empty string."
}
```

---

### TEST A16 — Update Amenity name > 50 chars
- **Method/Endpoint:** `PUT /api/v1/amenities/{amenity_id}`
- **Path param:** `0301365b-5935-460d-8e14-dcaf160a09ae`
- **Request body (51 chars):**

```
{
  "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Name must not exceed 50 characters."
}
```

---

**Author:** **Gwenaelle PICHOT** - Student at Holberton School  
**Repository:** holbertonschool-hbnb  
**Directory:** part2/hbnb

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
- **Result:** Swagger UI loads with namespaces: `users`, `amenities`, `places`, `reviews`

---

# USERS — Full Test Set

## USERS — Known Test Data

### User A
- **id:** `a1b11a32-5e6c-4754-ab8e-4b01f99708fe`
- **email:** `john.doe@example.com`
- **first_name/last_name:** `John Doe`

### User B
- **id:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **email initially:** `jay.p@example.com`
- **email later:** `new.email@example.com`
- **first_name/last_name later:** `Updated User`

### User C
- **id:** `51752be6-e2df-4241-8458-34e380733aff`
- **email:** `invalid@email`
- **first_name/last_name:** `Test User`
- **Note:** This user existed in the system at the time we listed users; it violates the stricter email format rule now enforced.

---

## ✅ USERS — Valid Cases

### TEST U1 — Create User
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**

```
{
  "first_name": "Jay",
  "last_name": "Paletan",
  "email": "jay.p@example.com",
  "password": "Password123"
}
```

- **Status:** 200
- **Response body:**

```
{
  "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "first_name": "Jay",
  "last_name": "Paletan",
  "email": "jay.p@example.com"
}
```

- **Notes**: password not returned

---

### TEST U2 — Get User by ID
- **Method/Endpoint:** `GET /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Status:** 200
- **Response body:**

```
{
  "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "first_name": "Jay",
  "last_name": "Paletan",
  "email": "jay.p@example.com"
}
```

---

### TEST U3 — List Users
- **Method/Endpoint:** `GET /api/v1/users/`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Status:** 200
- **Response body:**

```
[
  {
    "id": "a1b11a32-5e6c-4754-ab8e-4b01f99708fe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  {
    "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
    "first_name": "Jay",
    "last_name": "Paletan",
    "email": "jay.p@example.com"
  }
]
```

- **Notes**: password not returned

---

### TEST U4 — Update User names
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "first_name": "Updated",
  "last_name": "User"
}
```

- **Status:** 200
- **Response body:**

```
{
  "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "first_name": "Updated",
  "last_name": "User",
  "email": "jay.p@example.com"
}
```

---

### TEST U5 — Update User email
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "email": "NEW.EMAIL@Example.COM"
}
```

- **Status:** 200
- **Response body:**

```
{
  "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "first_name": "Updated",
  "last_name": "User",
  "email": "new.email@example.com"
}
```

- **Notes**: email normalized to lowercase

---

### TEST U6 — Update User password
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "password": "NewPass123"
}
```

- **Status:** 200
- **Response body:**

```
{
  "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
  "first_name": "Updated",
  "last_name": "User",
  "email": "new.email@example.com"
}
```

- **Notes**: password not returned

---

## ❌ USERS — Invalid / Error Cases

### TEST U7 — Create User duplicate email
- **Method/Endpoint:** `POST /api/v1/users/`
- **Action:** You clicked Execute twice for the same payload.
- **Request body:**

```
{
  "first_name": "Jay",
  "last_name": "Paletan",
  "email": "jay.p@example.com",
  "password": "Password123"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Email already exists."
}
```

---

### TEST U8 — Get User not found
- **Method/Endpoint:** `GET /api/v1/users/{user_id}`
- **Path param:** `11111111-1111-1111-1111-111111111111`
- **Response body:**
- **Status:** 404
- **Response body:**

```
{
  "error": "User not found"
}
```

---

### TEST U9 — Create User invalid fields
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**

```
{
  "first_name": "",
  "last_name": "",
  "email": "invalid-email",
  "password": "Password123"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "first_name is required and must be a non-empty string."
}
```

- **Notes**: validation stops at first failing rule (expected)

---

### TEST U10 — Create User invalid email only
- **Method/Endpoint:** `POST /api/v1/users/`
- **Request body:**

```
{
  "first_name": "Test",
  "last_name": "User",
  "email": "invalid-email",
  "password": "Password123"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Email must contain exactly one '@'."
}
```

---

### TEST U11 — Update User duplicate email
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "email": "john.doe@example.com"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Email already exists."
}
```

---

### TEST U12 — Update password too short
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "first_name": "Updated",
  "last_name": "paletan",
  "email": "string",
  "password": "string"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "password must have at least 8 characters."
}
```

- **Notes**: Shows password validation is enforced on update

---

### TEST U13 — Update is_admin forbidden
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "is_admin": true
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "Only an administrator can modify is_admin."
}
```

---

### TEST U14 — Update unknown field
- **Method/Endpoint:** `PUT /api/v1/users/{user_id}`
- **Path param:** `e208d65f-ae9f-4910-91b1-c7b627371c7d`
- **Request body:**

```
{
  "nickname": "JayJay"
}
```

- **Status:** 400
- **Response body:**

```
{
  "error": "nickname is not a valid field."
}
```

---

### TEST U15 — List Users (state verification after later operations)
- **Method/Endpoint:** `GET /api/v1/users/`
- **Status:** 400
- **Response body:**

```
[
  {
    "id": "a1b11a32-5e6c-4754-ab8e-4b01f99708fe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  {
    "id": "e208d65f-ae9f-4910-91b1-c7b627371c7d",
    "first_name": "Updated",
    "last_name": "User",
    "email": "new.email@example.com"
  },
  {
    "id": "51752be6-e2df-4241-8458-34e380733aff",
    "first_name": "Test",
    "last_name": "User",
    "email": "invalid@email"
  }
]
```

- **Notes**: Presence of an invalid email user suggests pre-existing data or earlier relaxed rules

---

**Author:** **Gwenaelle PICHOT** - Student at Holberton School  
**Repository:** holbertonschool-hbnb  
**Directory:** part2/hbnb

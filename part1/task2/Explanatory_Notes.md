# Sequence Diagrams – Explanatory Notes

## Overview

The four sequence diagrams illustrate how the HBnB application processes API requests through a layered architecture composed of:

- **USER** (Client)
- **API** (Presentation Layer)
- **BUSINESS LOGIC** (Domain Layer)
- **DATABASE** (Persistence Layer)

Each diagram demonstrates:

- The normal execution flow (success case)
- At least one failure scenario per layer
- The interaction between components across layers

The goal is to visualize how responsibilities are distributed and how information flows from request to response.

---

# 1. User Registration – `POST /users`

```
sequenceDiagram
    autonumber
    participant USER as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    USER->>API: POST /users (registration data)
    API->>BL: validateRegistration(data)

    alt Invalid input (Presentation/API validation)
        BL-->>API: ValidationError
        API-->>USER: 400 Bad Request
    else Input valid
        BL->>DB: check_email(email)
        DB-->>BL: emailExists true/false

        alt Email already exists
            BL-->>API: EmailAlreadyExists
            API-->>USER: 409 Conflict
        else Email available
            BL->>DB: save_new_user(user)
            alt Database failure
                DB-->>BL: DatabaseError
                BL-->>API: PersistenceError
                API-->>USER: 500 Internal Server Error
            else Saved successfully
                DB-->>BL: UserSaved
                BL-->>API: UserCreated(user)
                API-->>USER: 201 Created
            end
        end
    end
```

## Purpose

This diagram represents the process of creating a new user account.

## Key Steps

1. The USER sends registration data to the API.
2. The API forwards the data to the Business Logic layer for validation.
3. The Business Logic checks whether the email already exists.
4. If the email is available, the user is saved in the database.
5. The API returns a `201 Created` response upon success.

## Failure Scenarios

- **Presentation Layer**: Invalid input format → `400 Bad Request`
- **Business Logic Layer**: Email already exists → `409 Conflict`
- **Persistence Layer**: Database error during save → `500 Internal Server Error`

## Layer Contribution

- API handles request validation and HTTP responses.
- Business Logic enforces domain rules (unique email).
- Database performs data persistence.

---

# 2. Place Creation – `POST /places`

```
ssequenceDiagram
    autonumber
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: POST /places (place data)
    API->>BL: validatePlace(data)

    alt Invalid data
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid data
        BL->>DB: check_owner(owner_id)
        DB-->>BL: ownerExists=true/false

        alt Owner not found
            BL-->>API: OwnerNotFound
            API-->>U: 404 Not Found
        else Owner exists
            BL->>DB: save_new_place(place)

            alt Database failur
                DB-->>BL: DatabaseError
                BL-->>API: PersistenceError
                API-->>U: 500 Internal Server Error
            else Saved successfully
                DB-->>BL: savedPlace
                BL-->>API: PlaceCreated(place)
                API-->>U: 201 Created
            end
        end
    end
```

## Purpose

This diagram illustrates how a user creates a new place listing.

## Key Steps

1. The USER submits place data.
2. The API validates the input format.
3. The Business Logic verifies that the owner exists.
4. If valid, the place is saved in the database.
5. The API returns `201 Created`.

## Failure Scenarios

- **Presentation Layer**: Invalid place data → `400 Bad Request`
- **Business Logic Layer**: Owner not found → `404 Not Found`
- **Persistence Layer**: Database failure during save → `500 Internal Server Error`

## Layer Contribution

- API ensures proper request structure.
- Business Logic validates ownership rules.
- Database stores the new place entity.

---

# 3. Review Submission – `POST /places/{place_id}/reviews`

```
sequenceDiagram
    autonumber
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: POST /places/{place_id}/reviews (review data)
    API->>BL: validateReview(data)

    alt Invalid data
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid data
        BL->>DB: check_user(author_id)
        DB-->>BL: userExists=true/false

        alt User not found
            BL-->>API: UserNotFound
            API-->>U: 404 Not Found
        else User exists
            BL->>DB: check_place(place_id)
            DB-->>BL: placeExists=true/false

            alt Place not found
                BL-->>API: PlaceNotFound
                API-->>U: 404 Not Found
            else Place exists
                BL->>DB: check_permission(author_id, place_id)
                DB-->>BL: permission=true/false

                alt Permission denied
                    BL-->>API: PermissionDenied
                    API-->>U: 403 Forbidden
                else Allowed
                    BL->>DB: save_new_review(review)

                    alt Database failure
                        DB-->>BL: DatabaseError
                        BL-->>API: PersistenceError
                        API-->>U: 500 Internal Server Error
                    else Saved successfully
                        DB-->>BL: savedReview
                        BL-->>API: ReviewCreated(savedReview)
                        API-->>U: 201 Created
                    end
                end
            end
        end
    end
```

## Purpose

This diagram models the process of submitting a review for a place.

## Key Steps

1. The USER submits review data.
2. The API validates the input.
3. The Business Logic verifies:
   - The user exists
   - The place exists
   - The user has permission (e.g., has booked the place)
4. If all conditions are satisfied, the review is saved.
5. The API returns `201 Created`.

## Failure Scenarios

- **Presentation Layer**: Invalid review data → `400 Bad Request`
- **Business Logic Layer**:
  - User not found → `404 Not Found`
  - Place not found → `404 Not Found`
  - Permission denied → `403 Forbidden`
- **Persistence Layer**: Database failure during save → `500 Internal Server Error`

## Layer Contribution

- API validates and formats requests/responses.
- Business Logic enforces domain constraints (existence checks and permissions).
- Database persists the review entity.

---

# 4. Fetching a List of Places – `GET /places`

```
sequenceDiagram
    autonumber  
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: GET /places?lat=&lon=&max_price=&amenity=
    API->>BL: validateFilters(filters)

    alt Invalid filters
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid filters
        BL->>BL: buildSearchCriteria(filters)

        opt lat & lon provided
            BL->>BL: computeGeoArea(lat, lon)
        end

        opt max_price provided
            BL->>BL: setMaxPrice(max_price)
        end

        opt amenity provided
            BL->>BL: addAmenityFilter(amenity)
        end

        BL->>BL: validateSearchCriteria(criteria)

        alt Business rule violation
            BL-->>API: InvalidSearchCriteria
            API-->>U: 422 Unprocessable Entity
        else Criteria accepted
            BL->>DB: search_places(criteria)

            alt Database failure
                DB-->>BL: DatabaseError
                BL-->>API: PersistenceError
                API-->>U: 500 Internal Server Error
            else Query success
                DB-->>BL: places[]
                BL-->>API: places[]
                API-->>U: 200 OK (places[])
            end
        end
    end
```

## Purpose

This diagram represents retrieving a filtered list of places based on search criteria.

## Key Steps

1. The USER sends a request with optional query parameters.
2. The API validates filter format.
3. The Business Logic builds and validates search criteria.
4. The Database executes the search query.
5. The API returns `200 OK` with the result list.

## Failure Scenarios

- **Presentation Layer**: Invalid filters → `400 Bad Request`
- **Business Logic Layer**: Invalid search criteria → `422 Unprocessable Entity`
- **Persistence Layer**: Database query failure → `500 Internal Server Error`

## Layer Contribution

- API validates request parameters and handles HTTP responses.
- Business Logic constructs and validates search criteria.
- Database executes the search and returns matching results.

---

# Overall Architectural Flow

Across all four diagrams, the interaction pattern remains consistent:

1. The USER initiates an HTTP request.
2. The API forwards the request to the Business Logic layer.
3. The Business Logic applies domain rules and interacts with the Database.
4. The Database performs data retrieval or persistence.
5. A response is propagated back through the layers to the USER.

This consistent layered interaction demonstrates:

- Clear separation of responsibilities
- Controlled communication between layers
- Proper error handling at each architectural level
- Structured request lifecycle management

These sequence diagrams collectively validate the understanding of how the HBnB application processes API calls within a layered architecture.

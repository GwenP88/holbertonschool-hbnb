
# User Registration – `POST /users`

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

---

# Place Creation – `POST /places`

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

---

# Review Submission – `POST /places/{place_id}/reviews`

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

---

# Fetching a List of Places – `GET /places`

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


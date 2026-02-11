# Explanatory Notes – Sequence Diagrams for API Calls - English version

## Overview

This section presents four sequence diagrams illustrating how the HBnB application processes key API requests.

Each diagram demonstrates the interaction between the three architectural layers:

- **Presentation Layer** (API / Controllers)
- **Business Logic Layer**
- **Persistence Layer** (Repositories / Database)

The goal of these diagrams is to clearly represent the flow of information and the sequence of operations required to handle each API request.

---

# User Registration – `POST /users`

```
sequenceDiagram
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: POST /users (registration data)
    API->>BL: validateRegistration(data)

    alt Invalid data
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid data
        BL->>DB: check_email(email)
        DB-->>BL: emailExists=true/false

        alt Email already exists
            BL-->>API: EmailAlreadyExists
            API-->>U: 409 Conflict
        else Email available
            BL->>DB: save_new_user(user)
            DB-->>BL: UserSaved
            BL-->>API: UserCreated(user)
            API-->>U: 201 Created
        end
    end
```

## Purpose

This API call allows a new user to create an account in the system.

## Interaction Flow

1. The **User** sends registration data to the API.
2. The **Presentation Layer** forwards the request to the Business Logic layer via the facade pattern
3. The **Business Logic Layer** validates the input data.
4. If validation fails:
   - The API returns `400 Bad Request`.
5. If validation succeeds:
   - The Business Logic checks email uniqueness via the Persistence layer.
6. The **Persistence Layer** queries the database.
7. If the email already exists:
   - The API returns `409 Conflict`.
8. If the email is available:
   - The new user is saved in the database.
   - The API returns `201 Created`.

## Layer Contributions

- **Presentation Layer**: Handles HTTP request and response.
- **Business Logic Layer**: Applies validation rules and uniqueness constraints.
- **Persistence Layer**: Executes database checks and saves the user.

---

# Place Creation – `POST /places`

```
sequenceDiagram
    participant U as USER
    participant API as API
    participant BL as BUSINESS LOGIC
    participant DB as DATABASE

    U->>API: POST /place (registration data)
    API->>BL: validatePlace(data)

    alt Invalid data
        BL-->>API: ValidationError
        API-->>U: 400 Bad Request
    else Valid data
        BL->>DB: check_owner(owner)
        DB-->>BL: ownerExists=true/false

        alt ownerExists == false
            BL-->>API: OwnerNotFound
            API-->>U: 404 Not Found
        else ownerExists == true
            BL->>DB: save_new_place(place)
            DB-->>BL: savedPlace
            BL-->>API: PlaceCreated(place)
            API-->>U: 201 Created
        end
    end
```

## Purpose

This API call enables a user to create a new place listing.

## Interaction Flow

1. The User sends place data to the API.
2. The API forwards the request to the Business Logic layer.
3. The Business Logic validates the place data.
4. If validation fails:
   - The API returns `400 Bad Request`.
5. If valid:
   - The Business Logic verifies that the owner exists.
6. If the owner does not exist:
   - The API returns `404 Not Found`.
7. If the owner exists:
   - The place is saved via the Persistence layer.
   - The API returns `201 Created`.

## Layer Contributions

- **Presentation Layer**: Receives request and formats response.
- **Business Logic Layer**: Enforces validation and ownership rules.
- **Persistence Layer**: Persists the new place in the database.

---

# Review Submission – `POST /places/{place_id}/reviews`

```
sequenceDiagram
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

        alt userExists == false
            BL-->>API: UserNotFound
            API-->>U: 404 Not Found
        else userExists == true
            BL->>DB: check_place(place_id)
            DB-->>BL: placeExists=true/false

            alt placeExists == false
                BL-->>API: PlaceNotFound
                API-->>U: 404 Not Found

            else placeExists == true
                BL->>DB: check_permission(author_id, place_id)
                DB-->>BL: permission=true/false

                alt permission == false
                    BL-->>API: PermissionDenied
                    API-->>U: 403 Forbidden

                else permission == true
                    BL->>DB: save_new_review(review)
                    DB-->>BL: savedReview
                    BL-->>API: ReviewCreated(savedReview)
                    API-->>U: 201 Created
                end
            end    
        end
    end
```

## Purpose

This API call allows a user to submit a review for a specific place.

## Interaction Flow

1. The User sends review data to the API.
2. The API forwards the request to the Business Logic layer.
3. The Business Logic validates review data.
4. If validation fails:
   - The API returns `400 Bad Request`.
5. If valid:
   - The system verifies that the user exists.
   - The system verifies that the place exists.
6. If either does not exist:
   - The API returns `404 Not Found`.
7. The system checks permission rules (e.g., user eligibility).
8. If permission is denied:
   - The API returns `403 Forbidden`.
9. If all checks pass:
   - The review is saved via the Persistence layer.
   - The API returns `201 Created`.

## Layer Contributions

- **Presentation Layer**: Manages HTTP communication.
- **Business Logic Layer**: Applies validation and business rules.
- **Persistence Layer**: Performs existence checks and saves review data.

---

# Fetching a List of Places – `GET /places`

```
sequenceDiagram
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

        BL->>DB: search_places(SearchCriteria)
        DB-->>BL: places[]
        BL-->>API: places[]
        API-->>U: 200 OK (places[])    
    end
```

## Purpose

This API call retrieves a list of places based on optional filtering criteria.

## Interaction Flow

1. The User sends a GET request with optional filters (location, price, amenities).
2. The API forwards filters to the Business Logic layer.
3. The Business Logic validates filter parameters.
4. If invalid:
   - The API returns `400 Bad Request`.
5. If valid:
   - The Business Logic builds search criteria.
   - Optional filters are applied.
6. The Persistence layer executes the database query.
7. The resulting list of places is returned.
8. The API sends `200 OK` with the result (or an empty list if no results are found)

## Layer Contributions

- **Presentation Layer**: Handles query parameters and formats response.
- **Business Logic Layer**: Constructs search criteria and applies filters.
- **Persistence Layer**: Executes database queries.

---

# Architectural Consistency

Across all four diagrams:

- Communication follows a strict layered structure.
- The Presentation Layer does not directly access the database.
- The Business Logic Layer centralizes validation and rule enforcement.
- The Persistence Layer handles all database interactions.

This separation of concerns ensures:

- Maintainability
- Scalability
- Clear responsibility boundaries
- Strong architectural consistency

---
---

# Notes explicatives – Diagrammes de séquence des appels API - version française

## Vue d’ensemble

Cette section présente quatre diagrammes de séquence illustrant le traitement des principales requêtes API de l’application HBnB.

Chaque diagramme met en évidence les interactions entre les trois couches de l’architecture :

- **Presentation Layer** (API / Controllers)
- **Business Logic Layer**
- **Persistence Layer** (Repositories / Database)

L’objectif est de visualiser clairement le flux d’informations et l’enchaînement des opérations nécessaires au traitement de chaque requête.

---

# Inscription utilisateur – `POST /users`

## Objectif

Cette API permet la création d’un nouveau compte utilisateur.

## Déroulement des interactions

1. L’**utilisateur** envoie ses données d’inscription à l’API.
2. La **Presentation Layer** transmet la requête à la Business Logic via la facade.
3. La **Business Logic Layer** valide les données reçues.
4. Si la validation échoue :
   - L’API retourne `400 Bad Request`.
5. Si la validation réussit :
   - La couche métier vérifie l’unicité de l’email via la Persistence Layer.
6. La **Persistence Layer** interroge la base de données.
7. Si l’email existe déjà :
   - L’API retourne `409 Conflict`.
8. Si l’email est disponible :
   - Le nouvel utilisateur est enregistré.
   - L’API retourne `201 Created`.

## Contribution des couches

- **Presentation Layer** : réception et envoi des réponses HTTP.
- **Business Logic Layer** : validation des données et application des règles métier.
- **Persistence Layer** : vérification en base et sauvegarde de l’utilisateur.

---

# Création d’une place – `POST /places`

## Objectif

Cette API permet à un utilisateur de créer une nouvelle annonce de logement.

## Déroulement des interactions

1. L’utilisateur envoie les données de la place à l’API.
2. L’API transmet la requête à la Business Logic.
3. La couche métier valide les données de la place.
4. Si la validation échoue :
   - L’API retourne `400 Bad Request`.
5. Si les données sont valides :
   - La couche métier vérifie l’existence du propriétaire.
6. Si le propriétaire n’existe pas :
   - L’API retourne `404 Not Found`.
7. Si le propriétaire existe :
   - La place est enregistrée via la Persistence Layer.
   - L’API retourne `201 Created`.

## Contribution des couches

- **Presentation Layer** : gestion de la requête et réponse HTTP.
- **Business Logic Layer** : validation et vérification des règles métier.
- **Persistence Layer** : enregistrement en base de données.

---

# Soumission d’un avis – `POST /places/{place_id}/reviews`

## Objectif

Cette API permet à un utilisateur de soumettre un avis sur un logement.

## Déroulement des interactions

1. L’utilisateur envoie les données de l’avis à l’API.
2. L’API transmet la requête à la Business Logic.
3. La couche métier valide les données.
4. Si la validation échoue :
   - L’API retourne `400 Bad Request`.
5. Si les données sont valides :
   - Vérification de l’existence de l’utilisateur.
   - Vérification de l’existence du logement.
6. Si l’un des deux n’existe pas :
   - L’API retourne `404 Not Found`.
7. Vérification des règles de permission.
8. Si l’utilisateur n’a pas l’autorisation :
   - L’API retourne `403 Forbidden`.
9. Si toutes les conditions sont respectées :
   - L’avis est enregistré via la Persistence Layer.
   - L’API retourne `201 Created`.

## Contribution des couches

- **Presentation Layer** : gestion de la communication HTTP.
- **Business Logic Layer** : application des validations et règles métier.
- **Persistence Layer** : vérifications en base et enregistrement de l’avis.

---

# Récupération d’une liste de places – `GET /places`

## Objectif

Cette API permet de récupérer une liste de logements selon des critères de recherche optionnels (localisation, prix, équipements).

## Déroulement des interactions

1. L’utilisateur envoie une requête GET avec des filtres éventuels.
2. L’API transmet les paramètres à la Business Logic.
3. La couche métier valide les filtres.
4. Si les filtres sont invalides :
   - L’API retourne `400 Bad Request`.
5. Si les filtres sont valides :
   - Construction des critères de recherche.
   - Application des filtres optionnels.
6. La Persistence Layer exécute la requête en base.
7. Les résultats sont retournés à la couche métier.
8. L’API renvoie `200 OK` avec la liste des places (ou une liste vide si aucun résultat)

## Contribution des couches

- **Presentation Layer** : gestion des paramètres et réponse.
- **Business Logic Layer** : construction des critères et orchestration.
- **Persistence Layer** : exécution des requêtes SQL.

---

# Cohérence architecturale

Dans l’ensemble des diagrammes :

- La communication respecte strictement l’architecture en couches.
- La Presentation Layer n’accède jamais directement à la base de données.
- La Business Logic centralise toutes les validations et règles métier.
- La Persistence Layer gère exclusivement les interactions avec la base.

Cette séparation garantit :

- Une meilleure maintenabilité
- Une architecture évolutive
- Un faible couplage entre les couches
- Une responsabilité claire pour chaque composant

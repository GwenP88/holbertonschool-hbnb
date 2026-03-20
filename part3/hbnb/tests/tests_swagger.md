# Tests Swagger — HBnB Project

Ce document liste tous les tests manuels à effectuer via l'interface Swagger UI du projet HBnB.

---

## Accéder à Swagger

1. Lancer l'application :
```bash
python3 run.py
```

2. Ouvrir dans le navigateur :
```
http://127.0.0.1:5000/api/v1/
```

---

## Ordre recommandé des tests

```
1. Auth       → obtenir un token JWT
2. Users      → créer et gérer des utilisateurs
3. Amenities  → créer et gérer des amenities
4. Places     → créer et gérer des lieux
5. Reviews    → créer et gérer des reviews
6. Admin      → tester les privilèges admin
7. DELETE     → tous les tests de suppression (à faire en dernier)
```

---

## Comment utiliser l'authentification dans Swagger

Certains endpoints nécessitent un token JWT. Voici comment l'utiliser :

1. Obtenir un token via `POST /api/v1/auth/login`
2. Copier la valeur de `access_token` dans la réponse
3. Cliquer sur le bouton **Authorize** en haut à droite de Swagger
4. Saisir : `Bearer <ton_token>` (exemple : `Bearer eyJhbGci...`)
5. Cliquer sur **Authorize** puis **Close**

> Les endpoints avec un cadenas nécessitent cette étape.

---

## IDs utiles (données initiales — seed)

| Donnée | ID |
|--------|----|
| Admin | `36c9050e-ddd3-4c3b-9731-9f487208bbc1` |
| User John Doe | `7b5a1b64-4bb6-4581-8cd3-019863c6e3d9` |
| User Jane Doe | `76efe665-2825-4883-a382-8d76bb8ea472` |
| Amenity WiFi | `93282ff9-7af0-4b0d-beb1-407b6998b01f` |
| Amenity Swimming Pool | `984fc2e7-bb3b-49ff-9c93-6fe57119ba53` |
| Amenity Air Conditioning | `68615b51-bb01-4d8f-8222-a445efdf23b6` |
| Amenity Rooftop Terrace | `c5fcec1a-08f8-40ba-beae-fc5717d8f60e` |
| Amenity Private Parking | `62b29136-184b-48fd-88d5-650e8e94a3ab` |
| Place John — Sunny Loft | `ef448d99-36e6-4aa6-880a-59bab9bbe439` |
| Place Jane — Cozy Cottage | `9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d` |
| Review 1 — Jane → Sunny Loft | `27d20295-4bfe-4058-9232-d299cfcffefb` |
| Review 2 — John → Cozy Cottage | `12e8bfd8-968f-45b2-a450-8d0b6b7449de` |

---

## Données de test disponibles à créer (dans l'ordre)

### Users à créer (via `POST /api/v1/users/`)

| # | Prénom | Nom | Email | Password |
|---|--------|-----|-------|----------|
| 3 | Gwen | Aelle | `gwenaelle@email.com` | `string123` |
| 4 | Clem | Ent | `clement@email.com` | `string123` |
| 5 | Jen | Peplu | `jenpeplu@email.com` | `string123` |

### Amenities à créer (via `POST /api/v1/amenities/` — token admin requis)

| # | Nom | Description |
|---|-----|-------------|
| 3 | Fireplace | A cozy wood-burning fireplace perfect for cold evenings. |
| 4 | Hot Tub | *(sans description)* |
| 5 | Gym Room | *(sans description)* |
| 6 | Sauna | *(sans description)* |

### Places à créer

| # | Titre | Owner | Prix | Description | Latitude | Longitude |
|---|-------|-------|------|-------------|----------|-----------|
| 3 | Stylish Studio near the Beach | Gwen Aelle | 110 | A sleek and stylish studio just a 5-minute walk from the beach. Great ocean vibes. | 43.2965 | 5.3698 |
| 4 | Mountain Chalet with Fireplace | Clem Ent | 130 | A warm and rustic chalet nestled in the mountains, perfect for winter escapes. | 45.9237 | 6.8694 |
| 5 | Zen Garden Apartment | Jen Peplu | 85 | A tranquil apartment with a private zen garden, ideal for relaxation and meditation. | 43.6047 | 1.4442 |

### Reviews à créer

| # | Place | Reviewer | Note | Commentaire |
|---|-------|----------|------|-------------|
| 3 | Cozy Cottage (Jane) | Clem Ent | 5 | The cottage was an amazing retreat. The fireplace made everything so cozy. Highly recommended for a quiet weekend. |
| 4 | Stylish Studio (Gwen) | Jen Peplu | 4 | Charming and peaceful. The surroundings are beautiful. The parking was very convenient too. |
| 5 | Stylish Studio (Gwen) | John Doe | 5 | Super studio, very clean and stylish. The beach is literally around the corner. Perfect summer spot! |
| 6 | Mountain Chalet (Clem) | Jane Doe | 4 | Good value for money. A bit remote but perfectly designed. The fireplace was a bonus! |
| 7 | Mountain Chalet (Clem) | Jen Peplu | 5 | The chalet exceeded all expectations. Warm, rustic, and the views were absolutely stunning. A must-do! |
| 8 | Zen Garden (Jen) | John Doe | 5 | Such a peaceful stay. The zen garden is truly one of a kind. Perfect to recharge after a long week. |
| 9 | Zen Garden (Jen) | Gwen Aelle | 5 | So peaceful and unique. The zen garden is a real gem. I felt completely recharged after my stay. |
| 10 | Sunny Loft (John) | Clem Ent | 4 | Lovely loft with a very original concept. The rooftop terrace and hot tub were a great touch. Would recommend. |

---

## SECTION 1 — Auth

### TEST 1.1 — Login admin (valide)
**Endpoint :** `POST /api/v1/auth/login`

**Body :**
```json
{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}
```
**Résultat attendu :** `200 OK` avec un `access_token`

---

### TEST 1.2 — Login avec mauvais mot de passe
**Endpoint :** `POST /api/v1/auth/login`

**Body :**
```json
{
  "email": "admin@hbnb.io",
  "password": "mauvais_mot_de_passe"
}
```
**Résultat attendu :** `401 Invalid credentials`

---

### TEST 1.3 — Login avec email inexistant
**Endpoint :** `POST /api/v1/auth/login`

**Body :**
```json
{
  "email": "inexistant@test.com",
  "password": "admin1234"
}
```
**Résultat attendu :** `401 Invalid credentials`

---

### TEST 1.4 — Accès à l'endpoint protégé avec token valide
**Endpoint :** `GET /api/v1/auth/protected`
Requiert un token

**Résultat attendu :** `200 OK` avec `Hello, user <id>`

---

### TEST 1.5 — Accès à l'endpoint protégé sans token
**Endpoint :** `GET /api/v1/auth/protected`
(sans token dans Authorize)

**Résultat attendu :** `401 Missing Authorization Header`

---

## SECTION 2 — Users

### TEST 2.1 — Créer un utilisateur valide
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Gwen",
  "last_name": "Aelle",
  "email": "gwenaelle@email.com",
  "password": "string123"
}
```
**Résultat attendu :** `201` avec l'id du nouvel utilisateur

---

### TEST 2.2 — Créer un deuxième utilisateur
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Clem",
  "last_name": "Ent",
  "email": "clement@email.com",
  "password": "string123"
}
```
**Résultat attendu :** `201` avec l'id du nouvel utilisateur

---

### TEST 2.3 — Créer un utilisateur avec email déjà existant
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Duplicate",
  "last_name": "User",
  "email": "johndoe@email.com",
  "password": "string123"
}
```
**Résultat attendu :** `400 Email already exists`

---

### TEST 2.4 — Créer un utilisateur avec email invalide sans @
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Bad",
  "last_name": "Email",
  "email": "pas_un_email",
  "password": "string123"
}
```
**Résultat attendu :** `400 Email must contain exactly one '@'.`

---

### TEST 2.5 — Créer un utilisateur avec email invalide avec un espace
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Bad",
  "last_name": "Space",
  "email": "john doe@test.com",
  "password": "string123"
}
```
**Résultat attendu :** `400 Email must not contain spaces.`

---

### TEST 2.6 — Créer un utilisateur avec email invalide sans domaine
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Bad",
  "last_name": "Domain",
  "email": "john@test",
  "password": "string123"
}
```
**Résultat attendu :** `400 Email must have a valid domain with a '.'`

---

### TEST 2.7 — Créer un utilisateur avec mot de passe trop court
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Short",
  "last_name": "Pass",
  "email": "short@test.com",
  "password": "abc"
}
```
**Résultat attendu :** `400 password must have at least 8 characters`

---

### TEST 2.8 — Lister tous les utilisateurs
**Endpoint :** `GET /api/v1/users/`

**Résultat attendu :** `200` avec la liste de tous les utilisateurs

---

### TEST 2.9 — Récupérer un utilisateur par ID
**Endpoint :** `GET /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9`

Utiliser l'id de John du seed.

**Résultat attendu :** `200` avec les détails de John

---

### TEST 2.10 — Récupérer un utilisateur inexistant
**Endpoint :** `GET /api/v1/users/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 User not found`

---

### TEST 2.11 — Modifier son propre profil (valide)
Requiert le token de John (`johndoe@email.com` / `string123`)

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9`

**Body :**
```json
{
  "first_name": "Johnny",
  "last_name": "Doe"
}
```
**Résultat attendu :** `200` avec le prénom mis à jour

---

### TEST 2.12 — Modifier le profil d'un autre utilisateur sans être admin
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/76efe665-2825-4883-a382-8d76bb8ea472`

**Body :**
```json
{
  "first_name": "Hacked"
}
```
**Résultat attendu :** `403 Unauthorized action`

---

### TEST 2.13 — Essayer de modifier l'email via PUT /users
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9`

**Body :**
```json
{
  "email": "newemail@test.com"
}
```
**Résultat attendu :** `400 You cannot modify email or password`

---

### TEST 2.14 — Modifier l'email via l'endpoint dédié
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9/email`

**Body :**
```json
{
  "email": "john_new@test.com"
}
```
**Résultat attendu :** `200 Email updated successfully`

---

### TEST 2.15 — Modifier le mot de passe
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9/password`

**Body :**
```json
{
  "password": "newpassword123"
}
```
**Résultat attendu :** `200 Password updated successfully`

---

## SECTION 3 — Amenities

### TEST 3.1 — Créer une amenity (valide, en tant qu'admin)
Requiert le token admin

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "Fireplace",
  "description": "A cozy wood-burning fireplace perfect for cold evenings."
}
```
**Résultat attendu :** `201` avec l'id de la nouvelle amenity

---

### TEST 3.2 — Créer une amenity sans être admin
Requiert le token de John (non admin)

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "Jacuzzi",
  "description": "Luxury jacuzzi"
}
```
**Résultat attendu :** `403 Admin privileges required`

---

### TEST 3.3 — Créer une amenity avec nom déjà existant
Requiert le token admin

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "wifi",
  "description": "Another wifi"
}
```
**Résultat attendu :** `400 Amenity already exists`

---

### TEST 3.4 — Lister toutes les amenities
**Endpoint :** `GET /api/v1/amenities/`

**Résultat attendu :** `200` avec la liste

---

### TEST 3.5 — Récupérer une amenity par ID
**Endpoint :** `GET /api/v1/amenities/c5fcec1a-08f8-40ba-beae-fc5717d8f60e`

Utiliser l'id de Rooftop Terrace du seed.

**Résultat attendu :** `200` avec les détails de Rooftop Terrace

---

### TEST 3.6 — Récupérer une amenity inexistante
**Endpoint :** `GET /api/v1/amenities/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Amenity not found`

---

### TEST 3.7 — Modifier une amenity (en tant qu'admin)
Requiert le token admin

**Endpoint :** `PUT /api/v1/amenities/62b29136-184b-48fd-88d5-650e8e94a3ab`

Utiliser l'id de Private Parking du seed.

**Body :**
```json
{
  "name": "Parking gratuit",
  "description": "Free private parking"
}
```
**Résultat attendu :** `200` avec les détails mis à jour

---

### TEST 3.8 — Modifier une amenity sans être admin
Requiert le token de John

**Endpoint :** `PUT /api/v1/amenities/62b29136-184b-48fd-88d5-650e8e94a3ab`

**Body :**
```json
{
  "name": "Hacked amenity"
}
```
**Résultat attendu :** `403 Admin privileges required`

---

## SECTION 4 — Places

### TEST 4.1 — Créer un lieu (valide)
Requiert le token de Gwen (`gwenaelle@email.com` / `string123`)

**Endpoint :** `POST /api/v1/places/`

**Body :**
```json
{
  "title": "Stylish Studio near the Beach",
  "description": "A sleek and stylish studio just a 5-minute walk from the beach. Great ocean vibes.",
  "price": 110.00,
  "latitude": 43.2965,
  "longitude": 5.3698,
  "amenities": []
}
```
**Résultat attendu :** `201` avec les détails du lieu

---

### TEST 4.2 — Créer un lieu avec amenities
Requiert le token de Clem (`clement@email.com` / `string123`)

**Endpoint :** `POST /api/v1/places/`

**Body :**
```json
{
  "title": "Mountain Chalet with Fireplace",
  "description": "A warm and rustic chalet nestled in the mountains, perfect for winter escapes.",
  "price": 130.00,
  "latitude": 45.9237,
  "longitude": 6.8694,
  "amenities": ["<amenity_id_fireplace>", "62b29136-184b-48fd-88d5-650e8e94a3ab"]
}
```
**Résultat attendu :** `201` avec les amenities incluses dans la réponse

---

### TEST 4.3 — Créer un lieu avec prix négatif
Requiert le token de John

**Endpoint :** `POST /api/v1/places/`

**Body :**
```json
{
  "title": "Bad Place",
  "description": "Prix invalide",
  "price": -50.00,
  "latitude": 48.8566,
  "longitude": 2.3522
}
```
**Résultat attendu :** `400 Price must be a positive number`

---

### TEST 4.4 — Créer un lieu avec latitude invalide
Requiert le token de John

**Endpoint :** `POST /api/v1/places/`

**Body :**
```json
{
  "title": "Bad Place",
  "description": "Latitude invalide",
  "price": 50.00,
  "latitude": 999.00,
  "longitude": 2.3522
}
```
**Résultat attendu :** `400 Latitude must be between -90 and 90`

---

### TEST 4.5 — Lister tous les lieux
**Endpoint :** `GET /api/v1/places/`

**Résultat attendu :** `200` avec la liste des places

---

### TEST 4.6 — Récupérer un lieu par ID
**Endpoint :** `GET /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439`

Utiliser l'id du Sunny Loft de John (seed).

**Résultat attendu :** `200` avec détails de la place

---

### TEST 4.7 — Récupérer un lieu inexistant
**Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Place not found`

---

### TEST 4.8 — Modifier son propre lieu
Requiert le token de John

**Endpoint :** `PUT /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439`

**Body :**
```json
{
  "title": "Sunny Loft in the City Center - Rénové",
  "price": 150.00
}
```
**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 4.9 — Modifier le lieu d'un autre utilisateur
Requiert le token de Jane (`janedoe@email.com` / `string123`)

**Endpoint :** `PUT /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439`

**Body :**
```json
{
  "title": "Hacked place"
}
```
**Résultat attendu :** `403 Unauthorized action`

---

### TEST 4.10 — Ajouter une amenity à un lieu en tant que propriétaire
Requiert le token de John

**Endpoint :** `POST /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

Utiliser l'id WiFi du seed : `93282ff9-7af0-4b0d-beb1-407b6998b01f`

**Résultat attendu :** `200` avec l'amenity ajoutée dans la liste

---

### TEST 4.11 — Ajouter une amenity à un lieu sans être propriétaire
Requiert le token de Jane

**Endpoint :** `POST /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

**Résultat attendu :** `403 Unauthorized action`

---

### TEST 4.12 — Ajouter une amenity déjà liée
Requiert le token de John

**Endpoint :** `POST /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

(même amenity WiFi que le TEST 4.10)

**Résultat attendu :** `400 Amenity already added`

---

### TEST 4.13 — Ajouter une amenity inexistante
Requiert le token de John

**Endpoint :** `POST /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Amenity not found`

---

### TEST 4.14 — Retirer une amenity d'un lieu en tant que propriétaire
Requiert le token de John

**Endpoint :** `DELETE /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

**Résultat attendu :** `200` avec l'amenity retirée de la liste

---

### TEST 4.15 — Retirer une amenity non liée
Requiert le token de John

**Endpoint :** `DELETE /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

(même amenity WiFi, déjà retirée au TEST 4.14)

**Résultat attendu :** `400 Amenity not linked`

---

## SECTION 5 — Reviews

### TEST 5.1 — Créer une review (valide, par Gwen sur la place de John)
Requiert le token de Gwen (`gwenaelle@email.com` / `string123`)

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Fantastic loft, very well located. Modern and clean, I loved every minute of my stay!",
  "rating": 5,
  "place_id": "ef448d99-36e6-4aa6-880a-59bab9bbe439"
}
```
**Résultat attendu :** `201` avec les détails de la review

---

### TEST 5.2 — Créer une review sur son propre lieu
Requiert le token de John (`johndoe@email.com` / `string123`)

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Mon propre loft est super",
  "rating": 5,
  "place_id": "ef448d99-36e6-4aa6-880a-59bab9bbe439"
}
```
**Résultat attendu :** `400 You cannot review your own place`

---

### TEST 5.3 — Créer une deuxième review sur le même lieu (doublon)
Requiert le token de Jane (`janedoe@email.com` / `string123`)

> Jane a déjà une review sur le Sunny Loft (seed : `27d20295-4bfe-4058-9232-d299cfcffefb`)

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Deuxième review",
  "rating": 3,
  "place_id": "ef448d99-36e6-4aa6-880a-59bab9bbe439"
}
```
**Résultat attendu :** `400 Review already exists for this user and place`

---

### TEST 5.4 — Créer une review avec rating invalide
Requiert le token admin

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Note invalide",
  "rating": 10,
  "place_id": "ef448d99-36e6-4aa6-880a-59bab9bbe439"
}
```
**Résultat attendu :** `400 Rating must be between 1 and 5`

---

### TEST 5.5 — Créer une review sur un lieu inexistant
Requiert le token de Gwen

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Lieu inexistant",
  "rating": 3,
  "place_id": "00000000-0000-0000-0000-000000000000"
}
```
**Résultat attendu :** `404 Place not found`

---

### TEST 5.6 — Lister toutes les reviews
**Endpoint :** `GET /api/v1/reviews/`

**Résultat attendu :** `200` avec la liste des reviews

---

### TEST 5.7 — Récupérer une review par ID
**Endpoint :** `GET /api/v1/reviews/27d20295-4bfe-4058-9232-d299cfcffefb`

Utiliser l'id de la review 1 du seed (Jane → Sunny Loft).

**Résultat attendu :** `200` avec les détails de la review

---

### TEST 5.8 — Récupérer les reviews d'un lieu
**Endpoint :** `GET /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/reviews`

**Résultat attendu :** `200` avec les reviews du Sunny Loft

---

### TEST 5.9 — Récupérer les reviews d'un lieu inexistant
**Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000/reviews`

**Résultat attendu :** `404 Place not found`

---

### TEST 5.10 — Modifier sa propre review
Requiert le token de Jane

**Endpoint :** `PUT /api/v1/reviews/27d20295-4bfe-4058-9232-d299cfcffefb`

Utiliser l'id de la review 1 du seed (review de Jane).

**Body :**
```json
{
  "comment": "Appartement encore mieux que prévu !",
  "rating": 5
}
```
**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 5.11 — Modifier la review d'un autre utilisateur
Requiert le token de John

**Endpoint :** `PUT /api/v1/reviews/27d20295-4bfe-4058-9232-d299cfcffefb`

Utiliser l'id de la review 1 du seed (review de Jane).

**Body :**
```json
{
  "comment": "Review hackée"
}
```
**Résultat attendu :** `403 Unauthorized action`

---

## SECTION 6 — Admin

### TEST 6.0 — Login admin
**Endpoint :** `POST /api/v1/auth/login`

**Body :**
```json
{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}
```
**Résultat attendu :** `200 OK` avec un `access_token`

---

### TEST 6.1 — Admin modifie le profil d'un autre utilisateur
Requiert le token admin

**Endpoint :** `PUT /api/v1/users/76efe665-2825-4883-a382-8d76bb8ea472`

**Body :**
```json
{
  "first_name": "Janette",
  "last_name": "Doe"
}
```
**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 6.2 — Admin modifie un utilisateur inexistant
Requiert le token admin

**Endpoint :** `PUT /api/v1/users/00000000-0000-0000-0000-000000000000`

**Body :**
```json
{
  "first_name": "Ghost"
}
```
**Résultat attendu :** `404 User not found`

---

### TEST 6.3 — Admin tente de modifier email/password via PUT /users
Requiert le token admin

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9`

**Body :**
```json
{
  "email": "adminchange@test.com"
}
```
**Résultat attendu :** `400 You cannot modify email or password`

---

### TEST 6.4 — Admin modifie l'email d'un autre utilisateur via endpoint dédié
Requiert le token admin

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9/email`

**Body :**
```json
{
  "email": "john_admin_update@test.com"
}
```
**Résultat attendu :** `200 Email updated successfully`

---

### TEST 6.5 — Admin modifie le mot de passe d'un autre utilisateur via endpoint dédié
Requiert le token admin

**Endpoint :** `PUT /api/v1/users/7b5a1b64-4bb6-4581-8cd3-019863c6e3d9/password`

**Body :**
```json
{
  "password": "adminreset123"
}
```
**Résultat attendu :** `200 Password updated successfully`

---

### TEST 6.6 — Admin crée une amenity
Requiert le token admin

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "Sauna VIP",
  "description": "Luxury private sauna with aromatherapy options."
}
```
**Résultat attendu :** `201` avec le détail de la nouvelle amenity

---

### TEST 6.7 — Admin modifie une amenity existante
Requiert le token admin

**Endpoint :** `PUT /api/v1/amenities/<amenity_id_sauna>`

Utiliser l'id de Sauna noté lors de INIT-A6.

**Body :**
```json
{
  "name": "Sauna VIP",
  "description": "Luxury private sauna"
}
```
**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 6.8 — Admin modifie une amenity inexistante
Requiert le token admin

**Endpoint :** `PUT /api/v1/amenities/00000000-0000-0000-0000-000000000000`

**Body :**
```json
{
  "name": "Ghost amenity"
}
```
**Résultat attendu :** `404 Amenity not found`

---

### TEST 6.9 — Admin modifie le lieu d'un autre utilisateur
Requiert le token admin

**Endpoint :** `PUT /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439`

**Body :**
```json
{
  "title": "Sunny Loft - Modified by admin",
  "price": 180.00
}
```
**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 6.10 — Admin ajoute une amenity à un lieu qui ne lui appartient pas
Requiert le token admin

**Endpoint :** `POST /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

Utiliser l'id WiFi du seed : `93282ff9-7af0-4b0d-beb1-407b6998b01f`

**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 6.11 — Admin retire une amenity d'un lieu qui ne lui appartient pas
Requiert le token admin

**Endpoint :** `DELETE /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439/amenities/93282ff9-7af0-4b0d-beb1-407b6998b01f`

**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 6.12 — Admin crée une review sur le lieu d'un autre utilisateur
Requiert le token admin

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Admin review test on John's loft",
  "rating": 4,
  "place_id": "ef448d99-36e6-4aa6-880a-59bab9bbe439"
}
```
**Résultat attendu :** `201` avec les détails de la review

---

### TEST 6.13 — Admin modifie la review d'un autre utilisateur
Requiert le token admin

**Endpoint :** `PUT /api/v1/reviews/27d20295-4bfe-4058-9232-d299cfcffefb`

Utiliser l'id de la review 1 du seed (review de Jane).

**Body :**
```json
{
  "comment": "Review updated by admin",
  "rating": 4
}
```
**Résultat attendu :** `200` avec les données mises à jour

---

## SECTION 7 — DELETE

### Ordre recommandé des suppressions

```
1. Reviews      → supprimer les reviews avant les places/utilisateurs
2. Places       → supprimer les places avant les utilisateurs
3. Amenities    → supprimer les amenities créées en test
4. Users        → supprimer les comptes utilisateurs en dernier
```

---

### Reviews

#### TEST DEL-R1 — Supprimer sa propre review
Requiert le token de Jane

**Endpoint :** `DELETE /api/v1/reviews/27d20295-4bfe-4058-9232-d299cfcffefb`

Utiliser l'id de la review 1 du seed (review de Jane sur le Sunny Loft).

**Résultat attendu :** `200 Review deleted successfully`

---

#### TEST DEL-R2 — Supprimer la review d'un autre utilisateur (non admin)
Requiert le token de John

**Endpoint :** `DELETE /api/v1/reviews/<review_id_3>`

Utiliser l'id de INIT-R3 (review de Clem sur le Cozy Cottage).

**Résultat attendu :** `403 Unauthorized action`

---

#### TEST DEL-R3 — Supprimer une review inexistante
Requiert le token admin

**Endpoint :** `DELETE /api/v1/reviews/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Review not found`

---

#### TEST DEL-R4 — Admin supprime la review d'un autre utilisateur
Requiert le token admin

**Endpoint :** `DELETE /api/v1/reviews/<review_id_3>`

Utiliser l'id de INIT-R3 (review de Clem sur le Cozy Cottage).

**Résultat attendu :** `200 Review deleted successfully`

---

#### TEST DEL-R5 — Admin supprime une review inexistante
Requiert le token admin

**Endpoint :** `DELETE /api/v1/reviews/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Review not found`

---

### Places

#### TEST DEL-P1 — Supprimer son propre lieu
Requiert le token de Clem (`clement@email.com` / `string123`)

**Endpoint :** `DELETE /api/v1/places/<place_id_clem>`

Utiliser l'id noté lors de INIT-P4.

**Résultat attendu :** `200 Place deleted successfully`

---

#### TEST DEL-P2 — Supprimer le lieu d'un autre utilisateur sans être admin
Requiert le token de Jane

**Endpoint :** `DELETE /api/v1/places/ef448d99-36e6-4aa6-880a-59bab9bbe439`

**Résultat attendu :** `403 Unauthorized action`

---

#### TEST DEL-P3 — Supprimer un lieu inexistant
Requiert le token admin

**Endpoint :** `DELETE /api/v1/places/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Place not found`

---

#### TEST DEL-P4 — Vérifier qu'un lieu supprimé n'est plus récupérable
**Endpoint :** `GET /api/v1/places/<place_id_clem>`

Utiliser l'id supprimé au DEL-P1.

**Résultat attendu :** `404 Place not found`

---

#### TEST DEL-P5 — Vérifier que les reviews du lieu supprimé ont aussi disparu
**Endpoint :** `GET /api/v1/places/<place_id_clem>/reviews`

**Résultat attendu :** `404 Place not found`

---

#### TEST DEL-P6 — Admin supprime le lieu d'un autre utilisateur
Requiert le token admin

**Endpoint :** `DELETE /api/v1/places/<place_id_jen>`

Utiliser l'id noté lors de INIT-P5.

**Résultat attendu :** `200 Place deleted successfully`

---

### Amenities

#### TEST DEL-A1 — Supprimer une amenity sans être admin
Requiert le token de John

**Endpoint :** `DELETE /api/v1/amenities/<amenity_id_gym>`

Utiliser l'id noté lors de INIT-A5.

**Résultat attendu :** `403 Unauthorized action`

---

#### TEST DEL-A2 — Supprimer une amenity existante en tant qu'admin
Requiert le token admin

**Endpoint :** `DELETE /api/v1/amenities/<amenity_id_gym>`

**Résultat attendu :** `200 Amenity deleted successfully`

---

#### TEST DEL-A3 — Supprimer une amenity inexistante
Requiert le token admin

**Endpoint :** `DELETE /api/v1/amenities/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Amenity not found`

---

#### TEST DEL-A4 — Vérifier qu'une amenity supprimée n'est plus récupérable
**Endpoint :** `GET /api/v1/amenities/<amenity_id_gym>`

Utiliser l'id supprimé au DEL-A2.

**Résultat attendu :** `404 Amenity not found`

---

### Users

#### TEST DEL-U1 — Supprimer son propre compte
Requiert le token de Gwen (`gwenaelle@email.com` / `string123`)

**Endpoint :** `DELETE /api/v1/users/<user_id_gwen>`

Utiliser l'id noté lors de INIT-U3.

**Résultat attendu :** `200 User deleted successfully`

> Ce test supprime aussi les reviews écrites par Gwen, sa place, les reviews sur sa place, ainsi que les liens entre sa place et ses amenities.

---

#### TEST DEL-U2 — Supprimer le compte d'un autre utilisateur sans être admin
Requiert le token de John

**Endpoint :** `DELETE /api/v1/users/76efe665-2825-4883-a382-8d76bb8ea472`

**Résultat attendu :** `403 Unauthorized action`

---

#### TEST DEL-U3 — Supprimer un utilisateur inexistant
Requiert le token admin

**Endpoint :** `DELETE /api/v1/users/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 User not found`

---

#### TEST DEL-U4 — Admin supprime le compte d'un autre utilisateur
Requiert le token admin

**Endpoint :** `DELETE /api/v1/users/<user_id_jen>`

Utiliser l'id noté lors de INIT-U5.

**Résultat attendu :** `200 User deleted successfully`

> Ce test supprime aussi les reviews écrites par Jen, ses places éventuelles, les reviews de ses places, ainsi que les liens place/amenity associés.

---

## Récapitulatif des tests

| Section | Nombre de tests | Valides | Invalides (doivent échouer) |
|---------|-----------------|---------|------------------------------|
| Init | 13 | 13 | 0 |
| Auth | 5 | 2 | 3 |
| Users | 15 | 7 | 8 |
| Amenities | 8 | 3 | 5 |
| Places | 15 | 5 | 10 |
| Reviews | 11 | 4 | 7 |
| Admin | 14 | 9 | 5 |
| Delete | 18 | 9 | 9 |
| **Total** | **99** | **52** | **47** |
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

Les tests sont à effectuer dans cet ordre car certains dépendent des résultats précédents (token JWT, IDs créés).

```
1. Auth       → obtenir un token JWT
2. Users      → créer et gérer des utilisateurs
3. Amenities  → créer et gérer des amenities
4. Places     → créer et gérer des lieux
5. Reviews    → créer et gérer des reviews
```

---

## Comment utiliser l'authentification dans Swagger

Certains endpoints nécessitent un token JWT. Voici comment l'utiliser :

1. Obtenir un token via `POST /api/v1/auth/login`
2. Copier la valeur de `access_token` dans la réponse
3. Cliquer sur le bouton **Authorize** en haut à droite de Swagger
4. Saisir : `Bearer <ton_token>` (exemple : `Bearer eyJhbGci...`)
5. Cliquer sur **Authorize** puis **Close**

> Les endpoints avec un cadenas necessitent cette etape.

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
**Resultat attendu :** `200 OK` avec un `access_token`

> Sauvegarder le token — il sera utilise pour tous les tests suivants.

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
**Resultat attendu :** `401 Invalid credentials`

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
**Resultat attendu :** `401 Invalid credentials`

---

### TEST 1.4 — Acces a l'endpoint protege avec token valide
**Endpoint :** `GET /api/v1/auth/protected`
Requiert un token

**Resultat attendu :** `200 OK` avec `Hello, user <id>`

---

### TEST 1.5 — Acces a l'endpoint protege sans token
**Endpoint :** `GET /api/v1/auth/protected`
(sans token dans Authorize)

**Resultat attendu :** `401 Missing Authorization Header`

---

## SECTION 2 — Users

### TEST 2.1 — Creer un utilisateur valide
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@test.com",
  "password": "password123"
}
```
**Resultat attendu :** `201` avec l'id du nouvel utilisateur

> Sauvegarder l'id de l'utilisateur cree.

---

### TEST 2.2 — Creer un deuxieme utilisateur
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@test.com",
  "password": "password123"
}
```
**Resultat attendu :** `201` avec l'id du nouvel utilisateur

> Sauvegarder l'id de cet utilisateur.

---

### TEST 2.3 — Creer un utilisateur avec email deja existant
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Duplicate",
  "last_name": "User",
  "email": "john@test.com",
  "password": "password123"
}
```
**Resultat attendu :** `400 Email already exists`

---

### TEST 2.4 — Creer un utilisateur avec email invalide sans @
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Bad",
  "last_name": "Email",
  "email": "pas_un_email",
  "password": "password123"
}
```
**Resultat attendu :** `400 Email must contain exactly one '@'.`

### TEST 2.5 — Creer un utilisateur avec email invalide avec un espace
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Bad",
  "last_name": "Space",
  "email": "john doe@test.com",
  "password": "password123"
}
```
**Resultat attendu :** `400 Email must not contain spaces.`

### TEST 2.6 — Creer un utilisateur avec email invalide avec absence de domaine
**Endpoint :** `POST /api/v1/users/`

**Body :**
```json
{
  "first_name": "Bad",
  "last_name": "Domain",
  "email": "john@test",
  "password": "password123"
}
```
**Resultat attendu :** `400 Email must have a valid domain with a '.'`

---

### TEST 2.7 — Creer un utilisateur avec mot de passe trop court
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
**Resultat attendu :** `400 password must have at least 8 characters`

---

### TEST 2.8 — Lister tous les utilisateurs
**Endpoint :** `GET /api/v1/users/`

**Resultat attendu :** `200` avec la liste de tous les utilisateurs (admin + John + Jane)

---

### TEST 2.9 — Recuperer un utilisateur par ID
**Endpoint :** `GET /api/v1/users/<user_id>`

Utiliser l'id de John cree au TEST 2.1.

**Resultat attendu :** `200` avec les details de John

---

### TEST 2.10 — Recuperer un utilisateur inexistant
**Endpoint :** `GET /api/v1/users/00000000-0000-0000-0000-000000000000`

**Resultat attendu :** `404 User not found`

---

### TEST 2.11 — Modifier son propre profil (valide)
Requiert le token de John (faire POST /auth/login avec john@test.com / password123)

**Endpoint :** `PUT /api/v1/users/<user_id_john>`

**Body :**
```json
{
  "first_name": "Johnny",
  "last_name": "Doe"
}
```
**Resultat attendu :** `200` avec le prenom mis a jour

---

### TEST 2.12 — Modifier le profil d'un autre utilisateur sans etre admin
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/<user_id_jane>`

**Body :**
```json
{
  "first_name": "Hacked"
}
```
**Resultat attendu :** `403 Unauthorized action`

---

### TEST 2.13 — Essayer de modifier l'email via PUT /users
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/<user_id_john>`

**Body :**
```json
{
  "email": "newemail@test.com"
}
```
**Resultat attendu :** `400 You cannot modify email or password`

---

### TEST 2.14 — Modifier l'email via l'endpoint dedie
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/<user_id_john>/email`

**Body :**
```json
{
  "email": "john_new@test.com"
}
```
**Resultat attendu :** `200 Email updated successfully`

---

### TEST 2.15 — Modifier le mot de passe
Requiert le token de John

**Endpoint :** `PUT /api/v1/users/<user_id_john>/password`

**Body :**
```json
{
  "password": "newpassword123"
}
```
**Resultat attendu :** `200 Password updated successfully`

---

## SECTION 3 — Amenities

### TEST 3.1 — Creer une amenity (valide, en tant qu'admin)
Requiert le token admin

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "Parking",
  "description": "Private parking space available"
}
```
**Resultat attendu :** `201` avec l'id de la nouvelle amenity

> Sauvegarder l'id de l'amenity creee.

---

### TEST 3.2 — Creer une amenity sans etre admin
Requiert le token de John (non admin)

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "Jacuzzi",
  "description": "Luxury jacuzzi"
}
```
**Resultat attendu :** `403 Admin privileges required`

---

### TEST 3.3 — Creer une amenity avec nom deja existant
Requiert le token admin

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "wifi",
  "description": "Another wifi"
}
```
**Resultat attendu :** `400 Amenity already exists`

---

### TEST 3.4 — Lister toutes les amenities
**Endpoint :** `GET /api/v1/amenities/`

**Resultat attendu :** `200` avec la liste (wifi, swimming pool, air conditioning + parking)

---

### TEST 3.5 — Recuperer une amenity par ID
**Endpoint :** `GET /api/v1/amenities/<amenity_id>`

Utiliser l'id de Parking cree au TEST 3.1.

**Resultat attendu :** `200` avec les details de Parking

---

### TEST 3.6 — Recuperer une amenity inexistante
**Endpoint :** `GET /api/v1/amenities/00000000-0000-0000-0000-000000000000`

**Resultat attendu :** `404 Amenity not found`

---

### TEST 3.7 — Modifier une amenity (en tant qu'admin)
Requiert le token admin

**Endpoint :** `PUT /api/v1/amenities/<amenity_id_parking>`

**Body :**
```json
{
  "name": "Parking gratuit",
  "description": "Free private parking"
}
```
**Resultat attendu :** `200` avec les details mis a jour

---

### TEST 3.8 — Modifier une amenity sans etre admin
Requiert le token de John

**Endpoint :** `PUT /api/v1/amenities/<amenity_id_parking>`

**Body :**
```json
{
  "name": "Hacked amenity"
}
```
**Resultat attendu :** `403 Admin privileges required`

---

## SECTION 4 — Places

### TEST 4.1 — Creer un lieu (valide)
Requiert le token de John

**Endpoint :** `POST /api/v1/places/`

**Body :**
```json
{
  "title": "Bel appartement Paris",
  "description": "Superbe appartement au coeur de Paris",
  "price": 120.00,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "amenities": []
}
```
**Resultat attendu :** `201` avec les details du lieu

> Sauvegarder l'id du lieu cree.

---

### TEST 4.2 — Creer un lieu avec amenities
Requiert le token de John

**Endpoint :** `POST /api/v1/places/`

**Body :**
```json
{
  "title": "Villa avec piscine",
  "description": "Grande villa avec piscine privee",
  "price": 250.00,
  "latitude": 43.2965,
  "longitude": 5.3698,
  "amenities": ["984fc2e7-bb3b-49ff-9c93-6fe57119ba53"]
}
```
**Resultat attendu :** `201` avec les amenities incluses dans la reponse

---

### TEST 4.3 — Creer un lieu avec prix negatif
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
**Resultat attendu :** `400 Price must be a positive number`

---

### TEST 4.4 — Creer un lieu avec latitude invalide
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
**Resultat attendu :** `400 Latitude must be between -90 and 90`

---

### TEST 4.5 — Lister tous les lieux
**Endpoint :** `GET /api/v1/places/`

**Resultat attendu :** `200` avec la liste des lieux crees

---

### TEST 4.6 — Recuperer un lieu par ID
**Endpoint :** `GET /api/v1/places/<place_id>`

Utiliser l'id du lieu cree au TEST 4.1.

**Resultat attendu :** `200` avec owner, amenities et reviews imbriques

---

### TEST 4.7 — Recuperer un lieu inexistant
**Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000`

**Resultat attendu :** `404 Place not found`

---

### TEST 4.8 — Modifier son propre lieu
Requiert le token de John

**Endpoint :** `PUT /api/v1/places/<place_id>`

**Body :**
```json
{
  "title": "Bel appartement Paris - Renove",
  "price": 150.00
}
```
**Resultat attendu :** `200` avec les donnees mises a jour

---

### TEST 4.9 — Modifier le lieu d'un autre utilisateur
Requiert le token de Jane

**Endpoint :** `PUT /api/v1/places/<place_id_john>`

**Body :**
```json
{
  "title": "Hacked place"
}
```
**Resultat attendu :** `403 Unauthorized action`

---

### TEST 4.10 — Ajouter une amenity a un lieu
Requiert le token de John

**Endpoint :** `POST /api/v1/places/<place_id>/amenities/<amenity_id_wifi>`

Utiliser l'id du lieu de John et l'id de wifi : `c7a66c94-5a7e-4746-8c30-308f7695a36c`

**Resultat attendu :** `200` avec l'amenity ajoutee dans la liste

---

### TEST 4.11 — Ajouter une amenity deja liee
Requiert le token de John

**Endpoint :** `POST /api/v1/places/<place_id>/amenities/<amenity_id_wifi>`

(meme amenity que le test precedent)

**Resultat attendu :** `400 Amenity already added`

---

### TEST 4.12 — Ajouter une amenity inexistante
Requiert le token de John

**Endpoint :** `POST /api/v1/places/<place_id>/amenities/00000000-0000-0000-0000-000000000000`

**Resultat attendu :** `404 Amenity not found`

---

### TEST 4.13 — Retirer une amenity d'un lieu
Requiert le token de John

**Endpoint :** `DELETE /api/v1/places/<place_id>/amenities/<amenity_id_wifi>`

**Resultat attendu :** `200` avec l'amenity retiree de la liste

---

### TEST 4.14 — Retirer une amenity non liee
Requiert le token de John

**Endpoint :** `DELETE /api/v1/places/<place_id>/amenities/<amenity_id_wifi>`

(meme amenity que le test precedent, deja retiree)

**Resultat attendu :** `400 Amenity not linked`

---

## SECTION 5 — Reviews

### TEST 5.1 — Creer une review (valide, par Jane sur le lieu de John)
Requiert le token de Jane

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Superbe appartement, tres bien situe !",
  "rating": 5,
  "place_id": "<place_id_john>"
}
```
**Resultat attendu :** `201` avec les details de la review

> Sauvegarder l'id de la review creee.

---

### TEST 5.2 — Creer une review sur son propre lieu
Requiert le token de John

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Mon propre appartement est super",
  "rating": 5,
  "place_id": "<place_id_john>"
}
```
**Resultat attendu :** `400 You cannot review your own place`

---

### TEST 5.3 — Creer une deuxieme review sur le meme lieu (doublon)
Requiert le token de Jane

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Deuxieme review",
  "rating": 3,
  "place_id": "<place_id_john>"
}
```
**Resultat attendu :** `400 Review already exists for this user and place`

---

### TEST 5.4 — Creer une review avec rating invalide
Requiert le token de Admin

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Note invalide",
  "rating": 10,
  "place_id": "<place_id_john>"
}
```
**Resultat attendu :** `400 Rating must be between 1 and 5`

---

### TEST 5.5 — Creer une review sur un lieu inexistant
Requiert le token de Jane

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Lieu inexistant",
  "rating": 3,
  "place_id": "00000000-0000-0000-0000-000000000000"
}
```
**Resultat attendu :** `404 Place not found`

---

### TEST 5.6 — Lister toutes les reviews
**Endpoint :** `GET /api/v1/reviews/`

**Resultat attendu :** `200` avec la liste des reviews

---

### TEST 5.7 — Recuperer une review par ID
**Endpoint :** `GET /api/v1/reviews/<review_id>`

Utiliser l'id de la review creee au TEST 5.1.

**Resultat attendu :** `200` avec les details de la review

---

### TEST 5.8 — Recuperer les reviews d'un lieu
**Endpoint :** `GET /api/v1/places/<place_id>/reviews`

**Resultat attendu :** `200` avec la liste des reviews du lieu

---

### TEST 5.9 — Recuperer les reviews d'un lieu inexistant
**Endpoint :** `GET /api/v1/places/00000000-0000-0000-0000-000000000000/reviews`

**Resultat attendu :** `404 Place not found`

---

### TEST 5.10 — Modifier sa propre review
Requiert le token de Jane

**Endpoint :** `PUT /api/v1/reviews/<review_id>`

**Body :**
```json
{
  "comment": "Appartement encore mieux que prevu !",
  "rating": 5
}
```
**Resultat attendu :** `200` avec les donnees mises a jour

---

### TEST 5.11 — Modifier la review d'un autre utilisateur
Requiert le token de John

**Endpoint :** `PUT /api/v1/reviews/<review_id_jane>`

**Body :**
```json
{
  "comment": "Review hackee"
}
```
**Resultat attendu :** `403 Unauthorized action`

---

### TEST 5.12 — Supprimer sa propre review
Requiert le token de Jane

**Endpoint :** `DELETE /api/v1/reviews/<review_id>`

**Resultat attendu :** `200 Review deleted successfully`

---

### TEST 5.13 — Supprimer la review d'un autre utilisateur
Requiert le token de John

**Endpoint :** `DELETE /api/v1/reviews/<review_id_autre>`

**Resultat attendu :** `403 Unauthorized action`

---

### TEST 5.14 — Supprimer une review inexistante
Requiert le token admin

**Endpoint :** `DELETE /api/v1/reviews/00000000-0000-0000-0000-000000000000`

**Resultat attendu :** `404 Review not found`

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

Sauvegarder le token admin et l'utiliser dans Authorize.

---

## A — Tests admin avec les endpoints déjà existants

### Users

---

### TEST 6.1 — Admin modifie le profil d'un autre utilisateur

Requiert le token admin

**Endpoint :** `PUT /api/v1/users/<user_id_jane>`

**Body :**
```json
{
  "first_name": "Janette",
  "last_name": "Smith"
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

**Endpoint :** `PUT /api/v1/users/<user_id_john>`

**Body :**
```json
{
  "email": "adminchange@test.com"
}
```

**Résultat attendu :** `400 You cannot modify email or password`

> Ce test vérifie que la règle métier reste vraie même pour admin, sauf si tu as choisi l'inverse.

---

### TEST 6.4 — Admin modifie l'email d'un autre utilisateur via endpoint dédié

Requiert le token admin

**Endpoint :** `PUT /api/v1/users/<user_id_john>/email`

**Body :**
```json
{
  "email": "john_admin_update@test.com"
}
```

**Résultat attendu :**
- `200 Email updated successfully` si admin a ce droit
- `403 Unauthorized action` si seul le propriétaire peut le faire

> Ce test sert aussi à clarifier ta règle métier.

---

### TEST 6.5 — Admin modifie le mot de passe d'un autre utilisateur via endpoint dédié

Requiert le token admin

**Endpoint :** `PUT /api/v1/users/<user_id_john>/password`

**Body :**
```json
{
  "password": "adminreset123"
}
```

**Résultat attendu :**
- `200 Password updated successfully`
- `403 Unauthorized action`

---

### Amenities

---

### TEST 6.6 — Admin crée une amenity

Requiert le token admin

**Endpoint :** `POST /api/v1/amenities/`

**Body :**
```json
{
  "name": "Sauna",
  "description": "Private sauna available"
}
```

**Résultat attendu :** `201` avec l'id de la nouvelle amenity

---

### TEST 6.7 — Admin modifie une amenity existante

Requiert le token admin

**Endpoint :** `PUT /api/v1/amenities/<amenity_id>`

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

### Places

---

### TEST 6.9 — Admin modifie le lieu d'un autre utilisateur

Requiert le token admin

**Endpoint :** `PUT /api/v1/places/<place_id_john>`

**Body :**
```json
{
  "title": "Place modified by admin",
  "price": 180.00
}
```

**Résultat attendu :**
- `200` si admin a le droit de modifier tous les places
- `403 Unauthorized action` si seul le owner peut modifier

---

### TEST 6.10 — Admin ajoute une amenity à un lieu qui ne lui appartient pas

Requiert le token admin

**Endpoint :** `POST /api/v1/places/<place_id_john>/amenities/<amenity_id_wifi>`

**Résultat attendu :**
- `200` si admin a le droit
- `403 Unauthorized action`

---

### TEST 6.11 — Admin retire une amenity d'un lieu qui ne lui appartient pas

Requiert le token admin

**Endpoint :** `DELETE /api/v1/places/<place_id_john>/amenities/<amenity_id_wifi>`

**Résultat attendu :**
- `200` si admin a le droit
- `403 Unauthorized action`

---

### Reviews

---

### TEST 6.12 — Admin crée une review sur le lieu d'un autre utilisateur

Requiert le token admin

**Endpoint :** `POST /api/v1/reviews/`

**Body :**
```json
{
  "comment": "Admin review test",
  "rating": 4,
  "place_id": "<place_id_john>"
}
```

**Résultat attendu :** `201` avec les détails de la review

---

### TEST 6.13 — Admin modifie la review d'un autre utilisateur

Requiert le token admin

**Endpoint :** `PUT /api/v1/reviews/<review_id_jane>`

**Body :**
```json
{
  "comment": "Review updated by admin",
  "rating": 4
}
```

**Résultat attendu :** `200` avec les données mises à jour

---

### TEST 6.14 — Admin supprime la review d'un autre utilisateur

Requiert le token admin

**Endpoint :** `DELETE /api/v1/reviews/<review_id_jane>`

**Résultat attendu :** `200 Review deleted successfully`

---

### TEST 6.15 — Admin supprime une review inexistante

Requiert le token admin

**Endpoint :** `DELETE /api/v1/reviews/00000000-0000-0000-0000-000000000000`

**Résultat attendu :** `404 Review not found`

---

## Recapitulatif des tests

| Section | Nombre de tests | Valides | Invalides (doivent echouer) |
|---------|-----------------|---------|------------------------------|
| Auth | 5 | 2 | 3 |
| Users | 13 | 6 | 7 |
| Amenities | 8 | 4 | 4 |
| Places | 14 | 6 | 8 |
| Reviews | 14 | 5 | 9 |
| **Total** | **54** | **23** | **31** |

---

## IDs utiles (donnees initiales)

| Donnee | ID |
|--------|----|
| Admin | `36c9050e-ddd3-4c3b-9731-9f487208bbc1` |
| Amenity WiFi | `c7a66c94-5a7e-4746-8c30-308f7695a36c` |
| Amenity Swimming Pool | `984fc2e7-bb3b-49ff-9c93-6fe57119ba53` |
| Amenity Air Conditioning | `68615b51-bb01-4d8f-8222-a445efdf23b6` |
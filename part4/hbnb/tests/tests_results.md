# Test Suite — HBnB Part 3

Tous les tests sont des **tests d'intégration HTTP** : ils passent par les endpoints REST de l'API, utilisent une base SQLite **en mémoire** (isolée par test), et valident le comportement réel de l'application avec authentification JWT.

---

## Partie 1 — Tests Lite (`tests_lite.py`)

Fichier unique, autonome, couvrant les cas essentiels de chaque section. Idéal pour une vérification rapide.

### Lancer les tests

```bash
python3 -m unittest tests/tests_lite.py -v
```

### Résultat

```
Ran 57 tests
OK
```

### Couverture

| Section | Tests | Description |
|---------|-------|-------------|
| Auth | 5 | Login valide/invalide, endpoint protégé avec et sans token |
| Users | 13 | Création, lecture, modification (profil/email/password), suppression, droits admin |
| Amenities | 10 | Création admin uniquement, lecture publique, modification, suppression, doublons |
| Places | 14 | Création, validation prix/coords, gestion amenities, update/delete par owner ou admin |
| Reviews | 15 | Création, règles métier (own place, doublon, rating), update/delete par auteur ou admin |
| **Total** | **57** | **Tous OK ✅** |

### Ce que couvrent les tests lite

**Auth** — vérifie que le login retourne un token, que les mauvais credentials sont refusés, et que l'endpoint protégé est inaccessible sans token.

**Users** — vérifie la création avec validation (email, password), l'impossibilité de modifier email/password via `PUT /users`, les endpoints dédiés `/email` et `/password`, et les règles de propriété (un user ne peut modifier que son propre compte).

**Amenities** — vérifie que seul l'admin peut créer/modifier/supprimer une amenity, que les doublons sont refusés, et que la lecture est publique.

**Places** — vérifie la création avec validation (prix > 0, latitude/longitude), la gestion des amenities liées (ajout, doublon, suppression), et les droits owner/admin sur update et delete.

**Reviews** — vérifie les règles métier : impossible de reviewer sa propre place, une seule review par user par place, rating entre 1 et 5, droits auteur/admin sur update et delete.

---

## Partie 2 — Tests Détaillés

Cinq fichiers spécialisés couvrant exhaustivement chaque section. Utilise `test_helpers.py` comme base commune (setup SQLite in-memory, seed admin, helpers partagés).

### Lancer les tests

```bash
# Tous les fichiers détaillés
python3 -m unittest discover -s tests/ -p "tests_*.py" -v

# Un fichier à la fois
python3 -m unittest tests/tests_auth.py -v
python3 -m unittest tests/tests_users.py -v
python3 -m unittest tests/tests_amenities.py -v
python3 -m unittest tests/tests_places.py -v
python3 -m unittest tests/tests_reviews.py -v
```

### Résultat global

```
Ran 118 tests in ~320s
OK
```

---

### `tests_auth.py` — Authentification

**11 tests — Tous OK ✅**

Couvre le login (credentials valides, mauvais mot de passe, email inconnu, champs vides, body manquant), la structure du token retourné, et l'accès à l'endpoint protégé (avec token valide, sans token, avec token malformé ou Bearer vide).

---

### `tests_users.py` — Gestion des utilisateurs

**25 tests — Tous OK ✅**

| Catégorie | Tests |
|-----------|-------|
| Création valide | 2 |
| Création invalide (email, password) | 5 |
| Lecture (list, get by id, not found) | 3 |
| Update profil (own, other, sans token) | 4 |
| Update email (own, doublon, autre user) | 3 |
| Update password (own, autre user) | 2 |
| Admin (update, email, password, user inexistant) | 4 |
| Delete (own, other forbidden, not found, admin) | 5 |

Cas notables : tentative de modifier email/password via `PUT /users` retourne `400`, les endpoints dédiés `/email` et `/password` sont les seuls chemins autorisés. L'admin peut tout modifier sauf contourner cette restriction.

---

### `tests_amenities.py` — Gestion des amenities

**18 tests — Tous OK ✅**

| Catégorie | Tests |
|-----------|-------|
| Création admin (avec/sans description, lowercase) | 3 |
| Création interdite (sans token, non-admin) | 2 |
| Création invalide (doublon, nom vide) | 2 |
| Lecture (list, get by id, not found) | 3 |
| Update admin (valide, non-admin, sans token) | 3 |
| Update invalide (doublon, not found, nom vide) | 3 |
| Delete (admin, then 404, non-admin, not found) | 4 |

Cas notables : le nom est systématiquement normalisé en lowercase, les doublons sont détectés après normalisation, seul l'admin a accès aux opérations d'écriture.

---

### `tests_places.py` — Gestion des lieux

**30 tests — Tous OK ✅**

| Catégorie | Tests |
|-----------|-------|
| Création valide (avec/sans amenities) | 3 |
| Création interdite/invalide (sans token, prix, coords, amenity inconnue) | 7 |
| Lecture (list, get by id, not found) | 3 |
| Update (owner, non-owner, sans token, admin) | 4 |
| Ajout amenity (owner, non-owner, déjà liée, inexistante, admin) | 5 |
| Suppression amenity (owner, non liée, non-owner, admin) | 4 |
| Delete place (owner, then 404, non-owner, not found, admin) | 5 |

Cas notables : price = 0 et price < 0 sont tous les deux rejetés, latitude/longitude hors limites retournent `400`, les liens amenity-place sont bidirectionnels et validés.

---

### `tests_reviews.py` — Gestion des reviews

**34 tests — Tous OK ✅**

| Catégorie | Tests |
|-----------|-------|
| Création valide (rating min/max) | 3 |
| Création interdite/invalide (sans token, own place, doublon, rating, place inexistante) | 6 |
| Lecture (list, get by id, not found, by place, place inexistante) | 5 |
| Update (auteur, rating préservé, non-auteur, sans token, admin) | 5 |
| Delete (auteur, then 404, non-auteur, sans token, not found, admin) | 6 |
| Admin (create on any place, update any, delete any) | 3 |

Cas notables : un utilisateur ne peut pas reviewer sa propre place (`400`), une seule review par user par place (`400`), le rating doit être entre 1 et 5 inclus, l'admin peut créer/modifier/supprimer n'importe quelle review.

---

## Récapitulatif global

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `tests_auth.py` | 11 | ✅ OK |
| `tests_users.py` | 25 | ✅ OK |
| `tests_amenities.py` | 18 | ✅ OK |
| `tests_places.py` | 30 | ✅ OK |
| `tests_reviews.py` | 34 | ✅ OK |
| **Total détaillé** | **118** | **✅ OK** |

---

## Notes techniques

**Base de données** — chaque test instancie une base SQLite `sqlite:///:memory:` via `TestingConfig`. Les tables sont créées dans `setUp` et détruites dans `tearDown`, garantissant une isolation totale entre les tests.

**Admin** — l'utilisateur admin est inséré directement en base (bypass de l'API) car `POST /users` bloque explicitement le champ `is_admin` pour des raisons de sécurité.

**JWT** — les tokens sont obtenus via `POST /api/v1/auth/login` et passés dans le header `Authorization: Bearer <token>` pour chaque requête protégée.

---

## Author

**Gwenaelle PICHOT**  
Student at Holberton School  
Track: Project HBnB
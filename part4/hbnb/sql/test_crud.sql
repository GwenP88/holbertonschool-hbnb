-- ============================================================
-- SCRIPT DE TESTS CRUD COMPLET ET DÉTAILLÉ
-- HBnB Project
-- ============================================================

PRAGMA foreign_keys = ON;

-- Nettoyage avant les tests
DELETE FROM place_amenity;
DELETE FROM reviews;
DELETE FROM places;
DELETE FROM users WHERE id != '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- ==========================
-- 0. VÉRIFICATION DONNÉES INITIALES
-- ==========================

-- Vérifier que l'admin existe avec is_admin = TRUE
SELECT '-- TEST 0.1: Admin existe avec is_admin = TRUE' AS test;
SELECT id, first_name, last_name, email, is_admin
FROM users
WHERE email = 'admin@hbnb.io';
-- ATTENDU : 1 ligne avec is_admin = 1 (TRUE)

-- Vérifier que les 3 amenities sont insérées
SELECT '-- TEST 0.2: 3 amenities initiales présentes' AS test;
SELECT id, name, description
FROM amenities;
-- ATTENDU : 3 lignes (wifi, swimming pool, air conditioning)


-- ==========================
-- 1. TESTS CREATE VALIDES
-- ==========================

-- Insérer un utilisateur de test
SELECT '-- TEST 1.1: Insertion utilisateur valide' AS test;
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'John',
    'Doe',
    'john@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE
);
SELECT id, first_name, last_name, email, is_admin
FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : 1 ligne avec les données insérées

-- Insérer un deuxième utilisateur de test
SELECT '-- TEST 1.2: Insertion deuxième utilisateur valide' AS test;
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin)
VALUES (
    '55555555-5555-5555-5555-555555555555',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Jane',
    'Smith',
    'jane@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE
);
SELECT id, first_name, last_name, email
FROM users
WHERE id = '55555555-5555-5555-5555-555555555555';
-- ATTENDU : 1 ligne avec les données insérées

-- Insérer un lieu valide
SELECT '-- TEST 1.3: Insertion lieu valide' AS test;
INSERT INTO places (id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Test Place',
    'A nice place for testing',
    99.99,
    48.8566,
    2.3522,
    '11111111-1111-1111-1111-111111111111'
);
SELECT id, title, price, latitude, longitude, owner_id
FROM places
WHERE id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : 1 ligne avec les données insérées

-- Insérer une review valide (admin review le lieu de John)
SELECT '-- TEST 1.4: Insertion review valide' AS test;
INSERT INTO reviews (id, created_at, updated_at, comment, rating, author_id, place_id)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Great place, loved it!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    '22222222-2222-2222-2222-222222222222'
);
SELECT id, comment, rating, author_id, place_id
FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';
-- ATTENDU : 1 ligne avec rating = 5

-- Insérer une deuxième review valide (Jane review le lieu de John)
SELECT '-- TEST 1.5: Insertion deuxième review valide' AS test;
INSERT INTO reviews (id, created_at, updated_at, comment, rating, author_id, place_id)
VALUES (
    '66666666-6666-6666-6666-666666666666',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Nice place but a bit expensive.',
    3,
    '55555555-5555-5555-5555-555555555555',
    '22222222-2222-2222-2222-222222222222'
);
SELECT id, comment, rating, author_id, place_id
FROM reviews
WHERE id = '66666666-6666-6666-6666-666666666666';
-- ATTENDU : 1 ligne avec rating = 3

-- Lier deux amenities au lieu
SELECT '-- TEST 1.6: Lier amenities au lieu' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('22222222-2222-2222-2222-222222222222', 'c7a66c94-5a7e-4746-8c30-308f7695a36c');
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('22222222-2222-2222-2222-222222222222', '984fc2e7-bb3b-49ff-9c93-6fe57119ba53');
SELECT a.name
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : 2 lignes (wifi, swimming pool)


-- ==========================
-- 2. TESTS CREATE INVALIDES (doivent échouer)
-- ==========================

-- Doublon email utilisateur
SELECT '-- TEST 2.1: Doublon email (doit échouer)' AS test;
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin)
VALUES (
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Duplicate',
    'User',
    'john@test.com',
    '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq',
    FALSE
);
-- ATTENDU : ERREUR UNIQUE constraint failed: users.email

-- Doublon nom amenity
SELECT '-- TEST 2.2: Doublon nom amenity (doit échouer)' AS test;
INSERT INTO amenities (id, created_at, updated_at, name, description)
VALUES (
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'wifi',
    'Another wifi'
);
-- ATTENDU : ERREUR UNIQUE constraint failed: amenities.name

-- Lieu avec owner_id inexistant
SELECT '-- TEST 2.3: Lieu avec owner inexistant (doit échouer)' AS test;
INSERT INTO places (id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
    'cccccccc-cccc-cccc-cccc-cccccccccccc',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Ghost Place',
    'Owner does not exist',
    50.00,
    48.00,
    2.00,
    'ffffffff-ffff-ffff-ffff-ffffffffffff'
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- Review avec author_id inexistant
SELECT '-- TEST 2.4: Review avec auteur inexistant (doit échouer)' AS test;
INSERT INTO reviews (id, created_at, updated_at, comment, rating, author_id, place_id)
VALUES (
    'dddddddd-dddd-dddd-dddd-dddddddddddd',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Ghost review',
    4,
    'ffffffff-ffff-ffff-ffff-ffffffffffff',
    '22222222-2222-2222-2222-222222222222'
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- Review avec place_id inexistant
SELECT '-- TEST 2.5: Review avec place inexistante (doit échouer)' AS test;
INSERT INTO reviews (id, created_at, updated_at, comment, rating, author_id, place_id)
VALUES (
    'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Ghost review',
    4,
    '11111111-1111-1111-1111-111111111111',
    'ffffffff-ffff-ffff-ffff-ffffffffffff'
);
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- Doublon review même auteur même lieu
SELECT '-- TEST 2.6: Doublon review même auteur/lieu (doit échouer)' AS test;
INSERT INTO reviews (id, created_at, updated_at, comment, rating, author_id, place_id)
VALUES (
    'ffffffff-ffff-ffff-ffff-ffffffffffff',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Second review attempt',
    3,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    '22222222-2222-2222-2222-222222222222'
);
-- ATTENDU : ERREUR UNIQUE constraint failed

-- Doublon place_amenity
SELECT '-- TEST 2.7: Doublon place_amenity (doit échouer)' AS test;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'c7a66c94-5a7e-4746-8c30-308f7695a36c'
);
-- ATTENDU : ERREUR UNIQUE constraint failed

-- Price négatif
SELECT '-- TEST 2.8: Price négatif (doit échouer)' AS test;
INSERT INTO places (id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
    'gggggggg-gggg-gggg-gggg-gggggggggggg',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Negative Price Place',
    'This should fail',
    -10.00,
    48.00,
    2.00,
    '11111111-1111-1111-1111-111111111111'
);
-- ATTENDU : ERREUR CHECK constraint failed: price > 0

-- Latitude hors limites
SELECT '-- TEST 2.9: Latitude hors limites (doit échouer)' AS test;
INSERT INTO places (id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
    'hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Bad Latitude Place',
    'This should fail',
    50.00,
    999.00,
    2.00,
    '11111111-1111-1111-1111-111111111111'
);
-- ATTENDU : ERREUR CHECK constraint failed: latitude BETWEEN -90 AND 90

-- Longitude hors limites
SELECT '-- TEST 2.10: Longitude hors limites (doit échouer)' AS test;
INSERT INTO places (id, created_at, updated_at, title, description, price, latitude, longitude, owner_id)
VALUES (
    'iiiiiiii-iiii-iiii-iiii-iiiiiiiiiiii',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Bad Longitude Place',
    'This should fail',
    50.00,
    48.00,
    999.00,
    '11111111-1111-1111-1111-111111111111'
);
-- ATTENDU : ERREUR CHECK constraint failed: longitude BETWEEN -180 AND 180

-- Rating hors limites
SELECT '-- TEST 2.11: Rating hors limites (doit échouer)' AS test;
INSERT INTO reviews (id, created_at, updated_at, comment, rating, author_id, place_id)
VALUES (
    'jjjjjjjj-jjjj-jjjj-jjjj-jjjjjjjjjjjj',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'Bad rating review',
    10,
    '55555555-5555-5555-5555-555555555555',
    '22222222-2222-2222-2222-222222222222'
);
-- ATTENDU : ERREUR CHECK constraint failed: rating BETWEEN 1 AND 5


-- ==========================
-- 3. TESTS READ (SELECT)
-- ==========================

-- Lire tous les utilisateurs
SELECT '-- TEST 3.1: Lire tous les utilisateurs' AS test;
SELECT id, first_name, last_name, email, is_admin
FROM users;
-- ATTENDU : 3 lignes (admin, John, Jane)

-- Lire tous les lieux avec leur owner
SELECT '-- TEST 3.2: Lire tous les lieux avec leur owner' AS test;
SELECT p.id, p.title, p.price, u.first_name, u.last_name
FROM places p
JOIN users u ON p.owner_id = u.id;
-- ATTENDU : 1 ligne (Test Place, John Doe)

-- Lire toutes les reviews avec auteur et lieu
SELECT '-- TEST 3.3: Lire toutes les reviews avec auteur et lieu' AS test;
SELECT r.id, r.comment, r.rating, u.first_name, p.title
FROM reviews r
JOIN users u ON r.author_id = u.id
JOIN places p ON r.place_id = p.id;
-- ATTENDU : 2 lignes

-- Lire les amenities d'un lieu
SELECT '-- TEST 3.4: Lire les amenities du lieu de test' AS test;
SELECT a.id, a.name
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : 2 lignes (wifi, swimming pool)

-- Lire les lieux d'un utilisateur
SELECT '-- TEST 3.5: Lire les lieux de John' AS test;
SELECT id, title, price
FROM places
WHERE owner_id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : 1 ligne (Test Place)

-- Lire les reviews d'un lieu
SELECT '-- TEST 3.6: Lire les reviews du lieu de test' AS test;
SELECT r.comment, r.rating, u.first_name
FROM reviews r
JOIN users u ON r.author_id = u.id
WHERE r.place_id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : 2 lignes


-- ==========================
-- 4. TESTS UPDATE
-- ==========================

-- Modifier le prénom d'un utilisateur
SELECT '-- TEST 4.1: Modifier prénom utilisateur' AS test;
UPDATE users
SET first_name = 'Johnny', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';
SELECT id, first_name FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : first_name = 'Johnny'

-- Modifier le prix d'un lieu
SELECT '-- TEST 4.2: Modifier prix du lieu' AS test;
UPDATE places
SET price = 149.99, updated_at = CURRENT_TIMESTAMP
WHERE id = '22222222-2222-2222-2222-222222222222';
SELECT id, title, price FROM places
WHERE id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : price = 149.99

-- Modifier le commentaire d'une review
SELECT '-- TEST 4.3: Modifier commentaire review' AS test;
UPDATE reviews
SET comment = 'Updated comment!', updated_at = CURRENT_TIMESTAMP
WHERE id = '33333333-3333-3333-3333-333333333333';
SELECT id, comment FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';
-- ATTENDU : comment = 'Updated comment!'

-- Modifier le rating avec une valeur invalide
SELECT '-- TEST 4.4: Modifier rating avec valeur invalide (doit échouer)' AS test;
UPDATE reviews
SET rating = 6
WHERE id = '33333333-3333-3333-3333-333333333333';
-- ATTENDU : ERREUR CHECK constraint failed: rating BETWEEN 1 AND 5

-- Modifier le prix avec une valeur invalide
SELECT '-- TEST 4.5: Modifier price avec valeur négative (doit échouer)' AS test;
UPDATE places
SET price = -50.00
WHERE id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : ERREUR CHECK constraint failed: price > 0


-- ==========================
-- 5. TESTS DELETE
-- ==========================

-- Supprimer une review
SELECT '-- TEST 5.1: Supprimer une review' AS test;
DELETE FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';
SELECT id FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';
-- ATTENDU : 0 lignes

-- Supprimer un lieu qui a encore des reviews (doit échouer)
SELECT '-- TEST 5.2: Supprimer lieu avec reviews existantes (doit échouer)' AS test;
DELETE FROM places
WHERE id = '22222222-2222-2222-2222-222222222222';
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- Supprimer un utilisateur qui a encore des places (doit échouer)
SELECT '-- TEST 5.3: Supprimer user avec places existantes (doit échouer)' AS test;
DELETE FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';
-- ATTENDU : ERREUR FOREIGN KEY constraint failed

-- Suppression dans le bon ordre
SELECT '-- TEST 5.4: Suppression dans le bon ordre' AS test;

-- 1. Supprimer la review restante
DELETE FROM reviews
WHERE id = '66666666-6666-6666-6666-666666666666';

-- 2. Supprimer les liens place_amenity
DELETE FROM place_amenity
WHERE place_id = '22222222-2222-2222-2222-222222222222';

-- 3. Supprimer le lieu
DELETE FROM places
WHERE id = '22222222-2222-2222-2222-222222222222';

-- 4. Supprimer les utilisateurs de test
DELETE FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';
DELETE FROM users
WHERE id = '55555555-5555-5555-5555-555555555555';

-- Vérification finale
SELECT '-- VÉRIFICATION FINALE: Seules les données initiales restent' AS test;
SELECT id, first_name, email, is_admin FROM users;
-- ATTENDU : 1 ligne (admin uniquement)
SELECT id, name FROM amenities;
-- ATTENDU : 3 lignes (wifi, swimming pool, air conditioning)
SELECT id FROM places;
-- ATTENDU : 0 lignes
SELECT id FROM reviews;
-- ATTENDU : 0 lignes
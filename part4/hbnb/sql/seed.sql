PRAGMA foreign_keys = ON;

-- ============================================================
-- USERS
-- ============================================================

-- Insert the default administrator user.
-- Stores the fixed admin account with a hashed password and admin privileges.
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin) VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq', TRUE);

-- Insert an user1 : John Doe.
-- Stores the fixed account with a hashed password.
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin) VALUES ('7b5a1b64-4bb6-4581-8cd3-019863c6e3d9', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'John', 'Doe', 'johndoe@email.com', '$2b$12$JyTyQroHGueqPZhXN08BH.0hWFyynWH2rMF20.RPuyKGEqIJhibLe', FALSE);

-- Insert an user2 : Jane Doe.
-- Stores the fixed account with a hashed password.
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin) VALUES ('76efe665-2825-4883-a382-8d76bb8ea472', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Jane', 'Doe', 'janedoe@email.com', '$2b$12$1w/W3SN/JasBFhgI.XRA4eI6AEfdjPsrpD2apdMrJsofsEf2inPGq', FALSE);

-- Insert an user3 : Jean Peplu.
-- Stores the fixed account with a hashed password.
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin) VALUES ('76d64007-5865-492c-b06f-ac012b825812', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Jean', 'Peplu', 'jeanpeplu@email.com', '$2b$12$b2EOCKLS1ecP7PJOH7.iS..xVc5G8f2paM8czzX7uKraMOPePQ7Uy', FALSE);

-- ============================================================
-- AMENITIES
-- ============================================================

-- Insert the default WiFi amenity.
-- Stores the WiFi amenity with its initial description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('93282ff9-7af0-4b0d-beb1-407b6998b01f', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'wifi', 'High-speed wireless internet access available throughout the property.');

-- Insert the default swimming pool amenity.
-- Stores the swimming pool amenity with its initial description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('984fc2e7-bb3b-49ff-9c93-6fe57119ba53', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'swimming pool', 'Private or shared swimming pool available for guests.');

-- Insert the default air conditioning amenity.
-- Stores the air conditioning amenity without a description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('68615b51-bb01-4d8f-8222-a445efdf23b6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'air conditioning', NULL);

-- Insert the default Rooftop Terrace amenity.
-- Stores the Rooftop Terrace amenity without a description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('c5fcec1a-08f8-40ba-beae-fc5717d8f60e', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'rooftop terrace', 'A spacious rooftop terrace with panoramic city views, outdoor seating and a barbecue area');

-- Insert the default Private Parking amenity.
-- Stores the Private Parking amenity without a description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('62b29136-184b-48fd-88d5-650e8e94a3ab', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'private parking', 'Secure underground parking space included, available 24/7 for guests');

-- ============================================================
-- PLACE-AMENITIES
-- ============================================================

-- Insert amenities for place 1.
-- Stores wifi
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('ef448d99-36e6-4aa6-880a-59bab9bbe439', '93282ff9-7af0-4b0d-beb1-407b6998b01f');

-- Stores Rooftop Terrace
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('ef448d99-36e6-4aa6-880a-59bab9bbe439', 'c5fcec1a-08f8-40ba-beae-fc5717d8f60e')

-- Stores air conditioning
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('ef448d99-36e6-4aa6-880a-59bab9bbe439', '68615b51-bb01-4d8f-8222-a445efdf23b6')

-- Insert amenities for place 2.
-- Stores wifi
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('b7f90bd1-3466-4429-b57d-e00adb798bbc', '93282ff9-7af0-4b0d-beb1-407b6998b01f');

-- Insert amenities for place 3.
-- Stores wifi
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('57ea271c-e55e-4a4e-94cb-ab5319664e7e', '93282ff9-7af0-4b0d-beb1-407b6998b01f');

-- Stores swimming pool
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('57ea271c-e55e-4a4e-94cb-ab5319664e7e', '984fc2e7-bb3b-49ff-9c93-6fe57119ba53');

-- Stores air conditioning
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('57ea271c-e55e-4a4e-94cb-ab5319664e7e', '68615b51-bb01-4d8f-8222-a445efdf23b6');

-- Stores Private Parking 
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('57ea271c-e55e-4a4e-94cb-ab5319664e7e', '62b29136-184b-48fd-88d5-650e8e94a3ab');

-- Insert amenities for place 4.
-- Stores wifi
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('69354fdc-70f9-403a-9f88-c77147087909', '93282ff9-7af0-4b0d-beb1-407b6998b01f');

-- Stores Private Parking
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('69354fdc-70f9-403a-9f88-c77147087909', '62b29136-184b-48fd-88d5-650e8e94a3ab');

-- Insert amenities for place 5.
-- Stores wifi
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('5fcc6d25-3bf1-4701-b8dc-a8016def143d', '93282ff9-7af0-4b0d-beb1-407b6998b01f');

-- Stores Rooftop Terrace
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('5fcc6d25-3bf1-4701-b8dc-a8016def143d', 'c5fcec1a-08f8-40ba-beae-fc5717d8f60e');

-- Stores Private Parking
INSERT INTO place_amenity(place_id, amenity_id) VALUES ('5fcc6d25-3bf1-4701-b8dc-a8016def143d', '62b29136-184b-48fd-88d5-650e8e94a3ab');

-- ============================================================
-- PLACES
-- ============================================================

-- Insert the default place 1 user 1.
-- Stores the place 1, lyon.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('ef448d99-36e6-4aa6-880a-59bab9bbe439', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Sunny Loft in the City Center', 'A bright and modern loft located in the heart of the city, perfect for family.', 180, 45.7640, 4.8357, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9');

-- Insert the default place 2 user 1.
-- Stores the place 2, lyon.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('b7f90bd1-3466-4429-b57d-e00adb798bbc', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Cozy Studio in Central Lyon', 'A cozy studio in the heart of Lyon, close to shops and public transport. Perfect for a comfortable stay.', 80, 45.7640, 4.8357, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9');

-- Insert the default place 3 user 2.
-- Stores the place 3, annecy.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('57ea271c-e55e-4a4e-94cb-ab5319664e7e', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Charming Chalet by Lake Annecy', 'A cozy chalet near Lake Annecy, surrounded by nature. Perfect for a peaceful and relaxing stay.', 250, 45.8992, 6.1294, '76efe665-2825-4883-a382-8d76bb8ea472');

-- Insert the default place 4 user 2.
-- Stores the place 4, annecy.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('69354fdc-70f9-403a-9f88-c77147087909', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Family Apartment in Central Annecy', 'A spacious apartment in the heart of Annecy, close to the lake and shops. Perfect for a family stay.', 180, 45.8992, 6.1294, '76efe665-2825-4883-a382-8d76bb8ea472');

-- Insert the default place 5 user 3.
-- Stores the place 5, geneve.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('5fcc6d25-3bf1-4701-b8dc-a8016def143d', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Unique Apartment in Geneva', 'A stylish and atypical apartment in Geneva, close to the city center. Perfect for a memorable stay.', 140, 46.2044, 6.1432, '76d64007-5865-492c-b06f-ac012b825812');

-- Insert the default place 6 user 3.
-- Stores the place 6, geneve.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Modern Studio in Central Geneva', 'A modern studio in the heart of Geneva, close to shops and transport. Ideal for a comfortable stay.', 75, 46.2044, 6.1432, '76d64007-5865-492c-b06f-ac012b825812');

-- ============================================================
-- REVIEWS
-- ============================================================

-- Place 1 - Sunny Loft in the City Center (owner: John)
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('27d20295-4bfe-4058-9232-d299cfcffefb', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Absolutely loved the loft! Great location, very clean and comfortable. I would definitely stay here again.', 5, '76efe665-2825-4883-a382-8d76bb8ea472', 'ef448d99-36e6-4aa6-880a-59bab9bbe439');

INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('a1f8f3f0-7b5a-4db8-9f31-1100c8d10001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Nice place overall and well located in Lyon. A bit noisy at night, but still a pleasant stay.', 4, '76d64007-5865-492c-b06f-ac012b825812', 'ef448d99-36e6-4aa6-880a-59bab9bbe439');

-- Place 2 - Cozy Studio in Central Lyon (owner: John)
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('b2f8f3f0-7b5a-4db8-9f31-1100c8d10002', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Small but very functional studio. Perfect for a short stay and close to everything.', 4, '76efe665-2825-4883-a382-8d76bb8ea472', 'b7f90bd1-3466-4429-b57d-e00adb798bbc');

INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('c3f8f3f0-7b5a-4db8-9f31-1100c8d10003', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'The studio was clean and practical, but a little too small for my taste. Good location though.', 3, '76d64007-5865-492c-b06f-ac012b825812', 'b7f90bd1-3466-4429-b57d-e00adb798bbc');

-- Place 3 - Charming Chalet by Lake Annecy (owner: Jane)
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('d4f8f3f0-7b5a-4db8-9f31-1100c8d10004', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Beautiful chalet in a peaceful area. The surroundings were amazing and the stay was very relaxing.', 5, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9', '57ea271c-e55e-4a4e-94cb-ab5319664e7e');

INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('e5f8f3f0-7b5a-4db8-9f31-1100c8d10005', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Lovely place near Annecy. The chalet was cozy, but a few details could be improved.', 4, '76d64007-5865-492c-b06f-ac012b825812', '57ea271c-e55e-4a4e-94cb-ab5319664e7e');

-- Place 4 - Family Apartment in Central Annecy (owner: Jane)
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('f6f8f3f0-7b5a-4db8-9f31-1100c8d10006', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Very convenient apartment for a family trip. Spacious, well located and close to the lake.', 5, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9', '69354fdc-70f9-403a-9f88-c77147087909');

INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('07f8f3f0-7b5a-4db8-9f31-1100c8d10007', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'The apartment was decent and well placed, but I expected a bit more comfort for the price.', 3, '76d64007-5865-492c-b06f-ac012b825812', '69354fdc-70f9-403a-9f88-c77147087909');

-- Place 5 - Unique Apartment in Geneva (owner: Jean)
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('18f8f3f0-7b5a-4db8-9f31-1100c8d10008', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'A very original apartment with a lot of character. Great location in Geneva and a memorable stay.', 5, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9', '5fcc6d25-3bf1-4701-b8dc-a8016def143d');

INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('29f8f3f0-7b5a-4db8-9f31-1100c8d10009', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Interesting apartment and good location, but the decor was not really my style.', 2, '76efe665-2825-4883-a382-8d76bb8ea472', '5fcc6d25-3bf1-4701-b8dc-a8016def143d');

-- Place 6 - Modern Studio in Central Geneva (owner: Jean)
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('12e8bfd8-968f-45b2-a450-8d0b6b7449de', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Modern and well located studio, very convenient for a short stay in Geneva.', 4, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9', '9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d');

INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES
('3af8f3f0-7b5a-4db8-9f31-1100c8d10010', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'The location was good, but the studio felt too basic and not very comfortable for me.', 1, '76efe665-2825-4883-a382-8d76bb8ea472', '9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d');
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
-- PLACES
-- ============================================================

-- Insert the default place 1.
-- Stores the place 1.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('ef448d99-36e6-4aa6-880a-59bab9bbe439', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Sunny Loft in the City Center', 'A bright and modern loft located in the heart of the city, perfect for couples or solo travelers.', 95, 48.8566, 2.3522, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9');

-- Insert the default place 2.
-- Stores the place 2.
INSERT INTO places(id, created_at, updated_at, title, description, price, latitude, longitude, owner_id) VALUES ('9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Cozy Countryside Cottage', 'A charming stone cottage surrounded by nature, ideal for a peaceful getaway.', 75, 45.7640, 4.8357, '76efe665-2825-4883-a382-8d76bb8ea472');

-- ============================================================
-- REVIEWS
-- ============================================================

-- Insert the default review 1.
-- Stores the review 1.
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES ('27d20295-4bfe-4058-9232-d299cfcffefb', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Absolutely loved the loft! The location was unbeatable and the place was spotless. Would definitely come back.', 5, '76efe665-2825-4883-a382-8d76bb8ea472', 'ef448d99-36e6-4aa6-880a-59bab9bbe439');

-- Insert the default review 2.
-- Stores the review 2.
INSERT INTO reviews(id, created_at, updated_at, comment, rating, author_id, place_id) VALUES ('12e8bfd8-968f-45b2-a450-8d0b6b7449de', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Very nice cottage, charming and well-located. The fireplace was a great touch. Highly recommended!', 4, '7b5a1b64-4bb6-4581-8cd3-019863c6e3d9', '9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d');
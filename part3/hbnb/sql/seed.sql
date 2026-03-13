-- Insert the default administrator user.
-- Stores the fixed admin account with a hashed password and admin privileges.
INSERT INTO users (id, created_at, updated_at, first_name, last_name, email, password, is_admin) VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$Z24N6SlkS8E6YEjB5weWseNPC8oPALbIfEIjM/AanPP9JuheGsZFq', TRUE);

-- Insert the default WiFi amenity.
-- Stores the WiFi amenity with its initial description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('c7a66c94-5a7e-4746-8c30-308f7695a36c', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'wifi', 'High-speed wireless internet access available throughout the property.');

-- Insert the default swimming pool amenity.
-- Stores the swimming pool amenity with its initial description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('984fc2e7-bb3b-49ff-9c93-6fe57119ba53', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'swimming pool', 'Private or shared swimming pool available for guests.');

-- Insert the default air conditioning amenity.
-- Stores the air conditioning amenity without a description.
INSERT INTO amenities(id, created_at, updated_at, name, description) VALUES ('68615b51-bb01-4d8f-8222-a445efdf23b6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'air conditioning', NULL);
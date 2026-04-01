-- Create the users table if it does not already exist.
-- Stores user identity information, hashed password, timestamps,
-- and the administrator flag. 
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) NOT NULL PRIMARY KEY, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME NOT NULL, 
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL, 
    email VARCHAR(120) NOT NULL UNIQUE, 
    password VARCHAR(128) NOT NULL, 
    is_admin BOOLEAN NOT NULL DEFAULT FALSE);

-- Create the amenities table if it does not already exist.
-- Stores available amenities that can be linked to places.
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) NOT NULL PRIMARY KEY, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME NOT NULL, 
    name VARCHAR(50) NOT NULL UNIQUE, 
    description  VARCHAR(255));

-- Create the places table if it does not already exist.
-- Stores place information and the owner linked through a foreign key. 
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) NOT NULL PRIMARY KEY, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME NOT NULL, 
    title VARCHAR(100) NOT NULL, 
    description  VARCHAR(255) NOT NULL, 
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0), 
    latitude FLOAT NOT NULL CHECK (latitude BETWEEN -90 AND 90), 
    longitude FLOAT NOT NULL CHECK (longitude BETWEEN -180 AND 180), 
    owner_id CHAR(36) NOT NULL, 
    FOREIGN KEY (owner_id) REFERENCES users(id));

-- Create the association table between places and amenities if it does not already exist.
-- Stores many-to-many relationships between places and amenities.
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL, 
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id),
    PRIMARY KEY (place_id, amenity_id));

-- Create the reviews table if it does not already exist.
-- Stores user reviews for places including a comment and rating.
-- A unique constraint ensures a user can review a place only once. 
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) NOT NULL PRIMARY KEY, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME NOT NULL, 
    comment VARCHAR(500) NOT NULL, 
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5), 
    author_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id), UNIQUE (author_id, place_id));

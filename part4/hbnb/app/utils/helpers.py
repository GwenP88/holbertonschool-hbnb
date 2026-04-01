"""Utility helpers for place display: city name and image resolution."""

# --- City resolution ---

"""Utility to resolve a city name from latitude/longitude coordinates."""

CITY_LOCATIONS = {
    (45.7640, 4.8357): "Lyon",
    (45.8992, 6.1294): "Annecy",
    (46.2044, 6.1432): "Genève",
}

def get_city_name(latitude, longitude):
    """Return the city name matching the coordinates, or None if unknown."""
    return CITY_LOCATIONS.get((latitude, longitude))

# --- Image resolution ---

PLACE_IMAGES = {
    'ef448d99-36e6-4aa6-880a-59bab9bbe439': 'images/places/place_1.webp',
    'b7f90bd1-3466-4429-b57d-e00adb798bbc': 'images/places/place_2.webp',
    '57ea271c-e55e-4a4e-94cb-ab5319664e7e': 'images/places/place_3.webp',
    '69354fdc-70f9-403a-9f88-c77147087909': 'images/places/place_4.webp',
    '5fcc6d25-3bf1-4701-b8dc-a8016def143d': 'images/places/place_5.webp',
    '9bc8b8f5-ac16-4ce3-b3b1-91b1b30d934d': 'images/places/place_6.webp',
}

DEFAULT_IMAGE = 'images/places/place_default.webp'

def get_place_image(place_id):
    """Return the image path for a place, or a default image if unknown."""
    return PLACE_IMAGES.get(place_id, DEFAULT_IMAGE)
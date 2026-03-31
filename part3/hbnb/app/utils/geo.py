"""Utility to resolve a city name from latitude/longitude coordinates."""

CITY_LOCATIONS = {
    (45.7640, 4.8357): "Lyon",
    (45.8992, 6.1294): "Annecy",
    (46.2044, 6.1432): "Genève",
}

def get_city_name(latitude, longitude):
    """Return the city name matching the coordinates, or None if unknown."""
    return CITY_LOCATIONS.get((latitude, longitude))

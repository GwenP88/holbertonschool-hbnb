"""Application entry point that creates and runs the Flask app."""
from app import create_app

"""Flask application instance created from the app factory."""
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

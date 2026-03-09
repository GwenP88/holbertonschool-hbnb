"""Application configuration classes and environment-to-config mapping."""
import os


class Config:
    """Define base configuration values for the application."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Enable development settings such as debug mode."""
    DEBUG = True


"""Map environment names to configuration classes."""
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

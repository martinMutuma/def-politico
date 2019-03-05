"""Configuration file"""
import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_DEFAULT_FROM = os.getenv('SENDGRID_DEFAULT_FROM')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_TEST_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_TEST_URL')


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.environ.get('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'debug': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

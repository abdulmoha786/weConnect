import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aam786'
    DEBUG = False


class TestingConfig(Config):

    """Configurations for Testing."""

    TESTING = True
    DEBUG = True


app_config = {
             'development':Config,
             'testing': TestingConfig
            }


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CAS_SERVER = "https://fed.princeton.edu"
    CAS_AFTER_LOGIN = 'secure'
    CAS_LOGOUT_ROUTE = '/cas/logout'
    CAS_VALIDATE_ROUTE = '/cas/serviceValidate'
    CAS_LOGIN_ROUTE = 'https://fed.princeton.edu/cas/login'
    SECRET_KEY = 'aaaaimtesting'


# TODO: we can have different configurations for production etc as we need

# class ProductionConfig(Config):
#     DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

# class TestingConfig(Config):
#     TESTING = True



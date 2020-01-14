import os
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.sqlite'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

    CAS_SERVER = "https://fed.princeton.edu"
    CAS_AFTER_LOGIN = 'root'
    CAS_LOGOUT_ROUTE = '/cas/logout'
    CAS_VALIDATE_ROUTE = '/cas/validate'
    CAS_LOGIN_ROUTE = '/cas/login'
    SECRET_KEY = 'bd018ea8ad91ce61534aeb83'

    IMAGE_UPLOADS = "./orangepages/static/uploads/"
    IMAGE_UPLOADS_RELATIVE = "../static/uploads/"
    IMAGE_UPLOADS_POSTS = "./orangepages/static/uploads/posts/"
    IMAGE_UPLOADS_RELATIVE_POSTS = "../static/uploads/posts/"


# TODO: we can have different configurations for production etc as we need

# class ProductionConfig(Config):
#     DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

# class TestingConfig(Config):
#     TESTING = True

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.sqlite'
    SQLALCHEMY_DATABASE_URI = 'postgres://nmhcywqweatsfl:e21c40997b10f441ef74bc5f4cf8d9a6e3b2de3717c76f98efa4cfb03f95c81a@ec2-174-129-254-223.compute-1.amazonaws.com:5432/ddqrp7b6ke1cnf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

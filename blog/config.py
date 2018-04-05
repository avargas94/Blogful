import os


class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://avargas:Thinkful@localhost:5432/blogful"
    DEBUG = True

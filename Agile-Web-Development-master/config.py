''' Database config '''
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'development key'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'userpage.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

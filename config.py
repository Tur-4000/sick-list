import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 '557f6e018f88498cbd225a9c1a91e071'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Рабочие дни недели начиная с понедельника. 1 - рабочий день, 0 - выходной
    WORK_DAYS = '1111110'

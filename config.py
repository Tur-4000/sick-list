import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ты-никoгд@-НЕ-д0гадаешьcя'

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import User, Employes, Patients, Lists, Holiday, Diacrisis, Role


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Employes': Employes, 'Patients': Patients,
            'Lists': Lists, 'Holiday': Holiday, 'Diacrisis': Diacrisis,
            'Role': Role}


@app.cli.command()
def deploy():
    """Run deployment task."""
    # migrate database to latest version
    upgrade()

    # create or update user roles
    Role.insert_roles()

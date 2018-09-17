import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click
from app import create_app, db
from app.models import User, Employes, Patients, Lists, Holiday
from flask_migrate import Migrate, upgrade


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Employes': Employes, 'Patients': Patients,
            'Lists': Lists, 'Holiday': Holiday}


@app.cli.command()
def deploy():
    """Run deployment task."""
    # migrate database to latest version
    upgrade()

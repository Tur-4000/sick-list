import os
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

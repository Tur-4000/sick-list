from app import app, db
from app.models import User, Employes, Patients, Lists
# 
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Employes':Employes, 'Patients': Patients, 'Lists': Lists}
# 
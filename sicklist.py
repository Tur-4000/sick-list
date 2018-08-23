from app import app, db
from app.models import User, Employes, Patients, Lists, Holiday, Checkins
# 
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Employes':Employes, 'Patients': Patients,
            'Lists': Lists, 'Holiday': Holiday, 'Checkins': Checkins}
# 
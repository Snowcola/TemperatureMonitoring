from app import app, db
from app.models import Temp

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Temp':Temp}
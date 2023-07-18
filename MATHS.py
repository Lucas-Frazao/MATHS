from app import app, db
from app.models import User, Event


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event}

# To complete the application, you need to have a Python script at the top-level that defines the Flask application instance. Let's call this
# script microblog.py, and define it as a single line that imports the application instance:

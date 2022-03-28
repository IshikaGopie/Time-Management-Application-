from flaskserver import app
from flaskserver.models import User, Event, Sprint

@app.route("/")
def hello_world():
    return "hello_world"
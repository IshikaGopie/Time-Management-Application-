from flask import jsonify, request
from flaskserver import app
from flaskserver.models import User, CalendarEvent, Event

@app.route("/", methods = ['GET', 'POST'])
def event():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify(data)
    else:
        return jsonify(title = "Vacation", start = '2022-04-04T11:53', end = '2022-04-08T10:53')
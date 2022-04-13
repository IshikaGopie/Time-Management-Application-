from flaskserver import timeManagementTwo

from sqlite3 import IntegrityError
from flask import jsonify, request
from flaskserver import app, db
from flaskserver.models import User, CalendarEvent, Event

from datetime import datetime, timedelta

@app.route('/signup', methods=['POST'])
def signup():
  userdata = request.get_json()
  newuser = User( username=userdata['username'], email=userdata['email'] )
  newuser.set_password( userdata['password'] )
  try:
    db.session.add( newuser )
    db.session.commit()
  except IntegrityError:
    db.session.rollback()
    return 'username or email already exists'
  return 'user created'




@app.route("/events", methods = ['POST'])
def create_event():
    data = request.get_json()
    if ( data['priority'] == 'high' ):
        priority = 1
    elif( data['priority'] == 'medium' ):
        priority = 2
    else:
        priority = 3
    if ( data['location'] == "" or None ):
        location = None
    else:
        location = data['location']
    if ( data['description'] == "" or None ):
        description = None
    else:
        description = data['description']

    start = datetime.strptime(data['startDate'], '%Y-%m-%dT%H:%M')
    end = datetime.strptime(data['endDate'], '%Y-%m-%dT%H:%M')

    if ( data['tag'] == 'assignment' ):
        assignment = [999, data['title'], data['avgHrs'], priority, start, end]

    events(assignment)

    return "hello_world"

"""
    if ( data['tag'] == 'assignment' ):
        e = Event(
            id_user = data['user'],
            duration = avgHrs
        )
    else:
        e = Event(
            id_user = data['user'],
            duration = get_duration(start, end)
        )
    db.session.add(e)

    db.session.flush()

    ce = CalendarEvent(
        id_event = e.id_event,
        id_user = data['user'],
        title = data['title'],
        tag = data['tag'],
        priority = data['priority'],
        startDate = start,
        endDate = end,
        location = location,
        description = description
    )
    db.session.add(ce)

    db.session.commit()

    return format_event(ce)
"""




@app.route("/events", methods = ['GET'])
def get_events():
    ce = CalendarEvent.query.filter_by( id_user = 1 )

    list = []
    for e in ce:
        list.append(format_event(e))
        return {'events': list}




@app.route("/events/<id>", methods = ['GET'])
def get_event(id):
    ce = CalendarEvent.query.filter_by( id_calendar = id ).one()

    return {'event': format_event(ce)}




@app.route("/events/<id>", methods = ['DELETE'])
def delete_event(id):
    ce = CalendarEvent.query.filter_by( id_calendar = id ).one()

    if(ce.tag != "assignment"):
        e = Event.query.filter_by( id_event = ce.id_event ).one()
        db.session.delete(e)
    #else:
    #    "IN PROGRESS!"

    db.session.delete(ce)
    db.session.commit()

    return f'Event (id: {id}) deleted!'




@app.route("/events/<id>", methods = ['PUT'])
def update_event(id):
    ce = CalendarEvent.query.filter_by( id_calendar = id )

    data = request.get_json()

    if ( data['location'] == "" or None ):
        location = None
    else:
        location = data['location']
    if ( data['description'] == "" or None ):
        description = None
    else:
        description = data['description']

    ce.update(dict(
        title = data['title'],
        tag = data['tag'],
        priority = data['priority'],
        startDate = datetime.strptime(data['startDate'], '%Y-%m-%dT%H:%M'),
        endDate = datetime.strptime(data['endDate'], '%Y-%m-%dT%H:%M'),
        location = location,
        description = description
    ))

    db.session.commit()
    return {'event': format_event(ce.one())}




def format_event(calendar):
    return{
        "id": calendar.id_calendar,
        "title": calendar.title,
        "tag": calendar.tag,
        "priority": calendar.priority,
        "startDate": calendar.startDate,
        "endDate": calendar.endDate,
        "location": calendar.location,
        "description": calendar.description
    }




def get_duration(start, end):
    return (end - start).total_seconds() / 3600




def events(assignment):
    ce = CalendarEvent.query.filter(
            CalendarEvent.id_user == 1,
            CalendarEvent.tag != "assignment"
        )

    e_id = []
    e_startDate = []
    e_startTime = []
    e_duration = []

    for e in ce:
        #assignment[4] = start
        #assignment[5] = end
        if ((e.id_event not in e_id) and (assignment[4] <= e.endDate) and (assignment[5] >= e.endDate)):
            e_id.append(e.id_event)
            e_startDate.append(date_toString(e.startDate))
            e_startTime.append(time_toString(e.startDate))

    e = Event.query.filter(
        Event.id_user == 1
    )

    for i in e_id:
        for j in e:
            if(i == j.id_event):
                e_duration.append(j.duration)

    print("event details:")
    print(e_id)
    print(e_startDate)
    print(e_startTime)
    print(e_duration)


    ce = CalendarEvent.query.filter(
            CalendarEvent.id_user == 1,
            CalendarEvent.tag == "assignment"
        )

    id = []
    title = []
    duration = []
    priority = []
    startDate = []
    endDate = []

    id.append(assignment[0])
    title.append(assignment[1])
    duration.append(assignment[2])
    priority.append(assignment[3])
    startDate.append(date_toString(assignment[4]))
    endDate.append(date_toString(assignment[5]))


    #print("assignment details:")
    #print(id)
    #print(title)
    #print(duration)
    #print(priority)
    print(startDate)
    print(endDate)

    for e in ce:
        if ((e.id_event not in id) and (assignment[4] < e.endDate)):
            id.append(e.id_event)
            title.append(e.title)

    for i in id:
        start = None 
        end = None
        for e in ce:
            if(e.id_event == i):
                if((e.startDate < start) or (start == None)):
                    start = e.startDate
                if((e.endDate > end) or (end == None)):
                    end = e.endDate
            if(start and end != None):
                startDate.append(date_toString(start))
                endDate.append(date_toString(end))


    e = Event.query.filter(
            Event.id_user == 1
    )

    for i in id:
        for j in e:
            if(i == j.id_event):
                duration.append(j.duration)

    timeline = []
    print(timeline)
    timeline = timeManagementTwo.get_timeline(startDate, endDate, timeline)

    scheduled_tasks = timeManagementTwo.init_schedule(e_startTime, e_startDate, e_duration, timeline)

    scheduled_assignments = timeManagementTwo.get_scheduled_assignments(scheduled_tasks, id, title,
                                                                        duration, priority,
                                                                        startDate, endDate,
                                                                        timeline)

    print(timeline)
    print("\n")

    for i in scheduled_tasks:
        print(i)

    print("\n")

    for i in scheduled_assignments:
        print(i)

    #priority if full
    





def date_toString(datetime):
    return datetime.strftime("%Y-%m-%d")




def time_toString(datetime):
    return datetime.strftime("%I:%M %p")
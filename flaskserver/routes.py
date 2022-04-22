from collections import defaultdict
from importlib import reload

from flaskserver import timeManagement

from sqlite3 import IntegrityError
from flask import request
from flaskserver import app, db
from flaskserver.models import User, CalendarEvent, Event

from datetime import datetime

import json
import math

@app.route('/signup', methods=['POST'])
def signup():
    userdata = request.get_json()
    newuser = User(
      username=userdata['username'],
      email=userdata['email']
    )
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
    data = json.loads(request.form.get("values"))

    events = create (data)

    return events, 201




@app.route("/events", methods = ['GET'])
def get_events():
    ce = CalendarEvent.query.filter_by( id_user = 1 )

    list = []
    for e in ce:
        list.append(format_event(e))
        
    return {'data': list}




@app.route("/events", methods = ['DELETE'])
def delete_event():
    ce = CalendarEvent.query.filter_by( id_calendar = request.form.get("key") ).one()
    e = Event.query.filter_by( id_event = ce.id_event ).one()

    if(ce.tag != "assignment"):
        db.session.delete(e)
    else:
        if(CalendarEvent.query.filter_by( id_event = ce.id_event ).count() == 1):
            db.session.delete(e)


    db.session.delete(ce)

    db.session.commit()

    return f'Event (id: {id}) deleted!'




@app.route("/events", methods = ['PUT'])
def update_event():
    ce = CalendarEvent.query.filter_by( id_calendar = request.form.get("key") )
    data = json.loads(request.form.get("values"))

    if 'location' not in data:
        location = None
    elif ( data['location'] == "" or None ):
        location = None
    else:
        location = data['location']

    if 'description' not in data:
        description = None
    elif ( data['description'] == "" or None ):
        description = None
    else:
        description = data['description']

    ce.update(dict(
        title = data['text'],
        tag = data['tag'],
        priority = data['priority'],
        startDate = datetime.strptime(
            data['startDate'],
            '%Y-%m-%dT%H:%M:%SZ'
        ),
        endDate = datetime.strptime(
            data['endDate'],
            '%Y-%m-%dT%H:%M:%SZ'
        ),
        location = location,
        description = description
    ))

    db.session.commit()
    return ""




def create( data ):
    list = []
    mia = []

    if 'location' not in data:
        location = None
    elif ( data['location'] == "" or None ):
        location = None
    else:
        location = data['location']

    if 'description' not in data:
        description = None
    elif ( data['description'] == "" or None ):
        description = None
    else:
        description = data['description']

    start = datetime.strptime(
        data['startDate'],
        '%Y-%m-%dT%H:%M:%SZ'
    )

    end = datetime.strptime(
        data['endDate'],
        '%Y-%m-%dT%H:%M:%SZ'
    )

    e = Event(id_user = 1)
    db.session.add(e)

    db.session.flush()

    if ( data['tag'] == 'assignment' ):
        assignment = [
            data['text'],
            data['avgHrs'],
            data['priority'],
            start,
            end
        ]

        sprints, idList = events(assignment)



        for sprint in sprints:
            #print(sprint)
            startDate = datetime.strptime(
                sprint['date'] + sprint['start_time'],
                '%Y-%m-%d%I:%M %p'
            )

            endDate = datetime.strptime(
                sprint['date'] + sprint['end_time'],
                '%Y-%m-%d%I:%M %p'
            )

            if sprint['id'] == None:

                ce = CalendarEvent(
                    id_event = e.id_event,
                    id_user = 1,
                    title = data['text'],
                    tag = data['tag'],
                    priority = data['priority'],
                    startDate = startDate,
                    endDate = endDate,
                    location = location,
                    description = description
                )

                db.session.add(ce)

                db.session.flush()

            elif sprint['id'] in idList:
                #print("ID", sprint['id'])
                #print("calendarID", sprint['calendarID'])
                ce = CalendarEvent.query.get( sprint['calendarID'] )
                #print(ce)
                ce.startDate = startDate
                ce.endDate = endDate

                db.session.flush()


            list.append(format_event(ce))
    else:
        ce = CalendarEvent(
            id_event = e.id_event,
            id_user = 1,
            title = data['text'],
            tag = data['tag'],
            priority = data['priority'],
            startDate = start,
            endDate = end,
            location = location,
            description = description
        )

        db.session.add(ce)

        db.session.flush()

    if ( data['tag'] == 'assignment' ):
        for id in idList:
            missing = True
            if(id == None):
                continue
            for sprint in sprints:
                if((sprint['id'] == id)):
                    missing = False
            if missing == True:
                mia.append(id)

        #print(mia)

        for id in mia:
            e = Event.query.filter_by(id_event = id).first()

            db.session.delete(e)

    db.session.commit()

    if ( data['tag'] == 'assignment' ):
        return {'data': list}
    else:
        return {'data': format_event(ce)}




def events(assignment):
    ce = CalendarEvent.query.filter(
            CalendarEvent.id_user == 1,
            CalendarEvent.tag != "assignment",
            CalendarEvent.startDate >= assignment[3], 
            CalendarEvent.endDate <= assignment[4]
        )

    e_id = []
    e_startDate = []
    e_startTime = []
    e_duration = []

    for e in ce:
        if (e.id_event not in e_id):
            e_id.append(e.id_event)
            e_startDate.append(date_toString(e.startDate))
            e_startTime.append(time_toString(e.startDate))
            e_duration.append(int(get_duration(e.startDate, e.endDate)))

    e = Event.query.filter(
        Event.id_user == 1
    )

    print(assignment[3])
    print(assignment[4])

    ce = CalendarEvent.query.filter(
            CalendarEvent.id_user == 1,
            CalendarEvent.tag == "assignment",
            CalendarEvent.startDate >= assignment[3], 
            CalendarEvent.endDate <= assignment[4]
        )

    for i in ce:
        print(i)

    id_calendar = defaultdict(list)
    id_event = []
    title = []
    duration = []
    priority = []
    startDate = []
    endDate = []

    key = 0

    for x in range(int(assignment[1])):
        id_calendar[key].append(None)
    id_event.append(None)
    title.append(assignment[0])
    duration.append(int(math.ceil(float(assignment[1]))))
    priority.append(assignment[2])
    startDate.append(date_toString(assignment[3]))
    endDate.append(date_toString(assignment[4]))

    for e in ce:
        if e.id_event not in id_event:
            #print(e)
            key+=1
            id_event.append(e.id_event)
            title.append(e.title)
            priority.append(e.priority)
        id_calendar[key].append(e.id_calendar)
    
    
    #print("")

    for i in id_event[1:]:
        start = None
        end = None
        timelineDuration = 0
        for e in ce:
            if(e.id_event == i):
                #print(e)
                timelineDuration += get_duration(e.startDate, e.endDate)
                #print(timelineDuration)
                if((start == None) or (e.startDate < start)):
                    start = e.startDate
                if((end == None) or (e.endDate > end)):
                    end = e.endDate
        if(start and end != None):
            startDate.append(date_toString(start))
            endDate.append(date_toString(end))
            duration.append(int(math.ceil(timelineDuration)))

    """
    print(id_calendar)
    print(id_event)
    print(title)
    print(duration)
    print(priority)
    print(startDate)
    print(endDate)
    """
    """
    e = Event.query.filter(
            Event.id_user == 1
    )

    for i in id:
        for j in e:
            if(i == j.id_event):
                duration.append(j.duration)
    """
    
    timeline = []
    timeline = timeManagement.get_timeline(
        startDate, 
        endDate, 
        timeline
    )

    #print("calendar", id_calendar[0])
    
    #print(e_startTime)
    #print(e_startDate)
    #print(e_duration)
    #print(timeline)
    

    scheduled_tasks = timeManagement.init_schedule(
        e_startTime, 
        e_startDate, 
        e_duration, 
        timeline
    )

    #for i in scheduled_tasks:
    #    print(i)
    
    print(id_calendar)
    print(id_event)
    print(title)
    print(duration)
    print(priority)
    print(startDate)
    print(endDate)
    print(timeline)


    scheduled_assignments, results = timeManagement.get_scheduled_assignments(
        id_calendar,
        scheduled_tasks,
        id_event,
        title, 
        duration, 
        priority, 
        startDate, 
        endDate, 
        timeline
    )
    
    reload(timeManagement)

    for i in scheduled_assignments:
        print(i)

    #print(id_event)

    return scheduled_assignments, id_event




def format_event(calendar):
    return{
        "id": calendar.id_calendar,
        "text": calendar.title,
        "tag": calendar.tag,
        "priority": calendar.priority,
        "startDate": calendar.startDate,
        "endDate": calendar.endDate,
        "location": calendar.location,
        "description": calendar.description
    }




def get_duration(start, end):
    return (end - start).total_seconds() / 3600




def date_toString(datetime):
    return datetime.strftime("%Y-%m-%d")




def time_toString(datetime):
    return datetime.strftime("%I:%M %p")
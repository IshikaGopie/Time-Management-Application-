import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import React from 'react';
 
import 'devextreme/dist/css/dx.light.css';
 
import { data } from './data.js';

import Scheduler from 'devextreme-react/scheduler';
import { CheckBox } from 'devextreme-react/check-box';
import notify from 'devextreme/ui/notify';
 
const views = ["month","day", "week", "agenda"];
const currentDate = new Date(2022, 3, 4);

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      allowAdding: true,
      allowDeleting: true,
      allowResizing: true,
      allowDragging: true,
      allowUpdating: true,
    };
    this.onAllowAddingChanged = this.onAllowAddingChanged.bind(this);
    this.onAllowDeletingChanged = this.onAllowDeletingChanged.bind(this);
    this.onAllowResizingChanged = this.onAllowResizingChanged.bind(this);
    this.onAllowDraggingChanged = this.onAllowDraggingChanged.bind(this);
    this.onAllowUpdatingChanged = this.onAllowUpdatingChanged.bind(this);
    this.showAddedToast = this.showAddedToast.bind(this);
    this.showUpdatedToast = this.showUpdatedToast.bind(this);
    this.showDeletedToast = this.showDeletedToast.bind(this);

  }
  render() {
    return (
      <React.Fragment>
        <Scheduler
          timeZone="America/Los_Angeles"
          dataSource={data}
          views={views}
          defaultCurrentView="month"
          defaultCurrentDate={currentDate}
          startDayHour={9}
          endDayHour={19}
          height={600}
          editing={this.state}
          onAppointmentAdded={this.showAddedToast}
          onAppointmentUpdated={this.showUpdatedToast}
          onAppointmentDeleted={this.showDeletedToast}
        />
        <div className="options">
          <div className="caption">Options</div>
          <div className="options-container">
            <div className="option">
              <CheckBox
                defaultValue={this.state.allowAdding}
                text="Allow adding"
                onValueChanged={this.onAllowAddingChanged}
              />
            </div>
            <div className="option">
              <CheckBox
                defaultValue={this.state.allowDeleting}
                text="Allow deleting"
                onValueChanged={this.onAllowDeletingChanged}
              />
            </div>
            <div className="option">
              <CheckBox
                defaultValue={this.state.allowUpdating}
                text="Allow updating"
                onValueChanged={this.onAllowUpdatingChanged}
              />
            </div>
            <div className="option">
              <CheckBox
                defaultValue={this.state.allowResizing}
                text="Allow resizing"
                onValueChanged={this.onAllowResizingChanged}
                disabled={!this.state.allowUpdating}
              />
            </div>
            <div className="option">
              <CheckBox
                defaultValue={this.state.allowDragging}
                text="Allow dragging"
                onValueChanged={this.onAllowDraggingChanged}
                disabled={!this.state.allowUpdating}
              />
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }

  onAllowAddingChanged(e) {
    this.setState({ allowAdding: e.value });
  }

  onAllowDeletingChanged(e) {
    this.setState({ allowDeleting: e.value });
  }

  onAllowResizingChanged(e) {
    this.setState({ allowResizing: e.value });
  }

  onAllowDraggingChanged(e) {
    this.setState({ allowDragging: e.value });
  }

  onAllowUpdatingChanged(e) {
    this.setState({ allowUpdating: e.value });
  }

  showToast(event, value, type) {
    notify(`${event} "${value}" task`, type, 800);
  }

  showAddedToast(e) {
    this.showToast('Added', e.appointmentData.text, 'success');
  }

  showUpdatedToast(e) {
    this.showToast('Updated', e.appointmentData.text, 'info');
  }

  showDeletedToast(e) {
    this.showToast('Deleted', e.appointmentData.text, 'warning');
  }
}

export default App;

/*
import format from "date-fns/format";
import getDay from "date-fns/getDay";
import parse from "date-fns/parse";
import startOfWeek from "date-fns/startOfWeek";
import React, {Fragment, useState, useCallback, useMemo } from "react";
import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import DateTimePicker from 'react-datetime-picker'



const locales = {
    "en-US": require("date-fns/locale/en-US"),
};
const localizer = dateFnsLocalizer({
    format,
    parse,
    startOfWeek,
    getDay,
    locales,
});

const events = [
    {
        title: "Big Meeting",
        allDay: false,
        start: new Date(2022, 3, 1, 7, 0),
        end: new Date(2022, 3, 1, 9, 0),
    },
    {
        title: "Vacation",
        start: new Date('2022-04-04T11:53'),
        end: new Date('2022-04-08T10:53'),
    },
    {
        title: "Conference",
        start: new Date(2022, 3, 20, 9, 0),
        end: new Date(2022, 3, 23, []),
    },
];

function App() {
    const [newEvent, setNewEvent] = useState({ title: "", start: "", end: "" });
    const [allEvents, setAllEvents] = useState(events);
    //const [value, onChange] = useState(new Date());

    const [myEvents, setMyEvents] = useState(events)
    const moveEvent = useCallback(
        ({ event, start, end, isAllDay: droppedOnAllDaySlot = false }) => {
          const { allDay } = event
          if (!allDay && droppedOnAllDaySlot) {
            event.allDay = true
          }
    
          setMyEvents((prev) => {
            const existing = prev.find((ev) => ev.id === event.id) ?? {}
            const filtered = prev.filter((ev) => ev.id !== event.id)
            return [...filtered, { ...existing, start, end, allDay }]
          })
        },
        [setMyEvents]
      )
    
      const resizeEvent = useCallback(
        ({ event, start, end }) => {
          setMyEvents((prev) => {
            const existing = prev.find((ev) => ev.id === event.id) ?? {}
            const filtered = prev.filter((ev) => ev.id !== event.id)
            return [...filtered, { ...existing, start, end }]
          })
        },
        [setMyEvents]
      )
    function handleAddEvent() {
        setAllEvents([...allEvents, newEvent]);
    }

    return (
        <div className="App">
            <h1>Schedule</h1>
            <h2>Add New Event</h2>
            <div>
                <input type="text" placeholder="Add Title" style={{ width: "20%", marginRight: "10px" }} value={newEvent.title} onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })} />
                <DateTimePicker selected={newEvent.start} onChange={(start) => setNewEvent({ ...newEvent, start })} value={newEvent.start} />
                <DateTimePicker placeholderText="End Date" selected={newEvent.end} onChange={(end) => setNewEvent({ ...newEvent, end })} value={newEvent.end}/>
                <button stlye={{ marginTop: "10px" }} onClick={handleAddEvent}>
                    Add Event
                </button>
            </div>
            <Calendar 
               localizer={localizer} 
               events={allEvents} 
               startAccessor="start" 
               endAccessor="end" 
               onEventDrop={moveEvent}
               onEventResize={resizeEvent}
               popup
               resizable
               selectable 
                style={{ height: 500, margin: "50px" }} />
        </div>
    );
}

export default App;
*/


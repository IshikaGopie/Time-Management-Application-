import format from "date-fns/format";
import getDay from "date-fns/getDay";
import parse from "date-fns/parse";
import startOfWeek from "date-fns/startOfWeek";
import React, { useState } from "react";
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
               selectable 
                style={{ height: 500, margin: "50px" }} />
        </div>
    );
}

export default App;



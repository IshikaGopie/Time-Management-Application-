import format from "date-fns/format";
import getDay from "date-fns/getDay";
import parse from "date-fns/parse";
import startOfWeek from "date-fns/startOfWeek";
import React, { useState, useEffect } from "react";
import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import DateTimePicker from 'react-datetime-picker';
import Axios from 'axios';


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
    const url="http://localhost:5000/"
    const [newEvent, setNewEvent] = useState({ title: "", start: "", end: "" });
    const [allEvents, setAllEvents] = useState(events);
    //const [value, onChange] = useState(new Date());


    function handleAddEvent() {
        //console.log(newEvent)
        setAllEvents([...allEvents, newEvent]);
    }
    
    function submit(e){
        e.preventDefault();
        Axios.post(url, {
            title: newEvent.title,
            start: newEvent.start,
            end: newEvent.end
        })
            .then(res => {
                console.log(res.data)
            })
    }

    useEffect(() => {
        const getEvents = async() => {
            const {data : res} = await Axios.get(url);
            console.log(res);
        }
        getEvents();
    })

    return (
        <div className="App">
            <h1>Schedule</h1>
            <h2>Add New Event</h2>
            <div>
                <form onSubmit={(e) => submit(e)}>
                    <input type="text" onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })} placeholder="add_title" style={{ width: "20%", marginRight: "10px" }} value={newEvent.title} />
                    <DateTimePicker onChange={(start) => setNewEvent({ ...newEvent, start })} value={newEvent.start} />
                    <DateTimePicker onChange={(end) => setNewEvent({ ...newEvent, end })} value={newEvent.end}/>
                    <button style={{ marginTop: "10px" }} onClick={handleAddEvent}>
                        Add Event
                    </button>
                </form>
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



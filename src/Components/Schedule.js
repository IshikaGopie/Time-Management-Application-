
import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import React from 'react';
 
import 'devextreme/dist/css/dx.light.css';
 
import { data, priorities, categories } from './data.js';

import Scheduler, { Resource }  from 'devextreme-react/scheduler';
import { CheckBox } from 'devextreme-react/check-box';
import notify from 'devextreme/ui/notify';
import Axios from 'axios';
import * as AspNetData from 'devextreme-aspnet-data-nojquery';

const views = ["month","day", "week", "agenda"];
const currentDate = new Date(2022, 3, 4);

const url = 'http://localhost:5000';
const dataSource = AspNetData.createStore({
  key: 'EventID',
  loadUrl: `${url}/events`,
  insertUrl: `${url}/events`,
  updateUrl: `${url}/events`,
  deleteUrl: `${url}/DeleteEvent`,
  onBeforeSend: (_, ajaxOptions) => {
    ajaxOptions.xhrFields = { withCredentials: false };
  },
});

/*
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
    const url="http://localhost:5000"
    const [newEvent, setNewEvent] = useState({ title: "", start: "", end: "" });
    const [allEvents, setAllEvents] = useState(events);
    //const [value, onChange] = useState(new Date());


    function handleAddEvent() {
        //console.log(newEvent)
        setAllEvents([...allEvents, newEvent]);
    }
    
    function submit(e){
        e.preventDefault();
        Axios.post(`${url}/events`, {
            title: newEvent.title,
            tag: 'class',
            priority: 'high',
            description: '',
            location: '',
            startDate: newEvent.start,
            endDate: newEvent.end
        })
            .then(res => {
                console.log(res.data)
            })
    }

    /*useEffect(() => {
        const getEvents = async() => {
            const {data : res} = await Axios.get(url);
            console.log(res);
        }
        getEvents();
    })*/


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

    this.validationRules = {
      position: [
        { type: 'required', message: 'Position is required.' },
      ],
    };

    this.validateForm = (e) => {
      e.component.validate();
    };

  }

  onAppointmentFormOpening(e) {
    e.popup.option('showTitle', true);
    e.popup.option('title', e.appointmentData.text ? 
        e.appointmentData.text : 
        'Create a new event');

    const form = e.form
    let formItems = form.option("items"); 
        if (!formItems.find(function(i) { return i.dataField === "location" })) {
            formItems.push({
                colSpan: 2,
                label: { text: "Average Time:" },
                editorType: "dxTextBox",
  
            });
            form.option("items", formItems);
        }
}

  render() {
    return (

      <React.Fragment>
        <Scheduler
          timeZone="America/Caracas"
          dataSource={dataSource}
          views={views}
          defaultCurrentView="month"
          defaultCurrentDate={currentDate}
          startDayHour={0}
          endDayHour={24}
          height={600}
          editing={this.state}
          onAppointmentFormOpening={this.onAppointmentFormOpening}
          onAppointmentAdded={this.showAddedToast}
          onAppointmentUpdated={this.showUpdatedToast}
          onAppointmentDeleted={this.showDeletedToast}
         >
           <Resource
            dataSource={categories}
            fieldExpr="tag"
            label="Categories"
            validationRules={this.validationRules.position}
          />
          <Resource
            dataSource={priorities}
            fieldExpr="priority"
            label="Priority"
          />

          </Scheduler>
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


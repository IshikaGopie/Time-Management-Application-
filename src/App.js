import './App.css';
import SideMenu from './Components/SideMenu';
import Schedule from './Components/Schedule';
import Todo from './Components/Todo';
import LinkAccount from './Components/LinkAccount';
import FindClass from './Components/FindClass';
import Notifications from './Components/Notifications';
import Login from './Components/Login';

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import { useState } from 'react';

function App() {

  const [inactive, setInactive] = useState(false);

  return (
    <div className="App">
        <BrowserRouter>
          <SideMenu onCollapse={(inactive) => {
            console.log(inactive)
            setInactive(inactive)
          }} />
          <div className={`container ${inactive ? 'inactive' : ""}`}>
            <Routes>
              <Route exact path={'/'} element={<Schedule/>}></Route>
              <Route path={'/todo'} element={<Todo/>}></Route>
              <Route path={'/linkAccount'} element={<LinkAccount/>}></Route>
              <Route path={'/findClass'} element={<FindClass/>}></Route>
              <Route path={'/notifications'} element={<Notifications/>}></Route>
              <Route path={'/signin-login'} element={<Login/>}></Route>
            </Routes>
          </div>
        </BrowserRouter>
    </div>
  );
}

export default App;

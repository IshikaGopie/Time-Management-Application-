import React, { useEffect, useState } from 'react'
import logo from "../assets/logo/webscript.png";
import user from "../assets/user.jpg";
import MenuItem from "./MenuItem";

const menuItems = [
    {name:'Schedule', to: '/', iconClassName: "bi bi-calendar-fill"},
    {name:'Todo', to: '/todo', iconClassName: "bi bi-list-task"},
    {name:'Link Account', to: '/linkAccount', iconClassName: "bi bi-link"},
    {name:'Find Class', to: '/findClass', iconClassName: "bi bi-compass-fill"},
    {name:'Notifications', to: '/notifications', iconClassName: "bi bi-bell"},
];

const SideMenu = (props) =>{
    const [inactive, setInactive] = useState(false);
    useEffect(() => {
        props.onCollapse(inactive)
    },[inactive]);

    return (
        <div className={`side-menu ${inactive ? "inactive" : ""}`}>
            <div className="top-section">
                <div className="logo">
                    <img src={logo} alt="webscript"/>
                </div>
                <div onClick={() => setInactive(!inactive)} className="toggle-menu-btn">
                    {inactive ? (
                        <i class="bi bi-arrow-right-square-fill"></i>
                    ):(
                        <i class="bi bi-arrow-left-square-fill"></i>
                    )}
                </div>
            </div>
            <div className="divider"></div>
            <div className="main-menu">
                <ul>
                    {menuItems.map((menuItem, index) => (
                        <MenuItem
                        key={index}
                        name={menuItem.name}
                        to={menuItem.to}
                        iconClassName ={menuItem.iconClassName}
                        />
                    ))}
                    {/*<li>
                        <a className="menu-item">
                            <div className="menu-icon">
                                <i class="bi bi-calendar-fill"></i>
                            </div>
                            <span>Schedule</span>
                        </a>
                        <a className="menu-item">
                            <div className="menu-icon">
                                <i class="bi bi-list-task"></i>
                            </div>
                            <span>Todo</span>
                        </a>
                        <a className="menu-item">
                            <div className="menu-icon">
                                <i class="bi bi-link"></i>
                            </div>
                            <span>Link Account</span>
                        </a>
                        <a className="menu-item">
                            <div className="menu-icon">
                            <i class="bi bi-compass-fill"></i>
                            </div>
                            <span>Find Class</span>
                        </a>
                        <a className="menu-item">
                            <div className="menu-icon">
                            <i class="bi bi-bell"></i>
                            </div>
                            <span>Notifications</span>
                        </a>
                    </li> */}
                </ul>
            </div>
            <div className="side-menu-footer">
                <div className="avatar">
                    <img src={user} alt="user"></img>
                </div>
                <div className="user-info">
                    <h5>Jane Doe</h5>
                    <p><button class="log-out">Log out</button></p>
                    
                </div>
            </div>
        </div>
    );
};

export default SideMenu;
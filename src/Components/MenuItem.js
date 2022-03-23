import React from "react";
import {NavLink} from "react-router-dom";


const MenuItem = (props) => {
    const { name, iconClassName, onClick, to } = props;
    return(
        <li onClick={props.onClick}>
            <NavLink to={to} className="menu-item">
                <div className="menu-icon">
                    <i class={iconClassName}></i>
                </div>
                <span>{name}</span>
            </NavLink>
        </li>
    );
};

export default MenuItem;
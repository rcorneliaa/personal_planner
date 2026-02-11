import React from "react";
import {useNavigate} from "react-router-dom";

function HomePage(){
    const navigate = useNavigate();
    return (
        <div style = {{textAlign: "center", marginTop: "100xp"}}>
            <h1>Personal Planner</h1>
            <button onClick={()=> navigate("/todo")}>To-DO</button>

        </div>
    );
}

export default HomePage;
import React from "react";
import {useNavigate} from "react-router-dom";
import Logo from "./logo.png"

function HomePage(){
    const navigate = useNavigate();
    return (
        <div className="flex flex-col items-center justify-center bg-white-50">
      
      <img 
        src={Logo} 
        alt="Personal Planner Logo" 
        className="w-48 h-48 mb-6" 
      />

     
      <h1 className="text-5xl font-bold mb-4 text-purple-600 text-center">
        Personal Planner
      </h1>

      {/* Subtitlu */}
      <p className="text-xl text-gray-700 mb-8 text-center">
        Organize your tasks and vacations with ease!
      </p>
          <div className="flex gap-20">
            <button onClick={()=> navigate("/todo")}
                className="bg-violet-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition-colors">To-DO
                </button>
            <button onClick={()=> navigate("/vacations")}
                className="bg-violet-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition-colors">Vacations
                </button>
          </div>
        </div>
    );
}

export default HomePage;

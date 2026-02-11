import React, { useState, useEffect } from "react";
import { TrashIcon } from '@heroicons/react/24/solid';

function TodoPage() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split("T")[0]);


  useEffect(() => {
    fetch(`http://127.0.0.1:8000/tasks?date=${selectedDate}`)
      .then(res => res.json())
      .then(data => setTasks(data));
  }, [selectedDate]);

  const addTask = () => {
    fetch("http://127.0.0.1:8000/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTask, date: selectedDate })
    })
    .then(res => res.json())
    .then(() => {
      setTasks([...tasks, { title: newTask, date: selectedDate, status: "in progress" }]);
      setNewTask("");
    });
  };

  const deleteTask = (taskId) => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
      method: "DELETE"
    })
    .then(()=>{
      setTasks(tasks.filter(task => task.id !== taskId))
    }
    );
  };

  const markDone = (taskId) => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
      method: "PUT"
    })
    .then (()=>{
      setTasks(tasks.map(task=>task.id === taskId ? {... task, status: "done"} : task));
    });
  };

  return (
  <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
    <h1 className="text-violet-500 text-2xl font-bold mb-4 text-center">To-Do List</h1>

    <div className="flex gap-2 mb-4">
      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
        className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-500"
      />
      <input 
        type="text" 
        value={newTask} 
        onChange={(e) => setNewTask(e.target.value)} 
        placeholder="Add new task"
        className="flex-2 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button 
        onClick={addTask}
        className="bg-violet-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition-colors"
      >
        Add
      </button>
    </div>

    <ul className="space-y-2">
      {tasks.map((task, index) => (
        <li 
          key={index} 
          className="flex justify-between items-center bg-violet-50 p-3 rounded shadow-sm"
        >
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked = {task.status === "done"}
              onChange={()=> markDone(task.id)}
              className="w-5 h-5 accent-violet-500"
            />
            <span className={task.status === "done" ? "line-through text-gray-500" : ""}>
            {task.title}
            </span>
          </div>
          <TrashIcon 
            className="w-5 h-5 text-violet-500 hover:text-purple-700 cursor-pointer" 
            onClick={() => deleteTask(task.id)} 
          /> 
           
        </li>
      ))}
    </ul>
  </div>
);

}

export default TodoPage;

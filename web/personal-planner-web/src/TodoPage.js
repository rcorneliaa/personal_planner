import React, { useState, useEffect } from "react";

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

  return (
    <div>
      <h1>To-Do List</h1>
      <input
        type = "date"
        value = {selectedDate}
        onChange={(e)=> setSelectedDate(e.target.value)}
      />
      <input 
        type="text" 
        value={newTask} 
        onChange={(e) => setNewTask(e.target.value)} 
        placeholder="Add new task"
      />
      <button onClick={addTask}>Add</button>

      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            {task.title} - {task.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoPage;

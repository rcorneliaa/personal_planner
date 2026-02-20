import React, { useState, useEffect } from "react";
import { TrashIcon } from '@heroicons/react/24/solid';

function TodoPage() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [selectedDate, setSelectedDate] = useState(new Date().toLocaleDateString("en-CA"));
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState("");
  const [weeklyGoal, setWeeklyGoal] = useState(0);
  const [weekStart, setWeekStart] = useState(new Date().toLocaleDateString("en-CA"));


  useEffect(() => {
    fetch(`http://127.0.0.1:8000/tasks?date=${selectedDate}`)
      .then(res => res.json())
      .then(data => setTasks(data));
  }, [selectedDate]);

  useEffect(() => {
  const weekStart = getWeekStart(selectedDate); 
    fetch(`http://127.0.0.1:8000/habits/?week_start=${weekStart}`)
      .then(res => res.json())
      .then(data => setHabits(data));
  }, [selectedDate]);

  function getWeekStart(dateStr) {
    const date = new Date(dateStr);
    const day = date.getDay(); 
    const diff = date.getDate() - day + (day === 0 ? -6 : 1); 
    const weekStart = new Date(date.setDate(diff));
    return weekStart.toISOString().split("T")[0];
  }


  const addTask = () => {
    fetch("http://127.0.0.1:8000/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTask, date: selectedDate })
    })
    .then(res => res.json())
    .then((createdTask) => {
      setTasks([...tasks, createdTask]);
      setNewTask("");
    });
  };

  const addHabit = () => {
    fetch("http://127.0.0.1:8000/habits", {
      method: "POST",
      headers: {"Content-Type": "application/json" },
      body: JSON.stringify({title: newHabit, goal: weeklyGoal, logs: {} })
    })
    .then(res => res.json())
    .then((createdHabit) => {
      setHabits([...habits, { ...createdHabit, logs: {} }]);
      setNewHabit("");
      setWeeklyGoal(0);
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

  const deleteHabit = (habitId) => {
    fetch(`http://127.0.0.1:8000/habits/${habitId}`, {
      method: "DELETE"
    })
    .then(() => {
      setHabits(habits.filter(h => h.id !== habitId));
    });
  };

  const markDone = (taskId) => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
      method: "PUT"
    })
    .then (()=>{
      setTasks(tasks.map(task=>task.id === taskId ? {... task, status: "done"} : task));
    });
  };

  const toggleDay = (habitId, dayStr) => {
  setHabits(prev =>
    prev.map(h => {
      if (h.id !== habitId) return h;
      const newLogs = { ...(h.logs || {}) };
      newLogs[dayStr] = !newLogs[dayStr];
      return { ...h, logs: newLogs };
    })
  );

  fetch(`http://127.0.0.1:8000/habits/${habitId}?day=${dayStr}`, { method: "PUT" });
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
      <h1 className="text-violet-500 text-2xl font-bold mb-2">Habits (Weekly)</h1>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newHabit}
          onChange={e => setNewHabit(e.target.value)}
          placeholder="New habit"
          className="flex-1 border border-gray-300 rounded px-3 py-2"
        />
        <input
          type="number"
          value={weeklyGoal}
          onChange={e => setWeeklyGoal(Number(e.target.value))}
          placeholder="Goal"
          min={1}
          max={7}
          className="border border-gray-300 rounded px-3 py-2 w-20"
        />
        <button onClick={addHabit} className="bg-violet-500 text-white px-4 py-2 rounded">
          Add
        </button>
      </div>

      <table className="w-full text-center border-collapse">
        <thead>
          <tr>
            <th className="border p-1">Habit</th>
            {Array.from({length: 7}).map((_, i) => {
              const day = new Date(weekStart);
              day.setDate(day.getDate() + i);
              return <th key={i} className="border p-1">{day.toLocaleDateString("en-GB", { weekday: "short" })[0]}</th>
            })}
            <th className="border p-1">Goal</th>
            <th className="border p-1">Achieved</th>
            <th className="border p-1">Delete</th>
          </tr>
        </thead>
        <tbody>
          {habits.map(habit => {
            const achieved = Object.values(habit.logs || {}).filter(v => v).length;
            return (
              <tr key={habit.id}>
                <td className="border p-1">{habit.title}</td>
                {Array.from({length: 7}).map((_, i) => {
                  const day = new Date(weekStart);
                  day.setDate(day.getDate() + i);
                  const dayStr = day.toISOString().split("T")[0];
                  return (
                    <td
                      key={i}
                      onClick={() => toggleDay(habit.id, dayStr)}
                      className="border p-1 cursor-pointer"
                      style={{ backgroundColor: habit.logs?.[dayStr] ? "violet" : "white" }}
                    ></td>
                  )
                })}
                <td className="border p-1">{habit.weekly_goal}</td>
                <td className="border p-1">{achieved}</td>
                <td className="border p-1">
                  <button onClick={() => deleteHabit(habit.id)}>Delete</button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>

  </div>
);

}

export default TodoPage;

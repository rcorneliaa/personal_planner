import React, { useState, useEffect } from "react";
import { TrashIcon } from "@heroicons/react/24/solid";

/**
 * TodoPage component
 *
 * Main page for managing tasks and weekly habits.
 * Communicates with the FastAPI backend.
 *
 * Features:
 * - Add / delete / complete tasks
 * - Select date for tasks
 * - Track weekly habits
 * - Toggle habit completion per day
 *
 * Backend endpoints used:
 * - GET /tasks
 * - POST /tasks
 * - DELETE /tasks/{id}
 * - PUT /tasks/{id}
 * - GET /habits
 * - POST /habits
 * - DELETE /habits/{id}
 * - PUT /habits/{id}
 */

function TodoPage() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [selectedDate, setSelectedDate] = useState(formatDateLocal(new Date()));
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState("");
  const [weeklyGoal, setWeeklyGoal] = useState(0);

/**
 * Formats a Date object into YYYY-MM-DD string
 * used by the backend API.
 *
 * param {Date} date
 * returns {string}
 */
  function formatDateLocal(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
  }

/**
 * Calculates the Monday of the week for a given date.
 *
 * param {string} dateStr
 * returns {string}
 */

  function getWeekStart(dateStr) {
    const date = new Date(dateStr);
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    const monday = new Date(date);
    monday.setDate(diff);
    return formatDateLocal(monday);
  }

/**
 * Generates the 7 days of the current week.
 *
 * returns {Array}
 */

  function getWeekDays() {
    const start = new Date(weekStart);
    return Array.from({ length: 7 }, (_, i) => {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      return {
        label: d.toLocaleDateString("en-GB", { weekday: "short" })[0],
        date: formatDateLocal(d),
      };
    });
  }


  

  const weekStart = getWeekStart(selectedDate);
  const weekDays = getWeekDays();
 
  // ================= TASKS =================
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/tasks?date=${selectedDate}`)
      .then((res) => res.json())
      .then((data) => setTasks(data));
  }, [selectedDate]);

/**
 * Sends a request to create a new task.
 */
  const addTask = () => {
    fetch("http://127.0.0.1:8000/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTask, date: selectedDate }),
    })
      .then((res) => res.json())
      .then((createdTask) => {
        setTasks([...tasks, createdTask]);
        setNewTask("");
      });
  };

 /**
 * Deletes a task from the backend and updates UI.
 *
 * param {number} taskId
 */
  const deleteTask = (taskId) => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}`, { method: "DELETE" }).then(
      () => setTasks(tasks.filter((task) => task.id !== taskId))
    );
  };

  const markDone = (taskId) => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}`, { method: "PUT" }).then(
      () =>
        setTasks(
          tasks.map((task) =>
            task.id === taskId ? { ...task, status: "done" } : task
          )
        )
    );
  };

  // ================= HABITS =================
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/habits/?week_start=${weekStart}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("raw habits data:", data);
        setHabits(data)});
  }, [weekStart]);

  const addHabit = () => {
    fetch("http://127.0.0.1:8000/habits", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newHabit, goal: weeklyGoal }),
    })
      .then((res) => res.json())
      .then(() => {
        setNewHabit("");
        setWeeklyGoal(0);

        const ws = getWeekStart(selectedDate);
        fetch(`http://127.0.0.1:8000/habits/?week_start=${ws}`)
          .then((res) => res.json())
          .then((data) => setHabits(data));
      });
  };

  const deleteHabit = (habitId) => {
    fetch(`http://127.0.0.1:8000/habits/${habitId}`, { method: "DELETE" }).then(
      () => setHabits(habits.filter((h) => h.id !== habitId))
    );
  };


/**
 * Toggles habit completion for a specific day.
 *
 * param {number} habitId
 * param {string} dayStr
 */
  const toggleDay = (habitId, dayStr) => {
    // optimistic UI
    setHabits((prev) =>
      prev.map((h) => {
        if (h.id !== habitId) return h;
        const newLogs = { ...(h.logs || {}) };
        newLogs[dayStr] = !newLogs[dayStr];
        return { ...h, logs: newLogs };
      })
    );

    fetch(`http://127.0.0.1:8000/habits/${habitId}?day=${dayStr}`, {
      method: "PUT",
    });
  };

  // ================= UI =================
  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-violet-500 text-2xl font-bold mb-4 text-center">
        To-Do List
      </h1>

      <div className="flex gap-2 mb-4">
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="flex-1 border border-gray-300 rounded px-3 py-2"
        />
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Add new task"
          className="flex-2 border border-gray-300 rounded px-3 py-2"
        />
        <button
          onClick={addTask}
          className="bg-violet-500 text-white px-4 py-2 rounded"
        >
          Add
        </button>
      </div>

      <ul className="space-y-2">
        {tasks.map((task) => (
          <li
            key={task.id}
            className="flex justify-between items-center bg-violet-50 p-3 rounded"
          >
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={task.status === "done"}
                onChange={() => markDone(task.id)}
                className="w-5 h-5 accent-violet-500"
              />
              <span
                className={
                  task.status === "done" ? "line-through text-gray-500" : ""
                }
              >
                {task.title}
              </span>
            </div>
            <TrashIcon
              className="w-5 h-5 fill-violet-500 cursor-pointer"
              onClick={() => deleteTask(task.id)}
            />
          </li>
        ))}
      </ul>

      <h1 className="text-violet-500 text-2xl font-bold mt-6 mb-2">
        Habits (Weekly)
      </h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newHabit}
          onChange={(e) => setNewHabit(e.target.value)}
          placeholder="New habit"
          className="flex-1 border border-gray-300 rounded px-3 py-2"
        />
        <input
          type="number"
          value={weeklyGoal}
          onChange={(e) => setWeeklyGoal(Number(e.target.value))}
          min={1}
          max={7}
          className="border border-gray-300 rounded px-3 py-2 w-20"
        />
        <button
          onClick={addHabit}
          className="bg-violet-500 text-white px-4 py-2 rounded"
        >
          Add
        </button>
      </div>

      <table className="w-full text-center border-collapse">
        <thead>
          <tr>
            <th className="border p-1">Habit</th>
            {weekDays.map((d, i) => (
              <th key={i} className="border p-1">
                {d.label}
              </th>
            ))}
            <th className="border p-1">Goal</th>
            <th className="border p-1">Achieved</th>
            <th className="border p-1">Delete</th>
          </tr>
        </thead>
        <tbody>
          {habits.map((habit) => {
            console.log("habit logs keys:", Object.keys(habit.logs));
            console.log("habit logs values:", Object.values(habit.logs));
            const achieved = Object.values(habit.logs || {}).filter(Boolean)
              .length;

            return (
              <tr key={habit.id}>
                <td className="border p-1">{habit.title}</td>

                {weekDays.map((d, i) => {
                  const isDone = !!habit.logs?.[d.date];

                  return (
                    <td
                      key={i}
                      onClick={() => toggleDay(habit.id, d.date)}
                      className={`border p-1 cursor-pointer ${
                        isDone ? "bg-violet-500" : "bg-white"
                      }`}
                    ></td>
                  );
                })}

                <td className="border p-1">{habit.weekly_goal}</td>
                <td className="border p-1">{achieved}</td>
                <td className="border p-1">
                  <TrashIcon
                    className="w-5 h-5 fill-purple-500 cursor-pointer mx-auto"
                    onClick={() => deleteHabit(habit.id)}
                  />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default TodoPage;
import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8000';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetch(`${API_BASE}/tasks/`)
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(console.error);
  }, []);

  const addTask = async () => {
    if (!title.trim()) return;

    const newTask = {
      id: crypto.randomUUID(),
      title,
      description,
      completed: false,
    };

    try {
      const res = await fetch(`${API_BASE}/tasks/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask),
      });
      if (!res.ok) throw new Error('Failed to add task');
      setTasks([...tasks, newTask]);
      setTitle('');
      setDescription('');
    } catch (error) {
      console.error(error);
    }
  };

  const toggleComplete = async (id) => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    const updatedTask = { ...task, completed: !task.completed };

    try {
      const res = await fetch(`${API_BASE}/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTask),
      });
      if (!res.ok) throw new Error('Failed to update task');
      setTasks(tasks.map(t => (t.id === id ? updatedTask : t)));
    } catch (error) {
      console.error(error);
    }
  };

  const deleteTask = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete task');
      setTasks(tasks.filter(t => t.id !== id));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: 'auto' }}>
      <h1>Task Manager</h1>
      <div>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          style={{ width: '60%', marginRight: 8 }}
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
          style={{ width: '30%', marginRight: 8 }}
        />
        <button onClick={addTask}>Add Task</button>
      </div>
      <ul style={{ marginTop: 20 }}>
        {tasks.map(task => (
          <li key={task.id} style={{ marginBottom: 10 }}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleComplete(task.id)}
              style={{ marginRight: 8 }}
            />
            <strong>{task.title}</strong>: {task.description}
            <button
              onClick={() => deleteTask(task.id)}
              style={{ marginLeft: 12, color: 'red' }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

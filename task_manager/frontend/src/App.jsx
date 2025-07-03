import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  async function fetchTasks() {
    const res = await fetch(`${API_URL}/tasks`);
    const data = await res.json();
    setTasks(data);
  }

  async function addTask() {
    if (!title) return;
    await fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, completed: false }),
    });
    setTitle('');
    setDescription('');
    fetchTasks();
  }

  async function toggleComplete(id, completed) {
    await fetch(`${API_URL}/tasks/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !completed, title: tasks.find(t => t.id === id).title, description: tasks.find(t => t.id === id).description }),
    });
    fetchTasks();
  }

  async function deleteTask(id) {
    await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE' });
    fetchTasks();
  }

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 20 }}>
      <h1>Task Manager</h1>
      <input
        placeholder="Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
        style={{ width: '100%', marginBottom: 10 }}
      />
      <textarea
        placeholder="Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
        style={{ width: '100%', marginBottom: 10 }}
      />
      <button onClick={addTask}>Add Task</button>
      <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
        {tasks.map(task => (
          <li key={task.id} style={{ marginTop: 10, padding: 10, border: '1px solid #ddd' }}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleComplete(task.id, task.completed)}
            />{' '}
            <strong>{task.title}</strong>
            <p>{task.description}</p>
            <button onClick={() => deleteTask(task.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

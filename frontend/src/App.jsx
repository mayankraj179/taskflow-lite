import { useState, useEffect } from 'react'
import './App.css'

const API_BASE = '/api'

function App() {
  const [tasks, setTasks] = useState([])
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 })
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ title: '', description: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTasks()
    fetchStats()
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_BASE}/tasks`)
      if (response.ok) {
        const data = await response.json()
        setTasks(data)
      }
    } catch (err) {
      setError('Failed to fetch tasks')
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/tasks/stats`)
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (err) {
      console.error('Failed to fetch stats')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!formData.title.trim()) {
      setError('Title is required')
      return
    }

    try {
      const response = await fetch(`${API_BASE}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        setFormData({ title: '', description: '' })
        setShowForm(false)
        fetchTasks()
        fetchStats()
      } else {
        const data = await response.json()
        setError(data.detail || 'Failed to create task')
      }
    } catch (err) {
      setError('Failed to create task')
    }
  }

  const toggleTask = async (task) => {
    try {
      const response = await fetch(`${API_BASE}/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task.completed }),
      })

      if (response.ok) {
        fetchTasks()
        fetchStats()
      }
    } catch (err) {
      setError('Failed to update task')
    }
  }

  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        fetchTasks()
        fetchStats()
      }
    } catch (err) {
      setError('Failed to delete task')
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>TaskFlow Lite</h1>
          <p className="subtitle">Manage your tasks efficiently</p>
        </header>

        <div className="stats">
          <div className="stat-card">
            <span className="stat-number">{stats.total}</span>
            <span className="stat-label">Total</span>
          </div>
          <div className="stat-card">
            <span className="stat-number pending">{stats.pending}</span>
            <span className="stat-label">Pending</span>
          </div>
          <div className="stat-card">
            <span className="stat-number completed">{stats.completed}</span>
            <span className="stat-label">Completed</span>
          </div>
        </div>

        {error && <div className="error">{error}</div>}

        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Task'}
        </button>

        {showForm && (
          <form className="task-form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Task title *"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="input"
            />
            <textarea
              placeholder="Description (optional)"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="textarea"
              rows="3"
            />
            <button type="submit" className="btn btn-submit">
              Create Task
            </button>
          </form>
        )}

        {loading ? (
          <div className="loading">Loading tasks...</div>
        ) : (
          <div className="task-list">
            {tasks.length === 0 ? (
              <div className="empty-state">No tasks yet. Add your first task!</div>
            ) : (
              tasks.map((task) => (
                <div key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
                  <div className="task-content">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTask(task)}
                      className="checkbox"
                    />
                    <div className="task-details">
                      <h3 className="task-title">{task.title}</h3>
                      {task.description && (
                        <p className="task-description">{task.description}</p>
                      )}
                    </div>
                  </div>
                  <div className="task-actions">
                    <span className={`status-badge ${task.completed ? 'completed' : 'pending'}`}>
                      {task.completed ? 'Completed' : 'Pending'}
                    </span>
                    <button
                      className="btn btn-delete"
                      onClick={() => deleteTask(task.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App

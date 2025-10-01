import { useState, useEffect } from 'react'
import { createTask, listTasks } from './services/api'

function App() {
  const [tasks, setTasks] = useState([])
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchTasks = async () => {
    try {
      setLoading(true)
      const data = await listTasks()
      setTasks(data)
      setError(null)
    } catch (err) {
      setError('Failed to load tasks')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return

    try {
      setLoading(true)
      const result = await createTask(newTaskTitle)
      if (!result.id) {
        throw new Error('Failed to create task')
      }
      
      setNewTaskTitle('')
      await fetchTasks()
      setError(null)
    } catch (err) {
      setError('Failed to create task')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="todo-container">
      <h1>Todo List</h1>
      
      <form onSubmit={handleSubmit} className="todo-form">
        <div className="input-group">
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Add a new task"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            Add
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <ul className="todo-list">
          {tasks.map((task) => (
            <li key={task.id} className="todo-item">
              {task.title}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App

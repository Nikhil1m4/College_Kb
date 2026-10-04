import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiFetch } from '../lib/api'

export default function Admin() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function pingAdmin() {
      try {
        const data = await apiFetch('/api/admin/ping')
        setResult(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    pingAdmin()
  }, [])

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px' }}>
      <h1>Admin Dashboard</h1>
      <Link to="/">&larr; Back to Home</Link>
      
      <div style={{ marginTop: '30px' }}>
        {loading ? (
          <p>Checking admin access...</p>
        ) : error ? (
          <div style={{ padding: '20px', backgroundColor: '#fee', color: '#c00', border: '1px solid #c00', borderRadius: '8px' }}>
            <h3>Access Forbidden</h3>
            <p>{error}</p>
          </div>
        ) : (
          <div style={{ padding: '20px', backgroundColor: '#efe', color: '#090', border: '1px solid #090', borderRadius: '8px' }}>
            <h3>Access Granted</h3>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { apiFetch } from '../lib/api'

export default function Home() {
  const { signOut } = useAuth()
  const [userProfile, setUserProfile] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await apiFetch('/api/me')
        setUserProfile(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchProfile()
  }, [])

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px' }}>
      <h1>Home</h1>
      
      {loading ? (
        <p>Loading profile...</p>
      ) : error ? (
        <div style={{ color: 'red' }}>Failed to load profile: {error}</div>
      ) : (
        <div style={{ padding: '20px', backgroundColor: '#f0f0f0', borderRadius: '8px', marginBottom: '20px' }}>
          <p><strong>Email:</strong> {userProfile?.email}</p>
          <p><strong>Role:</strong> {userProfile?.role}</p>
        </div>
      )}

      <div style={{ display: 'flex', gap: '15px' }}>
        {userProfile?.role === 'admin' && (
          <Link to="/admin">Go to Admin Panel</Link>
        )}
        <Link to="/status">API Status Check</Link>
        <button onClick={signOut}>Log Out</button>
      </div>
    </div>
  )
}

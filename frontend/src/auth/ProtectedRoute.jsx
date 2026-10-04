import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from './AuthContext'

export default function ProtectedRoute() {
  const { session, loading } = useAuth()

  if (loading) return <p>Loading...</p>

  if (!session) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}

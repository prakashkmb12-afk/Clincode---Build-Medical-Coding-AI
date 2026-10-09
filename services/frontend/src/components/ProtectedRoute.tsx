import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth, AppRole } from '../context/AuthContext'

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedRoles?: AppRole[]
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center', background: '#0f172a', color: '#94a3b8' }}>
        <div>Loading ClinCode Session...</div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (allowedRoles && !allowedRoles.includes(user.role) && user.role !== 'admin') {
    // Redirect user to their own dashboard role route if unauthorized for this specific view
    return <Navigate to={`/dashboard/${user.role}`} replace />
  }

  return <>{children}</>
}

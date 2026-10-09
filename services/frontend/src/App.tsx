import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { Layout } from './components/Layout'

// Public Pages
import { Home } from './pages/Home'
import { AboutUs } from './pages/AboutUs'
import { Contact } from './pages/Contact'
import { Login } from './pages/Login'

// Role-Based Dashboards
import { CoderDashboard } from './pages/CoderDashboard'
import { CdiDashboard } from './pages/CdiDashboard'
import { ManagerDashboard } from './pages/ManagerDashboard'
import { AdminDashboard } from './pages/AdminDashboard'

// Core Workflow Pages
import { DocumentUpload } from './pages/DocumentUpload'
import { ProcessingCenter } from './pages/ProcessingCenter'
import { CodingReview } from './pages/CodingReview'
import { InvestigationWorkspace } from './pages/InvestigationWorkspace'
import { FinalResults } from './pages/FinalResults'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login />} />

          {/* Protected Dashboard & Workflow Routes */}
          <Route
            path="/dashboard/coder"
            element={
              <ProtectedRoute allowedRoles={['coder', 'admin']}>
                <Layout>
                  <CoderDashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/cdi"
            element={
              <ProtectedRoute allowedRoles={['cdi', 'admin']}>
                <Layout>
                  <CdiDashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/manager"
            element={
              <ProtectedRoute allowedRoles={['manager', 'admin']}>
                <Layout>
                  <ManagerDashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/admin"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <Layout>
                  <AdminDashboard />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Workflow Pages */}
          <Route
            path="/documents/new"
            element={
              <ProtectedRoute>
                <Layout>
                  <DocumentUpload />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/documents/:id/processing"
            element={
              <ProtectedRoute>
                <Layout>
                  <ProcessingCenter />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/documents/:id/review"
            element={
              <ProtectedRoute>
                <Layout>
                  <CodingReview />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/documents/:id/investigation"
            element={
              <ProtectedRoute>
                <Layout>
                  <InvestigationWorkspace />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/documents/:id/results"
            element={
              <ProtectedRoute>
                <Layout>
                  <FinalResults />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth, AppRole } from '../context/AuthContext'
import { LogIn, Shield, CheckCircle, AlertCircle, ArrowLeft, ExternalLink } from 'lucide-react'

export const Login: React.FC = () => {
  const { signInWithGoogle, demoLogin, loading, error, user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [selectedRole, setSelectedRole] = useState<AppRole>('coder')

  const from = (location.state as any)?.from?.pathname || `/dashboard/${selectedRole}`

  const handleGoogleSignIn = async () => {
    await signInWithGoogle(selectedRole)
    navigate(`/dashboard/${selectedRole}`, { replace: true })
  }

  const handleDemoSignIn = (role: AppRole) => {
    demoLogin(role)
    navigate(`/dashboard/${role}`, { replace: true })
  }

  if (user) {
    navigate(`/dashboard/${user.role}`, { replace: true })
  }

  const isUnauthorizedDomain = error?.includes('auth/unauthorized-domain')

  return (
    <div style={{ background: '#0f172a', color: '#f8fafc', minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: '1.5rem', fontFamily: 'Inter, sans-serif' }}>
      <div style={{ position: 'absolute', top: '1.5rem', left: '1.5rem' }}>
        <button onClick={() => navigate('/')} style={{ background: 'transparent', border: 'none', color: '#38bdf8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.9rem' }}>
          <ArrowLeft size={16} /> Back to Home
        </button>
      </div>

      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '16px', width: '100%', maxWidth: '460px', padding: '2.5rem 2rem', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)' }}>
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div style={{ display: 'inline-flex', background: '#2563eb', padding: '0.6rem 0.9rem', borderRadius: '12px', color: '#fff', fontWeight: 'bold', fontSize: '1.4rem', marginBottom: '1rem' }}>
            CC
          </div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, marginBottom: '0.4rem' }}>Sign In to ClinCode</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
            Clinical Documentation Intelligence & Medical Coding System
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem', fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 'bold', marginBottom: '0.4rem', color: '#f87171' }}>
              <AlertCircle size={18} />
              <span>{isUnauthorizedDomain ? 'Firebase Domain Authorization Required' : 'Authentication Error'}</span>
            </div>
            {isUnauthorizedDomain ? (
              <div style={{ lineHeight: 1.5 }}>
                <p style={{ margin: '0 0 0.5rem' }}>
                  Firebase blocked requests from <code>127.0.0.1</code>. Choose one of these quick fixes:
                </p>
                <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <a
                    href="http://localhost:3000/login"
                    style={{ background: '#2563eb', color: '#fff', padding: '0.4rem 0.8rem', borderRadius: '4px', textDecoration: 'none', textAlign: 'center', fontWeight: 600, fontSize: '0.8rem', display: 'inline-block' }}
                  >
                    🚀 Open via http://localhost:3000/login
                  </a>
                  <span style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
                    Or in Firebase Console ➔ Authentication ➔ Settings ➔ Authorized domains, add <code>127.0.0.1</code>.
                  </span>
                </div>
              </div>
            ) : (
              <div>{error}</div>
            )}
          </div>
        )}

        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem', fontWeight: 600 }}>
            Select Target Workspace Role:
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
            {(['coder', 'cdi', 'manager', 'admin'] as AppRole[]).map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => setSelectedRole(r)}
                style={{
                  padding: '0.5rem 0.75rem',
                  borderRadius: '6px',
                  border: selectedRole === r ? '2px solid #3b82f6' : '1px solid #334155',
                  background: selectedRole === r ? 'rgba(59, 130, 246, 0.15)' : '#0f172a',
                  color: selectedRole === r ? '#60a5fa' : '#94a3b8',
                  fontSize: '0.85rem',
                  fontWeight: selectedRole === r ? 600 : 400,
                  cursor: 'pointer',
                  textTransform: 'uppercase'
                }}
              >
                {r}
              </button>
            ))}
          </div>
        </div>

        {/* Primary Action: Google Sign-In */}
        <button
          onClick={handleGoogleSignIn}
          disabled={loading}
          style={{ width: '100%', background: '#ffffff', color: '#1e293b', border: 'none', padding: '0.85rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.95rem', cursor: loading ? 'not-allowed' : 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', marginBottom: '1.25rem' }}
        >
          <svg width="18" height="18" viewBox="0 0 18 18">
            <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.616z" />
            <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z" />
            <path fill="#FBBC05" d="M3.964 10.71 A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" />
            <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" />
          </svg>
          {loading ? 'Authenticating with Google...' : 'Continue with Google'}
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', margin: '1.25rem 0', color: '#475569', fontSize: '0.8rem' }}>
          <div style={{ flex: 1, height: '1px', background: '#334155' }}></div>
          <span>OR QUICK DEMO</span>
          <div style={{ flex: 1, height: '1px', background: '#334155' }}></div>
        </div>

        <button
          onClick={() => handleDemoSignIn(selectedRole)}
          style={{ width: '100%', background: '#334155', color: '#f8fafc', border: 'none', padding: '0.75rem', borderRadius: '8px', fontWeight: 500, fontSize: '0.9rem', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
        >
          <LogIn size={16} />
          Sign In as Demo {selectedRole.toUpperCase()}
        </button>

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.75rem', color: '#64748b', lineHeight: 1.5 }}>
          <Shield size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'middle' }} />
          Firebase Token Authentication enforced with backend RBAC roles.
        </div>
      </div>
    </div>
  )
}

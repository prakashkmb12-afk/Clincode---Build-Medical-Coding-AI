import React from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth, AppRole } from '../context/AuthContext'
import {
  FileText,
  UploadCloud,
  CheckCircle2,
  HelpCircle,
  BarChart3,
  ShieldCheck,
  LogOut,
  User,
  Activity,
  Layers,
  Search,
  Settings,
  AlertTriangle
} from 'lucide-react'

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout, switchRole } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleRoleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const role = e.target.value as AppRole
    switchRole(role)
    navigate(`/dashboard/${role}`)
  }

  const role = user?.role || 'coder'

  const navItemsByRole: Record<AppRole, Array<{ label: string; path: string; icon: any }>> = {
    coder: [
      { label: 'Overview', path: '/dashboard/coder', icon: Activity },
      { label: 'Upload Clinical Report', path: '/documents/new', icon: UploadCloud },
      { label: 'In Review', path: '/documents/DEMO-CHART-001/review', icon: FileText },
      { label: 'CDI Queries', path: '/dashboard/coder#queries', icon: HelpCircle },
      { label: 'Audit History', path: '/dashboard/coder#audit', icon: ShieldCheck }
    ],
    cdi: [
      { label: 'CDI Overview', path: '/dashboard/cdi', icon: Activity },
      { label: 'Pending Queries', path: '/dashboard/cdi#pending', icon: HelpCircle },
      { label: 'Resolved Queries', path: '/dashboard/cdi#resolved', icon: CheckCircle2 }
    ],
    manager: [
      { label: 'Throughput & Quality', path: '/dashboard/manager', icon: BarChart3 },
      { label: 'Acceptance Rates', path: '/dashboard/manager#acceptance', icon: CheckCircle2 },
      { label: 'QA Disagreements', path: '/dashboard/manager#qa', icon: AlertTriangle }
    ],
    admin: [
      { label: 'System Overview', path: '/dashboard/admin', icon: Activity },
      { label: 'User & Roles', path: '/dashboard/admin#users', icon: User },
      { label: 'Model Versions', path: '/dashboard/admin#models', icon: Layers },
      { label: 'System Health', path: '/dashboard/admin#health', icon: Settings }
    ]
  }

  const currentNavs = navItemsByRole[role] || navItemsByRole.coder

  return (
    <div className="app-container" style={{ display: 'flex', height: '100vh', width: '100vw', background: '#0f172a', color: '#f8fafc', overflow: 'hidden' }}>
      {/* Sidebar */}
      <aside style={{ width: '250px', background: '#1e293b', borderRight: '1px solid #334155', display: 'flex', flexDirection: 'column', padding: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem', padding: '0.5rem 0.75rem' }}>
          <div style={{ background: '#2563eb', padding: '0.4rem 0.6rem', borderRadius: '8px', color: '#fff', fontWeight: 'bold' }}>
            CC
          </div>
          <div>
            <div style={{ fontWeight: 'bold', fontSize: '1.1rem', color: '#f8fafc', letterSpacing: '-0.5px' }}>ClinCode</div>
            <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>AI Medical Coding</div>
          </div>
        </div>

        <div style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem', paddingLeft: '0.75rem' }}>
          Navigation ({role.toUpperCase()})
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', flex: 1 }}>
          {currentNavs.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '6px',
                  color: isActive ? '#38bdf8' : '#cbd5e1',
                  background: isActive ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                  fontWeight: isActive ? 600 : 400,
                  textDecoration: 'none',
                  fontSize: '0.9rem',
                  transition: 'all 0.15s ease'
                }}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* Demo Role Switcher */}
        <div style={{ background: '#0f172a', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155', marginTop: 'auto' }}>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.4rem' }}>Switch Role (Demo):</div>
          <select
            value={role}
            onChange={handleRoleChange}
            style={{ width: '100%', background: '#1e293b', color: '#f8fafc', border: '1px solid #475569', borderRadius: '4px', padding: '0.4rem', fontSize: '0.85rem' }}
          >
            <option value="coder">Coder Dashboard</option>
            <option value="cdi">CDI Specialist</option>
            <option value="manager">Manager Dashboard</option>
            <option value="admin">Admin Console</option>
          </select>
        </div>
      </aside>

      {/* Main Content Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Top Navbar */}
        <header style={{ height: '60px', background: '#1e293b', borderBottom: '1px solid #334155', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>ClinCode SaaS</span>
            <span style={{ color: '#475569' }}>/</span>
            <span style={{ fontWeight: 600, color: '#f8fafc', fontSize: '0.95rem', textTransform: 'capitalize' }}>
              {role} Workspace
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <Link to="/contact" style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.85rem' }}>Support</Link>
            <Link to="/about" style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.85rem' }}>About Us</Link>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', background: '#0f172a', padding: '0.35rem 0.75rem', borderRadius: '20px', border: '1px solid #334155' }}>
              <User size={16} color="#38bdf8" />
              <span style={{ fontSize: '0.85rem', color: '#e2e8f0', fontWeight: 500 }}>{user?.name || 'User'}</span>
              <span style={{ background: '#2563eb', color: '#fff', fontSize: '0.65rem', padding: '1px 6px', borderRadius: '10px', textTransform: 'uppercase', fontWeight: 'bold' }}>
                {user?.role}
              </span>
            </div>

            <button
              onClick={() => {
                logout()
                navigate('/')
              }}
              style={{ background: 'transparent', border: 'none', color: '#f87171', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem' }}
              title="Sign Out"
            >
              <LogOut size={16} />
              <span>Sign Out</span>
            </button>
          </div>
        </header>

        {/* Page Content Viewport */}
        <main style={{ flex: 1, overflow: 'auto', background: '#0f172a', padding: '1.5rem' }}>
          {children}
        </main>
      </div>
    </div>
  )
}

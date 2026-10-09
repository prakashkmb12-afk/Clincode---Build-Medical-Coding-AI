import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, DocumentResponse } from '../api/client'
import {
  FileText,
  UploadCloud,
  Clock,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Search,
  Plus
} from 'lucide-react'

export const CoderDashboard: React.FC = () => {
  const navigate = useNavigate()
  const [documents, setDocuments] = useState<DocumentResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    setLoading(true)
    try {
      const docs = await api.listDocuments(20)
      setDocuments(docs)
    } catch {
      // Fallback demo charts if backend table empty or initial setup
      setDocuments([
        { id: 'DEMO-CHART-001', external_ref: 'CHART-9081', doc_type: 'Inpatient Note', status: 'pending_review', created_at: '2026-10-09 10:15' },
        { id: 'DEMO-CHART-002', external_ref: 'CHART-8812', doc_type: 'ED Discharge', status: 'completed', created_at: '2026-10-09 09:30' },
        { id: 'DEMO-CHART-003', external_ref: 'CHART-7721', doc_type: 'Outpatient Clinic', status: 'in_investigation', created_at: '2026-10-08 16:45' }
      ])
    } finally {
      setLoading(false)
    }
  }

  const filteredDocs = documents.filter(d =>
    d.external_ref.toLowerCase().includes(search.toLowerCase()) ||
    d.doc_type.toLowerCase().includes(search.toLowerCase()) ||
    d.status.toLowerCase().includes(search.toLowerCase())
  )

  const pendingCount = documents.filter(d => d.status === 'pending_review' || d.status === 'in_review').length
  const completedCount = documents.filter(d => d.status === 'completed').length
  const processingCount = documents.filter(d => d.status === 'processing' || d.status === 'in_investigation').length

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Welcome Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem 1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0, color: '#f8fafc' }}>Coder Overview & Worklist</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginTop: '0.2rem' }}>
            Review AI-suggested ICD-10 codes, inspect evidence spans, and finalize clinical chart submissions.
          </p>
        </div>

        <button
          onClick={() => navigate('/documents/new')}
          style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.65rem 1.25rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.9rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', boxShadow: '0 4px 12px rgba(37, 99, 235, 0.3)' }}
        >
          <Plus size={18} /> Upload Clinical Report
        </button>
      </div>

      {/* Overview Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Assigned Charts</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f8fafc', margin: '0.3rem 0' }}>{documents.length}</div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Active in current shift</div>
        </div>

        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Pending Review</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#fbbf24', margin: '0.3rem 0' }}>{pendingCount}</div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Awaiting coder approval</div>
        </div>

        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>In Processing / AI</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#60a5fa', margin: '0.3rem 0' }}>{processingCount}</div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Pipeline running</div>
        </div>

        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Completed Charts</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#34d399', margin: '0.3rem 0' }}>{completedCount}</div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Signed off & exported</div>
        </div>
      </div>

      {/* Worklist Table */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: 0, color: '#f8fafc' }}>Clinical Worklist Queue</h2>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#0f172a', padding: '0.4rem 0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
            <Search size={16} color="#94a3b8" />
            <input
              type="text"
              placeholder="Search charts..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ background: 'transparent', border: 'none', color: '#f8fafc', fontSize: '0.85rem', outline: 'none' }}
            />
          </div>
        </div>

        {loading ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>Loading worklist...</div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>
                  <th style={{ padding: '0.75rem' }}>Document Ref ID</th>
                  <th style={{ padding: '0.75rem' }}>Document Type</th>
                  <th style={{ padding: '0.75rem' }}>Created At</th>
                  <th style={{ padding: '0.75rem' }}>Status</th>
                  <th style={{ padding: '0.75rem', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredDocs.map((doc) => (
                  <tr key={doc.id} style={{ borderBottom: '1px solid #1e293b' }}>
                    <td style={{ padding: '0.85rem 0.75rem', fontWeight: 600, color: '#f8fafc' }}>
                      <FileText size={16} style={{ verticalAlign: 'middle', marginRight: '6px', color: '#60a5fa' }} />
                      {doc.external_ref}
                    </td>
                    <td style={{ padding: '0.85rem 0.75rem', color: '#cbd5e1' }}>{doc.doc_type}</td>
                    <td style={{ padding: '0.85rem 0.75rem', color: '#94a3b8', fontSize: '0.85rem' }}>{doc.created_at}</td>
                    <td style={{ padding: '0.85rem 0.75rem' }}>
                      <span
                        style={{
                          padding: '0.25rem 0.6rem',
                          borderRadius: '12px',
                          fontSize: '0.75rem',
                          fontWeight: 600,
                          textTransform: 'uppercase',
                          background:
                            doc.status === 'completed' ? 'rgba(52, 211, 153, 0.15)' :
                            doc.status === 'in_investigation' ? 'rgba(168, 85, 247, 0.15)' :
                            'rgba(251, 191, 36, 0.15)',
                          color:
                            doc.status === 'completed' ? '#34d399' :
                            doc.status === 'in_investigation' ? '#c084fc' :
                            '#fbbf24'
                        }}
                      >
                        {doc.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td style={{ padding: '0.85rem 0.75rem', textAlign: 'right' }}>
                      <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                        <button
                          onClick={() => navigate(`/documents/${doc.id}/review`)}
                          style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.35rem 0.75rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 500, cursor: 'pointer' }}
                        >
                          Review Codes
                        </button>
                        {doc.status === 'in_investigation' && (
                          <button
                            onClick={() => navigate(`/documents/${doc.id}/investigation`)}
                            style={{ background: '#7c3aed', color: '#fff', border: 'none', padding: '0.35rem 0.75rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 500, cursor: 'pointer' }}
                          >
                            Agents View
                          </button>
                        )}
                        {doc.status === 'completed' && (
                          <button
                            onClick={() => navigate(`/documents/${doc.id}/results`)}
                            style={{ background: '#059669', color: '#fff', border: 'none', padding: '0.35rem 0.75rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 500, cursor: 'pointer' }}
                          >
                            Export FHIR
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

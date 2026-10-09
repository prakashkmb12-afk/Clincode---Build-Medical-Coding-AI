import React, { useState, useEffect } from 'react'
import { api, QueryResponse } from '../api/client'
import { HelpCircle, FileText, CheckCircle2, Send, AlertTriangle, Plus } from 'lucide-react'

export const CdiDashboard: React.FC = () => {
  const [queries, setQueries] = useState<QueryResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [newTitle, setNewTitle] = useState('')
  const [newEvidence, setNewEvidence] = useState('')
  const [newDraft, setNewDraft] = useState('')
  const [selectedDocId, setSelectedDocId] = useState('DEMO-CHART-001')
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    loadQueries()
  }, [])

  const loadQueries = async () => {
    setLoading(true)
    try {
      const q = await api.getQueries()
      setQueries(q)
    } catch {
      // Fallback CDI queries for demo
      setQueries([
        {
          id: 'cdi-q-101',
          document_id: 'DEMO-CHART-001',
          title: 'Specificity of Heart Failure Type',
          status: 'pending_physician',
          evidence_text: 'Patient presented with acute dyspnea on chronic heart failure background, EF 25%.',
          draft_query: 'Please clarify if heart failure is acute, chronic, or acute-on-chronic systolic/diastolic.',
          created_at: '2026-10-09 11:20'
        },
        {
          id: 'cdi-q-102',
          document_id: 'DEMO-CHART-003',
          title: 'Sepsis vs SIRS Documentation Link',
          status: 'resolved',
          evidence_text: 'Febrile 102.4F, tachycardia, elevated WBC. Empiric IV antibiotics started.',
          draft_query: 'Please confirm if the clinical presentation represents acute organ dysfunction due to sepsis.',
          created_at: '2026-10-08 14:15'
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleCreateQuery = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTitle || !newDraft) return
    try {
      const created = await api.createDirectQuery(selectedDocId, newTitle, newEvidence, newDraft)
      setQueries([created, ...queries])
      setShowModal(false)
      setNewTitle('')
      setNewEvidence('')
      setNewDraft('')
    } catch {
      // Demo fallback
      const mockQ: QueryResponse = {
        id: `cdi-q-${Date.now()}`,
        document_id: selectedDocId,
        title: newTitle,
        status: 'pending_physician',
        evidence_text: newEvidence,
        draft_query: newDraft,
        created_at: new Date().toISOString().replace('T', ' ').substring(0, 16)
      }
      setQueries([mockQ, ...queries])
      setShowModal(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem 1.5rem' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0, color: '#f8fafc' }}>CDI Specialist Dashboard</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginTop: '0.2rem' }}>
            Manage Clinical Documentation Improvement queries, document gaps, and physician query workflows.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.65rem 1.25rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.9rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <Plus size={18} /> Create Physician Query
        </button>
      </div>

      {/* Query Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Total Queries</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f8fafc', margin: '0.3rem 0' }}>{queries.length}</div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Active CDI portfolio</div>
        </div>

        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Pending Physician</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#fbbf24', margin: '0.3rem 0' }}>
            {queries.filter(q => q.status === 'pending_physician').length}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Awaiting clarification</div>
        </div>

        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '1.25rem' }}>
          <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Resolved Queries</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#34d399', margin: '0.3rem 0' }}>
            {queries.filter(q => q.status === 'resolved').length}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Updated chart notes</div>
        </div>
      </div>

      {/* Query List */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 1rem', color: '#f8fafc' }}>CDI Physician Query Portfolio</h2>

        {queries.map((q) => (
          <div key={q.id} style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '1.25rem', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: '#60a5fa', fontWeight: 600, marginRight: '0.5rem' }}>{q.document_id}</span>
                <strong style={{ fontSize: '1.05rem', color: '#f8fafc' }}>{q.title}</strong>
              </div>
              <span
                style={{
                  padding: '0.2rem 0.6rem',
                  borderRadius: '12px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  background: q.status === 'resolved' ? 'rgba(52, 211, 153, 0.15)' : 'rgba(251, 191, 36, 0.15)',
                  color: q.status === 'resolved' ? '#34d399' : '#fbbf24'
                }}
              >
                {q.status.replace('_', ' ')}
              </span>
            </div>

            <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
              <strong>Clinical Evidence Context:</strong> "{q.evidence_text}"
            </div>

            <div style={{ background: '#1e293b', padding: '0.75rem', borderRadius: '6px', borderLeft: '3px solid #3b82f6', fontSize: '0.9rem', color: '#cbd5e1' }}>
              <strong style={{ color: '#60a5fa', display: 'block', marginBottom: '0.2rem', fontSize: '0.8rem' }}>Draft Non-Leading Query:</strong>
              {q.draft_query}
            </div>
          </div>
        ))}
      </div>

      {/* Modal to Create Query */}
      {showModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(15, 23, 42, 0.85)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', width: '550px', padding: '1.5rem' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '1rem', color: '#f8fafc' }}>Draft Non-Leading CDI Query</h3>
            <form onSubmit={handleCreateQuery} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Document Ref ID:</label>
                <input
                  type="text"
                  value={selectedDocId}
                  onChange={e => setSelectedDocId(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Query Title / Documentation Gap:</label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={e => setNewTitle(e.target.value)}
                  placeholder="e.g. Sepsis vs Acute Organ Dysfunction"
                  style={{ width: '100%', padding: '0.6rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc' }}
                  required
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Supporting Evidence Text:</label>
                <textarea
                  value={newEvidence}
                  onChange={e => setNewEvidence(e.target.value)}
                  rows={2}
                  placeholder="Quote exact sentence from physician note..."
                  style={{ width: '100%', padding: '0.6rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Draft Physician Query (Non-Leading):</label>
                <textarea
                  value={newDraft}
                  onChange={e => setNewDraft(e.target.value)}
                  rows={3}
                  placeholder="Please clarify clinical documentation based on patient findings..."
                  style={{ width: '100%', padding: '0.6rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc' }}
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
                <button type="button" onClick={() => setShowModal(false)} style={{ background: '#334155', color: '#94a3b8', border: 'none', padding: '0.6rem 1rem', borderRadius: '6px', cursor: 'pointer' }}>Cancel</button>
                <button type="submit" style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.6rem 1.25rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 600 }}>Save Query</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

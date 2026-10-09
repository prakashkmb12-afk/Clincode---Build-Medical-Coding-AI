import React, { useState, useEffect } from 'react'

interface DocumentItem {
  id: string
  external_ref: string
  doc_type: string
  status: string
  created_at: string
}

interface SuggestionItem {
  id: string
  icd10_code: string
  description: string
  calibrated_conf: number
  band: 'auto' | 'review' | 'low'
  justification_md?: string
  evidence_spans?: Array<{ start: number; end: number; text: string }>
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'worklist' | 'review' | 'dashboard'>('review')
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [selectedDocId, setSelectedDocId] = useState<string>('')
  const [noteText, setNoteText] = useState<string>('')
  const [suggestions, setSuggestions] = useState<SuggestionItem[]>([])
  const [activeSpan, setActiveSpan] = useState<{ start: number; end: number } | null>(null)
  const [coderFeedback, setCoderFeedback] = useState<Record<string, string>>({})

  // Demo Note Content
  const demoNote = `CHIEF COMPLAINT:
Shortness of breath and worsening lower extremity swelling.

HISTORY OF PRESENT ILLNESS:
Patient is a 68-year-old male with a history of acute-on-chronic systolic heart failure presenting to the emergency department with severe dyspnea on exertion. Patient denies chest pain. Family history of diabetes mellitus.

PAST MEDICAL HISTORY:
Essential hypertension, type 2 diabetes mellitus, history of stroke.

ASSESSMENT AND PLAN:
1. Acute-on-chronic systolic heart failure: Initiate IV furosemide, monitor daily weights and electrolyte panel.
2. Hypertension: Continue home oral lisinopril.
3. Possible sepsis: Patient is febrile with elevated WBC count. Order blood cultures.`

  useEffect(() => {
    setNoteText(demoNote)
    setSelectedDocId('DEMO-CHART-001')
    setSuggestions([
      {
        id: 'sugg-1',
        icd10_code: 'I50.23',
        description: 'Acute-on-chronic systolic (congestive) heart failure',
        calibrated_conf: 0.96,
        band: 'auto',
        justification_md: 'Cited evidence confirms acute dyspnea on chronic heart failure background.',
        evidence_spans: [{ start: 67, end: 120, text: 'acute-on-chronic systolic heart failure' }]
      },
      {
        id: 'sugg-2',
        icd10_code: 'I10',
        description: 'Essential (primary) hypertension',
        calibrated_conf: 0.92,
        band: 'auto',
        justification_md: 'Documented under past medical history.',
        evidence_spans: [{ start: 275, end: 297, text: 'Essential hypertension' }]
      },
      {
        id: 'sugg-3',
        icd10_code: 'A41.9',
        description: 'Sepsis, unspecified organism',
        calibrated_conf: 0.58,
        band: 'low',
        justification_md: 'Possible sepsis flagged for CDI physician query.',
        evidence_spans: [{ start: 450, end: 465, text: 'Possible sepsis' }]
      }
    ])
  }, [])

  const handleAction = (suggestionId: string, action: 'accept' | 'reject') => {
    setCoderFeedback(prev => ({ ...prev, [suggestionId]: action }))
  }

  const handleEvidenceClick = (span: { start: number; end: number }) => {
    setActiveSpan(span)
  }

  return (
    <div className="app-container">
      <header className="navbar">
        <div className="logo">ClinCode Console</div>
        <div className="nav-links">
          <button className={activeTab === 'worklist' ? 'active' : ''} onClick={() => setActiveTab('worklist')}>Worklist</button>
          <button className={activeTab === 'review' ? 'active' : ''} onClick={() => setActiveTab('review')}>Chart Review</button>
          <button className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>Dashboard</button>
        </div>
      </header>

      <main className="content">
        {activeTab === 'review' && (
          <div className="split-view">
            {/* Note Viewer Panel */}
            <div className="panel">
              <div className="panel-header">
                <span className="panel-title">Clinical Note — {selectedDocId}</span>
                <span className="badge badge-auto">De-identified</span>
              </div>
              <div className="scroll-area">
                <pre className="note-text">
                  {noteText}
                </pre>
              </div>
            </div>

            {/* Code Suggestions Panel */}
            <div className="panel">
              <div className="panel-header">
                <span className="panel-title">Code Suggestions & Evidence</span>
                <span className="badge badge-review">{suggestions.length} Candidates</span>
              </div>
              <div className="scroll-area">
                {suggestions.map(sugg => {
                  const status = coderFeedback[sugg.id]
                  return (
                    <div key={sugg.id} className="card">
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span style={{ fontWeight: 'bold', fontSize: '1.1rem', color: '#60a5fa' }}>{sugg.icd10_code}</span>
                        <span className={`badge badge-${sugg.band}`}>{sugg.band.toUpperCase()} ({(sugg.calibrated_conf * 100).toFixed(0)}%)</span>
                      </div>
                      <div style={{ fontSize: '0.95rem', color: '#e2e8f0', marginBottom: '0.5rem' }}>{sugg.description}</div>
                      {sugg.justification_md && (
                        <div style={{ fontSize: '0.85rem', color: '#94a3b8', fontStyle: 'italic', marginBottom: '0.75rem' }}>
                          "{sugg.justification_md}"
                        </div>
                      )}

                      {sugg.evidence_spans && sugg.evidence_spans.length > 0 && (
                        <button
                          className="btn"
                          style={{ background: '#334155', color: '#60a5fa', marginBottom: '0.75rem' }}
                          onClick={() => handleEvidenceClick(sugg.evidence_spans![0])}
                        >
                          Jump to Evidence Span
                        </button>
                      )}

                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <button
                          className={`btn ${status === 'accept' ? 'btn-success' : 'btn-success'}`}
                          style={{ opacity: status && status !== 'accept' ? 0.4 : 1 }}
                          onClick={() => handleAction(sugg.id, 'accept')}
                        >
                          {status === 'accept' ? 'Accepted' : 'Accept'}
                        </button>
                        <button
                          className={`btn ${status === 'reject' ? 'btn-danger' : 'btn-danger'}`}
                          style={{ opacity: status && status !== 'reject' ? 0.4 : 1 }}
                          onClick={() => handleAction(sugg.id, 'reject')}
                        >
                          {status === 'reject' ? 'Rejected' : 'Reject'}
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'worklist' && (
          <div className="panel" style={{ height: '100%' }}>
            <div className="panel-header">
              <span className="panel-title">Coder Worklist</span>
            </div>
            <div className="scroll-area">
              <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
                    <th style={{ padding: '0.75rem' }}>Ref ID</th>
                    <th style={{ padding: '0.75rem' }}>Type</th>
                    <th style={{ padding: '0.75rem' }}>Status</th>
                    <th style={{ padding: '0.75rem' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style={{ borderBottom: '1px solid #1e293b' }}>
                    <td style={{ padding: '0.75rem' }}>DEMO-CHART-001</td>
                    <td style={{ padding: '0.75rem' }}>Discharge Summary</td>
                    <td style={{ padding: '0.75rem' }}><span className="badge badge-auto">READY</span></td>
                    <td style={{ padding: '0.75rem' }}>
                      <button className="btn btn-success" onClick={() => setActiveTab('review')}>Review Chart</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'dashboard' && (
          <div className="panel" style={{ height: '100%' }}>
            <div className="panel-header">
              <span className="panel-title">Coding Manager Dashboard</span>
            </div>
            <div className="scroll-area" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
              <div className="card">
                <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Auto-Accept Precision</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#34d399' }}>98.8%</div>
              </div>
              <div className="card">
                <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Top-5 Retrieval Recall</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#60a5fa' }}>88.5%</div>
              </div>
              <div className="card">
                <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Avg Review Time / Chart</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#fbbf24' }}>5.2 min</div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

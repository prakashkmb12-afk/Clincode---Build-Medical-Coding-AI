import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, SuggestionResponse } from '../api/client'
import {
  Check,
  X,
  Edit3,
  GitBranch,
  ShieldCheck,
  AlertTriangle,
  Send,
  ArrowRight,
  ExternalLink
} from 'lucide-react'

const SAMPLE_CLINICAL_NOTE = `CHIEF COMPLAINT:
Shortness of breath and worsening lower extremity swelling.

HISTORY OF PRESENT ILLNESS:
Patient is a 68-year-old male with a history of acute-on-chronic systolic heart failure presenting to the emergency department with severe dyspnea on exertion. Patient denies chest pain. Family history of diabetes mellitus.

PAST MEDICAL HISTORY:
Essential hypertension, type 2 diabetes mellitus, history of stroke.

ASSESSMENT AND PLAN:
1. Acute-on-chronic systolic heart failure: Initiate IV furosemide, monitor daily weights and electrolyte panel.
2. Hypertension: Continue home oral lisinopril.
3. Possible sepsis: Patient is febrile with elevated WBC count. Order blood cultures.`

export const CodingReview: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const docId = id || 'DEMO-CHART-001'

  const [noteText, setNoteText] = useState(SAMPLE_CLINICAL_NOTE)
  const [suggestions, setSuggestions] = useState<SuggestionResponse[]>([])
  const [activeSpan, setActiveSpan] = useState<{ start: number; end: number } | null>(null)
  const [actionsMap, setActionsMap] = useState<Record<string, { status: string; modifiedCode?: string; reason?: string }>>({})
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    loadChartData()
  }, [docId])

  const loadChartData = async () => {
    setLoading(true)
    try {
      const suggs = await api.getSuggestions(docId)
      setSuggestions(suggs)
    } catch {
      // Fallback suggestions for demo review
      setSuggestions([
        {
          id: 'sugg-1',
          document_id: docId,
          icd10_code: 'I50.23',
          description: 'Acute-on-chronic systolic (congestive) heart failure',
          calibrated_conf: 0.96,
          band: 'auto',
          justification_md: 'Documented in HPI and Assessment; acute dyspnea on chronic heart failure background.',
          evidence_spans: [{ start: noteText.indexOf('acute-on-chronic systolic heart failure'), end: noteText.indexOf('acute-on-chronic systolic heart failure') + 40, text: 'acute-on-chronic systolic heart failure' }],
          status: 'pending'
        },
        {
          id: 'sugg-2',
          document_id: docId,
          icd10_code: 'I10',
          description: 'Essential (primary) hypertension',
          calibrated_conf: 0.94,
          band: 'auto',
          justification_md: 'Documented in Past Medical History and Assessment Plan #2.',
          evidence_spans: [{ start: noteText.indexOf('Essential hypertension'), end: noteText.indexOf('Essential hypertension') + 22, text: 'Essential hypertension' }],
          status: 'pending'
        },
        {
          id: 'sugg-3',
          document_id: docId,
          icd10_code: 'A41.9',
          description: 'Sepsis, unspecified organism',
          calibrated_conf: 0.62,
          band: 'low',
          justification_md: 'Assessment #3 lists possible sepsis; febrile with elevated WBC.',
          evidence_spans: [{ start: noteText.indexOf('Possible sepsis'), end: noteText.indexOf('Possible sepsis') + 15, text: 'Possible sepsis' }],
          excludes1_warning: 'Check Excludes1: Do not code with SIRS non-infectious unless organism confirmed.',
          status: 'pending'
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (suggId: string, action: 'accept' | 'reject' | 'modify', modifiedCode?: string) => {
    setActionsMap(prev => ({
      ...prev,
      [suggId]: { status: action, modifiedCode }
    }))
    try {
      await api.submitAction({
        suggestion_id: suggId,
        action,
        modified_code: modifiedCode
      })
    } catch {
      // Action saved locally for offline demo
    }
  }

  const handleFinalSubmit = async () => {
    setSubmitting(true)
    try {
      await api.submitFinalReview(docId)
    } catch {
      // Submitted demo
    } finally {
      setSubmitting(false)
      navigate(`/documents/${docId}/results`)
    }
  }

  const renderHighlightedNote = () => {
    if (!activeSpan) return noteText

    const before = noteText.substring(0, activeSpan.start)
    const match = noteText.substring(activeSpan.start, activeSpan.end)
    const after = noteText.substring(activeSpan.end)

    return (
      <>
        {before}
        <mark style={{ background: 'rgba(245, 158, 11, 0.4)', color: '#fff', borderBottom: '2px solid #fbbf24', padding: '2px 4px', borderRadius: '4px' }}>
          {match}
        </mark>
        {after}
      </>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 110px)', gap: '1rem' }}>
      {/* Header Bar */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '0.85rem 1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: '#60a5fa', fontWeight: 600 }}>CHART REVIEW CONSOLE — {docId}</span>
          <h1 style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0, color: '#f8fafc' }}>
            Evidence-Linked Coding Review Workspace
          </h1>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <button
            onClick={() => navigate(`/documents/${docId}/investigation`)}
            style={{ background: '#7c3aed', color: '#fff', border: 'none', padding: '0.55rem 1rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <GitBranch size={16} /> Open LangGraph Investigation
          </button>
          <button
            onClick={handleFinalSubmit}
            disabled={submitting}
            style={{ background: '#059669', color: '#fff', border: 'none', padding: '0.55rem 1.25rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <Send size={16} /> Submit Final Chart
          </button>
        </div>
      </div>

      {/* Split Screen Container */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', flex: 1, overflow: 'hidden' }}>
        {/* Left Panel: Clinical Note Viewer */}
        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ padding: '0.75rem 1rem', background: '#0f172a', borderBottom: '1px solid #334155', fontSize: '0.85rem', fontWeight: 600, color: '#94a3b8' }}>
            De-Identified Clinical Report Text & Evidence Spans
          </div>
          <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', fontFamily: 'monospace', fontSize: '0.9rem', lineHeight: 1.6, color: '#cbd5e1', whiteSpace: 'pre-wrap' }}>
            {renderHighlightedNote()}
          </div>
        </div>

        {/* Right Panel: ICD-10 Code Suggestions */}
        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ padding: '0.75rem 1rem', background: '#0f172a', borderBottom: '1px solid #334155', fontSize: '0.85rem', fontWeight: 600, color: '#94a3b8', display: 'flex', justifyContent: 'space-between' }}>
            <span>Suggested ICD-10-CM Recommendations</span>
            <span>{suggestions.length} Candidates</span>
          </div>

          <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {suggestions.map((sugg) => {
              const currentAction = actionsMap[sugg.id]?.status || 'pending'
              return (
                <div
                  key={sugg.id}
                  style={{
                    background: '#0f172a',
                    border: currentAction === 'accept' ? '1px solid #34d399' : currentAction === 'reject' ? '1px solid #ef4444' : '1px solid #334155',
                    borderRadius: '8px',
                    padding: '1rem'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                      <span style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#60a5fa' }}>{sugg.icd10_code}</span>
                      <span
                        style={{
                          fontSize: '0.7rem',
                          fontWeight: 'bold',
                          padding: '2px 8px',
                          borderRadius: '10px',
                          textTransform: 'uppercase',
                          background: sugg.band === 'auto' ? 'rgba(52, 211, 153, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                          color: sugg.band === 'auto' ? '#34d399' : '#f87171'
                        }}
                      >
                        {sugg.band} ({Math.round(sugg.calibrated_conf * 100)}%)
                      </span>
                    </div>

                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      <button
                        onClick={() => handleAction(sugg.id, 'accept')}
                        style={{ background: currentAction === 'accept' ? '#059669' : '#334155', color: '#fff', border: 'none', padding: '0.3rem 0.6rem', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.2rem' }}
                      >
                        <Check size={14} /> Accept
                      </button>
                      <button
                        onClick={() => handleAction(sugg.id, 'reject')}
                        style={{ background: currentAction === 'reject' ? '#dc2626' : '#334155', color: '#fff', border: 'none', padding: '0.3rem 0.6rem', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.2rem' }}
                      >
                        <X size={14} /> Reject
                      </button>
                    </div>
                  </div>

                  <div style={{ fontSize: '0.9rem', color: '#f8fafc', fontWeight: 500, marginBottom: '0.4rem' }}>
                    {sugg.description}
                  </div>

                  <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.6rem' }}>
                    {sugg.justification_md}
                  </div>

                  {sugg.excludes1_warning && (
                    <div style={{ background: 'rgba(239, 68, 68, 0.12)', border: '1px solid #ef4444', color: '#fca5a5', padding: '0.4rem 0.6rem', borderRadius: '4px', fontSize: '0.75rem', marginBottom: '0.6rem' }}>
                      ⚠️ {sugg.excludes1_warning}
                    </div>
                  )}

                  {/* Evidence Spans Nav */}
                  {sugg.evidence_spans && sugg.evidence_spans.length > 0 && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                      <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Evidence Span:</span>
                      {sugg.evidence_spans.map((span, idx) => (
                        <button
                          key={idx}
                          onClick={() => setActiveSpan(span)}
                          style={{ background: '#1e293b', border: '1px solid #3b82f6', color: '#60a5fa', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', cursor: 'pointer' }}
                        >
                          "{span.text}"
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )})}
          </div>
        </div>
      </div>
    </div>
  )
}

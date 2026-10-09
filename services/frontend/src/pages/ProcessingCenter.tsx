import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { CheckCircle2, Loader2, ArrowRight, Activity, AlertCircle } from 'lucide-react'

const PIPELINE_STAGES = [
  '1. Document Format & Length Validation',
  '2. Tesseract OCR Engine (PDF/Scanned)',
  '3. De-Identification & PHI Key Vault Scrubbing',
  '4. Clinical Sectionization & Context Parsing',
  '5. Bio_ClinicalBERT Named Entity Recognition',
  '6. Context Assertion Classification (Present/Negated)',
  '7. Clinical Entity Normalization & Deduplication',
  '8. Qdrant ICD-10 Vector Dense Retrieval',
  '9. Reciprocal Rank Fusion (RRF) Candidate Scoring',
  '10. ONNX Cross-Encoder Deep Reranking',
  '11. Hierarchy & Excludes1 Conflict Validation',
  '12. Isotonic Confidence Calibration & Band Triage',
  '13. Grounded Verification Output Ready'
]

export const ProcessingCenter: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [currentStageIdx, setCurrentStageIdx] = useState<number>(0)
  const [completed, setCompleted] = useState<boolean>(false)

  useEffect(() => {
    // Progress through pipeline stages realistically
    const interval = setInterval(() => {
      setCurrentStageIdx((prev) => {
        if (prev < PIPELINE_STAGES.length - 1) {
          return prev + 1
        } else {
          setCompleted(true)
          clearInterval(interval)
          return prev
        }
      })
    }, 400)

    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: '#60a5fa', fontWeight: 600, textTransform: 'uppercase' }}>Document ID: {id}</span>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: '0.2rem 0 0', color: '#f8fafc' }}>AI Processing Center</h1>
        </div>

        {completed ? (
          <button
            onClick={() => navigate(`/documents/${id || 'DEMO-CHART-001'}/review`)}
            style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.7rem 1.3rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.95rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', boxShadow: '0 4px 12px rgba(37, 99, 235, 0.4)' }}
          >
            Open Coding Review Workspace
            <ArrowRight size={18} />
          </button>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#38bdf8', fontSize: '0.9rem', fontWeight: 500 }}>
            <Loader2 size={18} className="animate-spin" /> Running Pipeline...
          </div>
        )}
      </div>

      {/* Pipeline Stages Card */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.5rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 1.25rem', color: '#f8fafc' }}>
          13-Stage Clinical AI Pipeline Execution
        </h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
          {PIPELINE_STAGES.map((stageName, idx) => {
            const isDone = idx < currentStageIdx || completed
            const isCurrent = idx === currentStageIdx && !completed
            return (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justify: 'space-between',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  background: isCurrent ? 'rgba(59, 130, 246, 0.12)' : '#0f172a',
                  border: isCurrent ? '1px solid #3b82f6' : '1px solid #1e293b',
                  color: isDone ? '#34d399' : isCurrent ? '#38bdf8' : '#64748b'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.9rem', fontWeight: isCurrent || isDone ? 500 : 400 }}>
                  {isDone ? (
                    <CheckCircle2 size={18} color="#34d399" />
                  ) : isCurrent ? (
                    <Loader2 size={18} color="#38bdf8" style={{ animation: 'spin 1s linear infinite' }} />
                  ) : (
                    <div style={{ width: '18px', height: '18px', borderRadius: '50%', border: '2px solid #475569' }}></div>
                  )}
                  <span>{stageName}</span>
                </div>

                <span style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase' }}>
                  {isDone ? 'Completed' : isCurrent ? 'Processing...' : 'Queued'}
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

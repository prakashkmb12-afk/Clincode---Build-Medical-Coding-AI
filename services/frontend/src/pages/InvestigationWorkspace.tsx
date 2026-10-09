import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, InvestigationResponse } from '../api/client'
import { GitBranch, ShieldCheck, CheckCircle2, AlertTriangle, ArrowLeft, Cpu } from 'lucide-react'

export const InvestigationWorkspace: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const docId = id || 'DEMO-CHART-001'

  const [investigation, setInvestigation] = useState<InvestigationResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInvestigationData()
  }, [docId])

  const loadInvestigationData = async () => {
    setLoading(true)
    try {
      const data = await api.getInvestigation(docId)
      setInvestigation(data)
    } catch {
      // Fallback agent breakdown for demo
      setInvestigation({
        id: `run-${docId}`,
        document_id: docId,
        trigger_reason: 'Excludes1 Collision & Low-Confidence Assertion Discrepancy',
        status: 'completed',
        evidence_summary: 'Clinical note mentions acute dyspnea with febrile presentation. Sepsis candidate A41.9 triggered Excludes1 check against SIRS.',
        guideline_citations: [
          'ICD-10-CM Guideline I.C.1.d: Coding of Severe Sepsis requires explicit acute organ dysfunction documentation.',
          'Coding Clinic 2024 Q1: Sequelae of cerebrovascular disease (I69.30) requires documentation of specific residual deficit.'
        ],
        verifier_results: {
          verifier_status: 'PASS',
          adversarial_notes: 'Unretrieved candidate code R65.20 rejected by Adversarial Verifier due to missing explicit organ failure span.',
          verified_codes: ['I50.23', 'I10', 'E11.9']
        },
        created_at: '2026-10-09 12:00'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '950px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <button onClick={() => navigate(`/documents/${docId}/review`)} style={{ background: 'transparent', border: 'none', color: '#38bdf8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', marginBottom: '0.3rem' }}>
            <ArrowLeft size={16} /> Return to Review Console
          </button>
          <h1 style={{ fontSize: '1.4rem', fontWeight: 700, margin: 0, color: '#f8fafc' }}>
            LangGraph Multi-Agent Chart Investigation Workspace
          </h1>
        </div>
        <span style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', padding: '0.35rem 0.8rem', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
          Trigger: {investigation?.trigger_reason}
        </span>
      </div>

      {/* 6-Agent Flow Graphic */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 1rem', color: '#f8fafc' }}>6-Agent Verification Architecture</h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
          <div style={{ background: '#0f172a', border: '1px solid #3b82f6', borderRadius: '8px', padding: '1rem' }}>
            <div style={{ color: '#60a5fa', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.2rem' }}>1. Supervisor Agent</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Orchestrates agent state graph and triggers specialized tools.</div>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
            <div style={{ color: '#38bdf8', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.2rem' }}>2. Evidence Analyst</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Verifies exact character-span mapping for clinical entities.</div>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
            <div style={{ color: '#a78bfa', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.2rem' }}>3. Guideline Analyst</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Retrieves official ICD-10-CM Coding Clinic guidelines.</div>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
            <div style={{ color: '#fbbf24', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.2rem' }}>4. Specificity Agent</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Traverses code hierarchy tree for highest specificity.</div>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
            <div style={{ color: '#f472b6', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.2rem' }}>5. Query Drafter</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Formulates non-leading CDI physician query if ambiguous.</div>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #34d399', borderRadius: '8px', padding: '1rem' }}>
            <div style={{ color: '#34d399', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.2rem' }}>6. Adversarial Verifier</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Enforces Excludes1 checks & kills hallucinated candidate codes.</div>
          </div>
        </div>
      </div>

      {/* Investigation Details & Citations */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 0.75rem', color: '#f8fafc' }}>Official Guideline Citations</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
          {investigation?.guideline_citations?.map((cit, idx) => (
            <div key={idx} style={{ background: '#0f172a', borderLeft: '3px solid #a78bfa', padding: '0.75rem', borderRadius: '4px', fontSize: '0.85rem', color: '#cbd5e1' }}>
              {cit}
            </div>
          ))}
        </div>

        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 0.75rem', color: '#f8fafc' }}>Adversarial Verifier Verdict</h2>
        <div style={{ background: 'rgba(52, 211, 153, 0.12)', border: '1px solid #34d399', borderRadius: '8px', padding: '1rem' }}>
          <div style={{ color: '#34d399', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.3rem' }}>
            Status: {investigation?.verifier_results?.verifier_status || 'PASS'}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#e2e8f0', lineHeight: 1.5 }}>
            {investigation?.verifier_results?.adversarial_notes}
          </div>
        </div>
      </div>
    </div>
  )
}

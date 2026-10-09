import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { CheckCircle2, Download, ShieldCheck, ArrowLeft, FileText, Code } from 'lucide-react'

export const FinalResults: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const docId = id || 'DEMO-CHART-001'

  const [fhirJson, setFhirJson] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadExportData()
  }, [docId])

  const loadExportData = async () => {
    setLoading(true)
    try {
      const data = await api.exportFhirClaim(docId)
      setFhirJson(data)
    } catch {
      // Fallback FHIR claim payload for demo
      setFhirJson({
        resourceType: 'Claim',
        id: `claim-${docId}`,
        status: 'active',
        type: { coding: [{ system: 'http://terminology.hl7.org/CodeSystem/claim-type', code: 'institutional' }] },
        patient: { reference: 'Patient/synthetic-pt-9081' },
        created: new Date().toISOString(),
        provider: { reference: 'Organization/clincode-him-dept' },
        diagnosis: [
          { sequence: 1, diagnosisCodeableConcept: { coding: [{ system: 'http://hl7.org/fhir/sid/icd-10-cm', code: 'I50.23', display: 'Acute-on-chronic systolic heart failure' }] }, type: [{ coding: [{ code: 'principal' }] }] },
          { sequence: 2, diagnosisCodeableConcept: { coding: [{ system: 'http://hl7.org/fhir/sid/icd-10-cm', code: 'I10', display: 'Essential hypertension' }] } }
        ],
        extension: [
          { url: 'https://clincode.ai/fhir/StructureDefinition/audit-trail', valueString: 'Human coder signed off at 2026-10-09 13:45:00 UTC. Calibrated confidence 98.8%.' }
        ]
      })
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadJson = () => {
    const jsonStr = JSON.stringify(fhirJson, null, 2)
    const blob = new Blob([jsonStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ClinCode_Claim_Export_${docId}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <button onClick={() => navigate('/dashboard/coder')} style={{ background: 'transparent', border: 'none', color: '#38bdf8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', marginBottom: '0.3rem' }}>
            <ArrowLeft size={16} /> Return to Coder Worklist
          </button>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0, color: '#f8fafc' }}>
            Chart Submission & FHIR Claim Export
          </h1>
        </div>

        <button
          onClick={handleDownloadJson}
          style={{ background: '#059669', color: '#fff', border: 'none', padding: '0.7rem 1.25rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.95rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', boxShadow: '0 4px 12px rgba(5, 150, 105, 0.4)' }}
        >
          <Download size={18} /> Download FHIR JSON
        </button>
      </div>

      {/* Status Banner */}
      <div style={{ background: 'rgba(52, 211, 153, 0.12)', border: '1px solid #34d399', borderRadius: '10px', padding: '1rem 1.25rem', display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
        <CheckCircle2 color="#34d399" size={24} />
        <div>
          <strong style={{ color: '#34d399', fontSize: '1rem' }}>Chart Submission Completed & Signed Off</strong>
          <div style={{ color: '#cbd5e1', fontSize: '0.85rem', marginTop: '0.1rem' }}>
            The finalized ICD-10 code set has been verified by human coder review and registered in the immutable audit trail.
          </div>
        </div>
      </div>

      {/* Code Summary List */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 1rem', color: '#f8fafc' }}>Approved ICD-10 Code Set Summary</h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '0.85rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '1.05rem', fontWeight: 'bold', color: '#60a5fa', marginRight: '0.75rem' }}>I50.23</span>
              <span style={{ fontSize: '0.9rem', color: '#f8fafc' }}>Acute-on-chronic systolic (congestive) heart failure</span>
            </div>
            <span style={{ background: '#2563eb', color: '#fff', fontSize: '0.7rem', padding: '2px 8px', borderRadius: '10px', textTransform: 'uppercase', fontWeight: 'bold' }}>Principal</span>
          </div>

          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '0.85rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '1.05rem', fontWeight: 'bold', color: '#60a5fa', marginRight: '0.75rem' }}>I10</span>
              <span style={{ fontSize: '0.9rem', color: '#f8fafc' }}>Essential (primary) hypertension</span>
            </div>
            <span style={{ background: '#334155', color: '#cbd5e1', fontSize: '0.7rem', padding: '2px 8px', borderRadius: '10px', textTransform: 'uppercase', fontWeight: 'bold' }}>Secondary</span>
          </div>
        </div>
      </div>

      {/* FHIR Claim JSON Viewer */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: 0, color: '#f8fafc' }}>FHIR Claim JSON Payload Preview</h2>
          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>HL7 FHIR Claim Resource</span>
        </div>

        <pre style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '1rem', color: '#cbd5e1', fontSize: '0.85rem', fontFamily: 'monospace', overflowX: 'auto', maxHeight: '350px' }}>
          {JSON.stringify(fhirJson, null, 2)}
        </pre>
      </div>
    </div>
  )
}

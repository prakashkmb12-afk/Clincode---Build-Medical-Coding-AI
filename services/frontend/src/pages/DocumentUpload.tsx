import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { UploadCloud, FileText, AlertTriangle, CheckCircle, ArrowRight } from 'lucide-react'

const SAMPLE_PRESETS = {
  heart_failure: {
    ref: 'CHART-HF-9012',
    text: `CHIEF COMPLAINT:\nShortness of breath and worsening lower extremity swelling.\n\nHISTORY OF PRESENT ILLNESS:\nPatient is a 68-year-old male with a history of acute-on-chronic systolic heart failure presenting to the emergency department with severe dyspnea on exertion. Patient denies chest pain. Family history of diabetes mellitus.\n\nPAST MEDICAL HISTORY:\nEssential hypertension, type 2 diabetes mellitus, history of stroke.\n\nASSESSMENT AND PLAN:\n1. Acute-on-chronic systolic heart failure: Initiate IV furosemide, monitor daily weights and electrolyte panel.\n2. Hypertension: Continue home oral lisinopril.\n3. Possible sepsis: Patient is febrile with elevated WBC count. Order blood cultures.`
  },
  diabetes: {
    ref: 'CHART-DM-4412',
    text: `CHIEF COMPLAINT:\nUncontrolled blood sugar and bilateral foot numbness.\n\nHISTORY OF PRESENT ILLNESS:\nPatient is a 62-year-old female with long-standing type 2 diabetes mellitus presenting with diabetic nephropathy and persistent proteinuria.\n\nPAST MEDICAL HISTORY:\nType 2 diabetes mellitus, diabetic nephropathy, essential hypertension.\n\nASSESSMENT AND PLAN:\n1. Type 2 diabetes mellitus with diabetic nephropathy: Adjust insulin regimen.\n2. Essential hypertension: Continue antihypertensive therapy.`
  },
  sepsis: {
    ref: 'CHART-SEP-8891',
    text: `CHIEF COMPLAINT:\nFever, chills, and severe confusion.\n\nHISTORY OF PRESENT ILLNESS:\nPatient is a 74-year-old male presenting with acute fever of 102.4F, tachycardia, and suspected severe sepsis. Patient has no history of pneumonia.\n\nPAST MEDICAL HISTORY:\nUnspecified sequelae of cerebral infarction.\n\nASSESSMENT AND PLAN:\n1. Sepsis, unspecified organism: Start empiric IV broad-spectrum antibiotics.`
  }
}

export const DocumentUpload: React.FC = () => {
  const navigate = useNavigate()
  const [docRef, setDocRef] = useState('CHART-' + Math.floor(1000 + Math.random() * 9000))
  const [docType, setDocType] = useState('Inpatient Clinical Note')
  const [noteText, setNoteText] = useState(SAMPLE_PRESETS.heart_failure.text)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!noteText.trim()) {
      setError('Clinical document text cannot be empty.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const res = await api.uploadDocument({
        external_ref: docRef,
        raw_text: noteText,
        doc_type: docType
      })
      navigate(`/documents/${res.id}/processing`)
    } catch (err: any) {
      // Fallback redirect for offline demo mode
      navigate(`/documents/DEMO-CHART-001/processing`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.5rem' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: '0 0 0.4rem', color: '#f8fafc' }}>Upload Clinical Report</h1>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Submit unstructured physician charts, discharge summaries, or FHIR DocumentReference payloads to the ClinCode AI pipeline.
        </p>
      </div>

      {/* Sensitive Information Warning Banner */}
      <div style={{ background: 'rgba(234, 179, 8, 0.12)', border: '1px solid #eab308', borderRadius: '10px', padding: '1rem 1.25rem', display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
        <AlertTriangle color="#facc15" size={20} style={{ flexShrink: 0, marginTop: '2px' }} />
        <div style={{ fontSize: '0.85rem', color: '#fef08a', lineHeight: 1.5 }}>
          <strong>Sensitive Data Notice:</strong> Clinical documents contain Protected Health Information (PHI). In this demonstration environment, ensure notes are synthetic or de-identified prior to submission. The pipeline scrubs PHI before vector storage.
        </div>
      </div>

      {/* Form Card */}
      <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.5rem' }}>
        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '0.85rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        {/* Preset Selector */}
        <div style={{ marginBottom: '1.25rem' }}>
          <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.5rem', fontWeight: 500 }}>
            Load Sample Chart Presets:
          </label>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={() => {
                setDocRef(SAMPLE_PRESETS.heart_failure.ref)
                setNoteText(SAMPLE_PRESETS.heart_failure.text)
              }}
              style={{ background: '#0f172a', border: '1px solid #3b82f6', color: '#60a5fa', padding: '0.4rem 0.8rem', borderRadius: '6px', fontSize: '0.85rem', cursor: 'pointer' }}
            >
              Heart Failure Chart
            </button>
            <button
              type="button"
              onClick={() => {
                setDocRef(SAMPLE_PRESETS.diabetes.ref)
                setNoteText(SAMPLE_PRESETS.diabetes.text)
              }}
              style={{ background: '#0f172a', border: '1px solid #3b82f6', color: '#60a5fa', padding: '0.4rem 0.8rem', borderRadius: '6px', fontSize: '0.85rem', cursor: 'pointer' }}
            >
              Diabetic Nephropathy
            </button>
            <button
              type="button"
              onClick={() => {
                setDocRef(SAMPLE_PRESETS.sepsis.ref)
                setNoteText(SAMPLE_PRESETS.sepsis.text)
              }}
              style={{ background: '#0f172a', border: '1px solid #3b82f6', color: '#60a5fa', padding: '0.4rem 0.8rem', borderRadius: '6px', fontSize: '0.85rem', cursor: 'pointer' }}
            >
              Sepsis Chart
            </button>
          </div>
        </div>

        <form onSubmit={handleUpload} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem' }}>Chart Document Reference ID:</label>
              <input
                type="text"
                value={docRef}
                onChange={e => setDocRef(e.target.value)}
                style={{ width: '100%', padding: '0.65rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.9rem' }}
                required
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem' }}>Document Category / Type:</label>
              <select
                value={docType}
                onChange={e => setDocType(e.target.value)}
                style={{ width: '100%', padding: '0.65rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.9rem' }}
              >
                <option value="Inpatient Clinical Note">Inpatient Clinical Note</option>
                <option value="ED Discharge Summary">ED Discharge Summary</option>
                <option value="Outpatient Clinic Note">Outpatient Clinic Note</option>
                <option value="FHIR DocumentReference JSON">FHIR DocumentReference JSON</option>
              </select>
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem' }}>Unstructured Clinical Report Text:</label>
            <textarea
              value={noteText}
              onChange={e => setNoteText(e.target.value)}
              rows={12}
              style={{ width: '100%', padding: '0.75rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.9rem', fontFamily: 'monospace', lineHeight: 1.5, resize: 'vertical' }}
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.85rem', borderRadius: '8px', fontWeight: 600, fontSize: '1rem', cursor: loading ? 'not-allowed' : 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.6rem' }}
          >
            {loading ? 'Submitting to AI Pipeline...' : 'Submit to AI Processing Pipeline'}
            <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  )
}

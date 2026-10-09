import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, CheckCircle, ShieldAlert, BookOpen, Brain, Scale } from 'lucide-react'

export const AboutUs: React.FC = () => {
  return (
    <div style={{ background: '#0f172a', color: '#f8fafc', minHeight: '100vh', fontFamily: 'Inter, sans-serif' }}>
      {/* Top Header */}
      <header style={{ borderBottom: '1px solid #1e293b', background: '#1e293b', padding: '1rem 1.5rem' }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link to="/" style={{ color: '#38bdf8', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.9rem', fontWeight: 500 }}>
            <ArrowLeft size={16} /> Back to Home
          </Link>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>About ClinCode</div>
        </div>
      </header>

      <main style={{ maxWidth: '900px', margin: '0 auto', padding: '3rem 1.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '1rem', color: '#f8fafc' }}>
            Clinical Documentation Intelligence & Medical Coding Automation
          </h1>
          <p style={{ fontSize: '1.1rem', color: '#94a3b8', maxWidth: '700px', margin: '0 auto', lineHeight: 1.6 }}>
            ClinCode is a research-backed, evidence-linked medical coding assistance platform designed to improve coding speed, accuracy, and auditability while keeping human experts at the center.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
          {/* Section 1 */}
          <section style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <BookOpen color="#60a5fa" size={24} />
              <h2 style={{ fontSize: '1.35rem', fontWeight: 700, margin: 0 }}>The Medical Coding Challenge</h2>
            </div>
            <p style={{ color: '#cbd5e1', lineHeight: 1.7, fontSize: '0.95rem' }}>
              Hospital HIM departments face severe backlogs, high claim denial rates, and complex ICD-10-CM coding manuals spanning over 70,000 codes. Manual coding requires reading unstructured physician charts, identifying valid diagnoses, checking Excludes1 guidelines, and translating them into billable claim codes.
            </p>
          </section>

          {/* Section 2 */}
          <section style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <Brain color="#a78bfa" size={24} />
              <h2 style={{ fontSize: '1.35rem', fontWeight: 700, margin: 0 }}>Assertion-Aware NLP & Evidence Grounding</h2>
            </div>
            <p style={{ color: '#cbd5e1', lineHeight: 1.7, fontSize: '0.95rem', marginBottom: '1rem' }}>
              Traditional keyword matchers frequently misinterpret context—assigning codes for conditions that were explicitly ruled out or mentioned only as family history.
            </p>
            <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155', color: '#94a3b8', fontSize: '0.9rem' }}>
              <strong style={{ color: '#38bdf8' }}>ClinCode Solution:</strong> Bio_ClinicalBERT classifies assertion status (<span style={{ color: '#fca5a5' }}>Negated</span>, <span style={{ color: '#fde047' }}>Possible</span>, <span style={{ color: '#93c5fd' }}>Family History</span>, <span style={{ color: '#86efac' }}>Present</span>). Only verified active conditions advance to code retrieval.
            </div>
          </section>

          {/* Section 3 */}
          <section style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <Scale color="#34d399" size={24} />
              <h2 style={{ fontSize: '1.35rem', fontWeight: 700, margin: 0 }}>Retrieval & Verification vs Unrestricted LLMs</h2>
            </div>
            <p style={{ color: '#cbd5e1', lineHeight: 1.7, fontSize: '0.95rem' }}>
              Unrestricted LLMs can hallucinate non-existent ICD-10 codes or generate invalid billing combinations. ClinCode uses dense vector retrieval (Qdrant), RRF fusion, ONNX Cross-Encoders, and a 6-agent LangGraph verifier to guarantee every suggested code corresponds to an authentic candidate and exact text span.
            </p>
          </section>

          {/* Section 4 */}
          <section style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <ShieldAlert color="#fbbf24" size={24} />
              <h2 style={{ fontSize: '1.35rem', fontWeight: 700, margin: 0 }}>Project Scope & Limitations</h2>
            </div>
            <ul style={{ color: '#cbd5e1', lineHeight: 1.8, fontSize: '0.95rem', paddingLeft: '1.25rem' }}>
              <li>ClinCode is designed as a Human-in-the-Loop decision support tool, not an autonomous medical decision maker.</li>
              <li>Final chart submissions must be reviewed and signed off by a certified medical coder or HIM specialist.</li>
              <li>Demonstrations use de-identified synthetic clinical charts in compliance with HIPAA privacy standards.</li>
            </ul>
          </section>
        </div>
      </main>
    </div>
  )
}

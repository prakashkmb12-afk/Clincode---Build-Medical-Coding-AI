import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  Shield,
  Zap,
  CheckCircle,
  Brain,
  FileCheck,
  Lock,
  ArrowRight,
  Database,
  Activity,
  GitBranch
} from 'lucide-react'

export const Home: React.FC = () => {
  const { user, signInWithGoogle, demoLogin } = useAuth()
  const navigate = useNavigate()

  const handleGetStarted = () => {
    if (user) {
      navigate(`/dashboard/${user.role}`)
    } else {
      navigate('/login')
    }
  }

  return (
    <div style={{ background: '#0f172a', color: '#f8fafc', minHeight: '100vh', display: 'flex', flexDirection: 'column', fontFamily: 'Inter, sans-serif' }}>
      {/* Header Navigation */}
      <header style={{ borderBottom: '1px solid #1e293b', background: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(8px)', sticky: 'top', position: 'sticky', top: 0, zIndex: 100 }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '1rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ background: 'linear-gradient(135deg, #2563eb, #3b82f6)', padding: '0.5rem 0.75rem', borderRadius: '8px', fontWeight: 'bold', color: '#fff', fontSize: '1.1rem' }}>
              CC
            </div>
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '1.25rem', letterSpacing: '-0.5px' }}>ClinCode</div>
              <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Clinical Documentation Intelligence</div>
            </div>
          </div>

          <nav style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
            <a href="#how-it-works" style={{ color: '#cbd5e1', textDecoration: 'none', fontSize: '0.95rem' }}>How It Works</a>
            <a href="#capabilities" style={{ color: '#cbd5e1', textDecoration: 'none', fontSize: '0.95rem' }}>Capabilities</a>
            <a href="#security" style={{ color: '#cbd5e1', textDecoration: 'none', fontSize: '0.95rem' }}>Security</a>
            <Link to="/about" style={{ color: '#cbd5e1', textDecoration: 'none', fontSize: '0.95rem' }}>About Us</Link>
            <Link to="/contact" style={{ color: '#cbd5e1', textDecoration: 'none', fontSize: '0.95rem' }}>Contact</Link>
          </nav>

          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            {user ? (
              <button
                onClick={() => navigate(`/dashboard/${user.role}`)}
                style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.6rem 1.25rem', borderRadius: '6px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              >
                Go to Dashboard ({user.role.toUpperCase()})
                <ArrowRight size={16} />
              </button>
            ) : (
              <>
                <Link to="/login" style={{ color: '#cbd5e1', textDecoration: 'none', fontSize: '0.95rem', padding: '0.5rem 1rem' }}>
                  Sign In
                </Link>
                <button
                  onClick={handleGetStarted}
                  style={{ background: 'linear-gradient(135deg, #2563eb, #1d4ed8)', color: '#fff', border: 'none', padding: '0.65rem 1.35rem', borderRadius: '6px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', boxShadow: '0 4px 12px rgba(37, 99, 235, 0.3)' }}
                >
                  Get Started with ClinCode
                  <ArrowRight size={16} />
                </button>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section style={{ padding: '5rem 1.5rem 4rem', textAlign: 'center', maxWidth: '1100px', margin: '0 auto' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(37, 99, 235, 0.15)', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '0.4rem 1rem', borderRadius: '20px', color: '#60a5fa', fontSize: '0.85rem', fontWeight: 600, marginBottom: '1.5rem' }}>
          <Zap size={15} /> Evidence-Linked Medical Coding Automation
        </div>
        <h1 style={{ fontSize: '3.25rem', fontWeight: 800, lineHeight: 1.15, marginBottom: '1.5rem', background: 'linear-gradient(to right, #ffffff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Precision Medical Coding with Human-in-the-Loop Review
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#94a3b8', maxWidth: '800px', margin: '0 auto 2.5rem', lineHeight: 1.6 }}>
          ClinCode combines Bio_ClinicalBERT assertion classification, Reciprocal Rank Fusion, Cross-Encoder reranking, and LangGraph multi-agent verification to suggest verifiable ICD-10 codes directly grounded in clinical evidence.
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button
            onClick={handleGetStarted}
            style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.9rem 2rem', borderRadius: '8px', fontSize: '1.05rem', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem', boxShadow: '0 10px 25px -5px rgba(37, 99, 235, 0.4)' }}
          >
            Get Started with ClinCode
            <ArrowRight size={18} />
          </button>
          <button
            onClick={() => demoLogin('coder')}
            style={{ background: '#1e293b', color: '#e2e8f0', border: '1px solid #334155', padding: '0.9rem 2rem', borderRadius: '8px', fontSize: '1.05rem', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
          >
            Try Interactive Coder Demo
          </button>
        </div>
      </section>

      {/* Stats Banner */}
      <section style={{ borderTop: '1px solid #1e293b', borderBottom: '1px solid #1e293b', background: '#162032', padding: '2.5rem 1.5rem' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '2rem', textAlign: 'center' }}>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#34d399' }}>98.8%</div>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.3rem' }}>Auto-Accept Precision</div>
          </div>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#60a5fa' }}>88.5%</div>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.3rem' }}>Top-5 Retrieval Recall</div>
          </div>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#fbbf24' }}>5.2 min</div>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.3rem' }}>Avg Review Latency</div>
          </div>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#a78bfa' }}>6 Agents</div>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.3rem' }}>LangGraph Verifier</div>
          </div>
        </div>
      </section>

      {/* How ClinCode Works */}
      <section id="how-it-works" style={{ padding: '5rem 1.5rem', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <h2 style={{ fontSize: '2.25rem', fontWeight: 700, marginBottom: '0.75rem' }}>How ClinCode Works</h2>
          <p style={{ color: '#94a3b8', fontSize: '1.05rem', maxWidth: '650px', margin: '0 auto' }}>
            A rigorous 13-stage AI processing pipeline designed for verifiable medical coding auditability.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.75rem' }}>
            <div style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', width: '44px', height: '44px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}>
              <FileCheck size={22} />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>1. Document Intake & De-ID</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Ingests clinical notes, PDFs, or FHIR JSON. Scrubs PHI entities with encrypted key vaults before downstream NLP processing.
            </p>
          </div>

          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.75rem' }}>
            <div style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', width: '44px', height: '44px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}>
              <Brain size={22} />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>2. Assertion & RRF Fusion</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Bio_ClinicalBERT classifies assertion status (Present, Negated, Possible, Historical) to filter out non-active conditions.
            </p>
          </div>

          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.75rem' }}>
            <div style={{ background: 'rgba(34, 197, 94, 0.15)', color: '#4ade80', width: '44px', height: '44px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}>
              <GitBranch size={22} />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>3. LangGraph Verification</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Complex cases trigger 6 specialized agents (Evidence, Guideline, Specificity, Verifier) to check Excludes1 rules & citations.
            </p>
          </div>

          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '1.75rem' }}>
            <div style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', width: '44px', height: '44px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}>
              <CheckCircle size={22} />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem' }}>4. Human-in-the-Loop Review</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Medical coders review interactive split-screen evidence maps, accepting, modifying, or rejecting recommendations before submission.
            </p>
          </div>
        </div>
      </section>

      {/* Security Principles */}
      <section id="security" style={{ background: '#162032', padding: '4rem 1.5rem', borderTop: '1px solid #1e293b' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>Security & Governance Principles</h2>
            <p style={{ color: '#94a3b8' }}>Built with zero-trust healthcare data security standards.</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <Lock color="#38bdf8" size={24} style={{ flexShrink: 0, marginTop: '3px' }} />
              <div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.3rem' }}>Firebase Auth & RBAC</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5 }}>
                  Server-side authorization enforced on every FastAPI endpoint. Roles (Coder, CDI, Manager, Admin) are verified strictly on the backend.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
              <Shield color="#38bdf8" size={24} style={{ flexShrink: 0, marginTop: '3px' }} />
              <div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.3rem' }}>De-Identification Engine</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5 }}>
                  PHI scrubbers detect names, dates, and locations before vector store embeddings or LLM verifier prompts.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
              <Database color="#38bdf8" size={24} style={{ flexShrink: 0, marginTop: '3px' }} />
              <div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.3rem' }}>Immutable Audit Trail</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5 }}>
                  Every coder action, score adjustment, query resolution, and claim export is recorded with timestamps for complete compliance.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ marginTop: 'auto', borderTop: '1px solid #1e293b', background: '#0b1329', padding: '3rem 1.5rem 2rem' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem' }}>
          <div>
            <div style={{ fontWeight: 'bold', fontSize: '1.1rem', color: '#f8fafc' }}>ClinCode SaaS</div>
            <div style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '0.2rem' }}>
              Clinical Documentation Intelligence & Medical Coding Automation System
            </div>
          </div>

          <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.9rem' }}>
            <Link to="/about" style={{ color: '#94a3b8', textDecoration: 'none' }}>About Project</Link>
            <Link to="/contact" style={{ color: '#94a3b8', textDecoration: 'none' }}>Contact Team</Link>
            <Link to="/login" style={{ color: '#94a3b8', textDecoration: 'none' }}>Sign In</Link>
          </div>
        </div>
        <div style={{ textAlign: 'center', borderTop: '1px solid #1e293b', marginTop: '2rem', paddingTop: '1.5rem', fontSize: '0.75rem', color: '#64748b' }}>
          ClinCode is a research & clinical documentation assistance platform. Final coding submissions require verification by a certified medical coder.
        </div>
      </footer>
    </div>
  )
}

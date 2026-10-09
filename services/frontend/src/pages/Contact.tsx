import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Send, CheckCircle2, AlertCircle } from 'lucide-react'
import { api } from '../api/client'

export const Contact: React.FC = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [subject, setSubject] = useState('')
  const [message, setMessage] = useState('')

  const [loading, setLoading] = useState(false)
  const [successMsg, setSuccessMsg] = useState<string | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSuccessMsg(null)
    setErrorMsg(null)

    if (name.trim().length < 2) {
      setErrorMsg('Please enter your full name (at least 2 characters).')
      return
    }
    if (!email.includes('@') || !email.includes('.')) {
      setErrorMsg('Please enter a valid email address.')
      return
    }
    if (message.trim().length < 10) {
      setErrorMsg('Message must be at least 10 characters long.')
      return
    }

    setLoading(true)
    try {
      const res = await api.submitContact({
        name,
        email,
        subject: subject || 'ClinCode General Inquiry',
        message
      })
      setSuccessMsg(res.message)
      setName('')
      setEmail('')
      setSubject('')
      setMessage('')
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to submit contact message. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ background: '#0f172a', color: '#f8fafc', minHeight: '100vh', fontFamily: 'Inter, sans-serif' }}>
      <header style={{ borderBottom: '1px solid #1e293b', background: '#1e293b', padding: '1rem 1.5rem' }}>
        <div style={{ maxWidth: '800px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link to="/" style={{ color: '#38bdf8', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.9rem' }}>
            <ArrowLeft size={16} /> Back to Home
          </Link>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>Contact ClinCode Team</div>
        </div>
      </header>

      <main style={{ maxWidth: '650px', margin: '3rem auto', padding: '0 1.5rem' }}>
        <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '12px', padding: '2rem', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3)' }}>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: '0.5rem' }}>Get in Touch</h1>
          <p style={{ color: '#94a3b8', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
            Have questions regarding ClinCode AI pipeline, deployment, or technical specifications? Drop us a message below.
          </p>

          {successMsg && (
            <div style={{ background: 'rgba(34, 197, 94, 0.15)', border: '1px solid #22c55e', color: '#4ade80', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <CheckCircle2 size={20} />
              <div style={{ fontSize: '0.9rem' }}>{successMsg}</div>
            </div>
          )}

          {errorMsg && (
            <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <AlertCircle size={20} />
              <div style={{ fontSize: '0.9rem' }}>{errorMsg}</div>
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem', fontWeight: 500 }}>Full Name *</label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Dr. Alex Vance"
                style={{ width: '100%', padding: '0.75rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.95rem' }}
                required
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem', fontWeight: 500 }}>Email Address *</label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="alex.vance@hospital.org"
                style={{ width: '100%', padding: '0.75rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.95rem' }}
                required
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem', fontWeight: 500 }}>Subject</label>
              <input
                type="text"
                value={subject}
                onChange={e => setSubject(e.target.value)}
                placeholder="ClinCode API Integration & Qdrant Setup"
                style={{ width: '100%', padding: '0.75rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.95rem' }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.4rem', fontWeight: 500 }}>Message *</label>
              <textarea
                value={message}
                onChange={e => setMessage(e.target.value)}
                rows={5}
                placeholder="Enter details about your inquiry or technical question..."
                style={{ width: '100%', padding: '0.75rem', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', color: '#f8fafc', fontSize: '0.95rem', resize: 'vertical' }}
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '0.85rem', borderRadius: '8px', fontWeight: 600, fontSize: '1rem', cursor: loading ? 'not-allowed' : 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', marginTop: '0.5rem' }}
            >
              {loading ? 'Submitting Message...' : 'Send Message'}
              <Send size={18} />
            </button>
          </form>
        </div>
      </main>
    </div>
  )
}

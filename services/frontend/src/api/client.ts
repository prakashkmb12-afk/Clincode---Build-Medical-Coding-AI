const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'

let authToken: string | null = null

export const setAuthToken = (token: string | null) => {
  authToken = token
}

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>)
  }

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers
  })

  if (!response.ok) {
    let errorDetail = `API Error: ${response.status} ${response.statusText}`
    try {
      const errorJson = await response.json()
      if (errorJson.detail) {
        errorDetail = typeof errorJson.detail === 'string' ? errorJson.detail : JSON.stringify(errorJson.detail)
      }
    } catch {
      // JSON parse error ignored
    }
    throw new Error(errorDetail)
  }

  return response.json()
}

export interface DocumentResponse {
  id: string
  external_ref: string
  doc_type: string
  status: string
  raw_text?: string
  created_at: string
}

export interface SuggestionResponse {
  id: string
  document_id: string
  icd10_code: string
  description: string
  calibrated_conf: number
  band: 'auto' | 'review' | 'low'
  justification_md?: string
  evidence_spans?: Array<{ start: number; end: number; text: string }>
  excludes1_warning?: string
  status: string
}

export interface ActionRequest {
  suggestion_id: string
  action: 'accept' | 'reject' | 'modify'
  modified_code?: string
  reason?: string
}

export interface QueryResponse {
  id: string
  document_id: string
  title: string
  status: string
  evidence_text: string
  draft_query: string
  created_at: string
}

export interface InvestigationResponse {
  id: string
  document_id: string
  trigger_reason: string
  status: string
  evidence_summary?: string
  guideline_citations?: string[]
  verifier_results?: any
  final_suggestions?: any[]
  created_at: string
}

export interface AdminMetricsResponse {
  total_charts: number
  auto_accepted: number
  human_reviewed: number
  overall_precision: number
  top5_recall: number
  avg_latency_ms: number
  active_model_version: string
}

export interface ContactFormInput {
  name: string
  email: string
  subject: str
  message: string
}

export const api = {
  // Auth & Sync
  firebaseLogin: (idToken: string, requestedRole?: string) =>
    apiRequest<{ id: string; username: string; email: string; role: string }>(`/auth/firebase-login`, {
      method: 'POST',
      body: JSON.stringify({ id_token: idToken, requested_role: requestedRole })
    }),

  getMe: () => apiRequest<{ id: string; username: string; email: string; role: string }>(`/auth/me`),

  // Documents
  uploadDocument: (data: { external_ref: string; raw_text: string; doc_type?: string }) =>
    apiRequest<DocumentResponse>(`/documents`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  getDocument: (id: string) => apiRequest<DocumentResponse>(`/documents/${id}`),

  listDocuments: (limit: number = 20) => apiRequest<DocumentResponse[]>(`/documents?limit=${limit}`),

  // Suggestions & Review
  getSuggestions: (docId: string) => apiRequest<SuggestionResponse[]>(`/documents/${docId}/suggestions`),

  submitAction: (actionReq: ActionRequest) =>
    apiRequest<{ status: string; id: string }>(`/suggestions/action`, {
      method: 'POST',
      body: JSON.stringify(actionReq)
    }),

  submitFinalReview: (docId: string, notes?: string) =>
    apiRequest<{ status: string; document_id: string }>(`/documents/${docId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ notes })
    }),

  // CDI Queries
  getQueries: (docId?: string) =>
    apiRequest<QueryResponse[]>(docId ? `/documents/${docId}/queries` : `/queries`),

  createDirectQuery: (docId: string, title: string, evidenceText: string, draftQuery: string) =>
    apiRequest<QueryResponse>(`/documents/${docId}/queries`, {
      method: 'POST',
      body: JSON.stringify({ title, evidence_text: evidenceText, draft_query: draftQuery })
    }),

  // LangGraph Investigation
  triggerInvestigation: (docId: string, triggerReason: string) =>
    apiRequest<InvestigationResponse>(`/documents/${docId}/investigate`, {
      method: 'POST',
      body: JSON.stringify({ trigger_reason: triggerReason })
    }),

  getInvestigation: (runId: string) => apiRequest<InvestigationResponse>(`/investigations/${runId}`),

  // Export
  exportFhirClaim: (docId: string) => apiRequest<any>(`/documents/${docId}/export`),

  // Admin & Metrics
  getAdminMetrics: () => apiRequest<AdminMetricsResponse>(`/admin/metrics`),

  getAdminModels: () => apiRequest<any[]>(`/admin/models`),

  // Contact
  submitContact: (form: ContactFormInput) =>
    apiRequest<{ status: string; message: string; timestamp: string }>(`/contact`, {
      method: 'POST',
      body: JSON.stringify(form)
    })
}

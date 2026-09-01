import type { AnalyzeResponse } from '../types'

// Connected to Render backend
const API_BASE_URL = 'https://trustcheck-p6fz.onrender.com'

// Transform backend response format to app format
const transformBackendResponse = (data: any): AnalyzeResponse => {
  // Convert signal objects to readable strings
  const signals = Array.isArray(data.signals)
    ? data.signals.map((signal: any) => {
        if (typeof signal === 'string') return signal
        // Format: "SIGNAL_TYPE (Score: 30)" or just the type if no score
        const type = signal.type || 'Unknown signal'
        const score = signal.score ? ` (Score: ${signal.score})` : ''
        return type + score
      })
    : []

  return {
    risk_level: data.risk_level || 'UNKNOWN',
    risk_score: typeof data.risk_score === 'number' ? data.risk_score : 0,
    explanation: Array.isArray(data.explanation) 
      ? data.explanation.map((item: any) => typeof item === 'string' ? item : JSON.stringify(item))
      : [],
    signals: signals,
    urls: Array.isArray(data.urls) 
      ? data.urls.filter((u: any) => u && typeof u === 'string')
      : [],
    brands: Array.isArray(data.brands) 
      ? data.brands.filter((b: any) => b && typeof b === 'string')
      : [],
    safe_action: data.safe_action || 'Pause before interacting and verify the sender through a trusted channel.',
  }
}

export const realAnalyzeService = async (message: string): Promise<AnalyzeResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(`Analysis failed (${response.status})`)
  }

  const data = await response.json()
  return transformBackendResponse(data)
}

import type { AnalyzeResponse } from '../types'

// TODO: replace this placeholder with the deployed backend base URL.
const API_BASE_URL = 'TODO_BACKEND_BASE_URL'

export const realAnalyzeService = async (message: string): Promise<AnalyzeResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(`Analysis failed (${response.status})`)
  }

  return response.json() as Promise<AnalyzeResponse>
}

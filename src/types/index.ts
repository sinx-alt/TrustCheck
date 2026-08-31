export type RiskLevel = 'LOW' | 'SUSPICIOUS' | 'HIGH' | 'UNKNOWN'

export interface AnalyzeRequest {
  message: string
}

export interface AnalyzeResponse {
  risk_score?: number
  risk_level?: RiskLevel
  signals?: string[]
  urls?: string[]
  brands?: string[]
  explanation?: string[]
  safe_action?: string
}

export interface Exchange {
  id: string
  message: string
  response?: AnalyzeResponse
  error?: string
  createdAt: number
}

export type AnalyzeService = (message: string) => Promise<AnalyzeResponse>

import { realAnalyzeService } from './realAnalyzeService'
import type { AnalyzeService } from '../types'

// Connected to Render backend
export const analyzeService: AnalyzeService = realAnalyzeService

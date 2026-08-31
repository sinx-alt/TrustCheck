import { useCallback, useState } from 'react'
import { analyzeService } from '../api'
import type { AnalyzeResponse } from '../types'

export const useAnalyze = () => {
  const [isLoading, setIsLoading] = useState(false)

  const analyze = useCallback(async (message: string): Promise<AnalyzeResponse> => {
    setIsLoading(true)
    try {
      return await analyzeService(message)
    } finally {
      setIsLoading(false)
    }
  }, [])

  return { analyze, isLoading }
}

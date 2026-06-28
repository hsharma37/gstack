import { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

export function useAnalytics() {
  const [expectancy, setExpectancy] = useState<any>(null)
  const [heatmap, setHeatmap] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      try {
        const [exp, hm] = await Promise.all([
          apiClient.get('/analytics/expectancy'),
          apiClient.get('/analytics/heatmap'),
        ])
        setExpectancy(exp)
        setHeatmap(hm)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return { expectancy, heatmap, loading, error }
}

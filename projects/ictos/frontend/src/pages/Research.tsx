import { useState } from 'react'
import { apiClient } from '../api/client'

export function ResearchPage() {
  const [response, setResponse] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'backtest' | 'montecarlo' | 'backtrader'>('backtest')

  const runBacktest = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiClient.post('/research/backtest', {
        strategy: 'sma-crossover',
        symbol: 'EURUSD',
        timeframe: '1h',
        start: '2024-01-01',
        end: '2024-06-01',
        params: { fast: 10, slow: 30 },
      })
      setResponse(JSON.stringify(result, null, 2))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed')
    } finally {
      setIsLoading(false)
    }
  }

  const runMonteCarlo = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiClient.post('/research/montecarlo', {
        trials: 1000,
        scenario: {
          win_rate: 0.55,
          avg_win: 150,
          avg_loss: 100,
          num_trades: 100,
          initial_capital: 10000,
        },
      })
      setResponse(JSON.stringify(result, null, 2))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed')
    } finally {
      setIsLoading(false)
    }
  }

  const runBacktrader = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const result = await apiClient.post('/research/backtrader', {
        strategy: 'sma-crossover',
        symbol: 'EURUSD',
        timeframe: '1h',
        start: '2024-01-01',
        end: '2024-06-01',
        params: { fast: 10, slow: 30 },
      })
      setResponse(JSON.stringify(result, null, 2))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed')
    } finally {
      setIsLoading(false)
    }
  }

  const tabs = [
    { key: 'backtest' as const, label: 'VectorBT Backtest', action: runBacktest },
    { key: 'montecarlo' as const, label: 'Monte Carlo', action: runMonteCarlo },
    { key: 'backtrader' as const, label: 'Backtrader', action: runBacktrader },
  ]

  const btnStyle = (isActive: boolean): React.CSSProperties => ({
    padding: '10px 16px',
    borderRadius: 8,
    cursor: isLoading ? 'not-allowed' : 'pointer',
    background: isActive ? '#111' : '#fff',
    color: isActive ? '#fff' : '#111',
    border: '1px solid #ccc',
  })

  return (
    <section>
      <h2>Research</h2>
      <div style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => {
              setActiveTab(t.key)
              t.action()
            }}
            disabled={isLoading}
            style={btnStyle(activeTab === t.key)}
          >
            {isLoading && activeTab === t.key ? 'Running…' : t.label}
          </button>
        ))}
      </div>
      {error && <div style={{ color: 'red', marginBottom: 16 }}>{error}</div>}
      {response && (
        <pre
          style={{
            background: '#f6f8fa',
            padding: 16,
            borderRadius: 12,
            overflowX: 'auto',
            fontSize: 12,
          }}
        >
          {response}
        </pre>
      )}
    </section>
  )
}

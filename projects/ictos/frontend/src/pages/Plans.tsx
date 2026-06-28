import { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

export function PlansPage() {
  const [plans, setPlans] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiClient
      .get('/plans/')
      .then((data: any) => {
        setPlans(data || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const cardStyle: React.CSSProperties = {
    padding: 16,
    border: '1px solid #ccc',
    borderRadius: 12,
    background: '#fff',
  }

  return (
    <section>
      <h2>Trading Plans</h2>
      {loading ? (
        <p>Loading...</p>
      ) : plans.length === 0 ? (
        <p>No trading plans yet.</p>
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          {plans.map((plan: any) => (
            <div key={plan.id} style={cardStyle}>
              <p><strong>Date:</strong> {plan.date}</p>
              <p><strong>Pair:</strong> {plan.pair}</p>
              <p><strong>Session:</strong> {plan.session}</p>
              <p><strong>Bias:</strong> {plan.bias}</p>
              <p><strong>Risk/Trade:</strong> {(plan.risk_per_trade * 100).toFixed(1)}%</p>
              <p><strong>Max Trades:</strong> {plan.max_trades}</p>
              <p><strong>Notes:</strong> {plan.notes}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

import { useAnalytics } from '../hooks/useAnalytics'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

export function AnalyticsPage() {
  const { expectancy, heatmap, loading, error } = useAnalytics()

  const heatmapData = heatmap?.sessions
    ? Object.entries(heatmap.sessions).map(([name, data]: [string, any]) => ({
        name,
        count: data.count,
        winRate: Number((data.win_rate * 100).toFixed(1)),
        pnl: Number(data.pnl.toFixed(2)),
      }))
    : []

  const cardStyle: React.CSSProperties = {
    padding: 16,
    border: '1px solid #ccc',
    borderRadius: 12,
    background: '#fff',
    marginBottom: 24,
  }

  return (
    <section>
      <h2>Analytics</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? (
        <p>Loading analytics...</p>
      ) : (
        <div style={{ display: 'grid', gap: 24 }}>
          <div style={cardStyle}>
            <h3>Expectancy</h3>
            <ul>
              <li>Trades: {expectancy?.trades}</li>
              <li>Win rate: {((expectancy?.win_rate ?? 0) * 100).toFixed(1)}%</li>
              <li>Avg win: {expectancy?.avg_win?.toFixed(2)}</li>
              <li>Avg loss: {expectancy?.avg_loss?.toFixed(2)}</li>
              <li>Expectancy: {expectancy?.expectancy?.toFixed(2)}</li>
              <li>R-Factor: {expectancy?.r_factor?.toFixed(2)}</li>
            </ul>
          </div>
          <div style={cardStyle}>
            <h3>Session Heatmap</h3>
            {heatmapData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={heatmapData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#111" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p>No session data</p>
            )}
          </div>
        </div>
      )}
    </section>
  )
}

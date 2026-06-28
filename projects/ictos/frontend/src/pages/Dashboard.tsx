import { useAnalytics } from '../hooks/useAnalytics'

export function DashboardPage() {
  const { expectancy, loading, error } = useAnalytics()

  const cardStyle: React.CSSProperties = {
    padding: 16,
    border: '1px solid #ccc',
    borderRadius: 12,
    background: '#fff',
  }

  const valueStyle: React.CSSProperties = {
    fontSize: 32,
    fontWeight: 'bold',
    margin: '8px 0 0',
  }

  return (
    <section>
      <h2>Dashboard</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div
          style={{
            display: 'grid',
            gap: 16,
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          }}
        >
          <div style={cardStyle}>
            <h3 style={{ margin: 0, fontSize: 14, color: '#666' }}>Trades</h3>
            <p style={valueStyle}>{expectancy?.trades ?? 0}</p>
          </div>
          <div style={cardStyle}>
            <h3 style={{ margin: 0, fontSize: 14, color: '#666' }}>Win Rate</h3>
            <p style={valueStyle}>{((expectancy?.win_rate ?? 0) * 100).toFixed(1)}%</p>
          </div>
          <div style={cardStyle}>
            <h3 style={{ margin: 0, fontSize: 14, color: '#666' }}>Expectancy</h3>
            <p style={valueStyle}>{(expectancy?.expectancy ?? 0).toFixed(2)}</p>
          </div>
          <div style={cardStyle}>
            <h3 style={{ margin: 0, fontSize: 14, color: '#666' }}>R-Factor</h3>
            <p style={valueStyle}>{(expectancy?.r_factor ?? 0).toFixed(2)}</p>
          </div>
        </div>
      )}
    </section>
  )
}

import { Routes, Route, Link } from 'react-router-dom'
import { DashboardPage } from './pages/Dashboard'
import { AnalyticsPage } from './pages/Analytics'
import { ResearchPage } from './pages/Research'
import { JournalPage } from './pages/Journal'
import { PlansPage } from './pages/Plans'

const navStyle: React.CSSProperties = {
  padding: '10px 16px',
  borderRadius: 8,
  border: '1px solid #ccc',
  background: '#fff',
  color: '#111',
  textDecoration: 'none',
  cursor: 'pointer',
}

function App() {
  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <header style={{ marginBottom: 24 }}>
        <h1>ICTOS Phase 3</h1>
        <p>Analytics + Research Engine</p>
      </header>
      <nav style={{ display: 'flex', gap: 12, marginBottom: 24, flexWrap: 'wrap' }}>
        <Link to="/" style={navStyle}>Dashboard</Link>
        <Link to="/analytics" style={navStyle}>Analytics</Link>
        <Link to="/research" style={navStyle}>Research</Link>
        <Link to="/journal" style={navStyle}>Journal</Link>
        <Link to="/plans" style={navStyle}>Plans</Link>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/journal" element={<JournalPage />} />
          <Route path="/plans" element={<PlansPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

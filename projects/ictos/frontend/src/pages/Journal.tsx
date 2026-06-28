import { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

export function JournalPage() {
  const [entries, setEntries] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiClient
      .get('/journal/')
      .then((data: any) => {
        setEntries(data || [])
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
      <h2>Journal</h2>
      {loading ? (
        <p>Loading...</p>
      ) : entries.length === 0 ? (
        <p>No journal entries yet.</p>
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          {entries.map((entry: any) => (
            <div key={entry.id} style={cardStyle}>
              <p><strong>Date:</strong> {entry.date}</p>
              <p><strong>Setup Quality:</strong> {entry.setup_quality}/10</p>
              <p><strong>Execution Quality:</strong> {entry.execution_quality}/10</p>
              <p><strong>Notes:</strong> {entry.notes}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

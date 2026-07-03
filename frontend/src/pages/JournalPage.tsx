import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../api/client'

export default function JournalPage() {
  const queryClient = useQueryClient()
  const { data: entries } = useQuery({ queryKey: ['tasting-entries'], queryFn: api.listTastingEntries })
  const { data: beans } = useQuery({ queryKey: ['beans'], queryFn: api.listBeans })

  const [beanId, setBeanId] = useState('')
  const [rating, setRating] = useState(4)
  const [notes, setNotes] = useState('')

  const createEntry = useMutation({
    mutationFn: () => api.createTastingEntry({ bean_id: beanId, rating, notes_raw: notes }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasting-entries'] })
      setNotes('')
    },
  })

  const beanName = (id: string) => beans?.find((b) => b.id === id)?.name ?? 'Unknown bean'

  return (
    <div>
      <div className="eyebrow">Your palate</div>
      <h1>Cupping journal</h1>
      <p>Log what you're drinking. Loose notes get parsed into flavor tags automatically.</p>

      <div className="card" style={{ marginTop: 24, maxWidth: 480 }}>
        <h2>New entry</h2>
        <div className="form-field">
          <label htmlFor="bean">Bean</label>
          <select id="bean" value={beanId} onChange={(e) => setBeanId(e.target.value)}>
            <option value="">Select a bean…</option>
            {beans?.map((bean) => (
              <option key={bean.id} value={bean.id}>
                {bean.name}
              </option>
            ))}
          </select>
        </div>
        <div className="form-field">
          <label htmlFor="rating">Rating (1-5)</label>
          <input
            id="rating"
            type="number"
            min={1}
            max={5}
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
          />
        </div>
        <div className="form-field">
          <label htmlFor="notes">Notes</label>
          <textarea
            id="notes"
            rows={3}
            placeholder="tasted kinda like a fruit punch, low acid, really juicy"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>
        <button
          className="btn btn-primary"
          disabled={!beanId || createEntry.isPending}
          onClick={() => createEntry.mutate()}
        >
          {createEntry.isPending ? 'Saving…' : 'Log entry'}
        </button>
        {createEntry.isError && <p className="error-text">Couldn't save that entry.</p>}
      </div>

      <h2 style={{ marginTop: 40 }}>Past entries</h2>
      <div className="card-grid">
        {entries?.map((entry) => (
          <div className="card" key={entry.id}>
            <h2>{beanName(entry.bean_id)}</h2>
            {entry.rating && <p style={{ fontSize: 14 }}>Rating: {entry.rating}/5</p>}
            {entry.notes_raw && <p style={{ fontSize: 14 }}>{entry.notes_raw}</p>}
          </div>
        ))}
        {entries?.length === 0 && (
          <div className="empty-state">
            <p>No entries yet. Log your first cup above.</p>
          </div>
        )}
      </div>
    </div>
  )
}

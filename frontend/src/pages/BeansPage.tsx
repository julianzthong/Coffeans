import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'

export default function BeansPage() {
  const { data: beans, isLoading, error } = useQuery({ queryKey: ['beans'], queryFn: api.listBeans })

  return (
    <div>
      <div className="eyebrow">Discover</div>
      <h1>Beans worth chasing</h1>
      <p>Browse what's currently roasting, filtered by origin, process, and flavor — not just star ratings.</p>

      {isLoading && <p>Loading beans…</p>}
      {error && <p className="error-text">Couldn't load beans. Is the backend running?</p>}

      {beans && beans.length === 0 && (
        <div className="empty-state">
          <h2>No beans yet</h2>
          <p>Add a roastery and a bean via the API to get started, or wire up the scraper/Places ingestion.</p>
        </div>
      )}

      <div className="card-grid">
        {beans?.map((bean) => (
          <div className="card" key={bean.id}>
            <h2>{bean.name}</h2>
            <p style={{ margin: '0 0 12px', fontSize: 14 }}>
              {[bean.origin_region, bean.origin_country].filter(Boolean).join(', ') || 'Origin unknown'}
            </p>
            {bean.tasting_notes_structured?.summary && (
              <p style={{ fontSize: 14, marginBottom: 12 }}>{bean.tasting_notes_structured.summary}</p>
            )}
            <div>
              {bean.processing_method && <span className="tag">{bean.processing_method}</span>}
              {bean.roast_level && <span className="tag">{bean.roast_level} roast</span>}
              {bean.tasting_notes_structured?.flavor_tags?.map((tag) => (
                <span className="tag" key={tag}>
                  {tag}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'

export default function ShopsPage() {
  const { data: shops, isLoading, error } = useQuery({ queryKey: ['shops'], queryFn: api.listShops })
  const { data: roasteries } = useQuery({ queryKey: ['roasteries'], queryFn: api.listRoasteries })

  const roasteryName = (id: string | null) => roasteries?.find((r) => r.id === id)?.name

  return (
    <div>
      <div className="eyebrow">Explore</div>
      <h1>Shops &amp; roasteries</h1>
      <p>Cafés and roasters, including the ones without a storefront.</p>

      {isLoading && <p>Loading shops…</p>}
      {error && <p className="error-text">Couldn't load shops. Is the backend running?</p>}

      <div className="card-grid">
        {shops?.map((shop) => (
          <div className="card" key={shop.id}>
            <h2>{shop.name}</h2>
            {shop.address && <p style={{ fontSize: 14 }}>{shop.address}</p>}
            {shop.roastery_id && (
              <span className="tag">{roasteryName(shop.roastery_id) ?? 'Roastery'}</span>
            )}
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: 48 }}>Roasteries</h2>
      <div className="card-grid">
        {roasteries?.map((roastery) => (
          <div className="card" key={roastery.id}>
            <h2>{roastery.name}</h2>
            {roastery.city && (
              <p style={{ fontSize: 14 }}>
                {roastery.city}
                {roastery.state ? `, ${roastery.state}` : ''}
              </p>
            )}
            {!roastery.has_storefront && <span className="tag">Roasting only, no storefront</span>}
          </div>
        ))}
      </div>
    </div>
  )
}

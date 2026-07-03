const API_BASE = '/api'

export interface Roastery {
  id: string
  name: string
  description: string | null
  website: string | null
  city: string | null
  state: string | null
  has_storefront: boolean
  source: 'manual' | 'google_places' | 'scraped'
}

export interface Shop {
  id: string
  roastery_id: string | null
  name: string
  address: string | null
  latitude: number | null
  longitude: number | null
  amenities: Record<string, boolean>
}

export interface Bean {
  id: string
  roastery_id: string
  name: string
  origin_country: string | null
  origin_region: string | null
  processing_method: 'washed' | 'natural' | 'honey' | 'anaerobic' | 'other' | null
  roast_level: 'light' | 'medium' | 'dark' | null
  tasting_notes_raw: string | null
  tasting_notes_structured: {
    flavor_tags?: string[]
    acidity?: string | null
    body?: string | null
    sweetness?: string | null
    summary?: string | null
  }
  is_active: boolean
}

export interface TastingEntry {
  id: string
  bean_id: string
  rating: number | null
  notes_raw: string | null
  notes_structured: Record<string, unknown>
  brew_method: string | null
  created_at: string
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

function authHeaders(): HeadersInit {
  const token = localStorage.getItem('coffeans_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...options.headers,
    },
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new ApiError(res.status, body.detail ?? `Request failed: ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  // Auth
  signup: (email: string, password: string, display_name: string) =>
    request('/auth/signup', { method: 'POST', body: JSON.stringify({ email, password, display_name }) }),

  login: async (email: string, password: string) => {
    const form = new URLSearchParams()
    form.set('username', email)
    form.set('password', password)
    const res = await fetch(`${API_BASE}/auth/login`, { method: 'POST', body: form })
    if (!res.ok) throw new ApiError(res.status, 'Invalid email or password')
    return res.json() as Promise<{ access_token: string; token_type: string }>
  },

  // Roasteries
  listRoasteries: () => request<Roastery[]>('/roasteries'),
  createRoastery: (payload: Partial<Roastery>) =>
    request<Roastery>('/roasteries', { method: 'POST', body: JSON.stringify(payload) }),

  // Shops
  listShops: () => request<Shop[]>('/shops'),
  createShop: (payload: Partial<Shop>) =>
    request<Shop>('/shops', { method: 'POST', body: JSON.stringify(payload) }),

  // Beans
  listBeans: () => request<Bean[]>('/beans'),
  createBean: (payload: Partial<Bean>) => request<Bean>('/beans', { method: 'POST', body: JSON.stringify(payload) }),

  // Tasting journal
  listTastingEntries: () => request<TastingEntry[]>('/tasting-entries'),
  createTastingEntry: (payload: { bean_id: string; rating?: number; notes_raw?: string; brew_method?: string }) =>
    request<TastingEntry>('/tasting-entries', { method: 'POST', body: JSON.stringify(payload) }),
  deleteTastingEntry: (id: string) => request<void>(`/tasting-entries/${id}`, { method: 'DELETE' }),
}

export { ApiError }

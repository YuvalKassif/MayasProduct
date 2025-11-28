const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export type Json = Record<string, any>

async function request(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })
  if (!res.ok) {
    let detail: any
    try { detail = await res.json() } catch {}
    throw new Error(detail?.detail || `HTTP ${res.status}`)
  }
  const ct = res.headers.get('content-type') || ''
  if (ct.includes('application/json')) return res.json()
  return res.text()
}

export const api = {
  register: (email: string, password: string) => request('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) }),
  login: (email: string, password: string) => request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  me: () => request('/auth/me'),
  logout: () => request('/auth/logout', { method: 'POST' }),
  refresh: () => request('/auth/refresh', { method: 'POST' }),
  health: () => request('/health'),
  dbHealth: () => request('/health/db'),
  // Items
  listItems: (params?: { limit?: number; offset?: number; seller_id?: string }) => {
    const usp = new URLSearchParams()
    if (params?.limit) usp.set('limit', String(params.limit))
    if (params?.offset) usp.set('offset', String(params.offset))
    if (params?.seller_id) usp.set('seller_id', params.seller_id)
    const q = usp.toString()
    return request(`/items${q ? `?${q}` : ''}`)
  },
  getItem: (id: string) => request(`/items/${id}`),
  createItem: (body: Json) => request('/items', { method: 'POST', body: JSON.stringify(body) }),
  updateItem: (id: string, body: Json) => request(`/items/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  deleteItem: (id: string) => request(`/items/${id}`, { method: 'DELETE' }),
}

export default api

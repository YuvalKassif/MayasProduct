import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { Link } from 'react-router-dom'

export default function ItemsListPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['items', { limit: 20, offset: 0 }], queryFn: () => api.listItems({ limit: 20, offset: 0 }) })

  if (isLoading) return <div>Loading items...</div>
  if (error) return <div className="text-red-600">Failed to load items</div>

  const items = data?.items || []

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-semibold">Latest Items</h1>
        <Link to="/items/new" className="bg-black text-white px-3 py-2 rounded">Create Item</Link>
      </div>
      {items.length === 0 ? (
        <div className="text-gray-600">No items yet. Be the first to create one!</div>
      ) : (
        <ul className="grid grid-cols-1 gap-4">
          {items.map((it: any) => (
            <li key={it.id} className="bg-white p-4 rounded shadow">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">{it.title}</div>
                  <div className="text-sm text-gray-600">{it.brand || '—'} · {it.size || '—'} · {it.condition}</div>
                </div>
                <div className="font-semibold">{(it.price_cents/100).toFixed(2)} {it.currency}</div>
              </div>
              <div className="text-sm mt-2 text-gray-700 line-clamp-2">{it.description}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}


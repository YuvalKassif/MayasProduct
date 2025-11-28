import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'

export default function NavBar() {
  const { data } = useQuery({ queryKey: ['me'], queryFn: api.me, retry: 0 })
  return (
    <header className="bg-white border-b">
      <div className="max-w-3xl mx-auto p-4 flex items-center justify-between">
        <div className="font-semibold">Second‑Hand Clothing</div>
        <div className="text-sm text-gray-600">
          {data?.email ? `Signed in as ${data.email}` : 'Not signed in'}
        </div>
      </div>
    </header>
  )
}


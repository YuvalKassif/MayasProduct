import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Link } from 'react-router-dom'

export default function NavBar() {
  const qc = useQueryClient()
  const { data } = useQuery({ queryKey: ['me'], queryFn: api.me, retry: 0 })
  const logout = useMutation({
    mutationFn: () => api.logout(),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['me'] }),
  })
  return (
    <header className="bg-white border-b">
      <div className="max-w-3xl mx-auto p-4 flex items-center justify-between">
        <div className="font-semibold"><Link to="/">Second‑Hand Clothing</Link></div>
        <nav className="flex items-center gap-4 text-sm text-gray-700">
          <Link to="/items" className="underline">Items</Link>
          <Link to="/items/new" className="underline">Create</Link>
          {data?.email ? (
            <>
              <span className="text-gray-600 hidden sm:inline">{data.email}</span>
              <button onClick={() => logout.mutate()} className="text-gray-700 underline">Sign out</button>
            </>
          ) : (
            <>
              <Link to="/login" className="underline">Login</Link>
              <Link to="/register" className="underline">Register</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}

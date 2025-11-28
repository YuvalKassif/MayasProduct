import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import api from '@/lib/api'

export default function LoginPage() {
  const qc = useQueryClient()
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const m = useMutation({
    mutationFn: () => api.login(email, password),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      nav('/')
    },
    onError: (e: any) => setError(e.message || 'Login failed'),
  })

  return (
    <div className="bg-white shadow p-6 rounded">
      <h1 className="text-xl font-semibold mb-4">Login</h1>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <form onSubmit={(e) => { e.preventDefault(); m.mutate() }} className="space-y-3">
        <input value={email} onChange={e => setEmail(e.target.value)} type="email" placeholder="Email" className="w-full border rounded px-3 py-2" required />
        <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" className="w-full border rounded px-3 py-2" required />
        <button disabled={m.isPending} className="bg-black text-white px-4 py-2 rounded disabled:opacity-50">{m.isPending ? 'Signing in...' : 'Sign in'}</button>
      </form>
    </div>
  )
}


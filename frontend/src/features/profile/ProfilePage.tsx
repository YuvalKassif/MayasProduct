import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Link } from 'react-router-dom'

export default function ProfilePage() {
  const qc = useQueryClient()
  const me = useQuery({ queryKey: ['me'], queryFn: api.me, retry: 0 })
  const logout = useMutation({
    mutationFn: () => api.logout(),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['me'] }),
  })

  if (me.isLoading) return <div>Loading profile...</div>
  if (me.error) return (
    <div className="bg-white shadow p-6 rounded">
      <div className="mb-2">You are not signed in.</div>
      <Link className="underline" to="/login">Sign in</Link> or <Link className="underline" to="/register">Create account</Link>
    </div>
  )

  const user = me.data
  return (
    <div className="bg-white shadow p-6 rounded">
      <h1 className="text-xl font-semibold mb-4">Profile</h1>
      <div className="space-y-1">
        <div><span className="font-medium">Email:</span> {user.email}</div>
        <div><span className="font-medium">Verified:</span> {String(user.email_verified)}</div>
        <div><span className="font-medium">Role:</span> {user.role}</div>
      </div>
      <button onClick={() => logout.mutate()} className="mt-4 bg-gray-800 text-white px-4 py-2 rounded">Sign out</button>
    </div>
  )
}


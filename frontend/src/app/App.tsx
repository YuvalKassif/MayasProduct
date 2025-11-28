import { Outlet, Link, useLocation } from 'react-router-dom'
import NavBar from '../components/NavBar'

export default function App() {
  const { pathname } = useLocation()
  return (
    <div className="min-h-full">
      <NavBar />
      <main className="max-w-3xl mx-auto p-4">
        <div className="mb-4 text-sm text-gray-600">Route: {pathname}</div>
        <Outlet />
        <div className="mt-8 text-sm text-gray-500">
          <Link className="underline" to="/">Profile</Link> ·{' '}
          <Link className="underline" to="/login">Login</Link> ·{' '}
          <Link className="underline" to="/register">Register</Link>
        </div>
      </main>
    </div>
  )
}


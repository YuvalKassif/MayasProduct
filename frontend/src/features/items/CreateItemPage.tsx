import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, Link } from 'react-router-dom'
import api from '@/lib/api'

export default function CreateItemPage() {
  const qc = useQueryClient()
  const nav = useNavigate()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('tops')
  const [brand, setBrand] = useState('')
  const [size, setSize] = useState('')
  const [condition, setCondition] = useState('good')
  const [price, setPrice] = useState('') // dollars as string
  const [currency, setCurrency] = useState('USD')
  const [city, setCity] = useState('')
  const [country, setCountry] = useState('')
  const [error, setError] = useState<string | null>(null)

  const m = useMutation({
    mutationFn: async () => {
      const price_cents = Math.round(parseFloat(price) * 100) || 0
      return api.createItem({
        title,
        description: description || null,
        category,
        brand: brand || null,
        size: size || null,
        condition,
        price_cents,
        currency,
        location_city: city || null,
        location_country: country || null,
      })
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['items'] })
      nav('/items')
    },
    onError: (e: any) => setError(e.message || 'Create failed'),
  })

  return (
    <div className="bg-white shadow p-6 rounded">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-semibold">Create Item</h1>
        <Link to="/items" className="underline">Back to list</Link>
      </div>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <form onSubmit={(e) => { e.preventDefault(); m.mutate() }} className="grid grid-cols-1 gap-3">
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" required className="border rounded px-3 py-2" />
        <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" className="border rounded px-3 py-2" />
        <div className="grid grid-cols-2 gap-3">
          <select value={category} onChange={e => setCategory(e.target.value)} className="border rounded px-3 py-2">
            <option value="tops">Tops</option>
            <option value="bottoms">Bottoms</option>
            <option value="outerwear">Outerwear</option>
            <option value="dresses">Dresses</option>
            <option value="shoes">Shoes</option>
            <option value="accessories">Accessories</option>
            <option value="other">Other</option>
          </select>
          <select value={condition} onChange={e => setCondition(e.target.value)} className="border rounded px-3 py-2">
            <option value="new_with_tags">New with tags</option>
            <option value="like_new">Like new</option>
            <option value="good">Good</option>
            <option value="fair">Fair</option>
          </select>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <input value={brand} onChange={e => setBrand(e.target.value)} placeholder="Brand (optional)" className="border rounded px-3 py-2" />
          <input value={size} onChange={e => setSize(e.target.value)} placeholder="Size (optional)" className="border rounded px-3 py-2" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <input value={price} onChange={e => setPrice(e.target.value)} placeholder="Price (e.g., 25.00)" inputMode="decimal" className="border rounded px-3 py-2" />
          <input value={currency} onChange={e => setCurrency(e.target.value.toUpperCase())} placeholder="Currency (USD)" className="border rounded px-3 py-2" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <input value={city} onChange={e => setCity(e.target.value)} placeholder="City (optional)" className="border rounded px-3 py-2" />
          <input value={country} onChange={e => setCountry(e.target.value)} placeholder="Country (optional)" className="border rounded px-3 py-2" />
        </div>
        <button disabled={m.isPending} className="bg-black text-white px-4 py-2 rounded disabled:opacity-50">{m.isPending ? 'Creating…' : 'Create'}</button>
      </form>
    </div>
  )
}


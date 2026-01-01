'use client'

import { useState } from 'react'
import { Search, TrendingDown, Bell, BarChart3 } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8765'

export default function Home() {
  const [location, setLocation] = useState('')
  const [loading, setLoading] = useState(false)
  const [scanId, setScanId] = useState<string | null>(null)
  const [results, setResults] = useState<any>(null)

  const handleScan = async () => {
    if (!location.trim()) return
    
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/api/scan?user_id=demo-user`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location: location,
          guests: 2,
          currency: 'EUR'
        })
      })
      const data = await response.json()
      setScanId(data.data.scan_id)
      
      // Poll for results
      pollResults(data.data.scan_id)
    } catch (error) {
      console.error('Scan failed:', error)
      setLoading(false)
    }
  }

  const pollResults = async (id: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/api/scan/${id}`)
        const data = await response.json()
        
        if (data.scan.status === 'completed') {
          setResults(data)
          setLoading(false)
          clearInterval(interval)
        } else if (data.scan.status === 'failed') {
          setLoading(false)
          clearInterval(interval)
        }
      } catch (error) {
        console.error('Poll failed:', error)
      }
    }, 3000)
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">🕵️ SpyBnB</h1>
          <div className="flex gap-4">
            <a href="#" className="text-gray-600 hover:text-primary">Dashboard</a>
            <a href="#" className="text-gray-600 hover:text-primary">Alerts</a>
            <a href="#" className="bg-primary text-white px-4 py-2 rounded-lg">Sign Up</a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-5xl font-bold text-gray-900 mb-6">
          Spy on Your Airbnb Competitors
        </h2>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Track competitor prices, get alerts when they drop, and optimize your pricing strategy.
        </p>

        {/* Search Box */}
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-3.5 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Enter location (e.g., Paris, France)"
                className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleScan()}
              />
            </div>
            <button
              onClick={handleScan}
              disabled={loading}
              className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Scanning...' : 'Scan Now'}
            </button>
          </div>
        </div>
      </section>

      {/* Results */}
      {results && (
        <section className="max-w-7xl mx-auto px-4 py-10">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-2xl font-bold mb-6">
              Results for {results.scan.location}
            </h3>
            
            {/* Stats */}
            <div className="grid grid-cols-4 gap-6 mb-8">
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <p className="text-3xl font-bold text-primary">{results.scan.stats?.total_listings || 0}</p>
                <p className="text-gray-600">Listings</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <p className="text-3xl font-bold text-green-600">€{results.scan.stats?.avg_price || 0}</p>
                <p className="text-gray-600">Avg Price</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <p className="text-3xl font-bold text-blue-600">€{results.scan.stats?.min_price || 0}</p>
                <p className="text-gray-600">Min Price</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <p className="text-3xl font-bold text-purple-600">€{results.scan.stats?.max_price || 0}</p>
                <p className="text-gray-600">Max Price</p>
              </div>
            </div>

            {/* Listings Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left">Name</th>
                    <th className="px-4 py-3 text-left">Price/Night</th>
                    <th className="px-4 py-3 text-left">Rating</th>
                    <th className="px-4 py-3 text-left">Reviews</th>
                    <th className="px-4 py-3 text-left">Bedrooms</th>
                  </tr>
                </thead>
                <tbody>
                  {results.listings?.slice(0, 20).map((listing: any) => (
                    <tr key={listing.id} className="border-b hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <a href={listing.url} target="_blank" className="text-primary hover:underline">
                          {listing.name?.substring(0, 50)}...
                        </a>
                      </td>
                      <td className="px-4 py-3 font-semibold">€{listing.price_per_night}</td>
                      <td className="px-4 py-3">⭐ {listing.rating || 'N/A'}</td>
                      <td className="px-4 py-3">{listing.reviews_count || 0}</td>
                      <td className="px-4 py-3">{listing.bedrooms || 0}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      )}

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-center mb-12">Why SpyBnB?</h3>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-lg text-center">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingDown className="text-primary" size={32} />
            </div>
            <h4 className="text-xl font-bold mb-2">Price Tracking</h4>
            <p className="text-gray-600">Monitor competitor prices in real-time and never miss a price change.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-lg text-center">
            <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bell className="text-secondary" size={32} />
            </div>
            <h4 className="text-xl font-bold mb-2">Smart Alerts</h4>
            <p className="text-gray-600">Get notified when competitors drop their prices below your threshold.</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-lg text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="text-purple-600" size={32} />
            </div>
            <h4 className="text-xl font-bold mb-2">Analytics</h4>
            <p className="text-gray-600">Understand market trends with detailed analytics and insights.</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-10">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-2xl font-bold mb-2">🕵️ SpyBnB</p>
          <p className="text-gray-400">Monitor your Airbnb competition like a pro.</p>
          <p className="text-gray-500 mt-4">© 2026 SpyBnB. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}

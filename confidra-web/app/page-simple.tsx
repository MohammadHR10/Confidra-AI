'use client'

import { useState } from 'react'

export default function Home() {
  const [test, setTest] = useState('Hello World')

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          🛡️ Confidra AI
        </h1>
        <p className="text-center text-gray-300 mb-8">
          Contract Compliance Assistant
        </p>
        <div className="text-center">
          <p>{test}</p>
          <button 
            onClick={() => setTest('Button clicked!')}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded mt-4"
          >
            Test Button
          </button>
        </div>
      </div>
    </div>
  )
}

'use client'

import { useState } from 'react'

export default function Home() {
  const [test, setTest] = useState('Welcome to Confidra AI')

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            🛡️ Confidra AI
          </h1>
          <p className="text-xl text-gray-300">
            Contract Compliance Assistant
          </p>
        </header>

        <main className="max-w-4xl mx-auto">
          <div className="bg-slate-800 p-8 rounded-lg shadow-lg text-center">
            <h2 className="text-2xl font-semibold mb-4">{test}</h2>
            <p className="text-gray-300 mb-6">
              Upload contracts and ask questions while ensuring sensitive information stays protected.
            </p>
            
            <button 
              onClick={() => setTest('System is working!')}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg transition-colors"
            >
              Test Connection
            </button>
          </div>

          <div className="mt-8 grid md:grid-cols-2 gap-6">
            <div className="bg-slate-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-2">📄 Document Upload</h3>
              <p className="text-gray-300 text-sm">
                Upload PDF, DOCX, or TXT files for analysis
              </p>
            </div>
            
            <div className="bg-slate-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-2">❓ Smart Q&A</h3>
              <p className="text-gray-300 text-sm">
                Ask questions about your contracts safely
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

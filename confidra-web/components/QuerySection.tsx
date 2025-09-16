'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

interface QuerySectionProps {
  documentName: string
}

export default function QuerySection({ documentName }: QuerySectionProps) {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const askQuestion = async () => {
    if (!query.trim()) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          user_id: 'web_user'
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setResult(data)
      } else {
        setResult({
          action: 'error',
          reason: `API Error: ${response.status}`,
          safe_output: 'Failed to process your question.'
        })
      }
    } catch (error) {
      console.error('Error asking question:', error)
      setResult({
        action: 'error',
        reason: 'Connection error',
        safe_output: 'Unable to connect to the server.'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      askQuestion()
    }
  }

  const getStatusComponent = (result: any) => {
    switch (result.action) {
      case 'pass':
        return (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="status-approved"
          >
            <div className="font-bold mb-2">✅ APPROVED</div>
            <div>{result.safe_output}</div>
          </motion.div>
        )
      case 'blocked':
        return (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="status-blocked"
          >
            <div className="font-bold mb-2">🚫 BLOCKED</div>
            <div className="mb-2">Reason: {result.reason}</div>
            <div>{result.safe_output}</div>
          </motion.div>
        )
      case 'redacted':
        return (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="status-redacted"
          >
            <div className="font-bold mb-2">✏️ REDACTED</div>
            <div className="mb-2">Reason: {result.reason}</div>
            <div>{result.safe_output}</div>
          </motion.div>
        )
      case 'error':
        return (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="status-blocked"
          >
            <div className="font-bold mb-2">❌ ERROR</div>
            <div className="mb-2">Reason: {result.reason}</div>
            <div>{result.safe_output}</div>
          </motion.div>
        )
      default:
        return null
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-8 pb-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h2 className="text-3xl font-poppins font-medium text-white mb-4">
          Ask Questions About Your Contract
        </h2>
        <p className="text-gray-300">
          Document processed: <span className="text-accent font-medium">{documentName}</span>
        </p>
      </motion.div>

      <div className="space-y-6">
        {/* Query Input */}
        <div className="space-y-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="e.g., How many vacation days are provided? What are the termination terms?"
            className="w-full p-4 text-gray-800 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent"
          />

          <motion.button
            onClick={askQuestion}
            disabled={!query.trim() || loading}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: !loading && query.trim() ? 1.02 : 1 }}
            whileTap={{ scale: !loading && query.trim() ? 0.98 : 1 }}
          >
            {loading ? (
              <span className="flex items-center justify-center space-x-2">
                <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
                <span>Analyzing...</span>
              </span>
            ) : (
              '🚀 ASK QUESTION'
            )}
          </motion.button>
        </div>

        {/* Results */}
        {result && getStatusComponent(result)}

        {/* Suggested Questions */}
        <div className="mt-8">
          <h3 className="text-lg font-poppins font-medium text-white mb-4">
            Suggested Questions:
          </h3>
          <div className="grid md:grid-cols-2 gap-3">
            {[
              "How many vacation days are provided?",
              "What is the job title?",
              "When does employment start?",
              "What are the termination terms?",
              "What benefits are included?",
              "What are the work hours?"
            ].map((suggestion, index) => (
              <button
                key={index}
                onClick={() => setQuery(suggestion)}
                className="text-left p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

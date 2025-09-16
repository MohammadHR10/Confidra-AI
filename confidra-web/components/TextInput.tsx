'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

interface TextInputProps {
  onTextProcessed: (filename: string, success: boolean) => void
  processingStatus: 'idle' | 'processing' | 'success' | 'error'
  setProcessingStatus: (status: 'idle' | 'processing' | 'success' | 'error') => void
}

export default function TextInput({ 
  onTextProcessed, 
  processingStatus, 
  setProcessingStatus 
}: TextInputProps) {
  const [textContent, setTextContent] = useState('')

  const processText = async () => {
    if (!textContent.trim()) return

    setProcessingStatus('processing')

    try {
      const formData = new FormData()
      formData.append('filename', 'pasted_text.txt')
      formData.append('content', textContent)
      formData.append('sensitivity', 'protected')
      formData.append('timestamp', new Date().toISOString())

      const response = await fetch('/api/upload-document', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        onTextProcessed('pasted_text.txt', true)
      } else {
        onTextProcessed('pasted_text.txt', false)
      }
    } catch (error) {
      console.error('Error processing text:', error)
      onTextProcessed('pasted_text.txt', false)
    }
  }

  return (
    <div className="space-y-4">
      {/* Text Area */}
      <div className="bg-white rounded-lg border border-gray-300">
        <textarea
          value={textContent}
          onChange={(e) => setTextContent(e.target.value)}
          placeholder="Paste your contract or NDA text here..."
          className="w-full h-48 p-4 text-gray-800 resize-none rounded-lg border-none focus:outline-none focus:ring-2 focus:ring-accent"
        />
      </div>

      {/* Character Count */}
      <div className="text-sm text-gray-400 text-right">
        {textContent.length} characters
      </div>

      {/* Scan Button */}
      {textContent.trim() && (
        <motion.button
          onClick={processText}
          disabled={processingStatus === 'processing'}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          whileHover={{ scale: processingStatus !== 'processing' ? 1.02 : 1 }}
          whileTap={{ scale: processingStatus !== 'processing' ? 0.98 : 1 }}
        >
          {processingStatus === 'processing' ? (
            <span className="flex items-center justify-center space-x-2">
              <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
              <span>Processing...</span>
            </span>
          ) : (
            '🔍 SCAN FOR RISKS'
          )}
        </motion.button>
      )}

      {/* Status Messages */}
      {processingStatus === 'success' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="status-approved"
        >
          ✅ Text processed successfully!
        </motion.div>
      )}

      {processingStatus === 'error' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="status-blocked"
        >
          ❌ Failed to process text
        </motion.div>
      )}
    </div>
  )
}
